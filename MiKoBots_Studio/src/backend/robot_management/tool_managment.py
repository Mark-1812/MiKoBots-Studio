from PyQt5.QtWidgets import QMessageBox, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

import backend.core.variables as var

import numpy as np
import os
from stl import mesh
from pathlib import Path

from backend.calculations.kinematics_6_axis import ForwardKinematics_6, InverseKinmatics_6
from backend.calculations.kinematics_3_axis import ForwardKinematics_3, InverseKinematics_3
from backend.calculations.convert_matrix import MatrixToXYZ

from backend.file_managment.file_management import FileManagement

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import WarningMessageRe

from backend.simulation.robot import change_pos_robot, add_tool_sim, delete_tool_sim

from backend.run_program import run_single_line

class ToolManagment:
    def __init__(self):
        super().__init__()
        self.InverseKinematics_6 = InverseKinmatics_6()
        self.ForwardKinematics_6 = ForwardKinematics_6()
        
        self.InverseKinematics_3 = InverseKinematics_3()
        self.ForwardKinematics_3 = ForwardKinematics_3()
        
        self.file_management = FileManagement()
        
        self.selected_tool = None
        self.tool_type = None
        
    def GetToolInfo(self):
        return self.tool_type
        
    def SetupTool(self):
        event_manager.publish("request_delete_buttons_tool")
        event_manager.publish("request_clear_plotter_tool")
        event_manager.publish("request_delete_tool_combo")
        
        for i in range(len(var.TOOLS3D)):
            #event_manager.publish("request_delete_spacer_tool")
            event_manager.publish("request_create_buttons_tool", i, var.TOOLS3D)
            event_manager.publish("request_add_tool_combo", var.TOOLS3D[i][0])
            
            
        event_manager.publish("request_add_tool_combo", "No tool")
            

    def AddNewTool(self, robot, robot_name):
        # Select a new file with Qfiledialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        # if there is a file
        if not file_dialog.exec_():
            return
        
        file_path_tool = file_dialog.selectedFiles()[0]
        
        i = len(var.TOOLS3D)
        var.TOOLS3D.append([[],[],[],[],[],[],[],[],[],[],[],[]])
        
        # Get the name of the file
        filename = os.path.basename(file_path_tool)
        name, _ = os.path.splitext(filename)
        

        # get the name of the robot
        folder_name = robot_name       

        # Save the modified mesh to a new STL file             
        var.TOOLS3D[i][0] = name
        var.TOOLS3D[i][1] = (f"/Robot_library/{folder_name}/TOOLS_STL/ORIGINAL_{name}.STL")
        var.TOOLS3D[i][2] = (f"/Robot_library/{folder_name}/TOOLS_STL/{name}.STL")
        var.TOOLS3D[i][3] = "red"
        var.TOOLS3D[i][4] = [0,0,0,0,0,0] # Position origin
        var.TOOLS3D[i][5] = [0,0,0,0,0,0] # Tool frame
        var.TOOLS3D[i][6] = "Tool pin 1" # Tool pin number
        var.TOOLS3D[i][7] = "None" # Type of tool pin (Servo or relay)
        var.TOOLS3D[i][8] = ["min","max"] # min and max value
        var.TOOLS3D[i][9] = [0,0,0] # Offset XYZ tool
        var.TOOLS3D[i][10] = 0 # Turn camera 180 degrees
        var.TOOLS3D[i][11] = [0,0,0,0,0] # var.TOOL_SETTINGS_CAM[0], var.TOOL_SETTINGS_CAM[1], var.TOOL_SETTINGS_CAM[2], var.TOOL_SETTINGS_CAM[3], var.TOOL_SETTINGS_CAM[4]

        # Get the name of the folder of the current robot
        file_path_1 = self.file_management.GetFilePath(var.TOOLS3D[i][1])
        file_path_2 = self.file_management.GetFilePath(var.TOOLS3D[i][2])
        
        item = mesh.Mesh.from_file(file_path_tool)
        item.save(file_path_1)
        item.save(file_path_2)
        
        
        #event_manager.publish("request_delete_spacer_tool")
        event_manager.publish("request_new_buttons", i, var.TOOLS3D)
        event_manager.publish("request_delete_tool_combo")
        
        for j in range(len(var.TOOLS3D)):
            event_manager.publish("request_add_tool_combo", var.TOOLS3D[j][0])   
            
        event_manager.publish("request_add_tool_combo", "No tool")
        event_manager.publish("request_save_robot_tool")
                
    def changeTool(self, tool):
        delete_tool_sim()
    
        # if no tool
        if (tool + 1) > len(var.TOOLS3D):
            self.selected_tool = len(var.TOOLS3D)

            var.TOOL_FRAME = [0,0,0,0,0,0] 
            if var.NUMBER_OF_JOINTS == 6:
                joint_pos = self.InverseKinematics_6.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                matrix = self.ForwardKinematics_6.ForwardKinematics(joint_pos)
                change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
            elif var.NUMBER_OF_JOINTS == 3 and var.EXTRA_JOINT:
                try:
                    joint_pos = self.InverseKinematics_3.inverseKinematics(var.POS_AXIS_SIM)
                    matrix = self.ForwardKinematics_3.ForwardKinematics(joint_pos)
                    change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT) 
                except:
                    print(" Error")     
            return
    
    
        if len(var.TOOLS3D) > 0:
            file_path = self.file_management.GetFilePath(var.TOOLS3D[tool][2])
            
            data = [file_path, var.TOOLS3D[tool][3], np.eye(4), np.eye(4)]

            add_tool_sim(data)
 
            var.TOOL_FRAME = var.TOOLS3D[tool][5]            
            var.TOOL_OFFSET_CAM = var.TOOLS3D[tool][9]
            var.TOOL_SETTINGS_CAM = var.TOOLS3D[tool][11] 
                    
        self.selected_tool = tool
        
        if var.NUMBER_OF_JOINTS == 6:
            joint_pos = self.InverseKinematics_6.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
            matrix = self.ForwardKinematics_6.ForwardKinematics(joint_pos)
            change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)

        elif var.NUMBER_OF_JOINTS == 3:
            matrix = self.ForwardKinematics_3.ForwardKinematics([0,0,0])
            change_pos_robot(matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
            
        # send settings to the robot
        
            
                    
    def ShowSettings(self, tool):
        self.selected_tool = tool
        tool_settings = var.TOOLS3D[self.selected_tool]
        event_manager.publish("request_show_tool_settings", tool_settings)
        event_manager.publish("request_clear_plotter_tool")
        file_path = self.file_management.GetFilePath(tool_settings[2])
        event_manager.publish("request_show_tool", file_path)
                       
    def DeleteTool(self, item):
        answer = WarningMessageRe(var.LANGUAGE_DATA.get("message_sure_delete_tool"))
    
        if answer == False:
            return
        
        # Get the right path for the platform
        file_path_1 = self.file_management.GetFilePath(var.TOOLS3D[item][1])
        file_path_2 = self.file_management.GetFilePath(var.TOOLS3D[item][2])

        file_path_1 = Path(file_path_1)
        file_path_2 = Path(file_path_2)

        # Delete the stl files
        file_path_1.unlink()
        file_path_2.unlink()
        
        var.TOOLS3D[item] = []
        
        Robot_stl_old = var.TOOLS3D
        var.TOOLS3D = []
        for i in range(len(Robot_stl_old)):
            if Robot_stl_old[i] != []:
                var.TOOLS3D.append(Robot_stl_old[i])
                
        event_manager.publish("request_delete_buttons_tool")
        event_manager.publish("request_delete_tool_combo")
        event_manager.publish("request_set_tool", var.TOOLS3D)
        
        for i in range(len(var.TOOLS3D)):
            #event_manager.publish("request_delete_spacer_tool")
            event_manager.publish("request_new_buttons", i, var.TOOLS3D)
            event_manager.publish("request_add_tool_combo", var.TOOLS3D[i][0]) 
            
        event_manager.publish("request_add_tool_combo", "No tool")
        event_manager.publish("request_save_robot_tool")         
                
    def UpdateSettings(self): 
        if self.selected_tool == None:
            return
        
        data_tool = var.TOOLS3D[self.selected_tool]     
        data = event_manager.publish("request_get_tool_data", data_tool)
        
        var.TOOLS3D[self.selected_tool] = data[0]
        var.TOOL_FRAME = var.TOOLS3D[self.selected_tool][5]
        
        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(var.TOOLS3D[self.selected_tool][1])      
                    
        your_mesh = mesh.Mesh.from_file(file_path)

        rx = np.radians(var.TOOLS3D[self.selected_tool][4][3])
        ry = np.radians(var.TOOLS3D[self.selected_tool][4][4])
        rz = np.radians(var.TOOLS3D[self.selected_tool][4][5])

        # Define rotation matrices around X, Y, Z axes
        rotation_x = np.array([[1, 0, 0],
                            [0, np.cos(rx), -np.sin(rx)],
                            [0, np.sin(rx), np.cos(rx)]])

        rotation_y = np.array([[np.cos(ry), 0, np.sin(ry)],
                            [0, 1, 0],
                            [-np.sin(ry), 0, np.cos(ry)]])

        rotation_z = np.array([[np.cos(rz), -np.sin(rz), 0],
                            [np.sin(rz), np.cos(rz), 0],
                            [0, 0, 1]])

        # Combine rotation matrices
        rotation_matrix = rotation_x.dot(rotation_y).dot(rotation_z)

        # Apply the rotation to all vertices of the STL file
        for i, _ in enumerate(your_mesh.vectors):
            # Rotate each vertex
            your_mesh.vectors[i] = np.dot(rotation_matrix, your_mesh.vectors[i].T).T


        # For example, find the minimum and maximum coordinates of the vertices along each axis
        min_x, max_x = np.min(your_mesh.vectors[:, :, 0]), np.max(your_mesh.vectors[:, :, 0])
        min_y, max_y = np.min(your_mesh.vectors[:, :, 1]), np.max(your_mesh.vectors[:, :, 1])
        min_z, max_z = np.min(your_mesh.vectors[:, :, 2]), np.max(your_mesh.vectors[:, :, 2])

        # Compute the translations required to move each axis to the desired positions
        # For example, if you want the X, Y, Z axes to be at x_desired, y_desired, z_desired respectively
        x_desired = var.TOOLS3D[self.selected_tool][4][0]
        y_desired = var.TOOLS3D[self.selected_tool][4][1]
        z_desired = var.TOOLS3D[self.selected_tool][4][2]
        
        translation_x = x_desired - min_x
        translation_y = y_desired - min_y
        translation_z = z_desired - min_z

        # Apply the translations to all vertices of the STL file
        your_mesh.vectors[:, :, 0] += translation_x
        your_mesh.vectors[:, :, 1] += translation_y
        your_mesh.vectors[:, :, 2] += translation_z

        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(var.TOOLS3D[self.selected_tool][2])   

        your_mesh.save(file_path)  
        
        event_manager.publish("request_clear_plotter_tool")
        event_manager.publish("request_show_tool", file_path)