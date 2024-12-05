from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont, QDesktopServices
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

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

from backend.robot_management.communication import connect_robot, connect_robot_check
from backend.robot_management.communication import connect_io, connect_io_check
from backend.robot_management.communication import stop_robot, play_robot, pauze_robot

from backend.simulation import enable_simulation

from backend.run_program import run_script
from backend.run_program import stop_script
from backend.run_program import run_single_line

from backend.vision import connect_cam, cam_connected



class MenuField:
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QVBoxLayout(self.parent_frame)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.simulation_origin_gui = SimulationOriginGUI()
        self.simulation_objects_gui = SimulationObjectsGUI()
        self.connect_robot_window = ConnectDevice("ROBOT")
        self.connect_io_window = ConnectDevice("IO")
        self.connect_cam_window = ConnectDevice("CAMERA")
        self.vision_window = VisionWindow()
        self.file_management = FileManagement()

        frame = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        frame.setLayout(layout)
        self.layout.addWidget(frame)
        self.FrameButtons(layout)  

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(space_widget)      

        frame = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        frame.setLayout(layout)
        self.layout.addWidget(frame) 
        self.SimButtons(layout)

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(space_widget)   

        frame = QFrame()
        layout = QGridLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        frame.setLayout(layout)
        self.layout.addWidget(frame) 
        self.RobotButtons(layout)
        
        self.subscribeToEvents()

        self.parent_frame.setLayout(self.layout)
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_connect_button_color", self.ButtonConnectRobotColor)
        event_manager.subscribe("request_io_connect_button_color", self.ButtonConnectIOColor)
        event_manager.subscribe("request_robot_home_button_color", self.ButtonHomeRobotColor)
        event_manager.subscribe("request_cam_connect_button_color", self.ButtonConnectCamColor)
        event_manager.subscribe("request_stop_sim", self.ButtonStopSim)
        event_manager.subscribe("request_disable_robot_button", self.ButtonConnectRobotDisable)
        event_manager.subscribe("request_disable_io_button", self.ButtonConnectIODisable)
        event_manager.subscribe("request_disable_cam_button", self.ButtonConnectCamDisable)
        
    def FrameButtons(self, layout):
        image_path = self.file_management.resource_path('studio.png')
        
        button = QPushButton()
        button.setFixedSize(130,130)
        button.setIcon(QIcon(image_path))
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.mikobots.com")))
        button.setStyleSheet("border-radius: 15px;")
        button.setIconSize(button.size())
        layout.addWidget(button)
        
        button = QPushButton("New file")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: new_file())
        layout.addWidget(button)

        button = QPushButton("Save")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: save_file())
        layout.addWidget(button)

        button = QPushButton("Save as")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: save_as_file())
        layout.addWidget(button)

        button = QPushButton("Open")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: open_file())
        layout.addWidget(button)
  
   
   # simulation buttons
    def SimButtons(self, layout):
        title = QtWidgets.QLabel("Simulation")
        title.setStyleSheet(style_label_title)
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout.addWidget(title)
        
        simCheckbox = QCheckBox("Enable simulation")
        simCheckbox.setStyleSheet(style_checkbox)
        layout.addWidget(simCheckbox)
        simCheckbox.stateChanged.connect(lambda state: self.EnableSimulation(state))
        
        self.RunSim = QPushButton("Run simulation")
        self.RunSim.setFixedSize(130, 25)
        self.RunSim.setStyleSheet(style_button_menu)
        self.RunSim.clicked.connect(lambda: run_script(True))
        layout.addWidget(self.RunSim)
        
        self.StopSim = QPushButton("Stop simulation")
        self.StopSim.setFixedSize(130, 25)
        self.StopSim.setStyleSheet(style_button_menu)
        self.StopSim.clicked.connect(stop_script) 
        layout.addWidget(self.StopSim)
        
        button = QPushButton("add origin")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(self.simulation_origin_gui.show)
        layout.addWidget(button) 
        
        button = QPushButton("Show / hide")
        button.setFixedSize(130, 25)
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: self.ShowHide())
        layout.addWidget(button)  
   
    def ButtonStopSim(self):
        stop_script()   
   
    def EnableSimulation(self, state):
        enable_simulation(state)
        
    def ShowHide(self):
        self.simulation_objects_gui.openevent()
        self.simulation_objects_gui.show()   
        self.simulation_objects_gui.raise_()
        
    # Buttons that connect the robot and other
   
    def RobotButtons(self, layout):
        title = QtWidgets.QLabel("Robot")
        title.setStyleSheet(style_label_title)
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout.addWidget(title, 0, 0, 1, 2)
        
        self.button_connect_robot = QPushButton("Connect robot")
        self.button_connect_robot.setFixedSize(130, 25)
        self.button_connect_robot.setStyleSheet(style_button_menu)
        self.button_connect_robot.pressed.connect(lambda: self.connect_robot())
        layout.addWidget(self.button_connect_robot, 1, 0, 1, 2)

        self.button_connect_io = QPushButton("Connect IO robot")
        self.button_connect_io.setFixedSize(130, 25)
        self.button_connect_io.setStyleSheet(style_button_menu)
        self.button_connect_io.pressed.connect(lambda: self.connect_io())
        layout.addWidget(self.button_connect_io, 2, 0, 1, 2)
        
        self.button_connect_cam = QPushButton("Connect camera")
        self.button_connect_cam.setFixedSize(130, 25)
        self.button_connect_cam.setStyleSheet(style_button_menu)
        self.button_connect_cam.pressed.connect(lambda: self.connect_camera())
        layout.addWidget(self.button_connect_cam, 3, 0, 1, 2)

        button_send = QPushButton("Send to robot")
        button_send.setFixedSize(130, 25)
        button_send.setStyleSheet(style_button_menu)
        button_send.pressed.connect(lambda: run_script(False))
        layout.addWidget(button_send, 4, 0, 1, 2)            
        
        self.button_home_robot = QPushButton("Home")
        self.button_home_robot.setFixedSize(130, 25)
        self.button_home_robot.setStyleSheet(style_button_menu)
        self.button_home_robot.pressed.connect(lambda: run_single_line("robot.Home()"))
        layout.addWidget(self.button_home_robot, 5, 0, 1, 2)

        image_path = self.file_management.resource_path('pauze.png')
        button_pauze = QPushButton()
        button_pauze.setFixedSize(62, 25)
        button_pauze.setIcon(QIcon(image_path))
        button_pauze.setStyleSheet(style_button_menu)
        button_pauze.pressed.connect(lambda: self.pauze_robot())
        layout.addWidget(button_pauze, 6, 0, 1, 1)

        image_path = self.file_management.resource_path('play.png')
        button_play = QPushButton()
        button_play.setFixedSize(62, 25)
        button_play.setIcon(QIcon(image_path))
        button_play.setStyleSheet(style_button_menu)
        button_play.pressed.connect(lambda: self.play_robot())
        layout.addWidget(button_play, 6, 1, 1, 1)
        
        image_path = self.file_management.resource_path('stop.png')
        button_stop = QPushButton()
        button_stop.setFixedSize(130, 40)
        button_stop.setIcon(QIcon(image_path))
        button_stop.setStyleSheet(style_button_red)     
        button_stop.pressed.connect(lambda: self.stop_robot())
        layout.addWidget(button_stop, 7, 0, 1, 2)

    def stop_robot(self):
        stop_script()
        stop_robot()

    def pauze_robot(self):
        pauze_robot()

    def play_robot(self):
        play_robot()
        

    def connect_camera(self):
        if cam_connected():
            connect_cam()
        else:
            self.connect_cam_window.show()
            self.connect_cam_window.raise_()

    def connect_robot(self):
        if connect_robot_check():
            connect_robot()
        else:
            self.connect_robot_window.empty_list()
            self.connect_robot_window.show()
            self.connect_robot_window.raise_()

    def connect_io(self):
        if connect_robot_check():
            connect_robot()
        else:
            self.connect_io_window.empty_list()
            self.connect_io_window.show()
            self.connect_io_window.raise_()

