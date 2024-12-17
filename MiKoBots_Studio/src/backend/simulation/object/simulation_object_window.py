from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import  QFileDialog, QMessageBox

import numpy as np
from stl import mesh

from backend.core.event_manager import event_manager
from backend.calculations.convert_matrix import XYZToMatrix
from backend.file_managment import get_file_path

import vtk

import json
import os
from pathlib import Path

from gui.windows.message_boxes import WarningMessageRe

import backend.core.variables as var

class SimulationObjectWindow:
    def __init__(self):  
        self.pos_onject_nt = None
        self.origin_object_nr = None
        self.Objects_stl1 = []
        self.Objects_stl2 = []
        self.plotter_items = []

        self.renderer = None
        self.plotter = None
        self.interactor = None

    def SetupRenderer(self, renderer, plotter, interactor):
        self.renderer = renderer
        self.plotter = plotter
        self.interactor = interactor
  
    def AddNewObjectModel(self):
        # Select a new file with Qfiledialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('Open File')
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
        file_path_1 = get_file_path(self.Objects_stl1[i][1])
        file_path_2 = get_file_path(self.Objects_stl1[i][2]) 
        
        item = mesh.Mesh.from_file(file_path)
        item.save(file_path_1)
        item.save(file_path_2)
        
        name = self.Objects_stl1[i][0]
        event_manager.publish("request_create_buttons_1_object", i, name)
        self.ShowOriginObject(i)
        
        self.SaveObjectModels()

    ## open and save the settings
    def OpenObjectModels(self):
        # Get the right path for the platform
        file_path = get_file_path("/Simulation_library/settings.json")

        try:
            with open(file_path, 'r') as file:
                self.Objects_stl1 = json.load(file)
                for i in range(len(self.Objects_stl1)):
                    name = self.Objects_stl1[i][0]
                    event_manager.publish("request_create_buttons_1_object", i, name)
        except:
            print(var.LANGUAGE_DATA.get("message_no_3d_model"))        

    def SaveObjectModels(self):
        settings_file = self.Objects_stl1
    
        # Change the name of the folder, if the name of the robot is changed
        file_path = get_file_path("/Simulation_library/settings.json")
        
        try:
            with open(file_path, 'w') as file:
                json.dump(settings_file, file, indent=4)  
        except:
            print(var.LANGUAGE_DATA.get("message_error_saving_settings"))
    
    def ShowOriginObject(self, item):
        self.origin_object_nr = item
        
        event_manager.publish("request_clear_plotter_object")
        
        origin = self.Objects_stl1[item][4]
        event_manager.publish("request_set_data_origin_object", origin)

        # Get the right path for the platform
        file_path = get_file_path(self.Objects_stl1[item][2])

        event_manager.publish("request_object_plotter_preview", file_path)
        
    def ChangeOriginObject(self):     
        if self.origin_object_nr == None:
            return
        
        data = event_manager.publish("request_get_data_origin_object")

        self.Objects_stl1[self.origin_object_nr][4] = data[0]

        # Get the right path for the platform
        file_path = get_file_path(self.Objects_stl1[self.origin_object_nr][1])

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
        file_path = get_file_path(self.Objects_stl1[self.origin_object_nr][2])

        your_mesh.save(file_path)
        
        event_manager.publish("request_clear_plotter_object")
        event_manager.publish("request_object_plotter_preview", file_path)
        
        self.SaveObjectModels()
    
    def DeleteSTLObject1(self, item):  
        answer = WarningMessageRe(var.LANGUAGE_DATA.get("message_sure_delete_model"))

        # Check the response
        if answer == False:
            return  # User chose 'No'
    
        if item == self.origin_object_nr:
            event_manager.publish("request_clear_plotter_object")
            
            
        ## Also delete it out of the main plotter   
        items = []
        for i in range(len(self.Objects_stl2)):
            if self.Objects_stl2[i][0] == self.Objects_stl1[item][0]:
                items.append(i)
                
        items_to_delete = sorted(items, reverse=True)
        
        for i in range(len(items_to_delete)):
            self.DeleteObjectPlotter(items_to_delete[i])

      
        # Get the right path for the platform
        file_path_1 = get_file_path(self.Objects_stl1[item][1])
        file_path_2 = get_file_path(self.Objects_stl1[item][2])

        file_path_1 = Path(file_path_1)
        file_path_2 = Path(file_path_2)
            
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
            
        self.SaveObjectModels()
            


    # Change the position of the object in the simulation
    def ShowPosObject(self, item):
        self.pos_object_nr = item
        
        origin = self.Objects_stl2[item][3]
        event_manager.publish("request_set_data_pos_object", origin)

    def ChangePosObject(self): 
        item = self.pos_object_nr
        
        data = event_manager.publish("request_get_data_pos_object")

        self.Objects_stl2[self.pos_object_nr][3] = data[0]
        
        matrix_data= XYZToMatrix(self.Objects_stl2[item][3])


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
        self.plotter_items[item][2] = np.linalg.inv(matrix_data)

        self.rendering()
  
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

        # Make buttons
        name = self.Objects_stl2[i][0]
        event_manager.publish("request_create_buttons_2_object", i, name)

        # add object to the simulation
        self.AddObjectToSimulation(i)

        self.rendering()

    def AddObjectToSimulation(self, item):
        # add the new robot to the plotter
        self.plotter_items.append([[],[],[],[]])
        item = len(self.plotter_items) - 1

        # Add stl to plotter
        file_path = get_file_path(self.Objects_stl2[item][1])
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_path)
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        color_name = self.Objects_stl2[item][2]

        color = [0,0,0]
        if color_name == "red":
            color = [1,0,0]
        elif color_name == "darkgray":
            color = [0.4, 0.4, 0.4]

        self.plotter_items[item][0] = vtk.vtkActor()
        self.plotter_items[item][0].SetMapper(mapper)
        self.plotter_items[item][0].GetProperty().SetColor(color)
        self.plotter_items[item][1] = self.renderer.AddActor(self.plotter_items[item][0])
        self.plotter_items[item][2] = np.eye(4)
        self.plotter_items[item][3] = np.eye(4)  

    def DeleteObjectPlotter(self, item):
        # delete the item out of the simulation
        for i in range(len(self.plotter_items)):
            self.renderer.RemoveActor(self.plotter_items[i][0])
        
        self.plotter_items = []


        # delete the item out of the list and make a new list
        self.Objects_stl2[item] = []

        # make a new list delete the empty 
        Objects_stl2_old = self.Objects_stl2
        self.Objects_stl2 = []
        for i in range(len(Objects_stl2_old)):
            if Objects_stl2_old[i] != []:
                self.Objects_stl2.append(Objects_stl2_old[i])  

                
        event_manager.publish("request_delete_buttons_2_object")


        for i in range(len(self.Objects_stl2)):
            event_manager.publish("request_create_buttons_2_object", i, self.Objects_stl2[i][0])
            self.AddObjectToSimulation(i)
            self.pos_object_nr = i

            self.ShowPosObject(i)
            self.ChangePosObject()

        self.rendering()

    def ChangeColorObject(self, color_name, color_code, item):
        self.Objects_stl2[item][2] = color_name
        self.plotter_items[item][0].GetProperty().SetColor(color_code)

        self.rendering()

    def rendering(self):
        try:
            self.interactor.Disable()
            self.plotter.Render() 
            self.interactor.Enable()
        except:
            print("Error rendering")        


    # functions for when a document is opened or closed
    def OpenFile(self, objects):
        new_list = objects
        self.Objects_stl2 = []
        
        # see if the objects are in the main object list 1
        # makes a list with all the object that needed to be added to te simulation
        for i in range(len(new_list)):
            for j in range(len(self.Objects_stl1)):
                if new_list[i][0] == self.Objects_stl1[j][0]:
                    self.Objects_stl2.append(new_list[i])
                    
        # Add the items out of the list to the plotter
        for i in range(len(self.Objects_stl2)):
            # add the item to the simulation
            self.AddObjectToSimulation(i)

            # Make buttons
            name = self.Objects_stl2[i][0]
            event_manager.publish("request_create_buttons_2_object", i, name)

            # show the settings of the object so the position can be changeds
            self.ShowPosObject(i)
            self.ChangePosObject()

    def CloseFile(self):    
        # delete the item out of the simulation
        for i in range(len(self.plotter_items)):
            self.renderer.RemoveActor(self.plotter_items[i][0])
        
        self.plotter_items = []
        
        for i in range(len(self.Objects_stl2)):
            event_manager.publish("request_delete_buttons_2_object")
        self.Objects_stl2 = []

    def GetObjectsPlotter(self):
        return self.Objects_stl2







            