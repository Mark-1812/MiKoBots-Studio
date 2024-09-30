from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import  QFileDialog

import numpy as np
from stl import mesh

from backend.core.event_manager import event_manager
from backend.calculations.convert_matrix import XYZToMatrix
from backend.file_managment.file_management import FileManagement

import tkinter.messagebox
import json
import os

class SimulationObjectWindow(QObject):
    def __init__(self):
        self.file_management = FileManagement()
        self.pos_onject_nt = None
        self.origin_object_nr = None
        self.Objects_stl1 = []
        self.Objects_stl2 = []
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_open_doc_objects", self.OpenFile)
        event_manager.subscribe("request_close_doc_objects", self.CloseFile)
        event_manager.subscribe("request_get_objects_plotter", self.GetObjectsPlotter)
        
      
    def AddNewObjectModel(self):
        # Select a new file with Qfiledialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
        #file_dialog.setDirectory(str(var.FILE_PATH))
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        # if there is a file
        if not file_dialog.exec_():
            return
        
        file_path = file_dialog.selectedFiles()[0]
        
        i = len(self.Objects_stl1)
        self.Objects_stl1.append([[],[],[],[],[]])
        
        # Get the name of the file
        name = os.path.basename(file_path)
                        
        # Save the modified mesh to a new STL file             
        self.Objects_stl1[i][0] = name
        self.Objects_stl1[i][1] = (f"/Simulation_library/ORIGINAL_" + name)
        self.Objects_stl1[i][2] = (f"/Simulation_library/" + name)
        self.Objects_stl1[i][3] = "red"
        self.Objects_stl1[i][4] = [0,0,0,0,0,0] # Position origin
        
        # Get the right path for the platform
        file_path_1 = self.file_management.GetFilePath(self.Objects_stl1[i][1])
        file_path_2 = self.file_management.GetFilePath(self.Objects_stl1[i][2]) 
        
        item = mesh.Mesh.from_file(file_path)
        item.save(file_path_1)
        item.save(file_path_2)
        
        name = self.Objects_stl1[i][0]
        event_manager.publish("request_create_buttons_1_object", i, name)
        self.ShowOriginObject(i)

    def OpenObjectModels(self):
        # Get the right path for the platform
        file_path = self.file_management.GetFilePath("/Simulation_library/settings.json")

        try:
            with open(file_path, 'r') as file:
                self.Objects_stl1 = json.load(file)
                for i in range(len(self.Objects_stl1)):
                    name = self.Objects_stl1[i][0]
                    event_manager.publish("request_create_buttons_1_object", i, name)
        except:
            print("error occured file not found")        
    
    def ShowOriginObject(self, item):
        self.origin_object_nr = item
        
        event_manager.publish("request_clear_plotter_object")
        
        origin = self.Objects_stl1[item][4]
        event_manager.publish("request_set_data_origin_object", origin)

        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(self.Objects_stl1[item][2])

        event_manager.publish("request_object_plotter_preview", file_path)
        
    def ChangeOriginObject(self):     
        if self.origin_object_nr == None:
            return
        
        data = event_manager.publish("request_get_data_origin_object")

        self.Objects_stl1[self.origin_object_nr][4] = data[0]

        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(self.Objects_stl1[self.origin_object_nr][1])

        your_mesh = mesh.Mesh.from_file(file_path)

        rx = np.radians(self.Objects_stl1[self.origin_object_nr][4][3])
        ry = np.radians(self.Objects_stl1[self.origin_object_nr][4][4])
        rz = np.radians(self.Objects_stl1[self.origin_object_nr][4][5])

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
        x_desired = self.Objects_stl1[self.origin_object_nr][4][0]
        y_desired = self.Objects_stl1[self.origin_object_nr][4][1]
        z_desired = self.Objects_stl1[self.origin_object_nr][4][2]
        
        translation_x = x_desired - min_x
        translation_y = y_desired - min_y
        translation_z = z_desired - min_z

        # Apply the translations to all vertices of the STL file
        your_mesh.vectors[:, :, 0] += translation_x
        your_mesh.vectors[:, :, 1] += translation_y
        your_mesh.vectors[:, :, 2] += translation_z
        
        # Get the right path for the platform
        file_path = self.file_management.GetFilePath(self.Objects_stl1[self.origin_object_nr][2])

        your_mesh.save(file_path)
        
        event_manager.publish("request_clear_plotter_object")
        event_manager.publish("request_object_plotter_preview", file_path)
    
    def DeleteSTLObject1(self, item):  
        if not tkinter.messagebox.askokcancel("Delete", "Are you sure you want to delete this file? This action is permanent, and the model will no longer be available in any other files."):
            return
        
        if item == self.origin_object_nr:
            event_manager.publish("request_clear_plotter_object")
        
        # Get the right path for the platform
        file_path_1 = self.file_management.GetFilePath(self.Objects_stl1[item][1])
        file_path_2 = self.file_management.GetFilePath(self.Objects_stl1[item][2])
            
        # Delete the stl files
        file_path_1.unlink()
        file_path_2.unlink()
        
        # delte the item out of the list and make a new list
        self.Objects_stl1[item] = []
        
        Objects_stl1_old = self.Objects_stl1
        self.Objects_stl1 = []
        for i in range(len(Objects_stl1_old)):
            if Objects_stl1_old[i] != []:
                self.Objects_stl1.append(Objects_stl1_old[i])
        
        # delete all the buttons and replace them with new buttons
        event_manager.publish("request_delete_buttons_1_object")
    
        for i in range(len(self.Objects_stl1)):
            name = self.Objects_stl1[i][0]
            event_manager.publish("request_create_buttons_1_object", i, name)
        

    # Change the position of the object in the plotter
    def ShowPosObject(self, item):
        self.pos_object_nr = item
        
        origin = self.Objects_stl2[item][3]
        event_manager.publish("request_set_data_pos_object", origin)

    def ChangePosObject(self): 
        item = self.pos_object_nr
        
        data = event_manager.publish("request_get_data_pos_object")

        self.Objects_stl2[self.pos_object_nr][3] = data[0]
        
        combined_matrix = XYZToMatrix(self.Objects_stl2[item][3])
        event_manager.publish("request_change_pos_item", item, combined_matrix)

    # functions for when a document is opened or closed
    def OpenFile(self, objects):
        self.Objects_stl2 = objects
        
        for i in range(len(self.Objects_stl2)):
            try:
                self.AddNewObjectModel(i)
                self.ShowPosObject(i)
                self.ChangePosObject()
                
            except:
                tkinter.messagebox.showerror("error", f"could not find this item: {self.Objects_stl2[i][0]}")
                self.Objects_stl2[i] = []   
                
        Objects_stl2_old = self.Objects_stl2
        self.Objects_stl2 = []
        for j in range(len(Objects_stl2_old)):
            if Objects_stl2_old[j] != []:
                self.Objects_stl2.append(Objects_stl2_old[j])       

    def CloseFile(self):       
        for i in range(len(self.Objects_stl2)):
            self.DeleteObjectPlotter(i)
                
        self.Objects_stl2 = []

    def GetObjectsPlotter(self):
        return self.Objects_stl2

    # add or delete object in plotter    
    def ChangeColorObject(self, color, color_code, item):
        self.Objects_stl2[item][2] = color
        event_manager.publish("request_change_color_item", color_code, item)
  
    def AddObjectToPlotter(self, item):
        name = self.Objects_stl1[item][0]
        file_path = self.Objects_stl1[item][2]
        
        # MAKE A new list with the components in the plotter
        i = len(self.Objects_stl2)
        
        self.Objects_stl2.append([[],[],[],[]])
        self.Objects_stl2[i][0] = name
        self.Objects_stl2[i][1] = file_path
        self.Objects_stl2[i][2] = "red"
        self.Objects_stl2[i][3] = [0,0,0,0,0,0]
        
        # Add stl to plotter
        file_path = self.file_management.GetFilePath(self.Objects_stl2[i][1])
        
        data = [file_path, self.Objects_stl2[i][2], np.eye(4), np.eye(4)]
        
        event_manager.publish("request_add_item_to_plotter", data)
        
        # Make buttons
        name = self.Objects_stl2[i][0]
        event_manager.publish("request_create_buttons_2_object", i, name)

    def DeleteObjectPlotter(self, item):
        # delte the item out of the list and make a new list
        self.Objects_stl2[item] = []

        # Delete all the items out of the plotter
        event_manager.publish("request_delete_item_plotter")
         
        # make a new list delete the empty 
        Objects_stl2_old = self.Objects_stl2
        self.Objects_stl2 = []
        for i in range(len(Objects_stl2_old)):
            if Objects_stl2_old[i] != []:
                self.Objects_stl2.append(Objects_stl2_old[i])  
      

        event_manager.publish("request_delete_buttons_2_object")
         
        # Make new items
        for i in range(len(self.Objects_stl2)):
            name = self.Objects_stl2[i][0]
            event_manager.publish("request_create_buttons_2_object", i, name)
            
            # Add stl to plotter
            file_path = self.file_management.GetFilePath(self.Objects_stl2[i][1])
                
            data = [file_path, self.Objects_stl2[i][2], np.eye(4), np.eye(4)]
            event_manager.publish("request_add_item_to_plotter", data)
            
            self.pos_object_nr = i
            self.ChangePosObject()


 







            