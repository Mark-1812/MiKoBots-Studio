

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt, QPoint
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout, QMenu, QAction, QVBoxLayout, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QCursor, QIcon

from functools import partial

from gui.style import *

import numpy as np

from backend.core.event_manager import event_manager

from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from backend.file_managment.file_management import FileManagement
import vtk

from backend.simulation.floor import Floor
from backend.simulation.axis import Axis
from backend.simulation.simulation_interaction import CustomInteractorStyle

from backend.simulation.robot import setup_renderer_robot
from backend.simulation.object import setup_renderer_object
from backend.simulation.origins import setup_renderer_origin

from backend.run_program import run_single_line

import backend.core.variables as var

class SimulationGUI:
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)   
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.file_management = FileManagement()  
        
        self.views = [
            [(1, 0, 0), (0, 0, 0), (0, 0, 1)], 
            [(0, 1, 0), (0, 0, 0), (0, 0, 1)],
            [(0, 0, -1), (0, 0, 0), (0, 1, 0)],
            [(1, 1, 1), (0, 0, 0), (0, 0, 1)]
            ]
        

        self.CreatePlotter()
        self.floor = Floor(self.renderer)
        self.axis = Axis(self.renderer, 500)
        
        self.GUI()
        
        self.subscribeToEvents()
        self.floor.HideShowFloor()
        self.axis.HideShowAxis()

        setup_renderer_robot(self.renderer, self.plotter, self.interactor)
        setup_renderer_object(self.renderer, self.plotter, self.interactor)
        setup_renderer_origin(self.renderer, self.plotter, self.interactor)
        
        self.parent_frame.setLayout(self.layout)


    def subscribeToEvents(self):
        event_manager.subscribe("set_camera_pos_plotter", self.SetCameraPlotter)
        event_manager.subscribe("request_close_plotter", self.ClosePlotter)

    def CreatePlotter(self):
        frame1 = QFrame()
        frame1.setStyleSheet(style_frame)  # Ensure style_frame is defined
        self.layout.addWidget(frame1, 0, 0)
        
        self.layout1 = QGridLayout()
        self.layout1.setContentsMargins(8, 8, 8, 8)

        frame1.setLayout(self.layout1)
        
        # create a plotter
        self.plotter = QVTKRenderWindowInteractor(frame1)        
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        
        self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
        self.interactor_style = CustomInteractorStyle()
        self.interactor.SetInteractorStyle(self.interactor_style)
        self.interactor.AddObserver("RightButtonPressEvent", self.show_context_menu)

        self.camera = vtk.vtkCamera()
        # Set up mouse interaction
        
    def GUI(self):     

        button_menu = QHBoxLayout()
        button_menu.setContentsMargins(10,10,10,10)
        
        image_path = self.file_management.resource_path('3d view.png')
       
        self.button_view = QPushButton()
        self.button_view.setFixedSize(20,20)
        self.button_view.setIcon(QIcon(image_path))
        self.button_view.setToolTip('Change view')  
        self.button_view.setStyleSheet(style_button_3d)
        self.button_view.clicked.connect(partial(self.change_view))
        self.button_view.setFixedSize(40,20)
        
        image_path = self.file_management.resource_path('Assen_kruis.png')
        
        self.button_axis = QPushButton()
        self.button_axis.setFixedSize(20,20)
        self.button_axis.setIcon(QIcon(image_path))
        self.button_axis.setToolTip('Show/hide axis')
        self.button_axis.setStyleSheet(style_button_3d)
        self.button_axis.clicked.connect(self.ShowAxis)
        self.button_axis.setFixedSize(40,20)
        
        image_path = self.file_management.resource_path('floor.png')
        
        self.button_floor = QPushButton()
        self.button_floor.setFixedSize(20,20)
        self.button_floor.setIcon(QIcon(image_path))
        self.button_floor.setToolTip('Show/hide floor')
        self.button_floor.setStyleSheet(style_button_3d)
        self.button_floor.clicked.connect(self.ShowFloor)
        self.button_floor.setFixedSize(40,20)
        
        
        
        button_menu.addWidget(self.button_view)
        button_menu.addWidget(self.button_axis)
        button_menu.addWidget(self.button_floor)
        

       
        # Add the plotter to the layout
        self.layout1.addWidget(self.plotter,0,0)
        
         # Add the button menu layout to the main layout
        self.layout1.addLayout(button_menu,0,0, alignment=Qt.AlignTop | Qt.AlignCenter)  # Add the button menu at the top
        

        # Set the main layout for the frame

    def ShowFloor(self):
        self.floor.HideShowFloor()
        self.rendering()
        
    def ShowAxis(self):
        self.axis.HideShowAxis()
        self.rendering()
        
    def show_context_menu(self, obj, event):
        click_pos = self.interactor.GetEventPosition()


        context_menu = QMenu(self)

        # Add actions to the menu
        action1 = QAction("Move to", self)
        action1.triggered.connect(lambda: self.move_to(click_pos))
        context_menu.addAction(action1)

        #action2 = QAction("Action 2", self)
        #action2.triggered.connect(self.action2_triggered)
        #context_menu.addAction(action2)

        # Show the context menu at the mouse position
        context_menu.exec_(QCursor.pos())

    def move_to(self, position):
        # Here you can implement the logic for moving the object
        # Convert click position to 3D coordinates
        x = position[0]
        y = position[1]

        # Use the picker to get the 3D coordinates
        picker = vtk.vtkWorldPointPicker()
        picker.Pick(x, y, 0, self.renderer)

        picked_position = picker.GetPickPosition()

        posJoint = [picked_position[0], picked_position[1], picked_position[2], 180, 0 ,180]

        run_single_line(f"robot.MoveJ({posJoint}, {var.JOG_SPEED}, {var.JOG_ACCEL})")