# disable buttons
    def ButtonConnectRobotDisable(self, state):
        if state:
            self.button_connect_robot.setDisabled(True)
        else:
            self.button_connect_robot.setEnabled(True)

    def ButtonConnectIODisable(self, state):
        if state:
            self.button_connect_io.setDisabled(True)
        else:
            self.button_connect_io.setEnabled(True)
            
    def ButtonConnectCamDisable(self, state):
        if state:
            self.button_connect_cam.setDisabled(True)
        else:
            self.button_connect_cam.setEnabled(True)
            
# change color buttons
    def ButtonConnectRobotColor(self, connect):
        if connect:
            self.button_connect_robot.setStyleSheet(style_button_pressed)
            self.connect_robot_window.close()
        else:
            self.button_connect_robot.setStyleSheet(style_button_menu)

    def ButtonConnectIOColor(self, connect):
        if connect:
            self.button_connect_io.setStyleSheet(style_button_pressed)
            self.connect_io_window.close()
        else:
            self.button_connect_io.setStyleSheet(style_button_menu)
            
    def ButtonHomeRobotColor(self, home):
        if home:
            self.button_home_robot.setStyleSheet(style_button_pressed)
        else:
            self.button_home_robot.setStyleSheet(style_button_menu)
            
    def ButtonConnectCamColor(self, connect):
        if connect:
            self.button_connect_cam.setStyleSheet(style_button_pressed)
            self.connect_cam_window.close()
        else:
            self.button_connect_cam.setStyleSheet(style_button_menu)
      