from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import  Qt

from .robot_info import RobotInfo
from .robot_settings import RobotSettings
from .robot_overview import RobotOverview
from .robot_tools import RobotTools
from .robot_3d_model import Robot3DModel

from gui.style import *

class RobotFrame():
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        
        title = QLabel("Robot")
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        title.setFixedHeight(20)
        frame_layout.addWidget(title, 0, 0)
        
        tabs = QTabWidget()
        tabs.setStyleSheet(style_tabs)
        frame_layout.addWidget(tabs, 1, 0)        

        tab1 = QFrame()
        tab2 = QFrame()
        tab3 = QFrame()
        tab4 = QFrame()
        tab5 = QFrame()
        
        tabs.addTab(tab1, "Info")
        tabs.addTab(tab2, "Robot")
        tabs.addTab(tab3, "Tools")
        tabs.addTab(tab4, "Settings")
        tabs.addTab(tab5, "3D model")
        
        RobotInfo(tab1)        
        RobotOverview(tab2)
        RobotTools(tab3) 
        RobotSettings(tab4)
        Robot3DModel(tab5)