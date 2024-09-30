from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import tkinter.messagebox

from frontend.fields.field_settings import SettingsField
from frontend.fields.field_control import ControlField
from frontend.fields.field_program import ProgramField
from frontend.fields.field_log import LogField
from frontend.fields.field_menu import MenuField
from frontend.tabs_field.show_hide_tab import ShowHideTab

from backend.core.event_manager import event_manager

from backend.core.api import close_program
from backend.core.api import save_file

class MainWindow(QWidget):   
    def __init__(self):        
        super().__init__()
        width_window = 1200 
        height_window = 855
        
           
        self.setWindowTitle("MiKoBots Studio 0.1")
        self.setWindowIcon(QIcon('mikobot.ico'))
        self.setGeometry(100, 100, width_window, height_window)
        self.setMinimumSize(1340, 700)
        
        self.setStyleSheet(
            "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
            "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
            "QPushButton:hover { background-color: white; }"
            "QPushButton:pressed { background-color: darkorange; }"+
            "QLabel {font-size: 12px; font-family: Arial;}"+
            "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
            )

        layout = QGridLayout()
        self.setLayout(layout)
        self.CreateFrames(layout)

    def CreateFrames(self, layout):
        frame_programming_buttons = QFrame()
        frame_programming_buttons.setFixedWidth(150)
        layout.addWidget(frame_programming_buttons, 0, 0, 4, 1)

        frame_tabs = QFrame()  
        frame_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(frame_tabs, 0, 2, 1, 1) 

        frame_control_field = QFrame()
        frame_control_field.setMaximumHeight(230)
        frame_control_field.setMaximumWidth(1050)
        frame_control_field.setMinimumWidth(900)
        layout.addWidget(frame_control_field, 1, 2, 2, 1)

        frame_settings = QFrame()
        frame_settings.setFixedHeight(100)
        frame_settings.setMaximumWidth(1500)
        layout.addWidget(frame_settings, 3, 2, 1, 1) 
                    
        frame_programming = QFrame()
        frame_programming.setMaximumWidth(700)
        layout.addWidget(frame_programming, 0, 1, 2, 1)

        frame_log = QFrame()
        frame_log.setMaximumWidth(700)
        frame_log.setMaximumHeight(250)
        layout.addWidget(frame_log, 2, 1, 2, 1)
        
        self.ShowHideTab = ShowHideTab(frame_tabs)
        
        ControlField(frame_control_field)
        
        LogField(frame_log)
        
        SettingsField(frame_settings)
        ProgramField(frame_programming)
        
        MenuField(frame_programming_buttons, self.ShowHideTab)
        
        
        
        layout.update()
      
    def closeEvent(self, event):
        save = tkinter.messagebox.askquestion("Save","Do you want to save the document?")
        if save == "yes":
            save_file()
            
            
        close_program()
            
        
           
            
        

        