from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.file_managment.file_management import FileManagement

from gui.windows.simulation_objects_gui import SimulationObjectsGUI
from gui.windows.simulation_origin_gui import SimulationOriginGUI
from gui.windows.connect_device import ConnectDevice
from gui.windows.vision import VisionWindow

import webbrowser

from gui.style import *



from backend.core.event_manager import event_manager
import backend.core.variables as var

from backend.file_manager import save_file
from backend.file_manager import save_as_file
from backend.file_manager import open_file
from backend.file_manager import new_file

from backend.robot_management import connect_robot_com
from backend.robot_management import connect_io_com
from backend.robot_management import connect_robot_bt
from backend.robot_management import connect_io_bt

from backend.robot_management import stop_robot

from backend.simulation import enable_simulation

from backend.run_program import run_script
from backend.run_program import stop_script
from backend.run_program import run_single_line

from backend.vision import connect_cam



class MenuField(QWidget):
    def __init__(self, frame):
        
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        frame_layout.setSpacing(5) 
        
        self.simulation_origin_gui = SimulationOriginGUI()
        self.simulation_objects_gui = SimulationObjectsGUI()

        self.connect_robot_window = ConnectDevice("ROBOT")
        self.connect_io_window = ConnectDevice("IO")
        self.connect_cam_window = ConnectDevice("CAMERA")
        
        self.vision_window = VisionWindow()


        self.FrameButtons(frame_layout)
        # self.LibraryButtons(frame_layout)
        self.SimButtons(frame_layout)
        self.RobotButtons(frame_layout)
        
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_connect_button_color", self.ButtonConnectRobotColor)
        event_manager.subscribe("request_io_connect_button_color", self.ButtonConnectIOColor)
        event_manager.subscribe("request_robot_home_button_color", self.ButtonHomeRobotColor)
        event_manager.subscribe("request_cam_connect_button_color", self.ButtonConnectCamColor)
        event_manager.subscribe("request_stop_sim", self.ButtonStopSim)
        event_manager.subscribe("request_disable_robot_button", self.ButtonConnectRobotDisable)
        event_manager.subscribe("request_disable_io_button", self.ButtonConnectIODisable)
        event_manager.subscribe("request_disable_cam_button", self.ButtonConnectCamDisable)
        
    def openLink(self, url):
        webbrowser.open("https://www.mikobots.com")
        
    def FrameButtons(self, layout):
        file_management = FileManagement()
        image_path = file_management.resource_path('studio.png')
        pixmap = QPixmap(image_path)
        
        self.image_label = QLabel()      
        self.image_label.setPixmap(pixmap) 
        self.image_label.setFixedSize(140,140)
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
            button.setStyleSheet(style_button_menu)
            button.pressed.connect(action)
            layout.addWidget(button, row_index, 0)
            row_index += 1
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, layout.rowCount(), 0, 1, layout.columnCount())    
   
   # simulation buttons
    def SimButtons(self, layout):
        row = layout.rowCount()
        title = QtWidgets.QLabel("Simulation")
        title.setStyleSheet(style_label_title)
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout.addWidget(title, row, 0)
        
        simCheckbox = QCheckBox("Enable simulation")
        simCheckbox.setStyleSheet(style_checkbox)
        layout.addWidget(simCheckbox, row + 1, 0)
        simCheckbox.stateChanged.connect(lambda state: self.EnableSimulation(state))
        
        self.RunSim = QPushButton("Run simulation")
        self.RunSim.setStyleSheet(style_button_menu)
        self.RunSim.clicked.connect(lambda: run_script(True))
        layout.addWidget(self.RunSim, row + 2, 0)
        
        self.StopSim = QPushButton("Stop simulation")
        self.StopSim.setStyleSheet(style_button_menu)
        self.StopSim.clicked.connect(stop_script) 
        layout.addWidget(self.StopSim, row + 3, 0)
        
        button = QPushButton("add origin")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(self.simulation_origin_gui.show)
        layout.addWidget(button, row + 4, 0) 
        
        button = QPushButton("Show / hide")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: self.ShowHide())
        layout.addWidget(button, row + 5, 0) 

        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, layout.rowCount(), 0, 1, layout.columnCount())    
   
    def ButtonStopSim(self):
        stop_script()   
   
    def EnableSimulation(self, state):
        enable_simulation(state)
        
    def ShowHide(self):
        self.simulation_objects_gui.openevent()
        self.simulation_objects_gui.show()   
        
    # Buttons that connect the robot and other
   
    def RobotButtons(self, layout):
        row = layout.rowCount()
        title = QtWidgets.QLabel("Robot")
        title.setStyleSheet(style_label_title)
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout.addWidget(title, row, 0)
        
        self.BUTTON_CONNECT_ROBOT = QPushButton("Connect robot")
        self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_menu)
        layout.addWidget(self.BUTTON_CONNECT_ROBOT, row + 1, 0)
        self.BUTTON_CONNECT_ROBOT.pressed.connect(lambda: self.connect_robot())

        self.BUTTON_CONNECT_IO = QPushButton("Connect IO robot")
        self.BUTTON_CONNECT_IO.setStyleSheet(style_button_menu)
        layout.addWidget(self.BUTTON_CONNECT_IO, row + 2, 0)
        self.BUTTON_CONNECT_IO.pressed.connect(lambda: self.connect_io())
        
        self.BUTTON_CONNECT_CAM = QPushButton("Connect camera")
        self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_menu)
        layout.addWidget(self.BUTTON_CONNECT_CAM, row + 3, 0)
        self.BUTTON_CONNECT_CAM.pressed.connect(lambda: self.connect_camera())

        button_send = QPushButton("Send to robot")
        button_send.setStyleSheet(style_button_menu)
        button_send.pressed.connect(lambda: run_script(False))
        layout.addWidget(button_send, row + 4, 0)            
        
        self.BUTTON_HOME_ROBOT = QPushButton("Home")
        self.BUTTON_HOME_ROBOT.setStyleSheet(style_button_menu)
        self.BUTTON_HOME_ROBOT.pressed.connect(lambda: run_single_line("robot.Home()"))
        layout.addWidget(self.BUTTON_HOME_ROBOT, row + 5, 0)
        
        button_stop = QPushButton("Stop")
        button_stop.setFixedHeight(40)
        button_stop.setStyleSheet(style_button_red)     
        button_stop.pressed.connect(lambda: self.stop_robot())
        
        
        layout.addWidget(button_stop, row + 7, 0)

    def stop_robot(self):
        stop_script()
        stop_robot()
        

    def connect_camera(self):
        if var.CAM_CONNECT:
            connect_cam()
        else:
            self.connect_cam_window.empty_list()
            self.connect_cam_window.show()
            self.connect_cam_window.raise_()

    def connect_robot(self):
        if var.ROBOT_CONNECT and var.ROBOT_BLUETOOTH:
            connect_robot_bt()
        elif var.ROBOT_CONNECT and not var.ROBOT_BLUETOOTH:
            connect_robot_com()
        else:
            self.connect_robot_window.empty_list()
            self.connect_robot_window.show()
            self.connect_robot_window.raise_()

    def connect_io(self):
        if var.IO_CONNECT and var.IO_BLUETOOTH:
            connect_io_bt()
        elif var.IO_CONNECT and not var.IO_BLUETOOTH:
            connect_io_com()
        else:
            self.connect_io_window.empty_list()
            self.connect_io_window.show()
            self.connect_io_window.raise_()

