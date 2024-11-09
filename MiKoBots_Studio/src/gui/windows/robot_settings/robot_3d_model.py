from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from backend.core.event_manager import event_manager

from backend.robot_management  import show_3d_model_settings
from backend.robot_management  import delete_robot_model
from backend.robot_management  import change_origin_3d_model
from backend.robot_management  import add_new_3d_model
from backend.robot_management  import save_robot 


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        super().__init__()

    # Override the middle mouse button press event to rotate
    def OnMiddleButtonDown(self):
        self.StartRotate()

    def OnMiddleButtonUp(self):
        self.EndRotate()

    def OnMouseMove(self):
        if self.GetInteractor().GetControlKey():  # If Control is pressed
            return  # Do not rotate if Control is pressed

        self.Rotate()  # Rotate the camera

class Robot3DModel(QWidget): 
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
                
        self.Robot_buttons = []
        
        self.spacer_widget = None
        
        self.stl_actor = None
        self.plotter = None
        self.vtk_renderer = None
        
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_delete_buttons_3d_model", self.DeleteButtons)
        event_manager.subscribe("request_clear_plotter_3d_model", self.ClearPlotter)
        event_manager.subscribe("request_create_buttons_3d_model", self.CreateButtons)
        event_manager.subscribe("request_show_3d_model", self.ShowModel)
        event_manager.subscribe("request_show_origin_3d_model", self.SetOriginfields)
        event_manager.subscribe("request_get_origin_3d_model", self.GetOriginData)
    
    def GUI(self):
        self.main_layout = QGridLayout(self.frame)
        self.main_layout.setContentsMargins(3, 3, 3, 3)

        # Frame with the stl files
        title = QLabel("3D files:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.main_layout.addWidget(title,0,0)
        
        
        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        scroll.setFixedHeight(300)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout = QGridLayout(scroll_widget)
        
        scroll.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll,1,0)      
        
        # create layout plotter
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        frame_plotter.setFixedWidth(400)
        self.main_layout.addWidget(frame_plotter, 2, 0)
        frame_plotter.setLayout(self.layout_plotter)
        
        # frame with change origin
        layout_options = QGridLayout()
        frame_options = QFrame()
        frame_options.setMaximumWidth(250)
        self.main_layout.addWidget(frame_options,0,1,3,1)
        frame_options.setLayout(layout_options)
        
        
        title = QLabel("Change origin:")
        title.setFixedHeight(30)
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,0)
        
        labels = ["X:", "Y:", "Z:", "y:", "p:", "r:"]
        self.origin_pos = []
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            # make sure only int and float numbers are filled in
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            row = idx + 2
            col = 0

            layout_options.addWidget(label, row, col)
            layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        self.button_update = QPushButton("Update")
        self.button_update.setStyleSheet(style_button)
        layout_options.addWidget(self.button_update,8, 0, 1, 2)
        self.button_update.clicked.connect(lambda: change_origin_3d_model())
        
        self.button_add_new = QPushButton("Add new 3D model")
        self.button_add_new.setStyleSheet(style_button)
        layout_options.addWidget(self.button_add_new, 9, 0, 1, 2)
        self.button_add_new.clicked.connect(lambda: add_new_3d_model())  
        
        button = QPushButton("Save robot")
        button.setStyleSheet(style_button)
        layout_options.addWidget(button, 10, 0, 1, 2)
        button.clicked.connect(lambda: save_robot(True))   
        
        widget = QWidget()
        widget.setStyleSheet(style_widget)
        layout_options.addWidget(widget, 11,0,1,2)     
                        
   
    def open_plotter(self):
        if self.plotter is None:
            ## frame with the plotter
            self.plotter = QVTKRenderWindowInteractor(self)
            self.plotter.setFixedHeight(200)
            self.plotter.setFixedWidth(330)
            
            self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
            self.interactor_style = CustomInteractorStyle()
            self.interactor.SetInteractorStyle(self.interactor_style)
            
            
            # Set up a VTK renderer and add it to the interactor
            self.vtk_renderer = vtk.vtkRenderer()
            self.vtk_renderer.SetBackground(1.0, 1.0, 1.0)
            self.plotter.GetRenderWindow().AddRenderer(self.vtk_renderer)
            
            # Optional: Add axes
            axes = vtk.vtkAxesActor()
            axes_widget = vtk.vtkOrientationMarkerWidget()
            axes_widget.SetOrientationMarker(axes)
            axes_widget.SetInteractor(self.plotter)
            axes_widget.SetViewport(0.0, 0.0, 0.2, 0.2)  # Adjust viewport size if needed
            axes_widget.EnabledOn()
            
            # Start the interactor
            self.plotter.Initialize()
            self.plotter.Start()
            
            origin = [0, 0, 0]
            size = 100  # Example size; set as needed
            
            self.CreateAxis()
            
            self.add_vtk_plane(self.vtk_renderer, origin, [0, 0, 1], size, "blue")  # XY plane
            self.add_vtk_plane(self.vtk_renderer, origin, [0, 1, 0], size, "red")   # XZ plane
            self.add_vtk_plane(self.vtk_renderer, origin, [1, 0, 0], size, "green") # ZY plane
            
            self.layout_plotter.addWidget(self.plotter,0,0)
            
            self.camera = vtk.vtkCamera()
            self.SetCameraPlotter()

    def ShowModel(self, path):
        stl_reader = vtk.vtkSTLReader()
        stl_reader.SetFileName(path)
        stl_reader.Update()  # Ensure the STL data is loaded
        
        # Create a mapper for the STL data
        stl_mapper = vtk.vtkPolyDataMapper()
        stl_mapper.SetInputConnection(stl_reader.GetOutputPort())
    
        self.stl_actor = vtk.vtkActor()
        self.stl_actor.SetMapper(stl_mapper)
        self.stl_actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("red"))
        self.stl_actor.GetProperty().EdgeVisibilityOff()  # Equivalent to show_edges=False
        
        self.vtk_renderer.AddActor(self.stl_actor)
        
    def ClearPlotter(self):
       if self.stl_actor and self.vtk_renderer:
            self.vtk_renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window

    def ClosePlotter(self):
        if self.plotter:
            self.plotter.close() 
            self.plotter = None
            self.vtk_renderer = None

    def CreateButtons(self, item, robot_3d_data):
        if self.spacer_widget:
            self.spacer_widget.deleteLater()    
            self.spacer_widget.setParent(None)
            self.spacer_widget = None
            
        self.Robot_buttons.append([[],[],[],[],[]])
            
        label = QLabel(robot_3d_data[item][0])
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        self.layout.addWidget(label, item, 0)
        self.Robot_buttons[item][0] = label
        
        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: delete_robot_model(idx))
        self.layout.addWidget(button, item, 2)
        self.Robot_buttons[item][1] = button
        
        button = QPushButton("Origin")
        button.setFixedSize(75,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: show_3d_model_settings(idx))
        self.layout.addWidget(button, item, 3)
        self.Robot_buttons[item][2] = button
        
        def on_combobox_change(nr):
            robot_3d_data[nr][3] = combo_color.currentText()
            
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        for i in range(len(colors)):
            if colors[i] == robot_3d_data[item][3]:
                combo_nr = i
        
        combo_color = QComboBox()
        combo_color.addItems(colors)
        combo_color.setStyleSheet(style_combo)
        combo_color.setCurrentIndex(combo_nr)
        combo_color.currentIndexChanged.connect(lambda index, idx = item: on_combobox_change(idx))
        self.layout.addWidget(combo_color, item, 4)
        self.Robot_buttons[item][3] = combo_color
        
                        
        def on_linkage_change(nr):
            robot_3d_data[nr][5] = combo.currentText()
        
        linkages = ['Link 1', 'Link 2', 'Link 3', 'Link 4', 'Link 5', 'Link 6', 'Base']
        combo_nr = 0
        for i in range(len(linkages)):
            if linkages[i] == robot_3d_data[item][5]:
                combo_nr = i

        
        combo = QComboBox()
        combo.setStyleSheet(style_combo)
        combo.addItems(linkages)
        combo.setCurrentIndex(combo_nr)
        combo.currentIndexChanged.connect(lambda index, idx = item: on_linkage_change(idx))
        self.layout.addWidget(combo, item, 5)
        self.Robot_buttons[item][4] = combo
        
            
        self.spacer_widget = QWidget()
        self.spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def DeleteButtons(self):
        for i in range(len(self.Robot_buttons)):
            for j in range(len(self.Robot_buttons[i])):
                self.Robot_buttons[i][j].setParent(None)
                self.Robot_buttons[i][j].deleteLater()
                
        self.Robot_buttons = []    
        
        if self.spacer_widget:
            self.spacer_widget.deleteLater()    
            self.spacer_widget.setParent(None)
            self.spacer_widget = None

    def SetOriginfields(self, data):
        for i in range(6):
            self.origin_pos[i].setText(str(data[i]))
            
    def GetOriginData(self, data):
        for i in range(6):
            try:
                data[i] = float(self.origin_pos[i].text())
            except:
                data[i] = 0.0
                self.origin_pos[i].setText("0.0")
                
        return data
            
    def add_vtk_plane(self, renderer, origin, normal, size, color):
        # Create a plane source
        plane_source = vtk.vtkPlaneSource()
        plane_source.SetCenter(origin)

        # Set the normal vector for the plane
        plane_source.SetNormal(normal)

        # Set the size of the plane by defining two points in the plane
        if normal == [0, 0, 1]:  # XY plane
            plane_source.SetOrigin(-size / 2, -size / 2, 0)
            plane_source.SetPoint1(size / 2, -size / 2, 0)
            plane_source.SetPoint2(-size / 2, size / 2, 0)

        elif normal == [0, 1, 0]:  # XZ plane
            plane_source.SetOrigin(-size / 2, 0, -size / 2)
            plane_source.SetPoint1(size / 2, 0, -size / 2)
            plane_source.SetPoint2(-size / 2, 0, size / 2)

        elif normal == [1, 0, 0]:  # ZY plane
            plane_source.SetOrigin(0, -size / 2, -size / 2)
            plane_source.SetPoint1(0, size / 2, -size / 2)
            plane_source.SetPoint2(0, -size / 2, size / 2)

        # Mapper for the plane
        plane_mapper = vtk.vtkPolyDataMapper()
        plane_mapper.SetInputConnection(plane_source.GetOutputPort())

        # Actor for the plane
        plane_actor = vtk.vtkActor()
        plane_actor.SetMapper(plane_mapper)
        plane_actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d(color))
        plane_actor.GetProperty().SetOpacity(0.5)

        # Add the actor to the renderer
        renderer.AddActor(plane_actor)

    def CreateAxis(self):
        def create_arrow_actor(direction, color):
            # Create an arrow source
            arrow_source = vtk.vtkArrowSource()
            
            # Transform to orient the arrow in the desired direction
            transform = vtk.vtkTransform()
            transform.RotateWXYZ(direction[0], direction[1], direction[2], direction[3])
            transform.Scale(200, 50, 50)
            
            # Apply transformation
            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetTransform(transform)
            transform_filter.SetInputConnection(arrow_source.GetOutputPort())
            
            # Mapper
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transform_filter.GetOutputPort())
            
            # Actor
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(color)
            
            return actor

        # Create axis arrows
        self.x_axis_actor = create_arrow_actor([90, 1000, 0, 0], (1, 0, 0))  # Red for X-axis
        self.y_axis_actor = create_arrow_actor([90, 0, 0, 1000], (0, 1, 0))  # Green for Y-axis
        self.z_axis_actor = create_arrow_actor([90, 0, -1000, 0], (0, 0, 1))   # Blue for Z-axis
        
        # Add the axis actors to the scene
        self.vtk_renderer.AddActor(self.x_axis_actor)
        self.vtk_renderer.AddActor(self.y_axis_actor)
        self.vtk_renderer.AddActor(self.z_axis_actor)
    
    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.vtk_renderer.SetActiveCamera(self.camera)
        self.vtk_renderer.ResetCamera()
        #self.renderer.Render()
        self.plotter.Render() 