## axis

    def ClosePlotter(self):
    # Remove observers to avoid any lingering callbacks
        if hasattr(self, 'interactor') and self.interactor is not None:
            self.interactor.RemoveObservers("RightButtonPressEvent")

        # Finalize and terminate interactor
        if hasattr(self, 'plotter') and self.plotter is not None:
            render_window = self.plotter.GetRenderWindow()
            if render_window is not None:
                render_window.Finalize()  # Release OpenGL context and resources
            
        if hasattr(self, 'interactor') and self.interactor is not None:
            self.interactor.TerminateApp()  # Properly terminate the interactor
        
        # Explicitly delete references (optional but good practice)
        self.plotter = None
        self.renderer = None
        self.interactor = None
 
    def rendering(self):
        try:
            self.interactor.Disable()
            #self.renderer.Render()
            self.plotter.Render() 
            self.interactor.Enable()
        except:
            print("Error rendering")
           
    def SetCameraPlotter(self, view):
        self.camera.SetPosition(2000, -2000, 2000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.rendering()  
                
    def change_view(self):
        menu = QMenu()
        action1 = menu.addAction("Front view")
        action2 = menu.addAction("Right view")
        action3 = menu.addAction("Top view")
        action4 = menu.addAction("3D view")

        action = menu.exec_(self.button_view.mapToGlobal(self.button_view.rect().center()))
        if action == action1:
            self.camera.SetPosition(1000, 0, 0)
            self.camera.SetFocalPoint(0, 0, 0)
            self.camera.SetViewUp(0, 0, 1)
        elif action == action2:
            self.camera.SetPosition(0, -1000, 0)
            self.camera.SetFocalPoint(0, 0, 0)
            self.camera.SetViewUp(0, 0, 1)
        elif action == action3:
            self.camera.SetPosition(0, 0, 1000)
            self.camera.SetFocalPoint(0, 0, 0)
            self.camera.SetViewUp(0, 1, 0)
        elif action == action4:
            self.camera.SetPosition(2000, -2000, 2000)
            self.camera.SetFocalPoint(0, 0, 0)
            self.camera.SetViewUp(0, 0, 1)

        
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        self.rendering()  

        
                    

