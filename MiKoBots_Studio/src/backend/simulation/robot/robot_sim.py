import numpy as np
import vtk
from PyQt5.QtCore import QObject

class RobotSimulation:
    def __init__(self):
        super().__init__()     
        self.renderer = None
        self.plotter = None
        self.interactor = None

        self.plotter_robot = []
        self.plotter_tool = [None, None, None, None]


    def SetupRenderer(self, renderer, plotter, interactor):
        self.renderer = renderer
        self.plotter = plotter
        self.interactor = interactor
        
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
        elif data[1] == "blue":
            color = [0,0,1]
        elif data[1] == "black":
            color = [0,0,0]
        elif data[1] == "white":
            color = [1,1,1]
        elif data[1] == "yellow":
            color = [1,1,0]
        elif data[1] == "darkgray":
            color = [0.5,0.5,0.5]

        self.plotter_robot[item][0] = vtk.vtkActor()
        self.plotter_robot[item][0].SetMapper(mapper)
        self.plotter_robot[item][0].GetProperty().SetColor(color)
        self.plotter_robot[item][1] = self.renderer.AddActor(self.plotter_robot[item][0])
        self.plotter_robot[item][2] = data[2]
        self.plotter_robot[item][3] = data[3]  
        self.plotter_robot[item][4] = data[4] 
     
    def DeleteRobotPlotter(self):
        for i in range(len(self.plotter_robot)):
            self.renderer.RemoveActor(self.plotter_robot[i][0])
            
        self.plotter_robot = []
        
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

        self.rendering()
        
    def DeleteToolPlotter(self):
        if self.plotter_tool[0]:
            self.renderer.RemoveActor(self.plotter_tool[0])
            
            self.plotter_tool = [None, None, None, None]

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

    def rendering(self):
        try:
            self.interactor.Disable()
            self.plotter.Render() 
            self.interactor.Enable()
        except:
            print("Error rendering")
