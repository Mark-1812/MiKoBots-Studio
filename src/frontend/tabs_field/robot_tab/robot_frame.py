from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import  Qt

from .robot_info import RobotInfo
from .robot_settings import RobotSettings
from .robot_overview import RobotOverview
from .robot_tools import RobotTools
from .robot_3d_model import Robot3DModel


class RobotFrame():
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        
        title = QLabel("Robot")
        title.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        title.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        title.setFixedHeight(20)
        frame_layout.addWidget(title, 0, 0)
        
        tabs = QTabWidget()
        frame_layout.addWidget(tabs, 1, 0)
        
        tabs.setStyleSheet(
                "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
        #         "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
        #         "QPushButton:hover { background-color: white; }"
        #         "QPushButton:pressed { background-color: darkorange; }"+
        #         "QCheckBox {  background-color: white; }"+
        #         "QLabel {font-size: 12px; font-family: Arial;}"+
        #         "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()
        
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