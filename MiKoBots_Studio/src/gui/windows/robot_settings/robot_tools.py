from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

from backend.core.event_manager import event_manager

import backend.core.variables as var

from backend.robot_management  import add_new_tool
from backend.robot_management  import delete_tool
from backend.robot_management  import show_tool_settings
from backend.robot_management  import update_tool_settings
from backend.robot_management  import save_robot

from backend.simulation.axis import Axis
from backend.simulation.planes import Planes

from gui.style import *

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

class RobotTools(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
                
        self.Tools_robot_buttons = []
        self.stl_actor = None
        
        self.spacer_widget = None
        self.plotter = None
        self.renderer = None
  
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_create_buttons_tool", self.CreateButtons)
        event_manager.subscribe("request_new_buttons", self.CreateButtons)
        event_manager.subscribe("request_delete_buttons_tool", self.DeleteButtons)
        event_manager.subscribe("request_show_tool_settings", self.ShowSettings)
        event_manager.subscribe("request_get_tool_data", self.GetToolData)
        event_manager.subscribe("request_show_tool", self.ShowModel)
        event_manager.subscribe("request_clear_plotter_tool", self.ClearPlotter) 
        event_manager.subscribe("request_close_plotter_tool", self.ClosePlotter)     
        event_manager.subscribe("request_save_robot_tool", self.SaveRobot)
    
    def GUI(self):
        self.main_layout = QGridLayout(self.frame)
        self.main_layout.setContentsMargins(3, 3, 3, 3)

        # Frame with the stl files
        title = QLabel("Tools:")
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        self.main_layout.addWidget(title,0,0)
        
        
        # create an area where the parts will be placed
        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(330)
        scroll.setFixedHeight(300)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout = QGridLayout(scroll_widget)
        
        scroll.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll,1,0)    
        
        # create layout plotter
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        frame_plotter.setFixedWidth(330)
        self.main_layout.addWidget(frame_plotter, 2, 0)
        frame_plotter.setLayout(self.layout_plotter)

        # frame with change origin
        layout_options = QGridLayout()
        frame_options = QFrame()
        frame_options.setMaximumWidth(250)
        self.main_layout.addWidget(frame_options,0,1,3,1)
        frame_options.setLayout(layout_options)
        
        
        # put everything on the left side of the screen
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        self.main_layout.addWidget(spacer_widget, 3, 0)
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        self.main_layout.addWidget(spacer_widget, 0, 2)
        
        title = QLabel("Tool settings")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(250,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,0,0,1,4)
        
        title = QLabel("Change origin:")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,0,1,2)
        
        title = QLabel("Tool frame:")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,2,1,2)
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        self.entry_origin_pos = []
        self.ToolFrame = []
        
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.entry_origin_pos.append(entry)

            row = idx + 2
            col = 0

            layout_options.addWidget(label, row, col)
            layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
                       
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)
            
            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)
            entry.setValidator(validator)
            self.ToolFrame.append(entry)
            
            layout_options.addWidget(label, row, col + 2)
            layout_options.addWidget(entry, row, col + 3)  # Put entry in the next column
            
        # Pin settings tool
        row = layout_options.rowCount()
            
        title = QLabel("Pin settings tool:")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title, row, 0, 1, 4)    
            
        tools = ["Tool pin 1", "Tool pin 2", "Tool pin 3", "Tool pin 4", "Tool pin 5"]
        self.combobox_tool_pin = QComboBox() 
        self.combobox_tool_pin.setStyleSheet(style_combo)
        layout_options.addWidget(self.combobox_tool_pin, row + 1, 0, 1, 4)
        self.combobox_tool_pin.addItems(tools)

        ## define the type of tool, what is connected to the pin
        # no connection
        self.radio_button_no_con = QRadioButton()
        self.radio_button_no_con.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_no_con.setStyleSheet(style_radiobutton)
        layout_options.addWidget(self.radio_button_no_con,  row + 2,0)
        
        label = QLabel("No connection")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 2,1,1,3)
        
        # Relay
        self.radio_button_relay = QRadioButton()
        self.radio_button_relay.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_relay.setStyleSheet(style_radiobutton)
        layout_options.addWidget(self.radio_button_relay,  row + 3,0)
        
        label = QLabel("ON/OFF relay")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 3,1,1,3)
        
        # Servo
        self.radio_button_servo = QRadioButton()
        self.radio_button_servo.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_servo.setStyleSheet(style_radiobutton)
        layout_options.addWidget(self.radio_button_servo, row + 4,0)

        self.entry_servo_min = QLineEdit()
        self.entry_servo_min.setStyleSheet(style_entry)
        self.entry_servo_min.setPlaceholderText("Min")
        self.entry_servo_min.setFixedWidth(50)
        self.entry_servo_min.setValidator(validator)
        layout_options.addWidget(self.entry_servo_min, row + 4, 1)
        
        self.entry_servo_max = QLineEdit()
        self.entry_servo_max.setStyleSheet(style_entry)
        self.entry_servo_max.setPlaceholderText("Max")
        self.entry_servo_max.setFixedWidth(50)
        self.entry_servo_max.setValidator(validator)
        layout_options.addWidget(self.entry_servo_max, row + 4, 2)

        label = QLabel("Servo")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 4, 3)        
                       
        ## camera offset
        row = layout_options.rowCount()
        
        title = QLabel("Camera settings:")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(250,25)
        layout_options.addWidget(title, row, 0, 1, 4)
        
        label = QLabel("XYZ:")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 1, 0)
        
        self.cam_offset = []
        for i in range(3):
            entry_cam = QLineEdit()
            entry_cam.setStyleSheet(style_entry)
            entry_cam.setFixedWidth(50)
            entry_cam.setValidator(validator)
            layout_options.addWidget(entry_cam, row + 1, i + 1)
            
            self.cam_offset.append(entry_cam)
        
        # rotational compensation       
        label = QLabel("Rotation offset")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 2, 0 , 1, 3)
        
        self.camere_rotation_offset = QLineEdit()
        self.camere_rotation_offset.setText("0")
        self.camere_rotation_offset.setStyleSheet(style_entry)
        self.camere_rotation_offset.setFixedWidth(50)
        self.camere_rotation_offset.setValidator(validator)
        layout_options.addWidget(self.camere_rotation_offset, row + 2, 3)
        
     
        
        label = QLabel("small square")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 3, 0 , 1, 2)
        
        self.size_small_square = QLineEdit()
        self.size_small_square.setText("120")
        self.size_small_square.setStyleSheet(style_entry)
        self.size_small_square.setFixedWidth(50)
        self.size_small_square.setValidator(validator)
        layout_options.addWidget(self.size_small_square, row + 3, 2)
        
        self.z_dis_small_square = QLineEdit()
        self.z_dis_small_square.setPlaceholderText("Max")
        self.z_dis_small_square.setStyleSheet(style_entry)
        self.z_dis_small_square.setFixedWidth(50)
        self.z_dis_small_square.setValidator(validator)
        layout_options.addWidget(self.z_dis_small_square, row + 3, 3)

        label = QLabel("big square")
        label.setStyleSheet(style_label)
        layout_options.addWidget(label, row + 4, 0 , 1, 2)
        
        self.size_big_square = QLineEdit()
        self.size_big_square.setText("160")
        self.size_big_square.setStyleSheet(style_entry)
        self.size_big_square.setFixedWidth(50)
        self.size_big_square.setValidator(validator)
        layout_options.addWidget(self.size_big_square, row + 4, 2)
        
        self.z_dis_big_square = QLineEdit()
        self.z_dis_big_square.setPlaceholderText("Max")
        self.z_dis_big_square.setStyleSheet(style_entry)
        self.z_dis_big_square.setFixedWidth(50)
        self.z_dis_big_square.setValidator(validator)
        layout_options.addWidget(self.z_dis_big_square, row + 4, 3)
        
        # Camera turn 180 degrees        
        checkbox_cal_square = QCheckBox('Show calibration square')
        checkbox_cal_square.setStyleSheet(style_checkbox)
        layout_options.addWidget(checkbox_cal_square, row + 5, 0, 1, 4) 
        checkbox_cal_square.stateChanged.connect(self.show_square)
        
        
        row = layout_options.rowCount()
        
                       
        self.button_update = QPushButton("Update 3D model")
        self.button_update.setStyleSheet(style_button)
        layout_options.addWidget(self.button_update, row, 0, 1, 4)
        self.button_update.clicked.connect(lambda: update_tool_settings())
        
        self.button_add_new = QPushButton("Add new tool")
        self.button_add_new.setStyleSheet(style_button)
        layout_options.addWidget(self.button_add_new, row + 1, 0, 1, 4)
        self.button_add_new.clicked.connect(lambda: add_new_tool())    
        
        self.button_save_robot = QPushButton("Save robot")
        self.button_save_robot.setStyleSheet(style_button)
        layout_options.addWidget(self.button_save_robot, row + 2, 0, 1, 4)
        self.button_save_robot.clicked.connect(lambda: save_robot(True))      
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout_options.addWidget(spacer_widget, layout_options.rowCount(), 4)


    def show_square(self, state):
        if state == 2:  # Checked (Qt.Checked)
            var.CAM_SQUARE = True
        else:  # Unchecked (Qt.Unchecked)
            var.CAM_SQUARE = False

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
            self.renderer = vtk.vtkRenderer()
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.plotter.GetRenderWindow().AddRenderer(self.renderer)
            
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
            
            Axis(self.renderer)
            Planes(self.renderer)
            
            self.layout_plotter.addWidget(self.plotter,0,0)
            
            self.camera = vtk.vtkCamera()
            self.SetCameraPlotter()

    def SaveRobot(self):
        save_robot(False)

    def CreateButtons(self, item, tool_data):
        if self.spacer_widget:
            self.spacer_widget.deleteLater()  
            self.spacer_widget.setParent(None)
            self.spacer_widget = None
            
        self.Tools_robot_buttons.append([[],[],[],[]])
            
        label = QLabel(tool_data[item][0])
        self.layout.addWidget(label, item, 0)
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        self.Tools_robot_buttons[item][0] = label
        
        button = QPushButton("X")
        self.layout.addWidget(button, item, 1)
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_tool(idx))
        self.Tools_robot_buttons[item][1] = button
        
        button = QPushButton("Settings")
        self.layout.addWidget(button, item, 2)
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_tool_settings(idx))
        self.Tools_robot_buttons[item][2] = button
        
        def on_combobox_change(nr):
            tool_data[nr][3] = combo.currentText()
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        for i in range(len(colors)):
            if colors[i] == tool_data[item][3]:
                combo_nr = i
        
        combo = QComboBox()
        self.layout.addWidget(combo, item, 3)
        combo.setStyleSheet(style_combo)
        combo.addItems(colors)
        combo.setCurrentIndex(combo_nr)
        combo.currentIndexChanged.connect(lambda index, idx = item: on_combobox_change(idx))
        self.Tools_robot_buttons[item][3] = combo
            
        self.spacer_widget = QWidget()
        self.spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def DeleteButtons(self):
        for i in range(len(self.Tools_robot_buttons)):
            for j in range(4):
                self.Tools_robot_buttons[i][j].setParent(None)
                self.Tools_robot_buttons[i][j].deleteLater()

        self.Tools_robot_buttons = []
        
        if self.spacer_widget:
            self.spacer_widget.deleteLater()  
            self.spacer_widget.setParent(None)
            self.spacer_widget = None

    def ShowSettings(self, tool_settings): 
        if self.stl_actor == None:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window
        
        # Set the settings
        for i in range(6):
            self.entry_origin_pos[i].setText(str(tool_settings[4][i]))
            self.ToolFrame[i].setText(str(tool_settings[5][i]))
        
        # Set the combo box
        self.combobox_tool_pin.setCurrentText(tool_settings[6]) 
              
        if tool_settings[7] == "Servo":
            self.radio_button_servo.setChecked(True)
            self.radio_button_relay.setChecked(False)
        elif tool_settings[7] == "Relay":
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(True)
        else:
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(False)
            
        value = tool_settings[8]
        self.entry_servo_min.setText(str(value[0]))
        self.entry_servo_max.setText(str(value[1]))
        
        offset = tool_settings[9]
        for i in range(3):
            self.cam_offset[i].setText(str(offset[i]))
            
        self.camere_rotation_offset.setText(str(tool_settings[10]))
            
        cam_settings = tool_settings[11]
        self.z_dis_big_square.setText(str(cam_settings[0]))
        self.z_dis_small_square.setText(str(cam_settings[1]))
        self.size_big_square.setText(str(cam_settings[2]))
        self.size_small_square.setText(str(cam_settings[3]))
        
    def ClearPlotter(self):
        if self.stl_actor and self.plotter:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window

    def ClosePlotter(self):
        if self.plotter:
            self.plotter.close()
            self.plotter = None
            self.renderer = None

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
        
        self.renderer.AddActor(self.stl_actor)        
   
    def GetToolData(self, data_tool):
        if self.stl_actor == None:
            return
        
        for i in range(6):
            try:
                data_tool[4][i] = float(self.entry_origin_pos[i].text())
            except:
                data_tool[4][i] = 0
                self.entry_origin_pos[i].setText("0.0")
            
            try:
                data_tool[5][i] = float(self.ToolFrame[i].text())
            except:
                data_tool[5][i] = 0
                self.ToolFrame[i].setText("0.0")       
        
        data_tool[6] = self.combobox_tool_pin.currentText() 
           
           
        if self.radio_button_relay.isChecked():
            data_tool[7] = "Relay"
        elif self.radio_button_servo.isChecked():
            data_tool[7] = "Servo"
            value = ["0","0"]
            try:
                value[0] = float(self.entry_servo_min.text())
            except:
                value[0] = 0.0
                self.entry_servo_min.setText("0.0")
            
            try:
                value[1] = float(self.entry_servo_max.text())
            except:
                value[1] = 0.0
                self.entry_servo_max.setText("0.0")
                
            data_tool[8] = value
        elif self.radio_button_no_con.isChecked():
            data_tool[7] = "None"
        
        offset = []
        for i in range(3):
            try:
                value = float(self.cam_offset.text())
                offset.append(value)
            except:
                offset.append(0.0)
            
        data_tool[9] = offset
        
        data_tool[10] = self.camere_rotation_offset.text()
            
            
        cam_settings = ["0", "0", "0", "0"]
        cam_settings[0] = self.z_dis_big_square.text()
        cam_settings[1] = self.z_dis_small_square.text()
        cam_settings[2] = self.size_big_square.text()
        cam_settings[3] = self.size_small_square.text()  
        
        data_tool[11] = cam_settings
        
        return data_tool

    def SetCameraPlotter(self):
        self.camera.SetPosition(1000, -1000, 1000)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

        self.camera.ParallelProjectionOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
        #self.renderer.Render()
        self.plotter.Render() 
        