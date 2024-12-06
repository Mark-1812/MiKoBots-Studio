from PyQt5.QtCore import QObject
from backend.core.event_manager import event_manager
import vtk

import numpy as np

class SimulationOriginWindow(QObject):
    def __init__(self):
        super().__init__()     
        self.ORIGIN = []
        self.plotter_axis = []
        
        self.renderer = None
        self.plotter = None
        self.interactor = None

    def SetupRenderer(self, renderer, plotter, interactor):
        self.renderer = renderer
        self.plotter = plotter
        self.interactor = interactor
        
    def AddOrigin(self):
        item = len(self.ORIGIN)
        self.ORIGIN.append([[],[],[],[]])
        
        self.ORIGIN[item][0] = "New orign " + str(item)
        self.ORIGIN[item][1] = 0.0
        self.ORIGIN[item][2] = 0.0
        self.ORIGIN[item][3] = 0.0
        
        event_manager.publish("request_delete_space_origin")
        event_manager.publish("request_create_button_origin", item, self.ORIGIN[item])
        self.CreateAxes(item)
        self.ChangePosAxis(item, self.ORIGIN[item])

        self.rendering()

  
    def CreateAxes(self, item):
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

                     
    def SaveOrigin(self, item):      
        data = event_manager.publish("request_get_data_origin", item)
        self.ORIGIN[item] = data[0]
        self.ChangePosAxis(item, self.ORIGIN[item])
        
        origins_new = []
        for i in range(len(self.ORIGIN)):
            if self.ORIGIN[i][0] is not None:
                origins_new.append(self.ORIGIN[i])
        
        self.ORIGIN = origins_new
   
    def DeleteOrigin(self, item):
        # delete out of plotter
        event_manager.publish("request_delete_axis_plotter") 

        # delete the buttons
        event_manager.publish("request_delete_buttons_origin")  
        
        # Make a new list
        self.ORIGIN[item] = []
        origin_old = self.ORIGIN
        self.ORIGIN = []
        
        for i in range(len(origin_old)):
            if origin_old[i] != []:
                self.ORIGIN.append(origin_old[i])
                
        # Create new axis
        # Create new buttons
        for i in range(len(self.ORIGIN)):
            event_manager.publish("request_delete_space_origin")
            event_manager.publish("request_create_button_origin", i, self.ORIGIN[i])
            self.CreateAxes(i)   


    def DeleteAxisPlotter(self):
        for axis in self.plotter_axis:
            for actor in axis[1]:
                if actor:
                    self.renderer.RemoveActor(actor)

        # Clear the list to release memory
        self.plotter_axis.clear()

        self.rendering()

    def rendering(self):
        try:
            self.interactor.Disable()
            self.plotter.Render() 
            self.interactor.Enable()
        except:
            print("Error rendering")

  

# open and close if there is a new file opened or closed

    def GetOriginsPlotter(self):
        return self.ORIGIN
    
    def OpenFile(self, origins):
        self.ORIGIN = origins
        
        for i in range(len(self.ORIGIN)):
            event_manager.publish("request_delete_space_origin")
            event_manager.publish("request_create_button_origin", i, self.ORIGIN[i])
            self.CreateAxes(i) 
            self.ChangePosAxis(i, self.ORIGIN[i])
               
    def CloseFile(self):
        # delete the buttons
        event_manager.publish("request_delete_buttons_origin") 

        # delete out of plotter
        self.DeleteAxisPlotter()

                
        self.ORIGIN = []
