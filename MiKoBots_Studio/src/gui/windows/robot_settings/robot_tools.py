from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator, QDesktopServices

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from backend.simulation.simulation_interaction import CustomInteractorStyle
from backend.core.event_manager import event_manager

import backend.core.variables as var

from backend.robot_management.robot_settings  import add_new_tool, delete_tool, show_tool_settings, update_tool_settings, change_color_tool

from backend.vision import show_square_tool

from backend.simulation.axis import Axis
from backend.simulation.planes import Planes
from gui.style import *

URL_HELP_CAM = "https://mikobots.com/mikobots-studio/help/tool/camera-settings/" 
URL_HELP_PIN = "https://mikobots.com/mikobots-studio/help/tool/"
URL_HELP_TOOL_FRAME = "https://mikobots.com/mikobots-studio/help/tool/setup-tool-frame/"
URL_HELP_MODEL = "https://mikobots.com/mikobots-studio/help/tool/setup-3d-model/"

class RobotTools(QFrame):   
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self) 

                
        self.stl_actor = None
        self.frames = []
        
        self.spacer_widget = None
        self.plotter = None
  
        self.CreateToolField()
        self.CreateSettings()
        self.CreatePlotter()

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
        event_manager.subscribe("request_clear_settings", self.ClearSettings)     

    
    def CreatePlotter(self):    
        frame = QWidget()
        frame.setStyleSheet(style_widget)
        self.layout_plotter = QHBoxLayout()
        self.layout_plotter.setContentsMargins(5,0,5,5)
        frame.setLayout(self.layout_plotter)

        self.layout.addWidget(frame,2,0) 

    def OpenPlotter(self):
        ## frame with the plotter
        self.plotter = QVTKRenderWindowInteractor()
        
        self.interactor = self.plotter.GetRenderWindow().GetInteractor()  
        self.interactor_style = CustomInteractorStyle()
        self.interactor.SetInteractorStyle(self.interactor_style)
        
        # Set up a VTK renderer and add it to the interactor
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        self.plotter.GetRenderWindow().AddRenderer(self.renderer)
        
        self.plotter.Initialize()
        self.plotter.Start()

        Axis(self.renderer, 100)
        Planes(self.renderer)
        
        self.layout_plotter.addWidget(self.plotter)
        
        self.camera = vtk.vtkCamera()
        self.SetCameraPlotter()


    def ClosePlotter(self):
        if self.plotter:
            # self.plotter.Finalize()
            self.plotter.close()
            # self.interactor.TerminateApp() 
            # self.renderer.RemoveAllViewProps()

            # self.layout.removeWidget(self.plotter)
            # self.plotter.deleteLater() 

            self.renderer = None
            self.plotter = None
            self.interactor_style = None
            self.interactor = None  


    def CreateToolField(self):
        # Frame with the stl files
        title = QLabel("Tools:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title,0,0)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(300)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(self.scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area,1,0)  

    def CreateSettings(self):
        # frame with change origin
        layout_options = QVBoxLayout()
        layout_options.setContentsMargins(0, 0, 0, 0)
        layout_options.setSpacing(0)
        frame_options = QFrame()
        frame_options.setFixedWidth(280)
          
        
        title = QLabel("Tool settings")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(250,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title)

        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        layout_scroll = QGridLayout(scroll_widget) 
        layout_scroll.setSpacing(0)
        layout_scroll.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(scroll_widget)
        layout_options.addWidget(scroll) 
        
        frame = QFrame()
        layout_origin = QGridLayout()
        frame.setLayout(layout_origin)
        layout_scroll.addWidget(frame)
        self.OriginSettingsGUI(layout_origin)     
        
        frame = QFrame()
        layout_pin = QGridLayout()
        frame.setLayout(layout_pin)
        layout_scroll.addWidget(frame)
        self.PinSettingsGUI(layout_pin)
            
        frame = QFrame()
        layout_cam = QGridLayout()
        frame.setLayout(layout_cam)
        layout_scroll.addWidget(frame)
        self.CamSettingsGUI(layout_cam)
        
        frame = QFrame()
        layout_buttons = QGridLayout()
        layout_buttons.setSpacing(5)
        frame.setLayout(layout_buttons)
        layout_options.addWidget(frame)
        self.ButtonsSettingsGUI(layout_buttons)      

        self.layout.addWidget(frame_options,0,1,3,1)
        frame_options.setLayout(layout_options)                    

    def ButtonsSettingsGUI(self, layout):
        self.button_update = QPushButton("Update tool")
        self.button_update.setStyleSheet(style_button_menu)
        layout.addWidget(self.button_update)
        self.button_update.clicked.connect(lambda: update_tool_settings())
        
        self.button_add_new = QPushButton("Add new tool")
        self.button_add_new.setStyleSheet(style_button_menu)
        layout.addWidget(self.button_add_new)
        self.button_add_new.clicked.connect(lambda: add_new_tool())    
   
    def OriginSettingsGUI(self, layout):
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        button = QPushButton("?")
        button.setStyleSheet(style_button_help)
        button.setFixedSize(20,20)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(URL_HELP_MODEL)))
        layout.addWidget(button, 0, 0)
            
        title = QLabel("Change origin:")
        title.setStyleSheet(style_label_bold)
        layout.addWidget(title, 0, 1)
        
        button = QPushButton("?")
        button.setStyleSheet(style_button_help)
        button.setFixedSize(20,20)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(URL_HELP_TOOL_FRAME)))
        layout.addWidget(button, 0, 2)

        title = QLabel("Tool frame:")
        title.setStyleSheet(style_label_bold)
        layout.addWidget(title, 0, 3)
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        self.entry_origin_pos = []
        self.ToolFrame = []
        
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed


            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.entry_origin_pos.append(entry)

            row = idx + 1
            col = 0

            layout.addWidget(label, row, col)
            layout.addWidget(entry, row, col + 1)  # Put entry in the next column
                       
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)
            
            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)
            entry.setValidator(validator)
            self.ToolFrame.append(entry)
            
            layout.addWidget(label, row, col + 2)
            layout.addWidget(entry, row, col + 3)  # Put entry in the next column
   
    def PinSettingsGUI(self, layout):
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        button = QPushButton("?")
        button.setStyleSheet(style_button_help)
        button.setFixedSize(20,20)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(URL_HELP_PIN)))
        layout.addWidget(button, 0, 0) 
        
        title = QLabel("Pin settings tool:")
        title.setStyleSheet(style_label_bold)
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.addWidget(title, 0, 1, 1, 3)    
        

            
        tools = ["Tool pin 1", "Tool pin 2", "Tool pin 3", "Tool pin 4", "Tool pin 5"]
        self.combobox_tool_pin = QComboBox() 
        self.combobox_tool_pin.setStyleSheet(style_combo)
        layout.addWidget(self.combobox_tool_pin, 1, 0, 1, 4)
        self.combobox_tool_pin.addItems(tools)

        ## define the type of tool, what is connected to the pin
        # no connection
        self.radio_button_no_con = QRadioButton()
        self.radio_button_no_con.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_no_con.setStyleSheet(style_radiobutton)
        layout.addWidget(self.radio_button_no_con,  2, 0)
        
        label = QLabel("No connection")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 2, 1, 1, 3)
        
        # Relay
        self.radio_button_relay = QRadioButton()
        self.radio_button_relay.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_relay.setStyleSheet(style_radiobutton)
        layout.addWidget(self.radio_button_relay, 3, 0)
        
        label = QLabel("ON/OFF relay")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 3, 1, 1, 3)
        
        # Servo
        self.radio_button_servo = QRadioButton()
        self.radio_button_servo.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_servo.setStyleSheet(style_radiobutton)
        layout.addWidget(self.radio_button_servo, 4, 0)

        self.entry_servo_min = QLineEdit()
        self.entry_servo_min.setStyleSheet(style_entry)
        self.entry_servo_min.setPlaceholderText("Min")
        self.entry_servo_min.setFixedWidth(50)
        self.entry_servo_min.setValidator(validator)
        layout.addWidget(self.entry_servo_min, 4, 1)
        
        self.entry_servo_max = QLineEdit()
        self.entry_servo_max.setStyleSheet(style_entry)
        self.entry_servo_max.setPlaceholderText("Max")
        self.entry_servo_max.setFixedWidth(50)
        self.entry_servo_max.setValidator(validator)
        layout.addWidget(self.entry_servo_max, 4, 2)

        label = QLabel("Servo")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 4, 3)        
        
    def CamSettingsGUI(self, layout):
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        button = QPushButton("?")
        button.setStyleSheet(style_button_help)
        button.setFixedSize(20,20)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(URL_HELP_CAM)))
        layout.addWidget(button, 0, 0)
                
        title = QLabel("Camera settings:")
        title.setStyleSheet(style_label_bold)
        layout.addWidget(title, 0, 1, 1, 3)
        
        label = QLabel("Camera offset")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 1, 0, 1, 4)
        
        label = QLabel("XYZ:")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 2, 0)
        
        self.cam_offset = []
        for i in range(3):
            entry_cam = QLineEdit()
            entry_cam.setStyleSheet(style_entry)
            entry_cam.setFixedWidth(50)
            entry_cam.setValidator(validator)
            layout.addWidget(entry_cam, 2, i + 1)
            
            self.cam_offset.append(entry_cam)
        
        # rotational compensation       
        label = QLabel("Rotation offset in degreed")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 3, 0 , 1, 3)
        
        self.camere_rotation_offset = QLineEdit()
        self.camere_rotation_offset.setText("0")
        self.camere_rotation_offset.setStyleSheet(style_entry)
        self.camere_rotation_offset.setFixedWidth(50)
        self.camere_rotation_offset.setValidator(validator)
        layout.addWidget(self.camere_rotation_offset, 3, 3)
        
     
        
        label = QLabel("Small square")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 4, 0 , 1, 2)
        
        label = QLabel("Width")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 5, 0)
        
        self.size_small_square = QLineEdit()
        self.size_small_square.setText("120")
        self.size_small_square.setStyleSheet(style_entry)
        self.size_small_square.setFixedWidth(50)
        self.size_small_square.setValidator(validator)
        layout.addWidget(self.size_small_square, 5, 1)
        
        label = QLabel("Height")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 5, 2)
        
        self.z_dis_small_square = QLineEdit()
        self.z_dis_small_square.setPlaceholderText("Max")
        self.z_dis_small_square.setStyleSheet(style_entry)
        self.z_dis_small_square.setFixedWidth(50)
        self.z_dis_small_square.setValidator(validator)
        layout.addWidget(self.z_dis_small_square, 5, 3)

        label = QLabel("Big square")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 6, 0, 1, 2)
        
        label = QLabel("Width")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 7, 0)
        
        self.size_big_square = QLineEdit()
        self.size_big_square.setText("160")
        self.size_big_square.setStyleSheet(style_entry)
        self.size_big_square.setFixedWidth(50)
        self.size_big_square.setValidator(validator)
        layout.addWidget(self.size_big_square, 7, 1)
        
        label = QLabel("Height")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 7, 2)
        
        self.z_dis_big_square = QLineEdit()
        self.z_dis_big_square.setPlaceholderText("Max")
        self.z_dis_big_square.setStyleSheet(style_entry)
        self.z_dis_big_square.setFixedWidth(50)
        self.z_dis_big_square.setValidator(validator)
        layout.addWidget(self.z_dis_big_square, 7, 3)
              
        checkbox_cal_square = QCheckBox('Show calibration square')
        checkbox_cal_square.setStyleSheet(style_checkbox)
        layout.addWidget(checkbox_cal_square, 8, 0, 1, 4) 
        checkbox_cal_square.stateChanged.connect(self.show_square)

    def show_square(self, state):
        if state == 2:  # Checked (Qt.Checked)
            show_square_tool(True)
        else:  # Unchecked (Qt.Unchecked)
            show_square_tool(False)


    def CreateButtons(self, tool_data):
        item = len(self.frames)

        frame = QWidget()
        layout_tool = QHBoxLayout()
        layout_tool.setContentsMargins(5,0,5,5)
        frame.setLayout(layout_tool)
        self.frames.append(frame)

        label = QLabel(tool_data[0])
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        layout_tool.addWidget(label)
        
        button = QPushButton("X")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_tool(idx))
        layout_tool.addWidget(button)
        
        button = QPushButton("Settings")
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_tool_settings(idx))
        layout_tool.addWidget(button)
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        
        combo = QComboBox()
        combo.view().setMinimumWidth(170)
        combo.setStyleSheet(style_combo)
        combo.addItems(colors)
        combo.setCurrentText(tool_data[3])
        combo.currentTextChanged.connect(lambda text: change_color_tool(item, text))
        layout_tool.addWidget(combo)

        self.layout_scroll.addWidget(frame) 
    
    def DeleteButtons(self):
        for frame in self.frames:
            self.layout_scroll.removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater() 
            frame = None

        self.frames = []
        self.frames_layout = []


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
            self.radio_button_no_con.setChecked(False)
        elif tool_settings[7] == "Relay":
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(True)
            self.radio_button_no_con.setChecked(False)
        else:
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(False)
            self.radio_button_no_con.setChecked(True)
            
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
        
    def ClearSettings(self):
        # Set the settings
        for i in range(6):
            self.entry_origin_pos[i].setText("0.0")
            self.ToolFrame[i].setText("0.0")
        
        # Set the combo box
        self.combobox_tool_pin.setCurrentIndex(0)
              
        self.radio_button_no_con.setChecked(True)
        self.radio_button_servo.setChecked(False)
        self.radio_button_relay.setChecked(False)
            
        self.entry_servo_min.setText("")
        self.entry_servo_max.setText("")
        
        for i in range(3):
            self.cam_offset[i].setText(str("0.0"))
            
        self.camere_rotation_offset.setText("0.0")

        self.z_dis_big_square.setText("0.0")
        self.z_dis_small_square.setText("0.0")
        self.size_big_square.setText("0.0")
        self.size_small_square.setText("0.0")


    def ClearPlotter(self):
        if self.stl_actor and self.plotter:
            self.renderer.RemoveActor(self.stl_actor)
            self.stl_actor = None  # Clear the reference
            self.plotter.Render()  # Update the render window


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
        
        # get the origin of the part
        for i in range(6):
            try:
                data_tool[4][i] = float(self.entry_origin_pos[i].text())
            except:
                data_tool[4][i] = 0
                self.entry_origin_pos[i].setText("0.0")
                
        # get the tool frame
        for i in range(6):  
            try:
                data_tool[5][i] = float(self.ToolFrame[i].text())
            except:
                data_tool[5][i] = 0
                self.ToolFrame[i].setText("0.0")      
                
        
        # get the pin number
        data_tool[6] = self.combobox_tool_pin.currentText() 
        
        # get the type of tool
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
        
        
        # get the camera offset mm
        offset = []
        for i in range(3):
            try:
                value = float(self.cam_offset.text())
                offset.append(value)
            except:
                offset.append(0.0)
            
        data_tool[9] = offset
        
        # get the rotation offset of the camera
        data_tool[10] = self.camere_rotation_offset.text()
            
        # get the other cam settings
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

        
        
