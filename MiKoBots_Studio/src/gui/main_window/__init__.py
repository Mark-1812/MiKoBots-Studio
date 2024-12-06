from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSplitter, QHBoxLayout, QMainWindow, QLabel, QCheckBox, QComboBox, QSizePolicy, QScrollArea, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import *
import webbrowser
import sys
from backend.robot_management import setup_robot
from gui.main_window.field_settings import SettingsField
from gui.main_window.field_control import ControlField
from gui.main_window.field_program import ProgramField
from gui.main_window.field_log import LogField
from gui.main_window.field_menu import MenuField
from gui.main_window.simulation_frame import SimulationGUI
from backend.file_managment.file_management import FileManagement
from backend.core.event_manager import event_manager

from  backend.open_program import open_setting
from backend.robot_management.communication import close_robot, close_io

from backend.vision import close_cam
from backend.xbox import close_xbox

from backend.run_program import stop_script

from backend.file_manager import open_file_from_path

import backend.core.variables as var
from gui.windows.update_window import UpdateChecker
from gui.windows.message_boxes import CloseProgramMessage

from  backend import close_program

from backend.file_manager import save_file

class MainWindow(QMainWindow):   
    def __init__(self,  screen_geometry):  
        super().__init__()
        
        file_management = FileManagement()
        image_path = file_management.resource_path('mikobot.ico')
        
        width_window = 1200 
        height_window = 855
        
        self.screen_geometry = screen_geometry
           
        self.setWindowTitle("MiKoBots Studio")
        self.setWindowIcon(QIcon(image_path))
        self.setGeometry(100, 100, width_window, height_window)
        self.move_to_center(screen_geometry)
        self.setMinimumSize(900, 750)
        
        self.setStyleSheet("background-color: #E8E8E8;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        
        self.min_height_2 = 120
        self.min_height_3 = 110
        self.min_height_4 = 100
        self.min_height_5 = 176
        self.min_height_6 = 142   

        

        central_widget.setLayout(self.layout)

    def ShowMainWindow(self, file_path = None):
        self.show()
        self.CreateFrames()
        open_setting()
        setup_robot()
        
        import robot_library
        
        self.activateWindow()

        if file_path:
            open_file_from_path(file_path)
        
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.show_help()
            
    def show_help(self):
        # Open a help page (you can use a local file or a web page)
        help_url = "https://mikobots.com/help-mikobots-studio/"
        webbrowser.open(help_url)        
                    
    def move_to_center(self, screen_geometry):
        """Centers the main window on the primary screen."""
        # Center the main window on the primary screen
        frame_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())       

    def CreateFrames(self):
        self.MenuField = MenuField(self)
        self.layout.addWidget(self.MenuField)

        self.main_splitter = QSplitter(Qt.Horizontal)
        #self.main_splitter.splitterMoved.connect(self.MainSplitterSize) 
        
        self.middle_splitter = QSplitter(Qt.Vertical, self.main_splitter)
        self.middle_splitter.splitterMoved.connect(self.MiddleSplitterSize)      
        self.middle_splitter.setSizes([200, 100])
        self.GuiMiddleSplitter()
        
        self.right_splitter = QSplitter(Qt.Vertical, self.main_splitter)
        self.right_splitter.splitterMoved.connect(self.RightSplitterSize)
        self.GuiRightSplitter()

        self.main_splitter.addWidget(self.middle_splitter)  
        self.main_splitter.addWidget(self.right_splitter)
        
        self.layout.addWidget(self.main_splitter)

        self.main_splitter.setSizes([400, 400])  

    def GuiRightSplitter(self):
        ##### FRAME 4
        self.frame_4 = QWidget(self.right_splitter)
        self.frame_4.setStyleSheet(style_widget)

        layout_frame_4 = QGridLayout()
        layout_frame_4.setContentsMargins(0, 0, 0, 0)
        layout_frame_4.setSpacing(0)
        
        self.SimulationGUI = SimulationGUI(self.frame_4)
        layout_frame_4.addWidget(self.SimulationGUI, 0, 0)
        self.frame_4.setLayout(layout_frame_4)
        
        ##### FRAME 5
        self.frame_5 = QWidget(self.right_splitter)
        self.frame_5.setStyleSheet(style_widget)
        self.frame_5.setMaximumHeight(290)
        
        layout_frame_5 = QGridLayout()
        layout_frame_5.setContentsMargins(0, 0, 0, 0)
        layout_frame_5.setSpacing(0)
        
        self.ControlField = ControlField(self.frame_5)
        layout_frame_5.addWidget(self.ControlField, 0, 0)
        self.frame_5.setLayout(layout_frame_5)  

        self.frame_5_min = self.MinimizeFrame(layout_frame_5, "Control")
        
        ##### FRAME 6 
        self.frame_6 = QWidget(self.right_splitter)
        self.frame_6.setStyleSheet(style_widget)
        self.frame_6.setMaximumHeight(145)

        layout_frame_6 = QGridLayout()
        layout_frame_6.setContentsMargins(0, 0, 0, 0)
        layout_frame_6.setSpacing(0)
        
        self.SettingsField = SettingsField(self.frame_6)
        layout_frame_6.addWidget(self.SettingsField, 0, 0)
        self.frame_6.setLayout(layout_frame_6)        
            
        self.frame_6_min = self.MinimizeFrame(layout_frame_6, "Settings")

        self.right_splitter.addWidget(self.frame_4)        
        self.right_splitter.addWidget(self.frame_5)
        self.right_splitter.addWidget(self.frame_6)
             
    def GuiMiddleSplitter(self):
        ##### FRAME 2
        self.frame_2 = QWidget(self.middle_splitter)  
        self.frame_2.setStyleSheet(style_widget)
        self.frame_2.setMinimumWidth(200)

        layout_frame_2 = QGridLayout()
        layout_frame_2.setContentsMargins(0, 0, 0, 0)
        layout_frame_2.setSpacing(0)                 
        

        self.frame_2_programming = ProgramField(self.frame_2)
        layout_frame_2.addWidget(self.frame_2_programming)   
        self.frame_2.setLayout(layout_frame_2)       
              
        self.frame_2_min = self.MinimizeFrame(layout_frame_2, "Program")
           
        #### FRAME 3
        self.frame_3 = QWidget(self.middle_splitter)  
        self.frame_3.setStyleSheet(style_widget)

        layout_frame_3 = QGridLayout()
        layout_frame_3.setContentsMargins(0, 0, 0, 0)
        layout_frame_3.setSpacing(0)                 
                 
        self.frame_3_LogField = LogField(self.frame_3)
        layout_frame_3.addWidget(self.frame_3_LogField)
        self.frame_3.setLayout(layout_frame_3)  
            
        self.frame_3_min = self.MinimizeFrame(layout_frame_3, "Log")
        
        
        self.middle_splitter.addWidget(self.frame_2)        
        self.middle_splitter.addWidget(self.frame_3)

    def MinimizeFrame(self, layout, name):
        layout_min = QGridLayout()           
        frame = QFrame()
        frame.setLayout(layout_min) 
        frame.hide()
        
        title = QLabel(name)
        title.setStyleSheet(style_label_title)
        layout_min.addWidget(title, 0, 0)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(name))
        layout_min.addWidget(button, 0, 1)
                        
        layout.addWidget(frame , 0, 0)

        return frame

    # def MainSplitterSize(self):
    #     width_splitter_middle = self.middle_splitter.width()
    #     width_splitter_right = self.right_splitter.width()
        
    #     if width_splitter_right < 400:
    #         self.frame_4.hide()
    #         self.frame_5.hide()
    #         self.frame_6.hide()
    #         self.main_splitter.setSizes([1500, width_splitter_middle, 100])
    #     else:
    #         self.frame_4.show()
    #         self.frame_5.show()
    #         self.frame_6.show()
       
    def RightSplitterSize(self):
        frame_4_height = self.frame_4.height()
        frame_5_height = self.frame_5.height()
        frame_6_height = self.frame_6.height()
        
        min_height = 20
            
        if frame_5_height < self.min_height_5:
            self.ControlField.hide()
            self.frame_5_min.show()
            if frame_5_height < min_height:
                self.right_splitter.setSizes([frame_4_height, 20, frame_6_height])
        elif frame_5_height >= self.min_height_5:
            self.ControlField.show()
            self.frame_5_min.hide()
        
        if frame_6_height < self.min_height_6:
            self.SettingsField.hide()
            self.frame_6_min.show()
            if frame_6_height < min_height:
                self.right_splitter.setSizes([frame_4_height, frame_5_height, 20])
        elif frame_6_height >= self.min_height_6:
            self.SettingsField.show()
            self.frame_6_min.hide()         

    def MiddleSplitterSize(self):
        frame_2_height = self.frame_2.height()
        frame_3_height = self.frame_3.height()
        
        #print(f"frame 2 height {frame_2_height}")
        #print(f"frame 3 height {frame_3_height}")
        
        min_height = 20

        if frame_2_height < self.min_height_2:
            self.frame_2_programming.hide()
            self.frame_2_min.show()
            if frame_2_height < min_height:
                self.middle_splitter.setSizes([20, frame_3_height])
        elif frame_2_height >= self.min_height_2:
            self.frame_2_programming.show()
            self.frame_2_min.hide()
            
        if frame_3_height < self.min_height_3:
            self.frame_3_LogField.hide()
            self.frame_3_min.show()
            if frame_3_height < min_height:
                self.middle_splitter.setSizes([frame_2_height, 20])
        elif frame_3_height >= self.min_height_3:
            self.frame_3_LogField.show()
            self.frame_3_min.hide()
 
    def SizeUp(self, frame):
        frame_2_height = self.frame_2.height()
        frame_3_height = self.frame_3.height()
        frame_4_height = self.frame_4.height()
        frame_5_height = self.frame_5.height()
        frame_6_height = self.frame_6.height()
        width_splitter_middle = self.middle_splitter.width()

        
        if frame == "Program":
            self.middle_splitter.setSizes([self.min_height_2, frame_3_height - (self.min_height_2-38)])
            self.MiddleSplitterSize()
        if frame == "Log":
            self.middle_splitter.setSizes([frame_2_height - (self.min_height_3-38), self.min_height_3])
            self.MiddleSplitterSize()
        if frame == "Control":
            self.right_splitter.setSizes([frame_4_height - (self.min_height_5-38), self.min_height_5, frame_6_height])
            self.RightSplitterSize()
        if frame == "Settings":
            self.right_splitter.setSizes([frame_4_height - (self.min_height_6-38), frame_5_height, self.min_height_6])
            self.RightSplitterSize()
        if frame == 1:
            self.main_splitter.setSizes([1000, width_splitter_middle, 1500])
            self.MainSplitterSize()

      
    def closeEvent(self, event):  
        answer = CloseProgramMessage(var.LANGUAGE_DATA.get("title_save") , var.LANGUAGE_DATA.get("message_ask_save_program"))
        
        if answer == 1:
            save_file()
            event.accept()
        elif answer == 0:
            event.accept() 
        elif answer -1:
            event.ignore()
            return
            
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
        
        close_robot()
        close_io()
        self.SimulationGUI.ClosePlotter()
        close_cam()
        stop_script()
        close_xbox()
        
        close_program.run()
        
        self.SettingsField.RobotWindow.close()

        
        

           
            
        

        