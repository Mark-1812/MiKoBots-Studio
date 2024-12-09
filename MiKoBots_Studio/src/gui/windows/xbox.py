from PyQt5.QtWidgets import QSpacerItem, QLabel, QSizePolicy, QPushButton, QLineEdit, QHBoxLayout, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon

from backend.core.event_manager import event_manager
from backend.file_managment import get_image_path
from gui.style import *

class XBoxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xbox")
        self.setFixedSize(1000, 450)
        self.setStyleSheet(style_widget)
        self.setStyleSheet("background-color: #E8E8E8;")
        
        image_path = get_image_path('mikobot.ico')
        self.setWindowIcon(QIcon(image_path))
        
        self.buttons_settings = []
        self.buttons = ["D-PAD up", "D-PAD Right", "D-PAD Down", "D-PAD Left"]
        self.actions_buttons = ["Jog dis 100", "Jog dis 50", "Jog dis 10", "Jog dis 1", "None"]
        
        self.joystick_settings = []
        self.joysticks = ["LSB up-down", "LSB left-right", "RSB up-down", "RSB left-right"]
        self.actions_joysticks = ["Joint 1", "Joint 2", "Joint 3", "Joint 4", "Joint 5", "Joint 6", "X", "Y", "Z", "y", "p", "r", "None"]
        
        self.init_settings = {
            'D-PAD up': ['Jog dis 1', 'Jog dis 1', 'Jog dis 1', 'Jog dis 1'], 
            'D-PAD Right': ['Jog dis 10', 'Jog dis 10', 'Jog dis 10', 'Jog dis 10'], 
            'D-PAD Down': ['Jog dis 50', 'Jog dis 50', 'Jog dis 50', 'Jog dis 50'], 
            'D-PAD Left': ['Jog dis 100', 'Jog dis 100', 'Jog dis 100', 'Jog dis 100'], 
            'LSB up-down': ['X', 'y', 'Joint 1', 'Joint 4'], 
            'LSB left-right': ['Y', 'p', 'Joint 2', 'Joint 5'], 
            'RSB up-down': ['Z', 'r', 'Joint 3', 'Joint 6'], 
            'RSB left-right': ['Joint 1', 'Joint 1', 'Joint 1', 'Joint 1']
            }
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10) 
        
        layout_menu = QVBoxLayout() 
        menu_frame = QFrame()
        menu_frame.setStyleSheet(style_frame)
        menu_frame.setLayout(layout_menu)  
        layout.addWidget(menu_frame)
        
        self.MenuGUI(layout_menu)
        
        layout_controller = QVBoxLayout() 
        controller_frame = QFrame()
        controller_frame.setStyleSheet(style_frame)
        controller_frame.setLayout(layout_controller)  
        layout.addWidget(controller_frame)       
        
        image_path = get_image_path('controller_info.png')
        pixmap = QPixmap(image_path)
        
        label = QLabel()
        label.setFixedWidth(400)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout_controller.addWidget(label)
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_get_controller_settings", self.GetControllerSettings)
        event_manager.subscribe("request_set_controller_settings", self.SetControllerSettings)

    def GetControllerSettings(self):
        self.settings = {}
        
        for i in range(len(self.buttons)):
            action = [0]*4
            for j in range(4):
                action[j] = self.buttons_settings[i][j].currentText()
                
            self.settings[self.buttons[i]] = action
        
        for i in range(len(self.joysticks)):
            action = [0]*4
            for j in range(4):
                action[j] = self.joystick_settings[i][j].currentText()
                
            self.settings[self.joysticks[i]] = action  
            
        return self.settings
     
    def SetControllerSettings(self, settings): 
        if settings is None:
            settings = self.init_settings       
        
        for i in range(len(self.buttons)):
            action = settings[self.buttons[i]]
            for j in range(4):
                self.buttons_settings[i][j].blockSignals(True)
                self.buttons_settings[i][j].setCurrentText(action[j])
                self.buttons_settings[i][j].blockSignals(False)
        
        for i in range(len(self.joysticks)):
            action = settings[self.joysticks[i]]
            for j in range(4):
                self.joystick_settings[i][j].blockSignals(True)
                self.joystick_settings[i][j].setCurrentText(action[j])    
                self.joystick_settings[i][j].blockSignals(False)   
                
                

    def MenuGUI(self, layout):
        label = QLabel("Controller settings")
        label.setStyleSheet(style_label_title)
        layout.addWidget(label)
        
        label = QLabel("the Xbox controller has 2 or 4 states depending on the amount of joints")
        label.setWordWrap(True)
        label.setStyleSheet(style_label)
        layout.addWidget(label)
        
        
        label = QLabel("Button:")
        label.setStyleSheet(style_label_bold)
        label.setFixedWidth(80)
        layout.addWidget(label)
        
        label = QLabel("LB state -1")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)
        layout.addWidget(label)
        
        label = QLabel("RB state +1")
        label.setStyleSheet(style_label)
        label.setFixedWidth(100)
        layout.addWidget(label)

        
        frame = QFrame()
        layout_button = QHBoxLayout()
        layout_button.setContentsMargins(5,0,5,5)
        frame.setLayout(layout_button)
        layout.addWidget(frame) 
    
        label = QLabel("Button:")
        label.setStyleSheet(style_label_bold)
        label.setFixedWidth(80)
        layout_button.addWidget(label)
        
        for i in range(4):
            label = QLabel(f"State {1+i}:")
            label.setStyleSheet(style_label_bold)
            label.setFixedWidth(80)
            layout_button.addWidget(label)

        for button in self.buttons:
            frame = QFrame()
            layout_button = QHBoxLayout()
            layout_button.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_button)
            layout.addWidget(frame) 
        
            label = QLabel(button)
            label.setStyleSheet(style_label)
            label.setFixedWidth(80)
            layout_button.addWidget(label)
            
            state_1 = QComboBox()
            state_1.addItems(self.actions_buttons)
            state_1.setFixedWidth(100)
            state_1.setStyleSheet(style_combo)
            layout_button.addWidget(state_1)
            
            state_2 = QComboBox()
            state_2.addItems(self.actions_buttons)
            state_2.setFixedWidth(100)
            state_2.setStyleSheet(style_combo)
            layout_button.addWidget(state_2)
            
            state_3 = QComboBox()
            state_3.addItems(self.actions_buttons)
            state_3.setFixedWidth(100)
            state_3.setStyleSheet(style_combo)
            layout_button.addWidget(state_3)
            
            state_4 = QComboBox()
            state_4.addItems(self.actions_buttons)
            state_4.setFixedWidth(100)
            state_4.setStyleSheet(style_combo)
            layout_button.addWidget(state_4)
            
            self.buttons_settings.append([state_1, state_2, state_3, state_4])
            
            
        
    
        for joystick in self.joysticks:
            frame = QFrame()
            layout_button = QHBoxLayout()
            layout_button.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_button)
            layout.addWidget(frame) 
        
            label = QLabel(joystick)
            label.setStyleSheet(style_label)
            label.setFixedWidth(80)
            layout_button.addWidget(label)
            
            state_1 = QComboBox()
            state_1.addItems(self.actions_joysticks)
            state_1.setFixedWidth(100)
            state_1.setStyleSheet(style_combo)
            layout_button.addWidget(state_1)
            
            state_2 = QComboBox()
            state_2.addItems(self.actions_joysticks)
            state_2.setFixedWidth(100)
            state_2.setStyleSheet(style_combo)
            layout_button.addWidget(state_2)
            
            state_3 = QComboBox()
            state_3.addItems(self.actions_joysticks)
            state_3.setFixedWidth(100)
            state_3.setStyleSheet(style_combo)
            layout_button.addWidget(state_3)
            
            state_4 = QComboBox()
            state_4.addItems(self.actions_joysticks)
            state_4.setFixedWidth(100)
            state_4.setStyleSheet(style_combo)
            layout_button.addWidget(state_4)
            
            self.joystick_settings.append([state_1, state_2, state_3, state_4])
            
            
                        
        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(space_widget)  
    
