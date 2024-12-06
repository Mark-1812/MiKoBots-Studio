from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QRadioButton, QGridLayout, QDialog, QVBoxLayout, QFrame, QComboBox, QFileDialog, QButtonGroup
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QIcon

from .robot_settings import RobotSettings
from .robot_overview import RobotOverview
from .robot_tools import RobotTools
from .robot_3d_model import Robot3DModel

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from backend.simulation.axis import Axis
from backend.simulation.planes import Planes
from backend.simulation.simulation_interaction import CustomInteractorStyle
from backend.simulation.robot import setup_renderer_robot_preview
from backend.robot_management.robot_settings import save_robot
from backend.robot_management import change_robot

from gui.style import *

from backend.core.event_manager import event_manager
from backend.file_managment.file_management import FileManagement

class RobotWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot settings")
        self.setFixedSize(1200,600)
        self.setStyleSheet("background-color: #E8E8E8;")
        
        file_management = FileManagement()
        image_path = file_management.resource_path('mikobot.ico')
        self.setWindowIcon(QIcon(image_path))
        
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10) 
        
        self.plotter = None
        
        self.CreateTabs()
        self.CreateMenu()
        self.CreatePlotter()
        self.CreateSaveButton()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("set_camera_pos_plotter_preview", self.SetCameraPlotter)
        
    def CreateMenu(self):
        layout_menu = QVBoxLayout() 
        layout_menu.setAlignment(Qt.AlignTop)
        menu_frame = QWidget(self)
        menu_frame.setStyleSheet(style_widget)
        menu_frame.setFixedWidth(150)
        menu_frame.setLayout(layout_menu)  
        
        title = QLabel("Menus")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout_menu.addWidget(title)
                 
        self.button_group = QButtonGroup()     
        self.button_names = ["Robots", "Tools", "Settings", "3D model"]    
        
        for name in self.button_names:
            radio_button = QRadioButton(name)
            radio_button.toggled.connect(lambda checked, name=name: self.show_hide(name))
            radio_button.setStyleSheet(style_button_tab)  # Expands to fill the available space
            layout_menu.addWidget(radio_button)
            self.button_group.addButton(radio_button)

        self.button_group.buttons()[0].setChecked(True)

        self.layout.addWidget(menu_frame, 0, 0, 2, 1)

    def CreateTabs(self):
        self.RobotOverview = RobotOverview()
        self.layout.addWidget(self.RobotOverview, 0, 1, 2, 1)
        
        self.RobotTools = RobotTools()
        self.layout.addWidget(self.RobotTools, 0, 1, 2, 1)
        self.RobotTools.hide()
        
        self.RobotSettings = RobotSettings()   
        self.layout.addWidget(self.RobotSettings, 0, 1, 2, 1)
        self.RobotSettings.hide()  
        
        self.Robot3DModel = Robot3DModel()
        self.layout.addWidget(self.Robot3DModel, 0, 1, 2, 1)
        self.Robot3DModel.hide()
        
    def CreateSaveButton(self):
        # create layout plotter
        layout_button = QVBoxLayout()
        layout_button.setContentsMargins(10, 10, 10, 10) 
        frame = QWidget(self)
        frame.setStyleSheet(style_widget)
        frame.setFixedWidth(400)
        self.layout.addWidget(frame, 1, 2)
        frame.setLayout(layout_button)

        button = QPushButton("Save robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: save_robot())
        layout_button.addWidget(button)        

    def CreatePlotter(self):
        # create layout plotter
        self.layout_plotter = QGridLayout()
        self.layout_plotter.setContentsMargins(10, 10, 10, 10) 
        frame_plotter = QWidget(self)
        frame_plotter.setStyleSheet(style_widget)
        frame_plotter.setFixedWidth(400)
        self.layout.addWidget(frame_plotter, 0, 2)
        frame_plotter.setLayout(self.layout_plotter)


    def OpenPlotter(self):
        self.plotter = QVTKRenderWindowInteractor()
        self.plotter.setFixedHeight(500)
        
        self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
        self.interactor_style = CustomInteractorStyle()
        self.interactor.SetInteractorStyle(self.interactor_style)
        
        
        # Set up a VTK renderer and add it to the interactor
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        
        # Start the interactor
        self.plotter.Initialize()
        self.plotter.Start()
        
        Axis(self.renderer, 100)
        Planes(self.renderer)

        self.camera = vtk.vtkCamera()
        self.SetCameraPlotter()

        setup_renderer_robot_preview(self.renderer, self.plotter, self.interactor)

        self.layout_plotter.addWidget(self.plotter, 0, 0)
    
    def show_hide(self, library):
        if library == "Robots":
            self.RobotOverview .show()
            self.RobotTools.hide()
            self.RobotSettings.hide()
            self.Robot3DModel.hide()
            
        elif library == "Tools":
            self.RobotOverview .hide()
            self.RobotTools.show()
            self.RobotSettings.hide()
            self.Robot3DModel.hide()   
                        
        elif library == "Settings":
            self.RobotOverview .hide()
            self.RobotTools.hide()
            self.RobotSettings.show()
            self.Robot3DModel.hide()  
                                
        elif library == "3D model":
            self.RobotOverview .hide()
            self.RobotTools.hide()
            self.RobotSettings.hide()
            self.Robot3DModel.show()   
            
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
            self.interactor_style = None
            self.interactor = None

    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.plotter.Render() 

    def closeEvent(self, event):
        self.RobotTools.ClosePlotter()
        self.Robot3DModel.ClosePlotter()
        self.ClosePlotter()

        change_robot()
        