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



class MenuField(QWidget):
    def __init__(self, frame):
        super().__init__()
        
        main_layout = QVBoxLayout(frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.simulation_origin_gui = SimulationOriginGUI()
        self.simulation_objects_gui = SimulationObjectsGUI()

        self.connect_robot_window = ConnectDevice("ROBOT")
        self.connect_io_window = ConnectDevice("IO")
        self.connect_cam_window = ConnectDevice("CAMERA")
        
        self.vision_window = VisionWindow()

        frame = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        frame.setLayout(layout)
        main_layout.addWidget(frame)
        self.FrameButtons(layout)  

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(space_widget)      

        frame = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        frame.setLayout(layout)
        main_layout.addWidget(frame) 
        self.SimButtons(layout)

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(space_widget)   

        frame = QFrame()
        layout = QGridLayout()
        layout.setSpacing(5)
        frame.setLayout(layout)
        main_layout.addWidget(frame) 
        self.RobotButtons(layout)
        
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
        
    def FrameButtons(self, layout):
        file_management = FileManagement()
        image_path = file_management.resource_path('studio.png')
        
        button = QPushButton(self)
        button.setFixedSize(125,125)
        button.setIcon(QIcon(image_path))
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.mikobots.com")))
        button.setStyleSheet(style_button)
        layout.addWidget(button)
        
        button = QPushButton("New file")
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: new_file())
        layout.addWidget(button)

        button = QPushButton("Save")
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: save_file())
        layout.addWidget(button)

        button = QPushButton("Save as")
        button.setStyleSheet(style_button_menu)
        button.pressed.connect(lambda: save_as_file())
        layout.addWidget(button)

        button = QPushButton("Open")
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
        self.RunSim.setStyleSheet(style_button_menu)
        self.RunSim.clicked.connect(lambda: run_script(True))
        layout.addWidget(self.RunSim)
        
        self.StopSim = QPushButton("Stop simulation")
        self.StopSim.setStyleSheet(style_button_menu)
        self.StopSim.clicked.connect(stop_script) 
        layout.addWidget(self.StopSim)
        
        button = QPushButton("add origin")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(self.simulation_origin_gui.show)
        layout.addWidget(button) 
        
        button = QPushButton("Show / hide")
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
        
        self.BUTTON_CONNECT_ROBOT = QPushButton("Connect robot")
        self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_menu)
        self.BUTTON_CONNECT_ROBOT.pressed.connect(lambda: self.connect_robot())
        layout.addWidget(self.BUTTON_CONNECT_ROBOT, 1, 0, 1, 2)

        self.BUTTON_CONNECT_IO = QPushButton("Connect IO robot")
        self.BUTTON_CONNECT_IO.setStyleSheet(style_button_menu)
        self.BUTTON_CONNECT_IO.pressed.connect(lambda: self.connect_io())
        layout.addWidget(self.BUTTON_CONNECT_IO, 2, 0, 1, 2)
        
        self.BUTTON_CONNECT_CAM = QPushButton("Connect camera")
        self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_menu)
        self.BUTTON_CONNECT_CAM.pressed.connect(lambda: self.connect_camera())
        layout.addWidget(self.BUTTON_CONNECT_CAM, 3, 0, 1, 2)

        button_send = QPushButton("Send to robot")
        button_send.setStyleSheet(style_button_menu)
        button_send.pressed.connect(lambda: run_script(False))
        layout.addWidget(button_send, 4, 0, 1, 2)            
        
        self.BUTTON_HOME_ROBOT = QPushButton("Home")
        self.BUTTON_HOME_ROBOT.setStyleSheet(style_button_menu)
        self.BUTTON_HOME_ROBOT.pressed.connect(lambda: run_single_line("robot.Home()"))
        layout.addWidget(self.BUTTON_HOME_ROBOT, 5, 0, 1, 2)

        button_pauze = QPushButton("pauze")
        button_pauze.setStyleSheet(style_button_menu)
        button_pauze.pressed.connect(lambda: self.pauze_robot())
        layout.addWidget(button_pauze, 6, 0, 1, 1)

        button_play = QPushButton("play")
        button_play.setStyleSheet(style_button_menu)
        button_play.pressed.connect(lambda: self.play_robot())
        layout.addWidget(button_play, 6, 1, 1, 1)
        
        button_stop = QPushButton("Stop")
        button_stop.setFixedHeight(40)
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
            print("camere connected")
            connect_cam()
        else:
            print("camera not connected")
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
            self.connect_robot_window.close()
        else:
            self.BUTTON_CONNECT_ROBOT.setStyleSheet(style_button_menu)

    def ButtonConnectIOColor(self, connect):
        if connect:
            self.BUTTON_CONNECT_IO.setStyleSheet(style_button_pressed)
            self.connect_io_window.close()
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
            self.connect_cam_window.close()
        else:
            self.BUTTON_CONNECT_CAM.setStyleSheet(style_button_menu)
      