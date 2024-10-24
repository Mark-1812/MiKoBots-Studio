

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QDialog, QCheckBox, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog

from functools import partial

from gui.tabs_field.simulation.windows.simulation_objects_gui import SimulationObjectsGUI
from gui.tabs_field.simulation.windows.simulation_origin_gui import SimulationOriginGUI

from gui.style import *

import numpy as np

from backend.core.event_manager import event_manager

from backend.core.api import enable_simulation
from backend.core.api import stop_script
from backend.core.api import run_script

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        super().__init__()

    # Override the middle mouse button press event to rotate
    def OnMiddleButtonDown(self):
        print("oke")
        self.StartRotate()

    def OnMiddleButtonUp(self):
        print("stop")
        self.EndRotate()

    def OnMouseMove(self):
        if self.GetInteractor().GetControlKey():  # If Control is pressed
            return  # Do not rotate if Control is pressed

        self.Rotate()  # Rotate the camera

class SimulationGUI(QWidget):
    def __init__(self, frame):      
        super().__init__()        
        self.simulation_origin_gui = SimulationOriginGUI()
        self.simulation_objects_gui = SimulationObjectsGUI()
        
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
        
        self.layout = QGridLayout(frame)
        self.GUI()
        
        self.subscribeToEvents()

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
        event_manager.subscribe("request_stop_sim", self.ButtonStopSim)


    def GUI(self):     
        frame1 = QFrame()
        frame1.setStyleSheet("QFrame { background-color: white; border: 0px solid black; border-radius: 5px; }")
        self.layout.addWidget(frame1,0,0,1,6)
        self.layout1 = QGridLayout()
        frame1.setLayout(self.layout1)
        
        # create a plotter
        self.plotter = QVTKRenderWindowInteractor(self)            
        self.layout1.addWidget(self.plotter,0,0,2,9)
        
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.plotter.GetRenderWindow().GetInteractor()  

        self.interactor_style = CustomInteractorStyle()
        self.interactor.SetInteractorStyle(self.interactor_style)
        
        self.ShowPlane() 
        
        self.camera = vtk.vtkCamera()
        # Set up mouse interaction

        checkbox = QCheckBox('Enable simulator')
        checkbox.setChecked(False)  # Set the initial state of the checkbox
        checkbox.setMaximumWidth(100)
        checkbox.setStyleSheet("background-color: white")
        self.layout1.addWidget(checkbox,0,0)
        
        checkbox.stateChanged.connect(lambda state: self.EnableSimulation(state))

        self.button_view = QPushButton('Change view')
        self.button_view.setStyleSheet(style_button)
        self.button_view.clicked.connect(partial(self.change_view))
        self.button_view.setMaximumWidth(100)
        self.layout1.addWidget(self.button_view, 2, 0)

        button = QPushButton("add origin")
        button.setStyleSheet(style_button)
        button.clicked.connect(self.simulation_origin_gui.show)
        button.setMaximumWidth(100)
        self.layout1.addWidget(button,2,1) 
        
        button = QPushButton("Show / hide")
        button.setStyleSheet(style_button)
        button.clicked.connect(lambda: self.ShowHide())
        button.setMaximumWidth(100)
        self.layout1.addWidget(button,2,2) 

        self.button_play_sim = QPushButton('Play')  
        self.button_play_sim.setStyleSheet(style_button)
        self.button_play_sim.clicked.connect(lambda: run_script(True)) 
        self.button_play_sim.setMaximumWidth(100)
        self.button_play_sim.hide()
        self.layout1.addWidget(self.button_play_sim, 2, 3) 
        
        self.BUTTON_SIM_STOP = QPushButton('Stop')  
        self.BUTTON_SIM_STOP.setStyleSheet(style_button)
        self.BUTTON_SIM_STOP.clicked.connect(stop_script) 
        self.BUTTON_SIM_STOP.setMaximumWidth(100)
        self.BUTTON_SIM_STOP.hide()
        self.layout1.addWidget(self.BUTTON_SIM_STOP, 2, 4)        
        
        # self.button_show_line = QPushButton('Show line')   
        # self.button_show_line.clicked.connect(self.show_line)
        # self.button_show_line.setMaximumWidth(100)
        # self.button_show_line.hide()
        # self.layout1.addWidget(self.button_show_line, 2, 5)
        
        # self.button_delete_line = QPushButton('Delete line')   
        # self.button_delete_line.clicked.connect(lambda: self.delete_line)
        # self.button_delete_line.setMaximumWidth(100)
        # self.button_delete_line.hide()
        # self.layout1.addWidget(self.button_delete_line, 2, 6)
        
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet("background-color: white")
        self.layout1.addWidget(spacer_widget, 2, 8) 

    def ShowPlane(self): 
        size_plane = 750
        
        def create_grid_plane(distance, size):
            lines = vtk.vtkCellArray()
            points = vtk.vtkPoints()

            # Generate points and lines
            for i in range(-size, size + 1, distance):
                # Horizontal lines
                p1_id = points.InsertNextPoint(-size, i, 0)
                p2_id = points.InsertNextPoint(size, i, 0)
                lines.InsertNextCell(2)
                lines.InsertCellPoint(p1_id)
                lines.InsertCellPoint(p2_id)

                # Vertical lines
                p1_id = points.InsertNextPoint(i, -size, 0)
                p2_id = points.InsertNextPoint(i, size, 0)
                lines.InsertNextCell(2)
                lines.InsertCellPoint(p1_id)
                lines.InsertCellPoint(p2_id)

            # Create a polydata object for the grid
            grid_polydata = vtk.vtkPolyData()
            grid_polydata.SetPoints(points)
            grid_polydata.SetLines(lines)
            
            return grid_polydata
        
        grid_distance = 50  # 50 mm
        grid_polydata = create_grid_plane(grid_distance, size_plane)
        
        # Mapper and Actor for the grid
        grid_mapper = vtk.vtkPolyDataMapper()
        grid_mapper.SetInputData(grid_polydata)
        grid_actor = vtk.vtkActor()
        grid_actor.SetMapper(grid_mapper)
        
        grid_actor.GetProperty().SetColor(0, 0, 0)  # RGB color
        
        # Create a plane on the XY axis
        plane_source = vtk.vtkPlaneSource()
        plane_source.SetOrigin(-size_plane, -size_plane, 0)  # Bottom left corner
        plane_source.SetPoint1(size_plane, -size_plane, 00)   # Bottom right corner
        plane_source.SetPoint2(-size_plane, size_plane, 0)   # Top left corner
        plane_source.SetResolution(10, 10)    # Number of points along the plane

        # Mapper and Actor for the plane
        plane_mapper = vtk.vtkPolyDataMapper()
        plane_mapper.SetInputConnection(plane_source.GetOutputPort())
        plane_actor = vtk.vtkActor()
        plane_actor.SetMapper(plane_mapper)

        # Set the color of the plane (e.g., light gray)
        plane_actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # RGB color
        plane_actor.GetProperty().SetOpacity(0.5)

        # Add the plane and axes to the scene
        self.renderer.AddActor(grid_actor)  # Add the grid actor
        self.renderer.AddActor(plane_actor)

    def ButtonStopSim(self):
        stop_script()

    def ButtonPlaySim(self, state):
        if state:
            self.button_play_sim.setStyleSheet(
                "QPushButton { background-color: green; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"+
                "QPushButton:hover { background-color: white; }"
                ) 
        else:
            self.button_play_sim.setStyleSheet(
                "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"+
                "QPushButton:hover { background-color: white; }"
                ) 

    def EnableSimulation(self, state):
        enable_simulation(state)
        if state ==  2:
            self.button_play_sim.show()
            self.BUTTON_SIM_STOP.show()
            # self.button_show_line.show()
            # self.button_delete_line.show()
        else:
            self.button_play_sim.hide()         
            self.BUTTON_SIM_STOP.hide()
            # self.button_show_line.hide()
            # self.button_delete_line.hide()

    def ClosePlotter(self):
        print("close plotter")
        self.plotter.close()

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
        print(matrix)
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


    # add xis to plotter
    
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

        # Apply the transformation to each axis actor
        for axis in self.plotter_axis:
            for actor in axis[1]:
                actor.SetUserTransform(transform)

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

    def show_line(self):
        #var.SIM_SHOW_LINE = 1
        #print("test show line")
        #self.RUN_PROGRAM.run_script()
        #var.SIM_SHOW_LINE = 0
        pass

    def ShowHide(self):
        print("show window")
        self.simulation_objects_gui.openevent()
        self.simulation_objects_gui.show()            
                    

