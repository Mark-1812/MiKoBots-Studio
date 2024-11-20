

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

class SimulationGUI(QWidget):
    def __init__(self, frame):      
        super().__init__()      
        self.file_management = FileManagement()  
        
        
        
        self.views = [
            [(1, 0, 0), (0, 0, 0), (0, 0, 1)], 
            [(0, 1, 0), (0, 0, 0), (0, 0, 1)],
            [(0, 0, -1), (0, 0, 0), (0, 1, 0)],
            [(1, 1, 1), (0, 0, 0), (0, 0, 1)]
            ]
        
        self.plotter_items = []
        self.plotter_axis = []
        self.plotter_robot = []
        self.plotter_tool = [None, None, None, None]
        
        self.CreatePlotter(frame)
        self.floor = Floor(self.renderer)
        self.axis = Axis(self.renderer, 500)
        
        self.GUI(frame)
        
        self.subscribeToEvents()
        self.floor.HideShowFloor()
        self.axis.HideShowAxis()

        setup_renderer_robot(self.renderer, self.plotter, self.interactor)
        setup_renderer_object(self.renderer, self.plotter, self.interactor)
        setup_renderer_origin(self.renderer, self.plotter, self.interactor)
        

    def subscribeToEvents(self):
        event_manager.subscribe("request_add_axis_to_plotter", self.AddAxisToPlotter)
        event_manager.subscribe("request_change_pos_axis", self.ChangePosAxis)
        event_manager.subscribe("request_delete_axis_plotter", self.DeleteAxisPlotter) 
       
        event_manager.subscribe("set_camera_pos_plotter", self.SetCameraPlotter)

        event_manager.subscribe("request_close_plotter", self.ClosePlotter)

    def CreatePlotter(self, frame):
        self.layout = QGridLayout(frame)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
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
        
    def GUI(self, frame):     

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
        frame.setLayout(self.layout)  # Ensure the frame's layout is set

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
        
  
    # add axis to plotter
    
    def AddAxisToPlotter(self, item):
        pass
        self.plotter_axis.append([[[],[],[]],[[],[],[]],[],[]])
        
        pointOrigin = np.array([0, 0, 0])
        pointX = np.array([150, 0, 0])
        pointY = np.array([0, 150, 0])
        pointZ = np.array([0, 0, 150])
        
        line_x_source = vtk.vtkLineSource()
        line_x_source.SetPoint1(pointOrigin)
        line_x_source.SetPoint2(pointX)
        
        line_y_source = vtk.vtkLineSource()
        line_y_source.SetPoint1(pointOrigin)
        line_y_source.SetPoint2(pointY)
        
        line_z_source = vtk.vtkLineSource()
        line_z_source.SetPoint1(pointOrigin)
        line_z_source.SetPoint2(pointZ)
        
        # Store the VTK line objects
        self.plotter_axis[item][0][0] = line_x_source
        self.plotter_axis[item][0][1] = line_y_source
        self.plotter_axis[item][0][2] = line_z_source

        # Create mappers and actors for each line
        mapper_x = vtk.vtkPolyDataMapper()
        mapper_x.SetInputConnection(line_x_source.GetOutputPort())
        actor_x = vtk.vtkActor()
        actor_x.SetMapper(mapper_x)
        actor_x.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red color
        actor_x.GetProperty().SetLineWidth(5)

        mapper_y = vtk.vtkPolyDataMapper()
        mapper_y.SetInputConnection(line_y_source.GetOutputPort())
        actor_y = vtk.vtkActor()
        actor_y.SetMapper(mapper_y)
        actor_y.GetProperty().SetColor(0.0, 1.0, 0.0)  # Green color
        actor_y.GetProperty().SetLineWidth(5)

        mapper_z = vtk.vtkPolyDataMapper()
        mapper_z.SetInputConnection(line_z_source.GetOutputPort())
        actor_z = vtk.vtkActor()
        actor_z.SetMapper(mapper_z)
        actor_z.GetProperty().SetColor(0.0, 0.0, 1.0)  # Blue color
        actor_z.GetProperty().SetLineWidth(5)
        
        # Add the actors to the renderer
        self.plotter_axis[item][1][0] = actor_x
        self.plotter_axis[item][1][1] = actor_y
        self.plotter_axis[item][1][2] = actor_z

        self.renderer.AddActor(actor_x)
        self.renderer.AddActor(actor_y)
        self.renderer.AddActor(actor_z)
        
        # Initialize the transformation matrixes
        self.plotter_axis[item][2] = np.eye(4)  # Matrix for transformations
        self.plotter_axis[item][3] = np.eye(4)  # Another matrix (identity) 
        
        self.rendering() 
    
    def DeleteAxisPlotter(self):
        for axis in self.plotter_axis:
            for actor in axis[1]:
                if actor:
                    self.renderer.RemoveActor(actor)

        # Clear the list to release memory
        self.plotter_axis.clear()
        
        self.rendering() 
         
    def ChangePosAxis(self, item, pos):
        self.plotter_axis[item][2][0][3] = float(pos[1])
        self.plotter_axis[item][2][1][3] = float(pos[2])
        self.plotter_axis[item][2][2][3] = float(pos[3])

        transform = vtk.vtkTransform()
        transform.Translate(self.plotter_axis[item][2][0][3], self.plotter_axis[item][2][1][3], self.plotter_axis[item][2][2][3])

        
        self.plotter_axis[item][1][0].SetUserTransform(transform)
        self.plotter_axis[item][1][1].SetUserTransform(transform)
        self.plotter_axis[item][1][2].SetUserTransform(transform)

        self.rendering()
        

                  
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

        
                    

