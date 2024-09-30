from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSplitter, QMessageBox, QMainWindow, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import *
import webbrowser

from gui.fields.field_settings import SettingsField
from gui.fields.field_control import ControlField
from gui.fields.field_program import ProgramField
from gui.fields.field_log import LogField
from gui.fields.field_menu import MenuField
from gui.tabs_field.show_hide_tab import ShowHideTab
from backend.file_managment.file_management import FileManagement
from backend.core.event_manager import event_manager

from backend.core.api import close_program
from backend.core.api import save_file
from backend.core.api import open_settings

import backend.core.variables as var
from gui.update_window import UpdateChecker

from gui.save_window import AskSave

class MainWindow(QWidget):   
    def __init__(self,  screen_geometry):  
        file_management = FileManagement()
        image_path = file_management.resource_path('mikobot.ico')
              
        super().__init__()
        width_window = 1200 
        height_window = 855
        
        self.screen_geometry = screen_geometry
           
        self.setWindowTitle("MiKoBots Studio")
        self.setWindowIcon(QIcon(image_path))
        self.setGeometry(100, 100, width_window, height_window)
        self.move_to_center(screen_geometry)
        self.setMinimumSize(1340, 700)
        
        self.setStyleSheet("background-color: #E8E8E8;")

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.min_height_2 = 120
        self.min_height_3 = 110
        self.min_height_4 = 100
        self.min_height_5 = 176
        self.min_height_6 = 142        
        
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
        main_splitter = QSplitter(Qt.Horizontal)
        
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
        self.frame_5.setMaximumHeight(280)
        self.frame_5.setFrameStyle(QFrame.NoFrame)
        self.frame_5.setLayout(layout_frame_5)        

        self.frame_5_control = QFrame()
        self.frame_5_control.setFrameStyle(QFrame.NoFrame)
        layout_frame_5.addWidget(self.frame_5_control, 0, 0)
        
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
        
        self.right_splitter.addWidget(self.frame_4)        
        self.right_splitter.addWidget(self.frame_5)
        self.right_splitter.addWidget(self.frame_6)
        
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
        
        self.middle_splitter.addWidget(self.frame_2)        
        self.middle_splitter.addWidget(self.frame_3)
        
        self.middle_splitter.splitterMoved.connect(self.MiddleSplitterSize)      
        self.middle_splitter.setSizes([100, 20])

        
        self.frame1 = QFrame()
        self.frame1.setStyleSheet(style_frame)
        self.frame1.setFixedWidth(150)
        main_splitter.addWidget(self.frame1)#, 0, 0, 4, 1)
        
        
        
        main_splitter.addWidget(self.middle_splitter)
        main_splitter.addWidget(self.right_splitter)
        
        ControlField(self.frame_5_control)
        LogField(self.frame_3_log)
        SettingsField(self.frame_6_settings)
        ProgramField(self.frame_2_programming)
        self.ShowHideTab = ShowHideTab(self.frame_4_tabs)
        MenuField(self.frame1, self.ShowHideTab)
        
        layout.addWidget(main_splitter)
        layout.update()
        
    def RightSplitterSize(self):
        frame_4_height = self.frame_4.height()
        frame_5_height = self.frame_5.height()
        frame_6_height = self.frame_6.height()
        
        #print(f"frame 4 height {frame_4_height}")
        #print(f"frame 5 height {frame_5_height}")
        #print(f"frame 6 height {frame_6_height}")
        
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
            
    def show_main(self, startup_screen):
        startup_screen.accept()  # Close the startup screen
        self.showMaximized()  # Show the main window
        self.CreateFrames(self.layout)
        
        settings_file = open_settings()
        event_manager.publish("request_set_robot_port", settings_file[0])
        event_manager.publish("request_set_io_port", settings_file[1])
        event_manager.publish("request_set_cam_port", settings_file[2])
        event_manager.publish("request_set_jog_distance", settings_file[3])
             
        event_manager.publish("setup_robot")

        self.update_window = UpdateChecker(var.UPDATE_DESCRIPTION, var.UPDATE_VERSION, var.CURRENT_VERSION,  self.screen_geometry)  # Create an instance of UpdateChecker as a dialog
        
        if var.UPDATE:
            print("show update screen")
            self.update_window.setModal(True)  # Make it modal
            self.update_window.exec_()  # Show it as a modal dialog
      
    def closeEvent(self, event):  
        msg_box = QMessageBox()
        msg_box.setText("Do you want to save the program?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        msg_box.setStyleSheet(style_messagebox)

        # Execute and get the result
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            print("Program closed with saving")
            save_file()
            close_program()
            event.accept()
        elif reply == QMessageBox.No:
            print("Program closed without saving")
            close_program()
            event.accept()
        elif reply == QMessageBox.Cancel:
            event.ignore()
        

           
            
        

        