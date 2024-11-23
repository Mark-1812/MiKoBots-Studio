from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog, QButtonGroup
from PyQt5.QtCore import  Qt

from .vision_setup import VisionSetup
from .color_settings import ColorSettings

from gui.style import *

class VisionSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision settings")
        self.setFixedSize(800,750)
        self.setStyleSheet("background-color: #E8E8E8;")
        
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10) 
        
        self.CreateTabs()
        
        layout_menu = QGridLayout() 
        menu_frame = QFrame()
        menu_frame.setStyleSheet(style_frame)
        menu_frame.setFixedWidth(150)
        menu_frame.setLayout(layout_menu)  
        
        self.layout.addWidget(menu_frame,0,0)
        
        row = 0
        
        title = QLabel("Menus")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setFixedHeight(30)
        layout_menu.addWidget(title, row, 0)
                 
        button_group = QButtonGroup()     
        button_names = ["Vision setup", "Colors"]    
        
        for name in button_names:
            radio_button = QRadioButton(name)
            radio_button.toggled.connect(lambda checked, name=name: self.show_hide(name))
            radio_button.setStyleSheet(style_button_tab)  # Expands to fill the available space
            layout_menu.addWidget(radio_button, row + 1, 0)
            button_group.addButton(radio_button)
            row += 1

        button_group.buttons()[0].setChecked(True)
                 
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout_menu.addWidget(spacer_widget, layout_menu.rowCount(), 0, 1, 1) 
        
    def CreateTabs(self):
        self.show_frame_1 = 0
        self.frame_1 = QFrame()
        self.frame_1.setStyleSheet(style_frame)
        self.layout.addWidget(self.frame_1, 0, 1)
        self.RobotOverview = VisionSetup(self.frame_1)
        
        self.show_frame_2 = 0
        self.frame_2 = QFrame()
        self.frame_2.setStyleSheet(style_frame)
        self.layout.addWidget(self.frame_2, 0, 1)
        self.frame_2.hide()
        self.RobotTools = ColorSettings(self.frame_2)
        

    
    def show_hide(self, library):
        if library == "Vision setup":
            self.frame_1.show()
            self.frame_2.hide()
            
        elif library == "Colors":
            self.frame_1.hide()
            self.frame_2.show()
                        

        