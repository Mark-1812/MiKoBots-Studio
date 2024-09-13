from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget


from frontend.tabs_field.gcode.gcode_frame import GcodeFrame
from frontend.tabs_field.robot_tab.robot_frame import RobotFrame
from frontend.tabs_field.vision.vision_frame import VisionFrame
from frontend.tabs_field.simulation.simulation_frame import SimulationGUI

class ShowHideTab(QWidget):
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)

        
        self.CreateTabs(frame_layout)
    
    def CreateTabs(self, layout):
        ## simulation
        self.frameSimulation = QFrame()
        layout.addWidget(self.frameSimulation,0,0,layout.rowCount(),layout.columnCount())
        SimulationGUI(self.frameSimulation)
        
        # gcode
        self.show_gcode = 0
        self.frameGcode = QFrame()
        layout.addWidget(self.frameGcode,0,0,layout.rowCount(),layout.columnCount())
        self.frameGcode.hide()
        GcodeFrame(self.frameGcode)
        
        
        # Vision
        self.show_cam_setup = 0
        self.frameVision = QFrame()
        layout.addWidget(self.frameVision,0,0,layout.rowCount(),layout.columnCount())
        self.frameVision.hide()  
        VisionFrame(self.frameVision)   
        
        # robot
        self.show_robot = 0
        self.frameRobot = QFrame()       
        layout.addWidget(self.frameRobot,0,0,layout.rowCount(),layout.columnCount())
        self.frameRobot.hide()
        RobotFrame(self.frameRobot)
    
    def show_hide(self, library):
        if library == "Simulation":
            self.frameSimulation.show()
            self.frameGcode.hide()
            self.frameVision.hide()
            self.frameRobot.hide()
            print("Simulation")
            
        elif library == "Gcode":
            self.frameSimulation.hide()
            self.frameGcode.show()
            self.frameVision.hide()
            self.frameRobot.hide()    
            print("Gcode")
                        
        elif library == "Vision":
            self.frameSimulation.hide()
            self.frameGcode.hide()
            self.frameVision.show()
            self.frameRobot.hide()  
            print("Vision") 
                                
        elif library == "Robot":
            self.frameSimulation.hide()
            self.frameGcode.hide()
            self.frameVision.hide()
            self.frameRobot.show()   
            print("Robot")    
