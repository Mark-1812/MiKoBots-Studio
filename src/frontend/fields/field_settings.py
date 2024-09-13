from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QSlider, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.core.event_manager import event_manager

import backend.core.variables as var

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
                
        

    def GUI(self):
        layout = QGridLayout(self.frame)

        self.slider_speed = SettingSlider(layout, 0, 2, 150, "Jog speed") 
        self.slider_accel = SettingSlider(layout, 1, 2, 150, "Jog accel")
        
        title = QLabel("Settings")
        title.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(title, 0,0)
        
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        ####### com port settings
        label = QLabel("Com port robot:")
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_robot = QLineEdit()
        self.entry_com_robot.setFixedWidth(50)  # Set the width as needed
        self.entry_com_robot.setStyleSheet("background-color: white")

        layout.addWidget(label, 0, 8)
        layout.addWidget(self.entry_com_robot, 0, 9)  # Put entry in the next column
        
        ######## 
        label = QLabel("Com port IO:")
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_io = QLineEdit()
        self.entry_com_io.setFixedWidth(50)  # Set the width as needed
        self.entry_com_io.setStyleSheet("background-color: white")

        layout.addWidget(label, 1, 8)
        layout.addWidget(self.entry_com_io, 1, 9)  # Put entry in the next column       
        
        ######## 
        label = QLabel("CAM adress/ port: ")
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_com_cam = QLineEdit()
        self.entry_com_cam.setFixedWidth(50)  # Set the width as needed
        self.entry_com_cam.setStyleSheet("background-color: white")

        layout.addWidget(label, 0, 10)
        layout.addWidget(self.entry_com_cam, 0, 11)  # Put entry in the next column          
        
        ######## 
        label = QLabel("Jog distance:")
        label.setFixedWidth(100)  # Set the width as needed
            
        self.entry_jog_dis = QLineEdit()
        self.entry_jog_dis.setFixedWidth(50)  # Set the width as needed
        self.entry_jog_dis.setStyleSheet("background-color: white")

        layout.addWidget(label, 1, 10)
        layout.addWidget(self.entry_jog_dis, 1, 11)  # Put entry in the next column         
        
        ######## Xbox 
        Xbox_button = QPushButton("Xbox", parent=self.frame)
        Xbox_state = QLabel("", parent=self.frame)
        
        #XBox_controller = XBox(Xbox_button, Xbox_state, jog_entry, self.robot)
        
        Xbox_button.setMaximumWidth(80)
        Xbox_button.clicked.connect(lambda: XBox_controller.XBoxOn())
        layout.addWidget(Xbox_button, 1,0)

        Xbox_state.setAlignment(Qt.AlignLeft)
        layout.addWidget(Xbox_state,3,0)
        
        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 0, 1)
        
        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 0, 3)
        
    def GetCamPort(self):
        value = self.entry_com_cam.text()
        print(f"value cam port {value}")
        return value
    
    def SetCamPort(self, value):
        self.entry_com_cam.setText(value)
     
    def GetRobotPort(self):
        value = self.entry_com_robot.text()
        return value
    
    def SetRobotPort(self, value):
        self.entry_com_robot.setText(value)
    
    def GetIOPort(self):
        value = self.entry_com_io.text()
        return value
    
    def SetIOPort(self, value):
        self.entry_com_io.setText(value)
     
    def GetJogDistance(self):
        value = self.entry_jog_dis.text()
        print("get torovjslwhifd,jfsdfg")
        return value
    
    def SetJogDistance(self, value):
        self.entry_jog_dis.setText(value)

      
      
       
    
     
class SettingSlider():
    def __init__(self, layout, row, col, width, name):
        # Create the main vertical layout
        slider_layout = QGridLayout()
        self.name = name
        
        # Slider parameters
        min_value = 0
        max_value = 100
        initial_value = int((min_value + max_value) / 2)
        
        # Label for the minimum value
        min_label = QLabel(str(min_value))
        min_label.setFixedWidth(10)
        slider_layout.addWidget(min_label, 1, 0)
        
        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximumWidth(width)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.updateLabel)
        self.setSliderStyle()
        slider_layout.addWidget(self.slider, 1, 1)        

        # Label for the maximum value
        max_label = QLabel(str(max_value))
        max_label.setFixedWidth(20)
        slider_layout.addWidget(max_label, 1, 2)
        
        # Create a label to display the current slider value
        self.label = QLabel(f"{self.name}: {initial_value}")
        self.label.setAlignment(Qt.AlignCenter)
        slider_layout.addWidget(self.label, 0, 0, 1, 3)        
        
        layout.addLayout(slider_layout, row, col)
        
    def updateLabel(self, value):
        self.label.setText(f"{self.name}: {value}")
        if self.name == "Jog speed":
            var.JOG_SPEED = value
        if self.name == "Jog accel":
            var.JOG_ACCEL = value
                    
    def setSliderStyle(self):
        # Customize the slider's handle to be orange
        slider_style = """
        QSlider::handle:horizontal {
            background: orange;
            border: 1px solid #5c5c5c;
            width: 18px;
            margin: -2px 0; /* Handle is placed by default on the contents rect of the groove. Expand outside the groove */
            border-radius: 3px;
        }
        """
        self.slider.setStyleSheet(slider_style)