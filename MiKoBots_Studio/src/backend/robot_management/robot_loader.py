from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog

import json
import backend.core.variables as var
import numpy as np
import os
import stat
import shutil
import zipfile
from pathlib import Path

from backend.calculations import forwardKinematics, inverseKinematics, matrix_to_xyz

from backend.file_managment import get_file_path

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import InfoMessage, ErrorMessage, WarningMessageRe


from backend.simulation.robot import add_robot_sim, change_pos_robot, add_tool_sim, delete_robot_sim, delete_tool_sim


class RobotLoader(QObject):

    def __init__(self):
        super().__init__()
        
        #a list with all the robots that exsist
        self.robotFile = []    

        self.pos_axis = None
        self.pos_axis_sim = None

        self.pos_joint = None
        self.pos_joint_sim = None

        self.joint_speed = None
        self.joint_max_move = None

        self.selected_robot = None
        self.robot_name = None
        self.settings_robot = None

        var.NUMBER_OF_JOINTS = None

        var.TOOL_FRAME = None
        
             
            
    def CloseCurrentRobot(self):
        delete_robot_sim()
        event_manager.publish("request_delete_buttons_joint")
        event_manager.publish("request_delete_buttons_axis")
        event_manager.publish("request_delete_buttons_move")
        event_manager.publish("request_delete_tool_combo")
 
    def CreateNewButtons(self):
        event_manager.publish("request_create_buttons_joint", var.NUMBER_OF_JOINTS)
        event_manager.publish("request_create_buttons_axis", var.NUMBER_OF_JOINTS)  
        event_manager.publish("request_create_buttons_move", var.NUMBER_OF_JOINTS, var.NAME_JOINTS, var.NAME_AXIS)    


        for i in range(len(self.robotFile['Tools'])):
            event_manager.publish("request_add_tool_combo", self.robotFile['Tools'][i][0])
        event_manager.publish("request_add_tool_combo", "No tool")  
 
    def ChangeRobot(self):   
        event_manager.publish("request_set_robot_combo", var.ROBOT_NAME)
 
        # Platform for file path
        file = get_file_path("/Robot_library/" + var.ROBOT_NAME + "/settings.json") 
        
        # if the robot already exsist open the file of the robot
        try:
            with open(file, 'r') as file:
                self.robotFile = json.load(file)
        except FileNotFoundError:
            print(var.LANGUAGE_DATA.get("message_not_open_robot"))
                
        var.POS_AXIS_SIM = [0,0,0,0,0,0]
        var.POS_JOINT_SIM = [0,0,0,0,0,0]    
        var.POS_AXIS = [0,0,0,0,0,0]
        var.POS_JOINT = [0,0,0,0,0,0] 
        var.TOOL_FRAME = [0,0,0,0,0,0]  

        var.ROBOT_SETTINGS = self.robotFile['Settings']
        

        var.MAX_JOINT_MOVE = var.ROBOT_SETTINGS['Set_max_pos'][0]
        var.MAX_JOINT_SPEED = var.ROBOT_SETTINGS['Set_speed'][0]
        
        var.NUMBER_OF_JOINTS = int(var.ROBOT_SETTINGS['Set_number_of_joints'][0])
        var.DH_PARAM = var.ROBOT_SETTINGS['Set_dh_par'][0]

        
        if len(var.DH_PARAM) > var.NUMBER_OF_JOINTS:
            var.EXTRA_JOINT = 1
        else:
            var.EXTRA_JOINT = 0


        matrix = forwardKinematics(var.NUMBER_OF_JOINTS, [0]*var.NUMBER_OF_JOINTS, var.DH_PARAM)
        var.POS_AXIS_SIM = matrix_to_xyz(var.NUMBER_OF_JOINTS, matrix["TOOL"])   



    def ShowPosRobot(self):
        event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
        event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)



        
    def AddRobotToPlotter(self):
        settings_3d_model = self.robotFile['3Dfiles']


        for i in range(len(settings_3d_model)):
            file_path = get_file_path(settings_3d_model[i][2])   
            data = [file_path, settings_3d_model[i][3], np.eye(4), np.eye(4), settings_3d_model[i][5]]
            add_robot_sim(data)
            
        matrix = forwardKinematics(var.NUMBER_OF_JOINTS, [0]*var.NUMBER_OF_JOINTS, var.DH_PARAM)
        change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
        var.POS_AXIS_SIM = matrix_to_xyz(var.NUMBER_OF_JOINTS, matrix["TOOL"])  

        event_manager.publish("set_camera_pos_plotter", 3)         
    
  
    def changeTool(self, tool):
        delete_tool_sim()
        var.TOOL_SETTINGS = self.robotFile['Tools']  

        # if no tool
        if (tool + 1) > len(var.TOOL_SETTINGS):
            var.TOOL = len(var.TOOL_SETTINGS)
            
            var.TOOL_FRAME = [0,0,0,0,0,0] 
            var.TOOL_CAM_OFFSET = [0,0,0]    
            var.TOOL_TYPE = "None"
            var.TOOL_POS = 0
            
            joint_angles_end = inverseKinematics(var.NUMBER_OF_JOINTS,var.POS_AXIS_SIM, var.POS_JOINT_SIM)
            matrix = forwardKinematics(var.NUMBER_OF_JOINTS, joint_angles_end, var.DH_PARAM)
            change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
            
    

        elif len(var.TOOL_SETTINGS) > 0:
            file_path = get_file_path(var.TOOL_SETTINGS[tool][2])
            data = [file_path, var.TOOL_SETTINGS[tool][3], np.eye(4), np.eye(4)]

            add_tool_sim(data)

            var.TOOL_NAME = var.TOOL_SETTINGS[tool][0]
            var.TOOL_FRAME = var.TOOL_SETTINGS[tool][5]   
            var.TOOL_CAM_OFFSET = var.TOOL_SETTINGS[tool][9]         
            var.TOOL_TYPE = var.TOOL_SETTINGS[tool][7]
            var.TOOL_SERVO_SETTINGS = var.TOOL_SETTINGS[tool][8] 
            var.TOOL_POS = 0
            var.TOOL_CAM_SETTINGS = var.TOOL_SETTINGS[tool][11]

            string_tool_nr = var.TOOL_SETTINGS[tool][6]
            number = int(string_tool_nr.split()[-1]) - 1

            var.TOOL_PIN = var.ROBOT_SETTINGS["Set_tools"][0][number]


                    
        var.TOOL = tool
        
        joint_angles_end = inverseKinematics(var.NUMBER_OF_JOINTS,var.POS_AXIS_SIM, var.POS_JOINT_SIM)
        matrix = forwardKinematics(var.NUMBER_OF_JOINTS, joint_angles_end, var.DH_PARAM)
        change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
        
            
        # send settings to the robot       
            

    
    

                    
    
                            


        

         

     
               
 


            