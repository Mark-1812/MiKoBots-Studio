

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QDialog, QCheckBox, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog

from functools import partial

from gui.tabs_field.simulation.windows.simulation_objects_gui import SimulationObjectsGUI
from gui.tabs_field.simulation.windows.simulation_origin_gui import SimulationOriginGUI

from gui.style import *

import pyvistaqt as pvt
import pyvista as pv
import numpy as np

from backend.core.event_manager import event_manager

from backend.core.api import enable_simulation
from backend.core.api import stop_script
from backend.core.api import run_script


class SimulationGUI(QWidget):
    def __init__(self, frame):              
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
        self.plotter = pvt.QtInteractor()              
        self.layout1.addWidget(self.plotter,0,0,2,9)
        
        self.plotter.add_axes()
        self.plotter.camera_position = [(1, 1, 1), (0, 0, 0), (0, 0, 1)]
        self.plotter.reset_camera()
        self.plotter.show()           
        
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

    # add item to plotter

    def AddItemToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_items.append([[],[],[],[]])
        item = len(self.plotter_items) - 1
        
        self.plotter_items[item][0] = pv.read(data[0])
        self.plotter_items[item][1] = self.plotter.add_mesh(self.plotter_items[item][0], data[1], show_edges=False)
        self.plotter_items[item][2] = data[2]
        self.plotter_items[item][3] = data[3]  
        
    def DeleteItemPlotter(self):
        for i in range(len(self.plotter_items)):
            self.plotter.remove_actor(self.plotter_items[i][1])
        
        self.plotter_items = []

    def ChangePosItems(self, item, matrix):
        self.plotter_items[item][0].transform(self.plotter_items[item][2])
        self.plotter_items[item][2] = np.linalg.inv(matrix)
        self.plotter_items[item][0].transform(matrix)

    def ChangeColorItem(self, color, item):
        self.plotter_items[item][1].mapper.scalar_visibility = False 
        self.plotter_items[item][1].GetProperty().SetColor(color)
        self.plotter.update()

    # add xis to plotter
    
    def AddAxisToPlotter(self, item):
        self.plotter_axis.append([[[],[],[]],[[],[],[]],[],[]])
        
        pointOrigin = np.array([0, 0, 0])
        pointX = np.array([150, 0, 0])
        pointY = np.array([0, 150, 0])
        pointZ = np.array([0, 0, 150])
        
        self.plotter_axis[item][0][0] = pv.Line(pointOrigin, pointX)
        self.plotter_axis[item][0][1] = pv.Line(pointOrigin, pointY)
        self.plotter_axis[item][0][2] = pv.Line(pointOrigin, pointZ)
        
        self.plotter_axis[item][1][0] = self.plotter.add_mesh(self.plotter_axis[item][0][0], color="red", line_width=5)
        self.plotter_axis[item][1][1] = self.plotter.add_mesh(self.plotter_axis[item][0][1], color="green", line_width=5)
        self.plotter_axis[item][1][2] = self.plotter.add_mesh(self.plotter_axis[item][0][2], color="blue", line_width=5)

        self.plotter_axis[item][2] = np.eye(4)    # matrix
        self.plotter_axis[item][3] = np.eye(4)   
    
    def DeleteAxisPlotter(self):
        for j in range(len(self.plotter_axis)):            
            for i in range(3):  
                self.plotter.remove_actor(self.plotter_axis[j][1][i])
    
    def ChangePosAxis(self, item, pos):
        self.plotter_axis[item][2][0][3] = pos[1]
        self.plotter_axis[item][2][1][3] = pos[2]
        self.plotter_axis[item][2][2][3] = pos[3]

        for i in range(3):
            self.plotter_axis[item][0][i].transform(self.plotter_axis[item][3])  
            self.plotter_axis[item][0][i].transform(self.plotter_axis[item][2])  
            
        self.plotter_axis[item][3] = np.linalg.inv(self.plotter_axis[item][2])    # inverse matrix


    # function forrobot to the plotter
        
    def AddRobotToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_robot.append([[],[],[],[],[]])
        item = len(self.plotter_robot) - 1
        
        self.plotter_robot[item][0] = pv.read(data[0])
        self.plotter_robot[item][1] = self.plotter.add_mesh(self.plotter_robot[item][0], data[1], show_edges=False)
        self.plotter_robot[item][2] = data[2]
        self.plotter_robot[item][3] = data[3]  
        self.plotter_robot[item][4] = data[4] 
               
    def DeleteRobotPlotter(self):
        for i in range(len(self.plotter_robot)):
            self.plotter.remove_actor(self.plotter_robot[i][1])
            
        self.plotter_robot = []
        
    # add tool to the plotter    
        
    def AddToolToPlotter(self, data):
        # add the new robot to the plotter
        self.plotter_tool = [0,0,0,0]
        
        self.plotter_tool[0] = pv.read(data[0])
        self.plotter_tool[1] = self.plotter.add_mesh(self.plotter_tool[0], data[1], show_edges=False)
        self.plotter_tool[2] = data[2]
        self.plotter_tool[3] = data[3]  
        
        print("add tool to plotter")
        
    def DeleteToolPlotter(self):
        if self.plotter_tool[1]:
            self.plotter.remove_actor(self.plotter_tool[1])
            
            self.plotter_tool = [None, None, None, None]

    # change position of items in the plotter

    def ChangePosRobot(self, matrix, name_joints, number_of_joints, extra_joint):
        if len(self.plotter_robot) > number_of_joints - 1 + extra_joint:
            
            for i in range(len(self.plotter_robot)):
                if self.plotter_robot[i][4] == "Link 1":   
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[0]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[0]])
                    self.plotter_robot[i][3] = matrix[name_joints[0]]                  
                if self.plotter_robot[i][4] == "Link 2":             
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[1]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[1]])
                    self.plotter_robot[i][3] = matrix[name_joints[1]]               
                if self.plotter_robot[i][4] == "Link 3":             
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[2]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[2]])
                    self.plotter_robot[i][3] = matrix[name_joints[2]] 
                if self.plotter_robot[i][4] == "Link 4":             
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[3]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[3]])
                    self.plotter_robot[i][3] = matrix[name_joints[3]]                                     
                if self.plotter_robot[i][4] == "Link 5":             
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[4]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[4]])
                    self.plotter_robot[i][3] = matrix[name_joints[4]] 
                if self.plotter_robot[i][4] == "Link 6":             
                    self.plotter_robot[i][0].transform(self.plotter_robot[i][2])
                    self.plotter_robot[i][2] = np.linalg.inv(matrix[name_joints[5]])
                    self.plotter_robot[i][0].transform(matrix[name_joints[5]])
                    self.plotter_robot[i][3] = matrix[name_joints[5]]  
                    
                                                       
            if self.plotter_tool[0]:
                self.plotter_tool[0].transform(self.plotter_tool[2])
                self.plotter_tool[2] = np.linalg.inv(matrix[name_joints[6]])
                self.plotter_tool[0].transform(matrix[name_joints[6]])
                self.plotter_tool[3] = matrix[name_joints[6]]
  
                   
    def SetCameraPlotter(self, view):
        self.plotter.camera_position = self.views[view]
        self.plotter.camera.SetParallelProjection(True)
        self.plotter.camera.SetUseHorizontalViewAngle(True)
        self.plotter.reset_camera()       
                              
    def change_view(self):
        menu = QMenu()
        action1 = menu.addAction("Front view")
        action2 = menu.addAction("Right view")
        action3 = menu.addAction("Top view")
        action4 = menu.addAction("3D view")

        action = menu.exec_(self.button_view.mapToGlobal(self.button_view.rect().center()))
        if action == action1:
            self.SetCameraPlotter(0)
        elif action == action2:
            self.SetCameraPlotter(1)
        elif action == action3:
            self.SetCameraPlotter(2)
        elif action == action4:
            self.SetCameraPlotter(3)

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
                    

