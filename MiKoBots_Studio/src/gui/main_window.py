from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSplitter, QMessageBox, QMainWindow, QLabel, QCheckBox, QComboBox, QSizePolicy, QScrollArea, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import *
import webbrowser
import sys

from gui.fields.field_settings import SettingsField
from gui.fields.field_control import ControlField
from gui.fields.field_program import ProgramField
from gui.fields.field_log import LogField
from gui.fields.field_menu import MenuField
from gui.fields.simulation_frame import SimulationGUI
from backend.file_managment.file_management import FileManagement
from backend.core.event_manager import event_manager

from backend.robot_management import setup_robot
from backend.robot_management import close_robot
from backend.robot_management import close_io

from backend.vision import close_cam

from backend.run_program import stop_script

from backend.file_manager import open_file_from_path

import backend.core.variables as var
from gui.windows.update_window import UpdateChecker
from gui.windows.message_boxes import CloseProgramMessage

from  backend import close_program

from backend.file_manager import save_file

class MainWindow(QWidget):   
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
        self.setMinimumSize(900, 700)
        
        self.setStyleSheet("background-color: #E8E8E8;")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(self.layout)
        
        self.min_height_2 = 120
        self.min_height_3 = 110
        self.min_height_4 = 100
        self.min_height_5 = 176
        self.min_height_6 = 142   
        
        self.ControlField = None
        self.LogField = None
        self.SettingsField = None
        self.ProgramField = None
        self.SimulationGUI = None
        self.MenuField = None    
        
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

    def CreateFrames(self, layout):
        self.middle_splitter = QSplitter(Qt.Vertical)
        
        self.right_splitter = QSplitter(Qt.Vertical)
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        self.main_splitter.splitterMoved.connect(self.MainSplitterSize) 
        
        ## FRAME RIGHT
        
        ##### FRAME 4
        layout_frame_4 = QGridLayout()
        layout_frame_4.setContentsMargins(0, 0, 0, 0)
        layout_frame_4.setSpacing(0)
        
        self.frame_4 = QFrame()
        self.frame_4.setStyleSheet(style_frame)
        self.frame_4.setFrameStyle(QFrame.NoFrame)
        self.frame_4.setLayout(layout_frame_4)
        

        self.frame_4_tabs = QFrame()  
        
        self.frame_4_tabs.setMinimumWidth(200)
        self.frame_4_tabs.setFrameStyle(QFrame.NoFrame)
        layout_frame_4.addWidget(self.frame_4_tabs, 0, 0)
        
        ##### FRAME 5
        layout_frame_5 = QGridLayout()
        layout_frame_5.setContentsMargins(0, 0, 0, 0)
        layout_frame_5.setSpacing(0)
        
        self.frame_5 = QFrame()
        self.frame_5.setMaximumHeight(290)
        self.frame_5.setFrameStyle(QFrame.NoFrame)
        self.frame_5.setLayout(layout_frame_5)    
        
        # Create a QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setFrameStyle(QFrame.NoFrame)    
        self.scroll_area.setStyleSheet(style_scrollarea)

        self.frame_5_control = QFrame()
        self.frame_5_control.setFrameStyle(QFrame.NoFrame)
        
        self.scroll_area.setWidget(self.frame_5_control)
        self.scroll_area.setWidgetResizable(True)  # Allows the scroll area to resize with the frame

        layout_frame_5.addWidget(self.scroll_area, 0, 0)
        
        layout_frame_5_min = QGridLayout()           
        self.frame_5_min = QFrame()
        self.frame_5_min.setStyleSheet(style_frame)
        self.frame_5_min.setLayout(layout_frame_5_min) 
        self.frame_5_min.hide()
        
        title = QLabel("Control")
        title.setStyleSheet(style_label_title)
        layout_frame_5_min.addWidget(title, 0, 0)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(5))
        layout_frame_5_min.addWidget(button, 0, 1)
                        
        layout_frame_5.addWidget(self.frame_5_min , 0, 0)
        
        ##### FRAME 6 
        ##### Settings frame
        layout_frame_6 = QGridLayout()
        layout_frame_6.setContentsMargins(0, 0, 0, 0)
        layout_frame_6.setSpacing(0)
        
        self.frame_6 = QFrame()
        self.frame_6.setMaximumHeight(145)
        self.frame_6.setStyleSheet(style_frame)
        self.frame_6.setFrameStyle(QFrame.NoFrame)        
        self.frame_6.setLayout(layout_frame_6)        
            
        self.frame_6_settings = QFrame()
        self.frame_6_settings.setFrameStyle(QFrame.NoFrame) 
        layout_frame_6.addWidget(self.frame_6_settings, 0, 0)
         
        layout_frame_6_min = QGridLayout()           
        self.frame_6_min = QFrame()
        self.frame_6_min.setLayout(layout_frame_6_min) 
        self.frame_6_min.hide()
        
        title = QLabel("Settings")
        title.setStyleSheet(style_label_title)
        layout_frame_6_min.addWidget(title, 0, 0)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(6))
        layout_frame_6_min.addWidget(button, 0, 1)
                        
        layout_frame_6.addWidget(self.frame_6_min , 0, 0)
        
        
        
        
        
        
        ##### add frame 4 - 5 - 6 to the right splitter 
        
        layout_frame_right_min = QGridLayout()  
        self.frame_right_min = QFrame()
        self.frame_right_min.setStyleSheet(style_frame)
        self.frame_right_min.setLayout(layout_frame_right_min)   
        
        title = QLabel("Robot\n control")
        title.setStyleSheet(style_label_title)
        layout_frame_right_min.addWidget(title, 1, 0)
        
        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(1))
        layout_frame_right_min.addWidget(button, 0, 0)
        self.frame_right_min.hide()
        
        ##### Make a frame for the right splitter if it is minimized to the right
        
        self.right_splitter.addWidget(self.frame_4)        
        self.right_splitter.addWidget(self.frame_5)
        self.right_splitter.addWidget(self.frame_6)
        self.right_splitter.addWidget(self.frame_right_min)
        
        self.right_splitter.splitterMoved.connect(self.RightSplitterSize)
        

        ############
        ### FRAME MIDDLE
                 
        ##### FRAME 2
        layout_frame_2 = QGridLayout()
        layout_frame_2.setContentsMargins(0, 0, 0, 0)
        layout_frame_2.setSpacing(0)                 
                 
        self.frame_2 = QFrame()
        self.frame_2.setFrameStyle(QFrame.NoFrame)        
        self.frame_2.setLayout(layout_frame_2)  
        self.frame_2.setStyleSheet(style_frame)
        self.frame_2.setMinimumWidth(200)
        
        self.frame_2_programming = QFrame()
        self.frame_2_programming.setFrameStyle(QFrame.NoFrame) 
        layout_frame_2.addWidget(self.frame_2_programming)        
        
        layout_frame_2_min = QGridLayout()           
        self.frame_2_min = QFrame()
        self.frame_2_min.setLayout(layout_frame_2_min) 
        self.frame_2_min.hide()
        
        title = QLabel("Program field")
        title.setStyleSheet(style_label_title)
        layout_frame_2_min.addWidget(title, 0, 0)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(2))
        layout_frame_2_min.addWidget(button, 0, 1)
                        
        layout_frame_2.addWidget(self.frame_2_min , 0, 0)
           
        #### FRAME 3
        layout_frame_3 = QGridLayout()
        layout_frame_3.setContentsMargins(0, 0, 0, 0)
        layout_frame_3.setSpacing(0)                 
                 
        self.frame_3 = QFrame()
        self.frame_3.setFrameStyle(QFrame.NoFrame)   
        self.frame_3.setStyleSheet(style_frame)     
        self.frame_3.setLayout(layout_frame_3)  
        
        self.frame_3_log = QFrame()
        self.frame_3_log.setFrameStyle(QFrame.NoFrame)
        layout_frame_3.addWidget(self.frame_3_log)
        
        layout_frame_3_min = QGridLayout()           
        self.frame_3_min = QFrame()
        self.frame_3_min.setLayout(layout_frame_3_min) 
        self.frame_3_min.hide()
        
        title = QLabel("Log field")
        title.setStyleSheet(style_label_title)
        layout_frame_3_min.addWidget(title, 0, 0)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(3))
        layout_frame_3_min.addWidget(button, 0, 1)
        
        layout_frame_3.addWidget(self.frame_3_min , 0, 0)
        
        ### MIDDLE SPLITTER
        layout_frame_middle_min = QGridLayout()  
        self.frame_middle_min = QFrame()
        self.frame_middle_min.setStyleSheet(style_frame)
        self.frame_middle_min.setLayout(layout_frame_middle_min)   
        self.frame_middle_min.setMinimumWidth(200)
        
        title = QLabel("program")
        title.setStyleSheet(style_label_title)
        layout_frame_middle_min.addWidget(title, 1, 0)
        
        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(20)
        button.clicked.connect(lambda: self.SizeUp(1))
        layout_frame_middle_min.addWidget(button, 0, 0)
        self.frame_middle_min.hide()

        
        #####################
        self.middle_splitter.addWidget(self.frame_2)        
        self.middle_splitter.addWidget(self.frame_3)
        self.middle_splitter.addWidget(self.frame_middle_min)
        
        self.middle_splitter.splitterMoved.connect(self.MiddleSplitterSize)      
        self.middle_splitter.setSizes([100, 20])

        
        self.frame1 = QFrame()
        self.frame1.setStyleSheet(style_frame)
        self.frame1.setFixedWidth(150)
        self.main_splitter.addWidget(self.frame1)#, 0, 0, 4, 1)
        
        
        
        self.main_splitter.addWidget(self.middle_splitter)
        self.main_splitter.addWidget(self.right_splitter)
        
        layout.addWidget(self.main_splitter)
        
        self.main_splitter.setSizes([500, 100, 100])
        
        layout.update()
        
    def RightSplitterSize(self):
        frame_4_height = self.frame_4.height()
        frame_5_height = self.frame_5.height()
        frame_6_height = self.frame_6.height()
        
        min_height = 20
            
        if frame_5_height < self.min_height_5:
            self.frame_5_control.hide()
            self.frame_5_min.show()
            if frame_5_height < min_height:
                self.right_splitter.setSizes([frame_4_height, 20, frame_6_height])
        elif frame_5_height >= self.min_height_5:
            self.frame_5_control.show()
            self.frame_5_min.hide()
        
        if frame_6_height < self.min_height_6:
            self.frame_6_settings.hide()
            self.frame_6_min.show()
            if frame_6_height < min_height:
                self.right_splitter.setSizes([frame_4_height, frame_5_height, 20])
        elif frame_6_height >= self.min_height_6:
            self.frame_6_settings.show()
            self.frame_6_min.hide()         

    def MainSplitterSize(self):
        width_splitter_middle = self.middle_splitter.width()
        width_splitter_right = self.right_splitter.width()
        
        if width_splitter_right < 400:
            self.frame_4.hide()
            self.frame_5.hide()
            self.frame_6.hide()
            self.frame_right_min.show()
            self.main_splitter.setSizes([1500, width_splitter_middle, 100])
        else:
            self.frame_4.show()
            self.frame_5.show()
            self.frame_6.show()
            self.frame_right_min.hide()


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
            self.frame_3_log.hide()
            self.frame_3_min.show()
            if frame_3_height < min_height:
                self.middle_splitter.setSizes([frame_2_height, 20])
        elif frame_3_height >= self.min_height_3:
            self.frame_3_log.show()
            self.frame_3_min.hide()
 
    def SizeUp(self, frame):
        frame_2_height = self.frame_2.height()
        frame_3_height = self.frame_3.height()
        frame_4_height = self.frame_4.height()
        frame_5_height = self.frame_5.height()
        frame_6_height = self.frame_6.height()
        width_splitter_middle = self.middle_splitter.width()

        
        if frame == 2:
            self.middle_splitter.setSizes([self.min_height_2, frame_3_height - (self.min_height_2-38)])
            self.MiddleSplitterSize()
        if frame == 3:
            self.middle_splitter.setSizes([frame_2_height - (self.min_height_3-38), self.min_height_3])
            self.MiddleSplitterSize()
        if frame == 5:
            self.right_splitter.setSizes([frame_4_height - (self.min_height_5-38), self.min_height_5, frame_6_height])
            self.RightSplitterSize()
        if frame == 6:
            self.right_splitter.setSizes([frame_4_height - (self.min_height_6-38), frame_5_height, self.min_height_6])
            self.RightSplitterSize()
        if frame == 1:
            self.main_splitter.setSizes([1000, width_splitter_middle, 1500])
            self.MainSplitterSize()
            
    def show_main(self, startup_screen, file_path):
        startup_screen.accept()  # Close the startup screen
        self.showMaximized()  # Show the main window
        self.CreateFrames(self.layout)
        
        self.ControlField = ControlField(self.frame_5_control)
        self.LogField = LogField(self.frame_3_log)
        self.SettingsField = SettingsField(self.frame_6_settings)
        self.ProgramField = ProgramField(self.frame_2_programming)
        self.SimulationGUI = SimulationGUI(self.frame_4_tabs)
        self.MenuField = MenuField(self.frame1)
        
        event_manager.publish("request_set_jog_distance", var.SETTINGS_FILE[3])
             
        setup_robot()

        self.update_window = UpdateChecker(var.UPDATE_DESCRIPTION, var.UPDATE_VERSION, var.CURRENT_VERSION,  self.screen_geometry)  # Create an instance of UpdateChecker as a dialog
        
        if var.UPDATE:
            self.update_window.setModal(True)  # Make it modal
            self.update_window.exec_()  # Show it as a modal dialog
            
        if file_path:
            open_file_from_path(file_path)
      
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
        
        close_program.run()
        
        self.SettingsField.RobotWindow.close()

        
        

           
            
        

        