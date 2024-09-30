from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QSlider, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.core.event_manager import event_manager

from gui.style import *

import backend.core.variables as var

from backend.core.api import xbox_on

class SettingsField(QWidget):
    def __init__(self, frame):
        self.frame = frame
   
        self.GUI()
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_get_cam_port", self.GetCamPort)
        event_manager.subscribe("request_set_cam_port", self.SetCamPort)
        
        event_manager.subscribe("request_get_robot_port", self.GetRobotPort)
        event_manager.subscribe("request_set_robot_port", self.SetRobotPort)
        
        event_manager.subscribe("request_get_io_port", self.GetIOPort)
        event_manager.subscribe("request_set_io_port", self.SetIOPort)
        
        event_manager.subscribe("request_get_jog_distance", self.GetJogDistance)
        event_manager.subscribe("request_set_jog_distance", self.SetJogDistance)
        
        event_manager.subscribe("request_button_controller_connect", self.ButtonConnectController)
        event_manager.subscribe("request_state_controller_label", self.StateControllerLabel)
        
        event_manager.subscribe("request_get_speed", self.GetSpeed)
        event_manager.subscribe("request_get_accel", self.GetAccel)
                
    def GUI(self):
        layout = QGridLayout(self.frame)

        self.slider_speed = SettingSlider(layout, 0, 2, 150, "Jog speed") 
        self.slider_accel = SettingSlider(layout, 1, 2, 150, "Jog accel")
        
        title = QLabel("Settings")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(title, 0,0)
        
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        ####### com port settings
        label = QLabel("Com port robot:")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_robot = QLineEdit()
        self.entry_com_robot.setFixedWidth(50)  # Set the width as needed
        self.entry_com_robot.setStyleSheet(style_entry)
        self.entry_com_robot.setValidator(validator)

        layout.addWidget(label, 0, 8)
        layout.addWidget(self.entry_com_robot, 0, 9)  # Put entry in the next column
        
        ######## 
        label = QLabel("Com port IO:")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_io = QLineEdit()
        self.entry_com_io.setFixedWidth(50)  # Set the width as needed
        self.entry_com_io.setStyleSheet(style_entry)

        layout.addWidget(label, 1, 8)
        layout.addWidget(self.entry_com_io, 1, 9)  # Put entry in the next column       
        
        ######## 
        label = QLabel("CAM adress/ port: ")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_cam = QLineEdit()
        self.entry_com_cam.setFixedWidth(50)  # Set the width as needed
        self.entry_com_cam.setStyleSheet(style_entry)

        layout.addWidget(label, 0, 10)
        layout.addWidget(self.entry_com_cam, 0, 11)  # Put entry in the next column          
        
        ######## 
        label = QLabel("Jog distance:")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_jog_dis = QLineEdit()
        self.entry_jog_dis.setFixedWidth(50)  # Set the width as needed
        self.entry_jog_dis.setStyleSheet(style_entry)

        layout.addWidget(label, 1, 10)
        layout.addWidget(self.entry_jog_dis, 1, 11)  # Put entry in the next column         
        
        ######## Xbox 
        self.controller_button = QPushButton("Controller")
        self.controller_button.setStyleSheet(style_button)
        self.controller_state = QLabel("")
        
        self.controller_button.setMaximumWidth(80)
        self.controller_button.clicked.connect(xbox_on)
        layout.addWidget(self.controller_button, 1,0)

        self.controller_state.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.controller_state,3,0)
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, 0, 1)
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, 0, 3)
 
    def StateControllerLabel(self, state):
        self.controller_state.setText(state)
 
    def ButtonConnectController(self, connect):
        if connect:
            self.controller_button.setStyleSheet(style_button_pressed)
        else:
            self.controller_button.setStyleSheet(style_button)
        
    def GetSpeed(self):
        return self.slider_speed.current_value
    
    def GetAccel(self):
        return self.slider_accel.current_value

        
    def GetCamPort(self):
        value = self.entry_com_cam.text()
        print(f"value cam port {value}")
        if value == "":
            return "0"
        else:
            return value
    
    def SetCamPort(self, value):
        self.entry_com_cam.setText(value)
     
    def GetRobotPort(self):
        value = self.entry_com_robot.text()
        if value == "":
            return "0"
        else:
            return value
    
    def SetRobotPort(self, value):
        self.entry_com_robot.setText(value)
    
    def GetIOPort(self):
        value = self.entry_com_io.text()
        if value == "":
            return "0"
        else:
            return value
    
    def SetIOPort(self, value):
        self.entry_com_io.setText(value)
     
    def GetJogDistance(self):
        value = self.entry_jog_dis.text()
        if value == "":
            return "1"
        else:
            return value
    
    def SetJogDistance(self, value):
        self.entry_jog_dis.setText(value)

      
      
       
    
     
class SettingSlider():
    def __init__(self, layout, row, col, width, name):
        # Create the main vertical layout
        slider_layout = QGridLayout()
        self.name = name
        
        # Slider parameters
        min_value = 1
        max_value = 100
        initial_value = int((min_value + max_value) / 2)
        self.current_value = 50
        
        # Label for the minimum value
        min_label = QLabel(str(min_value))
        min_label.setStyleSheet(style_label)
        min_label.setFixedWidth(10)
        slider_layout.addWidget(min_label, 1, 0)
        
        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet(style_slider)
        self.slider.setMaximumWidth(width)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.updateLabel)
        slider_layout.addWidget(self.slider, 1, 1)        

        # Label for the maximum value
        max_label = QLabel(str(max_value))
        max_label.setStyleSheet(style_label)
        max_label.setFixedWidth(20)
        slider_layout.addWidget(max_label, 1, 2)
        
        # Create a label to display the current slider value
        self.label = QLabel(f"{self.name}: {initial_value}")
        self.label.setStyleSheet(style_label)
        self.label.setAlignment(Qt.AlignCenter)
        slider_layout.addWidget(self.label, 0, 0, 1, 3)        
        
        layout.addLayout(slider_layout, row, col)
        
    def updateLabel(self, value):
        self.label.setText(f"{self.name}: {value}")
        self.current_value = value
                    

