from PyQt5.QtWidgets import QMessageBox, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

import backend.core.variables as var

import numpy as np
import os
from stl import mesh
from pathlib import Path

from backend.file_managment.file_management import FileManagement

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import WarningMessageRe


class ToolManagment:
    def __init__(self):
        super().__init__()

        self.file_management = FileManagement()     
        self.selected_tool = None

        self.settings_tools = []

    def SetSettings(self, settings):
        self.settings_tools = settings
        self.selected_tool = None


        event_manager.publish("request_delete_buttons_tool")
        event_manager.publish("request_clear_plotter_tool")
        event_manager.publish("request_clear_settings")  
              

        for setting in settings:
            event_manager.publish("request_create_buttons_tool", setting)  


    def ChangeColor(self, item, color):
        self.settings_tools[item][3] = color

    def AddNewTool(self, robot, robot_name):
        # Select a new file with Qfiledialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        # if there is a file
        if not file_dialog.exec_():
            return
        
        file_path_tool = file_dialog.selectedFiles()[0]
        
        i = len(self.settings_tools)
        self.settings_tools.append([[],[],[],[],[],[],[],[],[],[],[],[]])
        
        # Get the name of the file
        filename = os.path.basename(file_path_tool)
        name, _ = os.path.splitext(filename)
        

        # get the name of the robot
        folder_name = robot_name       

        # Save the modified mesh to a new STL file             
        self.settings_tools[i][0] = name
        self.settings_tools[i][1] = (f"/Robot_library/{folder_name}/TOOLS_STL/ORIGINAL_{name}.STL")
        self.settings_tools[i][2] = (f"/Robot_library/{folder_name}/TOOLS_STL/{name}.STL")
        self.settings_tools[i][3] = "red"
        self.settings_tools[i][4] = [0,0,0,0,0,0] # Position origin
        self.settings_tools[i][5] = [0,0,0,0,0,0] # Tool frame
        self.settings_tools[i][6] = "Tool pin 1" # Tool pin number
        self.settings_tools[i][7] = "None" # Type of tool pin (Servo or relay)
        self.settings_tools[i][8] = ["min","max"] # min and max value
        self.settings_tools[i][9] = [0,0,0] # Offset XYZ tool
        self.settings_tools[i][10] = 0 # Turn camera 180 degrees
        self.settings_tools[i][11] = [0,0,0,0,0] 

        # Get the name of the folder of the current robot
        file_path_1 = self.file_management.GetFilePath(self.settings_tools[i][1])
        file_path_2 = self.file_management.GetFilePath(self.settings_tools[i][2])
        
        item = mesh.Mesh.from_file(file_path_tool)
        item.save(file_path_1)
        item.save(file_path_2)
        
        
        event_manager.publish("request_new_buttons", self.settings_tools[i])

                             
    def ShowSettings(self, tool):
        self.selected_tool = tool
        tool_settings = self.settings_tools[self.selected_tool]
        
        event_manager.publish("request_show_tool_settings", tool_settings)
        event_manager.publish("request_clear_plotter_tool")
        
        file_path = self.file_management.GetFilePath(tool_settings[2])
        event_manager.publish("request_show_tool", file_path)
                       
    def DeleteTool(self, item):
        answer = WarningMessageRe(var.LANGUAGE_DATA.get("message_sure_delete_tool"))
    
        if answer == False:
            return
        
        # Get the right path for the platform
        file_path_1 = self.file_management.GetFilePath(self.settings_tools[item][1])
        file_path_2 = self.file_management.GetFilePath(self.settings_tools[item][2])

        file_path_1 = Path(file_path_1)
        file_path_2 = Path(file_path_2)

        # Delete the stl files
        file_path_1.unlink()
        file_path_2.unlink()
        
        self.settings_tools[item] = []
        
        Robot_stl_old = self.settings_tools
        self.settings_tools = []
        for i in range(len(Robot_stl_old)):
            if Robot_stl_old[i] != []:
                self.settings_tools.append(Robot_stl_old[i])
                
        event_manager.publish("request_delete_buttons_tool")
        
        for setting in self.settings_tools:
            event_manager.publish("request_new_buttons", setting)
            
    
                
    def UpdateSettings(self): 
        if self.selected_tool == None:
            return
        
        data_tool = self.settings_tools[self.selected_tool]     
        data = event_manager.publish("request_get_tool_data", data_tool)[0]
        
        self.settings_tools[self.selected_tool] = data
        var.TOOL_FRAME = self.settings_tools[self.selected_tool][5]
        
        file_path = self.file_management.GetFilePath(self.settings_tools[self.selected_tool][1])      
                    
        your_mesh = mesh.Mesh.from_file(file_path)

        rx = np.radians(self.settings_tools[self.selected_tool][4][3])
        ry = np.radians(self.settings_tools[self.selected_tool][4][4])
        rz = np.radians(self.settings_tools[self.selected_tool][4][5])

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
        x_desired = self.settings_tools[self.selected_tool][4][0]
        y_desired = self.settings_tools[self.selected_tool][4][1]
        z_desired = self.settings_tools[self.selected_tool][4][2]
        
        translation_x = x_desired - min_x
        translation_y = y_desired - min_y
        translation_z = z_desired - min_z

        # Apply the translations to all vertices of the STL file
        your_mesh.vectors[:, :, 0] += translation_x
        your_mesh.vectors[:, :, 1] += translation_y
        your_mesh.vectors[:, :, 2] += translation_z

        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(self.settings_tools[self.selected_tool][2])   

        your_mesh.save(file_path)  
        
        event_manager.publish("request_clear_plotter_tool")
        event_manager.publish("request_show_tool", file_path)