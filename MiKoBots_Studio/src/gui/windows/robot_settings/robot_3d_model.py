from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QHBoxLayout, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from backend.simulation.simulation_interaction import CustomInteractorStyle

from backend.simulation.axis import Axis
from backend.simulation.planes import Planes

from backend.core.event_manager import event_manager

from backend.robot_management  import show_3d_model_settings
from backend.robot_management  import delete_robot_model
from backend.robot_management  import change_origin_3d_model
from backend.robot_management  import add_new_3d_model
from backend.robot_management  import save_robot 



class Robot3DModel: 
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)


        self.layout.setContentsMargins(3, 3, 3, 3)
                
        self.Robot_buttons = []
        
        self.spacer_widget = None
        
        self.stl_actor = None
        self.plotter = None
        self.renderer = None
        self.frames = []
        
        self.GUI()
        self.subscribeToEvents()

        self.parent_frame.setLayout(self.layout)
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_delete_buttons_3d_model", self.DeleteButtons)
        event_manager.subscribe("request_clear_plotter_3d_model", self.ClearPlotter)
        event_manager.subscribe("request_create_buttons_3d_model", self.CreateButtons)
        event_manager.subscribe("request_show_3d_model", self.ShowModel)
        event_manager.subscribe("request_show_origin_3d_model", self.SetOriginfields)
        event_manager.subscribe("request_get_origin_3d_model", self.GetOriginData)
    
    def GUI(self):
        # Frame with the stl files
        title = QLabel("3D files:", self.parent_frame)
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title,0,0)
        
        
        scroll = QScrollArea(self.parent_frame)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        scroll.setFixedHeight(300)
        
        scroll_widget = QWidget(scroll)
        scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(scroll_widget)
        self.layout.addWidget(scroll,1,0)      
        
        # create layout plotter
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        frame_plotter.setFixedWidth(400)
        self.layout.addWidget(frame_plotter, 2, 0)
        frame_plotter.setLayout(self.layout_plotter)
        
        # frame with change origin
        layout_options = QGridLayout()
        frame_options = QFrame()
        frame_options.setMaximumWidth(250)
        self.layout.addWidget(frame_options,0,1,3,1)
        frame_options.setLayout(layout_options)
        
        
        title = QLabel("Change origin:")
        title.setFixedHeight(30)
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,0)
        
        labels = ["X:", "Y:", "Z:", "y:", "p:", "r:"]
        self.origin_pos = []
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            # make sure only int and float numbers are filled in
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            row = idx + 2
            col = 0

            layout_options.addWidget(label, row, col)
            layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        self.button_update = QPushButton("Update")
        self.button_update.setStyleSheet(style_button)
        layout_options.addWidget(self.button_update,8, 0, 1, 2)
        self.button_update.clicked.connect(lambda: change_origin_3d_model())
        
        self.button_add_new = QPushButton("Add new 3D model")
        self.button_add_new.setStyleSheet(style_button)
        layout_options.addWidget(self.button_add_new, 9, 0, 1, 2)
        self.button_add_new.clicked.connect(lambda: add_new_3d_model())  
        
        button = QPushButton("Save robot")
        button.setStyleSheet(style_button)
        layout_options.addWidget(button, 10, 0, 1, 2)
        button.clicked.connect(lambda: save_robot(True))   
        
        widget = QWidget()
        widget.setStyleSheet(style_widget)
        layout_options.addWidget(widget, 11,0,1,2)     
                        
   
    def open_plotter(self):
        if self.plotter is None:
            print(" plotter")

            ## frame with the plotter
            self.plotter = QVTKRenderWindowInteractor()
            self.plotter.Initialize()
            self.plotter.setFixedHeight(200)
            self.plotter.setFixedWidth(330)
            
            self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
            self.interactor_style = CustomInteractorStyle()
            self.interactor.SetInteractorStyle(self.interactor_style)
            
            
            # Set up a VTK renderer and add it to the interactor
            self.renderer = vtk.vtkRenderer()
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.plotter.GetRenderWindow().AddRenderer(self.renderer)
            
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
            
            self.layout_plotter.addWidget(self.plotter,0,0)
            
            self.camera = vtk.vtkCamera()
            self.SetCameraPlotter()

    def ShowModel(self, path):
        stl_reader = vtk.vtkSTLReader()
        stl_reader.SetFileName(path)
        stl_reader.Update()  # Ensure the STL data is loaded
        
        # Create a mapper for the STL data
        stl_mapper = vtk.vtkPolyDataMapper()
        stl_mapper.SetInputConnection(stl_reader.GetOutputPort())
    
        self.stl_actor = vtk.vtkActor()
        self.stl_actor.SetMapper(stl_mapper)
        self.stl_actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("red"))
        self.stl_actor.GetProperty().EdgeVisibilityOff()  # Equivalent to show_edges=False
        
        self.renderer.AddActor(self.stl_actor)
        
    def ClearPlotter(self):
       if self.stl_actor and self.renderer:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window

    def ClosePlotter(self):
        if self.plotter:
            self.plotter.close() 
            self.plotter = None
            self.renderer = None

    def CreateButtons(self, item, robot_3d_data):
        self.Robot_buttons.append([[],[],[],[],[]])
        

        frame = QFrame()
        layout_model = QHBoxLayout()
        layout_model.setContentsMargins(5,0,5,5)
        frame.setLayout(layout_model)
        self.layout_scroll.addWidget(frame) 
        self.frames.append(frame)
            
        label = QLabel(robot_3d_data[item][0])
        label.setStyleSheet(style_label)
        label.setFixedWidth(120)
        layout_model.addWidget(label)
        self.Robot_buttons[item][0] = label
        
        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: delete_robot_model(idx))
        layout_model.addWidget(button)
        self.Robot_buttons[item][1] = button
        
        button = QPushButton("Origin")
        button.setFixedSize(75,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: show_3d_model_settings(idx))
        layout_model.addWidget(button)
        self.Robot_buttons[item][2] = button
        
        def on_combobox_change(nr):
            robot_3d_data[nr][3] = combo_color.currentText()
            
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        for i in range(len(colors)):
            if colors[i] == robot_3d_data[item][3]:
                combo_nr = i
        
        combo_color = QComboBox()
        combo_color.view().setMinimumWidth(170)
        combo_color.addItems(colors)
        combo_color.setStyleSheet(style_combo)
        combo_color.setCurrentIndex(combo_nr)
        combo_color.currentIndexChanged.connect(lambda index, idx = item: on_combobox_change(idx))
        layout_model.addWidget(combo_color)
        self.Robot_buttons[item][3] = combo_color
        
                        
        def on_linkage_change(nr):
            robot_3d_data[nr][5] = combo.currentText()
        
        linkages = ['Link 1', 'Link 2', 'Link 3', 'Link 4', 'Link 5', 'Link 6', 'Base']
        combo_nr = 0
        for i in range(len(linkages)):
            if linkages[i] == robot_3d_data[item][5]:
                combo_nr = i

        
        combo = QComboBox()
        combo.view().setMinimumWidth(170)
        combo.setStyleSheet(style_combo)
        combo.addItems(linkages)
        combo.setCurrentIndex(combo_nr)
        combo.currentIndexChanged.connect(lambda index, idx = item: on_linkage_change(idx))
        layout_model.addWidget(combo)
        self.Robot_buttons[item][4] = combo
        pass

    def DeleteButtons(self):
        # for frame in self.frames:
        #     self.layout_scroll.removeWidget(frame)
        #     frame.deleteLater() 
        #     frame = None

        # self.frames = []

        pass
    
    def SetOriginfields(self, data):
        for i in range(6):
            self.origin_pos[i].setText(str(data[i]))
            
    def GetOriginData(self, data):
        for i in range(6):
            try:
                data[i] = float(self.origin_pos[i].text())
            except:
                data[i] = 0.0
                self.origin_pos[i].setText("0.0")
                
        return data
            
    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        #self.renderer.Render()
        self.plotter.Render() 