from PyQt5.QtWidgets import  QFileDialog
from PyQt5.QtCore import QObject

from backend.core.event_manager import event_manager
import backend.core.variables as var

from backend.file_managment.file_management import FileManagement

from gui.windows.message_boxes import WarningMessageRe

import os
from pathlib import Path
import json
from stl import mesh
import numpy as np



class Robot3dModel(QObject):
    def __init__(self):
        super().__init__()
        self.file_management = FileManagement()
        self.model_3d_item = None

    def setup(self):
        event_manager.publish("request_delete_buttons_3d_model")
        event_manager.publish("request_clear_plotter_3d_model")
        
        for i in range(len(var.ROBOT3D)):
            event_manager.publish("request_create_buttons_3d_model", i, var.ROBOT3D)  


    def AddNewModel(self, robot, robot_name):
        # Select a new file with Qfiledialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        # if there is a file
        if not file_dialog.exec_():
            return
        
        event_manager.publish("request_clear_plotter_3d_model")
        
        file_path = file_dialog.selectedFiles()[0]
        
        i = len(var.ROBOT3D)
        var.ROBOT3D.append([[],[],[],[],[],[]])
        
        # Get the name of the file
        name = os.path.basename(file_path)
        
        # Get the name of the folder of the current robot
        folder_name = robot_name 

        # Save the modified mesh to a new STL file             
        var.ROBOT3D[i][0] = name
        var.ROBOT3D[i][1] = (f"/Robot_library/{folder_name}/ROBOT_STL/ORIGINAL_{name}")
        var.ROBOT3D[i][2] = (f"/Robot_library/{folder_name}/ROBOT_STL/{name}")
        var.ROBOT3D[i][3] = "red"
        var.ROBOT3D[i][4] = [0,0,0,0,0,0] # Position origin


        # Get the name of the folder of the current robot
        file_path_1 = self.file_management.GetFilePath(var.ROBOT3D[i][1])
        file_path_2 = self.file_management.GetFilePath(var.ROBOT3D[i][2])
        
        item = mesh.Mesh.from_file(file_path)
        item.save(file_path_1)
        item.save(file_path_2)
        
        
        
        event_manager.publish("request_create_buttons_3d_model", i, var.ROBOT3D)
        event_manager.publish("request_show_3d_model", file_path_2)     
        
        event_manager.publish("request_save_robot_tool")
            
    def ChangeOrigin3dModel(self): 
        if self.model_3d_item is None:
            return
                
        data = var.ROBOT3D[self.model_3d_item][4]      
        data = event_manager.publish("request_get_origin_3d_model", data)   
        
        var.ROBOT3D[self.model_3d_item][4] = data[0]     
           
            
        # Get the name of the folder of the current robot
        file_path = self.file_management.GetFilePath(var.ROBOT3D[self.model_3d_item][1])               
        your_mesh = mesh.Mesh.from_file(file_path)

        rx = np.radians(var.ROBOT3D[self.model_3d_item][4][3])
        ry = np.radians(var.ROBOT3D[self.model_3d_item][4][4])
        rz = np.radians(var.ROBOT3D[self.model_3d_item][4][5])

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
        x_desired = var.ROBOT3D[self.model_3d_item][4][0]
        y_desired = var.ROBOT3D[self.model_3d_item][4][1]
        z_desired = var.ROBOT3D[self.model_3d_item][4][2]
        
        translation_x = x_desired - min_x
        translation_y = y_desired - min_y
        translation_z = z_desired - min_z

        # Apply the translations to all vertices of the STL file
        your_mesh.vectors[:, :, 0] += translation_x
        your_mesh.vectors[:, :, 1] += translation_y
        your_mesh.vectors[:, :, 2] += translation_z

        # Get the name of the folder of the current robot
        file_path = self.file_management.GetFilePath(var.ROBOT3D[self.model_3d_item][2])
        
        your_mesh.save(file_path)
        
        event_manager.publish("request_clear_plotter_3d_model")
        event_manager.publish("request_show_3d_model", file_path)

    def DeleteRobotItem(self, item):  
        answer = WarningMessageRe(var.LANGUAGE_DATA.get("Message_delete_for_sure"), var.LANGUAGE_DATA.get("Message_action_damage_robot"))
     
        if answer == False:
            return

        # Get the name of the folder of the current robot
        file_path_1 = self.file_management.GetFilePath(var.ROBOT3D[item][1])
        file_path_2 = self.file_management.GetFilePath(var.ROBOT3D[item][2])
                
        file_path_1 = Path(file_path_1)
        file_path_2 = Path(file_path_2)

        file_path_1.unlink()
        file_path_2.unlink()
        
        var.ROBOT3D[item] = []
        
        Robot_stl_old = var.ROBOT3D
        var.ROBOT3D = []
        for i in range(len(Robot_stl_old)):
            if Robot_stl_old[i] != []:
                var.ROBOT3D.append(Robot_stl_old[i])
        
        event_manager.publish("request_delete_buttons_3d_model")
        
        for i in range(len(var.ROBOT3D)):
            event_manager.publish("request_create_buttons_3d_model", i, var.ROBOT3D)
            
        event_manager.publish("request_save_robot_tool")     
        
        # after delete show the first model
        self.model_3d_item = 0
        self.Show3dModelSettings(self.model_3d_item)   
                       
    def Show3dModelSettings(self, item):
        self.model_3d_item = item
        
        event_manager.publish("request_clear_plotter_3d_model")
        event_manager.publish("request_show_origin_3d_model", var.ROBOT3D[item][4])

        # Get the name of the folder of the current robot
        file_path = self.file_management.GetFilePath(var.ROBOT3D[item][2])
        event_manager.publish("request_show_3d_model", file_path)

  