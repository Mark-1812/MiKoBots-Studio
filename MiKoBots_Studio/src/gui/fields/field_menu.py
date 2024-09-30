from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.file_managment.file_management import FileManagement

import webbrowser

from gui.style import *

from backend.core.event_manager import event_manager
import backend.core.variables as var

from backend.core.api import new_file
from backend.core.api import save_file
from backend.core.api import save_as_file
from backend.core.api import open_file

from backend.core.api import connect_robot
from backend.core.api import connect_io
from backend.core.api import connect_cam
from backend.core.api import home
from backend.core.api import jog_joint
from backend.core.api import run_script
from backend.core.api import stop_script

import os

class MenuField():
    def __init__(self, frame, showhidetab):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        self.ShowHideTab = showhidetab

        self.FrameButtons(frame_layout)
        self.LibraryButtons(frame_layout)
        self.RobotButtons(frame_layout)
        
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_connect_button_color", self.ButtonConnectRobotColor)
        event_manager.subscribe("request_io_connect_button_color", self.ButtonConnectIOColor)
        event_manager.subscribe("request_robot_home_button_color", self.ButtonHomeRobotColor)
        event_manager.subscribe("request_cam_connect_button_color", self.ButtonConnectCamColor)
        
    def openLink(self, url):
        webbrowser.open("https://www.mikobots.com")
        
    def FrameButtons(self, layout):
        file_management = FileManagement()
        image_path = file_management.resource_path('studio.png')
        pixmap = QPixmap(image_path)
        
        self.image_label = QLabel()      
        self.image_label.setPixmap(pixmap) 
        self.image_label.mousePressEvent = self.openLink

        layout.addWidget(self.image_label, 0, 0)
              
        row_index = layout.rowCount()
        buttons = {
            "New file": lambda: new_file(),
            "Save": lambda: save_file(),
            "Save as": lambda: save_as_file(),
            "Open": lambda: open_file(),
        }

        for label, action in buttons.items():
            button = QPushButton(label)
            button.setStyleSheet(style_button)
            button.pressed.connect(action)
            layout.addWidget(button, row_index, 0)
            row_index += 1
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, layout.rowCount(), 0, 1, layout.columnCount())    

    def LibraryButtons(self, layout):                              
        row = layout.rowCount()
                 
        button_group = QButtonGroup()     
        button_names = ["Simulation", "Gcode", "Vision", "Robot"]    

        button_style = """
            QRadioButton::indicator {
                width: 1px; /* Reduce size to minimal without setting it to 0 */
                height: 1px; /* Same for height to avoid the error */
                background-color: transparent; /* Make the indicator invisible */            }
            QRadioButton {
                background-color: orange;
                border: 0px solid gray;
                border-radius: 3px;
                height: 35px;
                padding: 0px 25px; /* Adjust padding to ensure text is centered */
                font-size: 12px;
                font-family: Arial;
                text-align: center; /* Center the text horizontally */
             }
            QRadioButton:hover {
                background-color: white;
            }
            QRadioButton:checked {
                background-color: green;
                color: black;
            }
        """
        
        for name in button_names:
            radio_button = QRadioButton(name)
            radio_button.toggled.connect(lambda checked, name=name: self.ShowHideTab.show_hide(name))
            radio_button.setStyleSheet(button_style)  # Expands to fill the available space
            layout.addWidget(radio_button, row, 0)
            button_group.addButton(radio_button)
            row += 1

        button_group.buttons()[0].setChecked(True)
                 
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, layout.rowCount(), 0, 1, layout.columnCount())      
   
    # Buttons that connect the robot and other
   
    def RobotButtons(self, layout):
        row = layout.rowCount()
        title = QtWidgets.QLabel("Robot")
        title.setStyleSheet(style_label_title)
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout.addWidget(title, row, 0)
        
        self.BUTTON_CONNECT_ROBOT = QPushButton("Connect robot")
        self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button)
        layout.addWidget(self.BUTTON_CONNECT_ROBOT, row + 1, 0)
        self.BUTTON_CONNECT_ROBOT.pressed.connect(connect_robot)

        self.BUTTON_CONNECT_IO = QPushButton("Connect IO robot")
        self.BUTTON_CONNECT_IO.setStyleSheet(style_button)
        layout.addWidget(self.BUTTON_CONNECT_IO, row + 2, 0)
        self.BUTTON_CONNECT_IO.pressed.connect(connect_io)
        
        self.BUTTON_CONNECT_CAM = QPushButton("Connect camera")
        self.BUTTON_CONNECT_CAM.setStyleSheet(style_button)
        layout.addWidget(self.BUTTON_CONNECT_CAM, row + 3, 0)
        self.BUTTON_CONNECT_CAM.pressed.connect(connect_cam)
        print(self.BUTTON_CONNECT_CAM)

        button_send = QPushButton("Send to robot")
        button_send.setStyleSheet(style_button)
        button_send.pressed.connect(lambda: run_script(False))
        layout.addWidget(button_send, row + 4, 0)            
        
        self.BUTTON_HOME_ROBOT = QPushButton("Home")
        self.BUTTON_HOME_ROBOT.setStyleSheet(style_button)
        self.BUTTON_HOME_ROBOT.pressed.connect(home)
        layout.addWidget(self.BUTTON_HOME_ROBOT, row + 5, 0)
        
        button_home_pos = QPushButton("Move to home")
        button_home_pos.setStyleSheet(style_button)
        button_home_pos.pressed.connect(lambda: jog_joint([0]*var.NUMBER_OF_JOINTS))
        layout.addWidget(button_home_pos, row + 6, 0)    
        
        button_stop = QPushButton("Stop")
        button_stop.setFixedHeight(40)
        button_stop.setStyleSheet(style_button_red)     
        button_stop.pressed.connect(stop_script)
        
        
        layout.addWidget(button_stop, row + 7, 0)

    def ButtonConnectRobotColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_pressed)
        else:
            self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button)

    def ButtonConnectIOColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_IO.setStyleSheet(style_button_pressed)
        else:
            self.BUTTON_CONNECT_IO.setStyleSheet(style_button)
            
    def ButtonHomeRobotColor(self, home):
        if home:
            self.BUTTON_HOME_ROBOT.setStyleSheet(style_button_pressed)
        else:
            self.BUTTON_HOME_ROBOT.setStyleSheet(style_button)
            
    def ButtonConnectCamColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_pressed)
        else:
            self.BUTTON_CONNECT_CAM.setStyleSheet(style_button)
      