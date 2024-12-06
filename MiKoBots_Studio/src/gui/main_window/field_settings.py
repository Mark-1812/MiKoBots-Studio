from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.core.event_manager import event_manager
from backend.file_managment.file_management import FileManagement
from gui.style import *

import backend.core.variables as var

from backend.xbox import xbox_on
from backend.robot_management  import change_robot, get_robots
from backend.robot_management.communication  import send_settings_robot

from gui.windows.robot_settings import RobotWindow
from gui.windows.vision import VisionWindow
from gui.windows.vision_settings import VisionSettingsWindow
from gui.windows.xbox import XBoxWindow

class SettingsField(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.setStyleSheet(style_widget)
        self.layout.setSpacing(5)

        self.RobotWindow = RobotWindow()
        self.VisionWindow = VisionWindow()
        self.file_management = FileManagement()
        self.XboxWindow = XBoxWindow()
        self.VisionSettingsWindow = VisionSettingsWindow()
   
        self.GUI()
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_get_jog_distance", self.GetJogDistance)
        event_manager.subscribe("request_set_jog_distance", self.SetJogDistance)
        
        event_manager.subscribe("request_button_controller_connect", self.ButtonConnectController)
        event_manager.subscribe("request_state_controller_label", self.StateControllerLabel)
        
        event_manager.subscribe("request_get_speed", self.GetSpeed)
        event_manager.subscribe("request_set_speed", self.SetSpeed)

        event_manager.subscribe("request_get_accel", self.GetAccel)
        event_manager.subscribe("request_set_accel", self.SetAccel)
        
        event_manager.subscribe("request_add_robot_combo", self.AddRobotCombo)
        event_manager.subscribe("request_delete_robot_combo", self.DeleteRobotCombo)
        event_manager.subscribe("request_set_robot_combo", self.SetRobotCombo)
        
        
                
    def GUI(self):
        title = QLabel("Settings")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(title, 0,0)
        
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        frame = QFrame()
        layout_robot = QHBoxLayout()
        layout_robot.setContentsMargins(0, 0, 0, 0)
        layout_robot.setAlignment(Qt.AlignLeft)
        layout_robot.setSpacing(5)
        frame.setLayout(layout_robot)
        self.layout.addWidget(frame, 1, 0) 
            
        self.combo_robot = QComboBox(self)
        self.combo_robot.currentIndexChanged.connect(lambda index: change_robot(index))
        self.combo_robot.setStyleSheet(style_combo)
        self.combo_robot.setFixedWidth(150)
        layout_robot.addWidget(self.combo_robot)
        
        image_path = self.file_management.resource_path('settings.png')
        self.button_settings_robot = QPushButton()
        self.button_settings_robot.setToolTip('Settings robot')  
        self.button_settings_robot.setFixedSize(20,20)
        self.button_settings_robot.setIcon(QIcon(image_path))
        self.button_settings_robot.clicked.connect(lambda: self.ShowRobotWindow())
        self.button_settings_robot.setStyleSheet(style_button)
        layout_robot.addWidget(self.button_settings_robot)
        
        
        image_path = self.file_management.resource_path('upload.png')
        self.button_settings_send = QPushButton() 
        self.button_settings_send.setToolTip('Upload settings')  
        self.button_settings_send.setFixedSize(20,20)
        self.button_settings_send.setIcon(QIcon(image_path))
        self.button_settings_send.setStyleSheet(style_button)
        self.button_settings_send.clicked.connect(send_settings_robot)
        layout_robot.addWidget(self.button_settings_send)


        ### vision
        frame = QFrame()
        layout_vision = QHBoxLayout()
        layout_vision.setContentsMargins(0, 0, 0, 0)
        layout_vision.setAlignment(Qt.AlignLeft)
        layout_vision.setSpacing(5)
        frame.setLayout(layout_vision)
        self.layout.addWidget(frame, 2, 0) 

        label = QLabel("Vision")
        label.setStyleSheet(style_label)
        layout_vision.addWidget(label)

        image_path = self.file_management.resource_path('settings.png')
        button = QPushButton()
        button.setToolTip('Settings vision')  
        button.setFixedSize(20,20)
        button.setIcon(QIcon(image_path))
        button.clicked.connect(lambda: self.ShowVisionWindows())
        button.setStyleSheet(style_button)
        layout_vision.addWidget(button)
  
        image_path = self.file_management.resource_path('vision.png')
        self.vision_button = QPushButton()
        self.vision_button.setStyleSheet(style_button)
        self.vision_button.setFixedSize(20,20)
        self.vision_button.setIcon(QIcon(image_path))
        self.vision_button.setIconSize(self.vision_button.size())
        self.vision_button.clicked.connect(self.VisionWindow.show)
        layout_vision.addWidget(self.vision_button)         
        

        ######## Xbox 
        frame = QFrame()
        layout_controller = QHBoxLayout()
        layout_controller.setContentsMargins(0, 0, 0, 0)
        layout_controller.setAlignment(Qt.AlignLeft)
        layout_controller.setSpacing(5)
        frame.setLayout(layout_controller)
        self.layout.addWidget(frame, 3, 0) 

        image_path = self.file_management.resource_path('controller.png')
        self.controller_button = QPushButton()
        self.controller_button.setStyleSheet(style_button)
        self.controller_button.setFixedSize(20,20)
        self.controller_button.setIcon(QIcon(image_path))
        self.controller_button.setIconSize(self.controller_button.size())
        self.controller_button.clicked.connect(xbox_on)
        layout_controller.addWidget(self.controller_button)
        
        image_path = self.file_management.resource_path('settings.png')
        controller_settings = QPushButton()
        controller_settings.setStyleSheet(style_button)
        controller_settings.setFixedSize(20,20)
        controller_settings.setIcon(QIcon(image_path))
        controller_settings.setIconSize(self.controller_button.size())
        controller_settings.clicked.connect(self.ShowXBoxWindow)
        layout_controller.addWidget(controller_settings)        

                
        self.controller_state = QLabel("")
        self.controller_state.setAlignment(Qt.AlignLeft)
        layout_controller.addWidget(self.controller_state)



        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(spacer_widget, 0, 1, 3, 1)


        
        frame = QFrame()
        frame.setFixedWidth(300)
        layout_sliders = QVBoxLayout()
        layout_sliders.setSpacing(5)
        frame.setLayout(layout_sliders)
        self.layout.addWidget(frame, 0, 2, 3, 1)

        self.slider_speed = SettingSlider(layout_sliders, 150, "Jog speed") 
        self.slider_accel = SettingSlider(layout_sliders, 150, "Jog accel")
        self.slider_jog = SettingSlider(layout_sliders, 150, "Jog distance")
        
    def AddRobotCombo(self, robot):
        self.combo_robot.blockSignals(True)
        self.combo_robot.addItem(robot)
        self.combo_robot.blockSignals(False)
        
    def SetRobotCombo(self, robot):
        self.combo_robot.blockSignals(True)
        self.combo_robot.setCurrentText(robot)
        self.combo_robot.blockSignals(False)
        
    def DeleteRobotCombo(self):
        self.combo_robot.blockSignals(True)
        self.combo_robot.clear()
        self.combo_robot.blockSignals(False)
        
    def ShowXBoxWindow(self):
        self.XboxWindow.show()
        self.XboxWindow.raise_()               
        
    def ShowRobotWindow(self):
        self.RobotWindow.RobotOverview.DeleteButtons()

        robots = get_robots()
        for i in range(len(robots)):
            self.RobotWindow.RobotOverview.CreateButtons(i, robots[i][0])

        self.RobotWindow.Robot3DModel.OpenPlotter()
        self.RobotWindow.RobotTools.OpenPlotter()
        self.RobotWindow.OpenPlotter()

        robot = var.SELECTED_ROBOT
        self.RobotWindow.RobotOverview.Robots_buttons[robot].setChecked(True)

        self.RobotWindow.exec_()

        self.activateWindow()

    def ShowVisionWindows(self):
        self.VisionSettingsWindow.show()
        self.VisionSettingsWindow.raise_()
 
    def StateControllerLabel(self, state):
        self.controller_state.setText(state)
 
    def ButtonConnectController(self, connect):
        if connect:
            self.controller_button.setStyleSheet(style_button_pressed)
        else:
            self.controller_button.setStyleSheet(style_button)
        
    def GetSpeed(self):
        return self.slider_speed.current_value

    def SetSpeed(self, value):
        self.slider_speed.slider.setValue(int(value))
    
    def GetAccel(self):
        return self.slider_accel.current_value

    def SetAccel(self, value):
        self.slider_accel.slider.setValue(int(value))

    def GetJogDistance(self):
        return self.slider_jog.current_value
    
    def SetJogDistance(self, value):
        self.slider_jog.slider.setValue(int(value))
      
      
       
   
     
     
class SettingSlider():
    def __init__(self, layout, width, name):
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
        slider_layout.addWidget(min_label, 0, 2)
        
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
        slider_layout.addWidget(self.slider, 0, 3)        

        # Label for the maximum value
        max_label = QLabel(str(max_value))
        max_label.setStyleSheet(style_label)
        max_label.setFixedWidth(20)
        slider_layout.addWidget(max_label, 0, 4)
        
        # Create a label to display the current slider value
        self.label = QLabel(f"{self.name}: ")
        self.label.setStyleSheet(style_label)
        self.label.setFixedWidth(90)
        slider_layout.addWidget(self.label, 0, 0)        
        
        self.input = QLineEdit(str(initial_value))
        self.input.setStyleSheet(style_entry)
        self.input.setFixedWidth(30)
        slider_layout.addWidget(self.input, 0, 1)  

        self.input.textChanged.connect(self.on_text_changed)

        layout.addLayout(slider_layout)
        
    def updateLabel(self, value):
        self.current_value = value
        self.input.setText(str(value))
        
        if self.name == "Jog speed":
            var.JOG_SPEED = value
        if self.name == "Jog accel":
            var.JOG_ACCEL = value
    
    def on_text_changed(self, text):
        try:
            value = int(text)
            self.slider.setValue(value)
        except:
            print(var.LANGUAGE_DATA.get("message_fill_in_rounf_number"))
                    