# disable buttons
    def ButtonConnectRobotDisable(self, state):
        if state:
            self.BUTTON_CONNECT_ROBOT.setDisabled(True)
        else:
            self.BUTTON_CONNECT_ROBOT.setEnabled(True)

    def ButtonConnectIODisable(self, state):
        if state:
            self.BUTTON_CONNECT_IO.setDisabled(True)
        else:
            self.BUTTON_CONNECT_IO.setEnabled(True)
            
    def ButtonConnectCamDisable(self, state):
        if state:
            self.BUTTON_CONNECT_CAM.setDisabled(True)
        else:
            self.BUTTON_CONNECT_CAM.setEnabled(True)
            
# change color buttons

    def ButtonConnectRobotColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_pressed)
            #self.connect_robot_window.close()
        else:
            self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_menu)

    def ButtonConnectIOColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_IO.setStyleSheet(style_button_pressed)
            #self.connect_io_window.close()
        else:
            self.BUTTON_CONNECT_IO.setStyleSheet(style_button_menu)
            
    def ButtonHomeRobotColor(self, home):
        if home:
            self.BUTTON_HOME_ROBOT.setStyleSheet(style_button_pressed)
        else:
            self.BUTTON_HOME_ROBOT.setStyleSheet(style_button_menu)
            
    def ButtonConnectCamColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_pressed)
            #self.connect_cam_window.close()
        else:
            self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_menu)
      