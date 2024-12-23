from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QDoubleValidator, QIcon

from gui.style import *

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from backend.core.event_manager import event_manager

from backend.file_managment import get_image_path

from backend.simulation.axis import Axis
from backend.simulation.planes import Planes
from backend.simulation.simulation_interaction import CustomInteractorStyle

from backend.simulation.object import open_object_models
from backend.simulation.object import show_origin_object
from backend.simulation.object import change_origin_object
from backend.simulation.object import delete_stl_object_1
from backend.simulation.object import add_new_object_model
from backend.simulation.object import add_object_to_plotter
from backend.simulation.object import show_pos_object
from backend.simulation.object import change_pos_object
from backend.simulation.object import delete_object_plotter
from backend.simulation.object import change_color_object


class SimulationObjectsGUI(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.setWindowTitle("Add item")
        
        image_path = get_image_path('mikobot.ico')
        self.setWindowIcon(QIcon(image_path))
        self.setFixedSize(1000, 700)
        

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.setStyleSheet("background-color: #E8E8E8;")
        
        self.plotter = None
        self.renderer = None

        self.stl_actor = None
        
        self.Buttons2 = []
        self.Buttons1 = []
        
        self.origin_pos = []
        self.pos_entry = []
        
        self.spacer_widget_2 = None
        
        
        self.subscribeToEvents()
        self.GUI()
        
        open_object_models()
          
    def subscribeToEvents(self):
        event_manager.subscribe("request_create_buttons_1_object", self.CreateButtons1)
        event_manager.subscribe("request_delete_buttons_1_object", self.DeleteButtons1)
        
        event_manager.subscribe("request_create_buttons_2_object", self.CreateButtons2)
        event_manager.subscribe("request_delete_buttons_2_object", self.DeleteButtons2)
        
        event_manager.subscribe("request_set_data_origin_object", self.SetDataOriginObject)
        event_manager.subscribe("request_get_data_origin_object", self.GetDataOriginObject)

        event_manager.subscribe("request_set_data_pos_object", self.SetDataPosObject)
        event_manager.subscribe("request_get_data_pos_object", self.GetDataPosObject)

        event_manager.subscribe("request_object_plotter_preview", self.AddModelToPlotter)
        event_manager.subscribe("request_clear_plotter_object", self.ClearPlotter) 

    def ClearPlotter(self):
        if self.stl_actor:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window

    def AddModelToPlotter(self, file_path):
        stl_reader = vtk.vtkSTLReader()
        stl_reader.SetFileName(file_path)
        stl_reader.Update()  # Ensure the STL data is loaded
        
        # Create a mapper for the STL data
        stl_mapper = vtk.vtkPolyDataMapper()
        stl_mapper.SetInputConnection(stl_reader.GetOutputPort())
    
        self.stl_actor = vtk.vtkActor()
        self.stl_actor.SetMapper(stl_mapper)
        self.stl_actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("red"))
        self.stl_actor.GetProperty().EdgeVisibilityOff()  # Equivalent to show_edges=False
        
        self.renderer.AddActor(self.stl_actor)
        
        self.SetCameraPlotter()
        
    # set and get the origin data   
    def SetDataOriginObject(self, origin):
        for i in range(6):
            self.origin_pos[i].setText(str(origin[i]))
            
    def GetDataOriginObject(self):
        data = [0,0,0,0,0,0]
        for i in range(6):
            data[i] = float(self.origin_pos[i].text())
            
        return data

    # Set and get the position of the object
    def SetDataPosObject(self, pos):
        for i in range(6):
            self.pos_entry[i].setText(str(pos[i]))
   
    def GetDataPosObject(self):
        data = [0,0,0,0,0,0]
        for i in range(6):
            try:
                data[i] = float(self.pos_entry[i].text())
            except:
                data[i] = 0.0
            
        return data


    # Create the buttons for all the stl files that are saved in the mikobots studio
    def CreateButtons1(self, item, name):
        self.Buttons1.append([[],[],[],[]])

        frame = QFrame()
        frame.setFixedWidth(280)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 5)
        frame.setLayout(layout)
        self.scroll_area1.addWidget(frame) 
        
        label = QLabel(name)
        label.setStyleSheet(style_label)
        layout.addWidget(label)
        self.Buttons1[item][0] = label

        button = QPushButton("X")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_stl_object_1(idx))
        layout.addWidget(button)
        self.Buttons1[item][1] = button
 
        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: add_object_to_plotter(idx))
        layout.addWidget(button)
        self.Buttons1[item][2] = button
        
        button = QPushButton("Origin")
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_origin_object(idx))
        layout.addWidget(button)
        self.Buttons1[item][3] = button
        

    def DeleteButtons1(self):         
        while self.scroll_area1.count():
            item = self.scroll_area1.takeAt(0)  # Take the first item from the layout
            widget = item.widget()   # If it's a widget, delete it
            if widget is not None:
                widget.deleteLater()  # This ensures the widget is properly deleted
            else:
                self.scroll_area1.removeItem(item)  # If it's not a widget, just remove it (e.g., a spacer item)

        self.Buttons1 = []  


    # create the buttons for the objects that are shown in the plotter
    def CreateButtons2(self, item, name):
        self.Buttons2.append([[],[],[],[],[],[]])

        frame = QFrame()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 5)
        frame.setLayout(layout)
        self.scroll_area2.addWidget(frame) 

        label = QLabel(name)
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        layout.addWidget(label)
        self.Buttons2[item][0] = label
        
        button = QPushButton("X")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_object_plotter(idx))
        layout.addWidget(button)
        self.Buttons2[item][1] = button
               
        button = QPushButton("Position")
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_pos_object(idx))
        layout.addWidget(button)
        self.Buttons2[item][2] = button
       
        colors = ['red', 'blue', 'green', 'yellow','white', 'darkgray']
        combo_nr = 0
        
        self.combo = QComboBox()
        self.combo.view().setMinimumWidth(170)
        self.combo.setStyleSheet(style_combo)
        self.combo.addItems(colors)
        self.combo.setCurrentIndex(combo_nr)
        self.combo.currentIndexChanged.connect(lambda index, idx = item: self.ChangeColorCombo(idx))
        layout.addWidget(self.combo)
        self.Buttons2[item][3] = self.combo
            

    def DeleteButtons2(self):
        # Delete all the buttons
        while self.scroll_area2.count():
            item = self.scroll_area2.takeAt(0)  # Take the first item from the layout
            widget = item.widget()   # If it's a widget, delete it
            if widget is not None:
                widget.deleteLater()  # This ensures the widget is properly deleted
            else:
                self.scroll_area2.removeItem(item)  # If it's not a widget, just remove it (e.g., a spacer item)

        self.Buttons2 = []  
        
    def ChangeColorCombo(self, nr):
        color = [0,0,0]
        if self.combo.currentText() == "red":
            color = [1,0,0]
        elif self.combo.currentText() == "blue":
            color = [0,0,1]
        elif self.combo.currentText() == "green":
            color = [0,1,0]
        elif self.combo.currentText() == "black":
            color = [0,0,0]
        elif self.combo.currentText() == "white":
            color = [1,1,1]
        elif self.combo.currentText() == "yellow":
            color = [1,1,0]
        elif self.combo.currentText() == "darkgray":
            color = [0.5,0.5,0.5]
            
        change_color_object(self.combo.currentText(), color, nr)
        


    # Create the plotter and load the list
    def openevent(self):
        if self.plotter is None:
            ## frame with the plotter
            self.plotter = QVTKRenderWindowInteractor(self)
            self.plotter.Initialize()
            self.plotter.setFixedHeight(200)
            self.plotter.setFixedWidth(330)
            
            
            # Set up a VTK renderer and add it to the interactor
            self.renderer = vtk.vtkRenderer()
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.plotter.GetRenderWindow().AddRenderer(self.renderer)
            
            self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
            self.interactor_style = CustomInteractorStyle()
            self.interactor.SetInteractorStyle(self.interactor_style)
            
            # Optional: Add axes
            axes = vtk.vtkAxesActor()
            axes_widget = vtk.vtkOrientationMarkerWidget()
            axes_widget.SetOrientationMarker(axes)
            axes_widget.SetInteractor(self.plotter)
            axes_widget.SetViewport(0.0, 0.0, 0.2, 0.2)  # Adjust viewport size if needed
            axes_widget.EnabledOn()
            
            # Start the interactor
            self.plotter.Initialize()
            self.plotter.Start()
            
            Axis(self.renderer, 100)
            Planes(self.renderer)
            
            self.layout_plotter.addWidget(self.plotter,2,0) 
            
            self.camera = vtk.vtkCamera()
            self.SetCameraPlotter()
        
    def closeEvent(self, event):
        if self.plotter:
            self.plotter.close()
            self.plotter = None
            self.renderer = None
        
    
    
                  
    def GUI(self):
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        frame_1_layout = QGridLayout()
        frame_1_layout.setAlignment(Qt.AlignTop)
        frame_1_layout.setContentsMargins(0, 0, 0, 0)
        frame_1_layout.setSpacing(0)
        frame_1_items = QFrame()
        frame_1_items.setFixedWidth(300)
        frame_1_items.setStyleSheet(style_frame)
        frame_1_items.setLayout(frame_1_layout)
        
        frame_2_layout = QGridLayout()
        frame_2_position = QFrame()
        frame_2_position.setStyleSheet(style_frame)
        frame_2_position.setLayout(frame_2_layout)
        
        frame_3_layout = QVBoxLayout()
        frame_3_layout.setAlignment(Qt.AlignTop)
        frame_3_layout.setContentsMargins(0, 0, 0, 0)
        frame_3_layout.setSpacing(0)
        frame_3_3dfiles = QFrame()
        frame_3_3dfiles.setFixedWidth(300)
        frame_3_3dfiles.setStyleSheet(style_frame)
        frame_3_3dfiles.setLayout(frame_3_layout)
        
        frame_4_layout = QGridLayout()
        frame_4_plotter = QFrame()
        frame_4_plotter.setStyleSheet(style_frame)
        frame_4_plotter.setLayout(frame_4_layout)
        
        frame_5_layout = QGridLayout()
        frame_5_origin = QFrame()
        frame_5_origin.setStyleSheet(style_frame)
        frame_5_origin.setLayout(frame_5_layout)
        
        self.layout.addWidget(frame_1_items, 0, 0)
        self.layout.addWidget(frame_2_position, 1, 0)
        self.layout.addWidget(frame_3_3dfiles, 0, 1, 2, 1)
        self.layout.addWidget(frame_4_plotter, 0, 2)
        self.layout.addWidget(frame_5_origin, 1, 2)
  
  
        #### frame 1
        title = QLabel("Items")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_1_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_area2 = QVBoxLayout(scroll_widget)
        self.scroll_area2.setContentsMargins(0, 0, 0, 0)
        self.scroll_area2.setSpacing(0)
        self.scroll_area2.setAlignment(Qt.AlignTop)
        
        
        scroll.setWidget(scroll_widget)
        frame_1_layout.addWidget(scroll) 


        #### frame 2   
        title = QLabel("Change position:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_2_layout.addWidget(title, 0, 0, 1, 2)
        
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.pos_entry.append(entry)

            row = idx + 1
            col = 0

            frame_2_layout.addWidget(label, row, col)
            frame_2_layout.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        button_update_pos = QPushButton("Update")
        button_update_pos.setStyleSheet(style_button)
        button_update_pos.clicked.connect(lambda: change_pos_object())
        frame_2_layout.addWidget(button_update_pos,7, 0, 1, 2)


        ## frame 3
        title = QLabel("3D files:")
        title.setFixedHeight(30)
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_3_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        scroll.setFixedHeight(300)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_area1 = QVBoxLayout(scroll_widget)
        self.scroll_area1.setContentsMargins(0, 0, 0, 0)
        self.scroll_area1.setSpacing(0)
        self.scroll_area1.setAlignment(Qt.AlignTop)
        
        
        scroll.setWidget(scroll_widget)
        frame_3_layout.addWidget(scroll) 
               
         
        ## frame 4
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        frame_4_layout.addWidget(frame_plotter, 0, 0)
        frame_plotter.setLayout(self.layout_plotter)  
                
                
                
        ## frame 5 
        title = QLabel("Change origin:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_5_layout.addWidget(title,0,0,1,2)
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            row = idx + 1 
            col = 0

            frame_5_layout.addWidget(label, row, col)
            frame_5_layout.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        button = QPushButton("Update")
        button.setStyleSheet(style_button)
        frame_5_layout.addWidget(button,7, 0, 1, 2)
        button.clicked.connect(lambda: change_origin_object())
    
        
        button = QPushButton("Add new 3D model")
        button.setStyleSheet(style_button)
        frame_5_layout.addWidget(button, 8, 0, 1, 2)
        button.clicked.connect(lambda: add_new_object_model())


    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        #self.renderer.Render()
        self.plotter.Render() 
        
    

        
