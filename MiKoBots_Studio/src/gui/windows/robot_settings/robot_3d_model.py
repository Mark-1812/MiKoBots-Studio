from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QHBoxLayout, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from backend.simulation.simulation_interaction import CustomInteractorStyle
from backend.simulation.axis import Axis
from backend.simulation.planes import Planes

from backend.core.event_manager import event_manager

from backend.robot_management.robot_settings  import show_3d_model_settings, delete_robot_model, change_origin_3d_model, add_new_3d_model, change_link_3d_model, change_color_3d_model


class Robot3DModel(QFrame):   
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self) 
        self.Robot_buttons = []
        
        self.spacer_widget = None
        
        self.stl_actor = None
        self.plotter = None
        self.vtk_renderer = None
        self.frames = []

        self.CreateModelField()
        self.CreatePlotter()
        self.CreateSettings()
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_delete_buttons_3d_model", self.DeleteButtons)
        event_manager.subscribe("request_clear_plotter_3d_model", self.ClearPlotter)
        event_manager.subscribe("request_create_buttons_3d_model", self.CreateButtons)
        event_manager.subscribe("request_show_3d_model", self.ShowModel)
        event_manager.subscribe("request_show_origin_3d_model", self.SetOriginfields)
        event_manager.subscribe("request_get_origin_3d_model", self.GetOriginData)
        event_manager.subscribe("request_clear_settings_3d_model", self.ClearSettings)
        
    
    def CreateModelField(self):
        title = QLabel("3D files:")
        title.setStyleSheet(style_label_title)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title,0,0)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(300)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(self.scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area,1,0)     

    def CreatePlotter(self):    
        frame = QWidget()
        frame.setStyleSheet(style_widget)
        self.layout_plotter = QHBoxLayout()
        self.layout_plotter.setContentsMargins(5,0,5,5)
        frame.setLayout(self.layout_plotter)

        self.layout.addWidget(frame,2,0) 

    def OpenPlotter(self):
        ## frame with the plotter
        self.plotter = QVTKRenderWindowInteractor()
        
        self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
        self.interactor_style = CustomInteractorStyle()
        self.interactor.SetInteractorStyle(self.interactor_style)
        
        # Set up a VTK renderer and add it to the interactor
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        
        self.plotter.Initialize()
        self.plotter.Start()

        Axis(self.renderer, 100)
        Planes(self.renderer)
        
        self.layout_plotter.addWidget(self.plotter)
        
        self.camera = vtk.vtkCamera()
        self.SetCameraPlotter()

    def CreateSettings(self):
        layout_options = QVBoxLayout()
        frame_options = QWidget()
        frame_options.setStyleSheet(style_widget)
        frame_options.setMaximumWidth(250)
        self.layout.addWidget(frame_options, 0, 1, 3, 1)
        
        title = QLabel("Change origin:")
        title.setFixedHeight(30)
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title)
        
        labels = ["X:", "Y:", "Z:", "y:", "p:", "r:"]
        self.origin_pos = []
        for name in labels:
            frame = QWidget()
            layout_axis = QHBoxLayout()
            layout_axis.setContentsMargins(0,0,0,0)
            frame.setLayout(layout_axis)
            layout_options.addWidget(frame)

            label = QLabel(name)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20) 

            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            layout_axis.addWidget(label)
            layout_axis.addWidget(entry) 
            
        self.button_update = QPushButton("Update")
        self.button_update.setStyleSheet(style_button_menu)
        layout_options.addWidget(self.button_update)
        self.button_update.clicked.connect(lambda: change_origin_3d_model())
        
        self.button_add_new = QPushButton("Add new 3D model")
        self.button_add_new.setStyleSheet(style_button_menu)
        layout_options.addWidget(self.button_add_new)
        self.button_add_new.clicked.connect(lambda: add_new_3d_model())  

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_options.addItem(space_widget)   

        frame_options.setLayout(layout_options)

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
        
        self.rendering()
        
    def ClearPlotter(self):
       if self.stl_actor and self.renderer:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window

    def ClosePlotter(self):
        if self.plotter:
            # self.plotter.Finalize()
            self.plotter.close()
            # self.interactor.TerminateApp() 
            # self.renderer.RemoveAllViewProps()

            # self.layout.removeWidget(self.plotter)
            # self.plotter.deleteLater() 

            self.renderer = None
            self.plotter = None
            # self.interactor_style = None
            # self.interactor = None

    def CreateButtons(self, item, robot_3d_data):
        frame = QWidget()
        layout_model = QHBoxLayout()
        layout_model.setContentsMargins(5,0,5,5)
        frame.setLayout(layout_model)
        self.frames.append(frame)
            
        label = QLabel(robot_3d_data[item][0])
        label.setStyleSheet(style_label)
        label.setFixedWidth(120)
        layout_model.addWidget(label)
        
        button_delete = QPushButton("X")
        button_delete.setFixedSize(25,25)
        button_delete.setStyleSheet(style_button)
        button_delete.pressed.connect(lambda: delete_robot_model(item))
        layout_model.addWidget(button_delete)
        
        button_origin = QPushButton("Origin")
        button_origin.setFixedSize(75,25)
        button_origin.setStyleSheet(style_button)
        button_origin.pressed.connect(lambda: show_3d_model_settings(item))
        layout_model.addWidget(button_origin)
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        
        combo_color = QComboBox()
        combo_color.view().setMinimumWidth(170)
        combo_color.addItems(colors)
        combo_color.setStyleSheet(style_combo)
        combo_color.setCurrentText(robot_3d_data[item][3])
        combo_color.currentTextChanged.connect(lambda text: change_color_3d_model(item, text))
        layout_model.addWidget(combo_color)

        
        linkages = ['Link 1', 'Link 2', 'Link 3', 'Link 4', 'Link 5', 'Link 6', 'Base']

        combo_link = QComboBox()
        combo_link.view().setMinimumWidth(170)
        combo_link.setStyleSheet(style_combo)
        combo_link.addItems(linkages)
        combo_link.setCurrentText(robot_3d_data[item][5])
        combo_link.currentTextChanged.connect(lambda text: change_link_3d_model(item, text))
        layout_model.addWidget(combo_link)

        self.layout_scroll.addWidget(frame) 

    def SetOriginfields(self, data):
        for i in range(6):
            self.origin_pos[i].setText(str(data[i]))

    def ClearSettings(self):
        for i in range(6):
            self.origin_pos[i].setText("0.0")

            
    def GetOriginData(self, data):
        for i in range(6):
            try:
                data[i] = float(self.origin_pos[i].text())
            except:
                data[i] = 0.0
                self.origin_pos[i].setText("0.0")
                
        return data

    def DeleteButtons(self):
        for frame in self.frames:
            self.layout_scroll.removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater() 
            frame = None

        self.frames = []

    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.plotter.Render() 

    def rendering(self):
        try:
            self.interactor.Disable()
            self.plotter.Render() 
            self.interactor.Enable()
        except:
            print("Error rendering")