

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt, QPoint
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout, QMenu, QAction, QVBoxLayout, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QCursor, QIcon

from functools import partial

from gui.style import *

import numpy as np


import vtk




class ObjectSim():
    def __init__(self):
        self.plotter_items = []

        self.renderer = None
    
    def SetupRenderer(self, renderer):
        self.renderer = renderer
    
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
        
    def DeleteItemPlotter(self):
        for i in range(len(self.plotter_items)):
            self.renderer.RemoveActor(self.plotter_items[i][0])
        
        self.plotter_items = []

    def ChangePosItems(self, item, matrix):
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


