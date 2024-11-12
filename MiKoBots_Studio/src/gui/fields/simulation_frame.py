

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt, QPoint
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout, QMenu, QAction, QVBoxLayout, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QCursor, QIcon

from functools import partial

from gui.style import *

import numpy as np

from backend.core.event_manager import event_manager

from backend.simulation import simulation_move_gui

from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from backend.file_managment.file_management import FileManagement
import vtk

from backend.simulation.floor import Floor
from backend.simulation.axis import Axis


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        super().__init__()

    # Override the middle mouse button press event to rotate
    def OnMiddleButtonDown(self):
        self.StartRotate()

    def OnMiddleButtonUp(self):
        self.EndRotate()

    def OnMouseMove(self):
        if self.GetInteractor().GetControlKey():  # If Control is pressed
            return  # Do not rotate if Control is pressed

        self.Rotate()  # Rotate the camera

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
        self.axis = Axis(self.renderer)
        
        self.GUI(frame)
        
        self.subscribeToEvents()
        self.floor.HideShowFloor()
        self.axis.HideShowAxis()
        

    def subscribeToEvents(self):
        event_manager.subscribe("request_add_item_to_plotter", self.AddItemToPlotter)
        event_manager.subscribe("request_add_robot_to_plotter", self.AddRobotToPlotter)
        event_manager.subscribe("request_add_tool_to_plotter", self.AddToolToPlotter)
       
        event_manager.subscribe("request_delete_item_plotter", self.DeleteItemPlotter)
        event_manager.subscribe("request_delete_robot_plotter", self.DeleteRobotPlotter)
        event_manager.subscribe("request_delete_tool_plotter", self.DeleteToolPlotter)
       
        event_manager.subscribe("request_change_color_item", self.ChangeColorItem)
       
        event_manager.subscribe("request_move_robot", self.ChangePosRobot)
        event_manager.subscribe("request_change_pos_item", self.ChangePosItems) 
       
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

        simulation_move_gui(posJoint, "MoveJ")



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
        self.interactor.Disable()
        #self.renderer.Render()
        self.plotter.Render() 
        self.interactor.Enable()
        
        
        
    # add item to plotter

    def AddItemToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_items.append([[],[],[],[]])
        item = len(self.plotter_items) - 1
        
        reader = vtk.vtkSTLReader()
        reader.SetFileName(data[0])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        color = [0,0,0]
        if data[1] == "red":
            color = [1,0,0]
        elif data[1] == "darkgray":
            color = [0.4, 0.4, 0.4]

        self.plotter_items[item][0] = vtk.vtkActor()
        self.plotter_items[item][0].SetMapper(mapper)
        self.plotter_items[item][0].GetProperty().SetColor(color)
        self.plotter_items[item][1] = self.renderer.AddActor(self.plotter_items[item][0])
        self.plotter_items[item][2] = data[2]
        self.plotter_items[item][3] = data[3]  
        
        self.rendering() 
        
    def DeleteItemPlotter(self):
        for i in range(len(self.plotter_items)):
            self.renderer.RemoveActor(self.plotter_items[i][0])
        
        self.plotter_items = []
        self.rendering() 

    def ChangePosItems(self, item, matrix):
        matrix_data = matrix
        vtk_matrix = vtk.vtkMatrix4x4()
        # Copy the values from your matrix into the vtkMatrix4x4
        vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                            matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                            matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                            matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))

        # Now apply the vtkMatrix4x4 to your transform
        transform = vtk.vtkTransform()
        transform.SetMatrix(vtk_matrix)
        
        self.plotter_items[item][0].SetUserTransform(transform)
        self.plotter_items[item][2] = np.linalg.inv(matrix)
     
        self.rendering()  
        
    def ChangeColorItem(self, color_object, item):  
        self.plotter_items[item][0].GetProperty().SetColor(color_object)
        self.rendering() 


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
        
        
    # function forrobot to the plotter
        
    def AddRobotToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_robot.append([[],[],[],[],[]])
        item = len(self.plotter_robot) - 1

        reader = vtk.vtkSTLReader()
        reader.SetFileName(data[0])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        color = [0,0,0]
        if data[1] == "red":
            color = [1,0,0]
        elif data[1] == "darkgray":
            color = [0.4, 0.4, 0.4]

        self.plotter_robot[item][0] = vtk.vtkActor()
        self.plotter_robot[item][0].SetMapper(mapper)
        self.plotter_robot[item][0].GetProperty().SetColor(color)
        self.plotter_robot[item][1] = self.renderer.AddActor(self.plotter_robot[item][0])#, data[1], show_edges=False)
        self.plotter_robot[item][2] = data[2]
        self.plotter_robot[item][3] = data[3]  
        self.plotter_robot[item][4] = data[4] 
        
        self.rendering() 
     
    def DeleteRobotPlotter(self):
        for i in range(len(self.plotter_robot)):
            self.renderer.RemoveActor(self.plotter_robot[i][0])
            
        self.plotter_robot = []
        self.rendering() 
        
    # add tool to the plotter    
        
    def AddToolToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_tool = [0,0,0,0]

        reader = vtk.vtkSTLReader()
        reader.SetFileName(data[0])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        color = [0,0,0]
        if data[1] == "red":
            color = [1,0,0]
        elif data[1] == "darkgray":
            color = [0.4, 0.4, 0.4]

        self.plotter_tool[0] = vtk.vtkActor()
        self.plotter_tool[0].SetMapper(mapper)
        self.plotter_tool[0].GetProperty().SetColor(color)
        self.plotter_tool[1] = self.renderer.AddActor(self.plotter_tool[0])#, data[1], show_edges=False)
        self.plotter_tool[2] = data[2]
        self.plotter_tool[3] = data[3]  
        
    def DeleteToolPlotter(self):
        if self.plotter_tool[0]:
            self.renderer.RemoveActor(self.plotter_tool[0])
            
            self.plotter_tool = [None, None, None, None]
        
        self.rendering() 

    # change position of items in the plotter

    def ChangePosRobot(self, matrix, name_joints, number_of_joints, extra_joint):
        if len(self.plotter_robot) > number_of_joints - 1 + extra_joint:
            
            for i in range(len(self.plotter_robot)):
                if self.plotter_robot[i][4] == "Link 1":   
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[0]])

                    matrix_data = matrix[name_joints[0]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  

                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[0]]                  
                if self.plotter_robot[i][4] == "Link 2":
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[1]])

                    matrix_data = matrix[name_joints[1]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  

                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[1]]       

                if self.plotter_robot[i][4] == "Link 3":
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[2]])

                    matrix_data = matrix[name_joints[2]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  

                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[2]] 
                if self.plotter_robot[i][4] == "Link 4":      
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[3]])
            
                    matrix_data = matrix[name_joints[3]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  
                    
                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[3]]                                     
                if self.plotter_robot[i][4] == "Link 5":            
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[4]])

                    matrix_data = matrix[name_joints[4]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  
                    
                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[4]] 

                if self.plotter_robot[i][4] == "Link 6":       
                    matrix_data = self.plotter_robot[i][2]
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[5]])

                    matrix_data = matrix[name_joints[5]]
                    vtk_matrix = vtk.vtkMatrix4x4()
                    # Copy the values from your matrix into the vtkMatrix4x4
                    vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                        matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                        matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                        matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                    # Now apply the vtkMatrix4x4 to your transform
                    transform = vtk.vtkTransform()
                    transform.SetMatrix(vtk_matrix)  
                    
                    self.plotter_robot[i][0].SetUserTransform(transform)
                    self.plotter_robot[i][3] = matrix[name_joints[5]]  
                    
                                                   
            if self.plotter_tool[0]:
                matrix_data = self.plotter_tool[2]
                self.plotter_tool[2] = np.linalg.inv(matrix[name_joints[6]])
                
                matrix_data = matrix[name_joints[6]]
                vtk_matrix = vtk.vtkMatrix4x4()
                # Copy the values from your matrix into the vtkMatrix4x4
                vtk_matrix.DeepCopy((matrix_data[0][0], matrix_data[0][1], matrix_data[0][2], matrix_data[0][3],
                                    matrix_data[1][0], matrix_data[1][1], matrix_data[1][2], matrix_data[1][3],
                                    matrix_data[2][0], matrix_data[2][1], matrix_data[2][2], matrix_data[2][3],
                                    matrix_data[3][0], matrix_data[3][1], matrix_data[3][2], matrix_data[3][3]))
                # Now apply the vtkMatrix4x4 to your transform
                transform = vtk.vtkTransform()
                transform.SetMatrix(vtk_matrix) 
                    
                self.plotter_tool[0].SetUserTransform(transform)
                self.plotter_tool[3] = matrix[name_joints[6]]  
  
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

        
                    

