from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QHBoxLayout, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from backend.core.event_manager import event_manager

from gui.style import *

from backend.robot_management  import change_robot
from backend.robot_management.communication  import send_settings_io
from backend.robot_management.communication  import send_settings_robot
from backend.robot_management  import save_robot
from backend.robot_management  import export_robot
from backend.robot_management  import import_robot
from backend.robot_management  import delete_robot
from backend.robot_management  import create_new_robot

class RobotOverview(QWidget):   
    def __init__(self, frame):
        super().__init__()
        self.frame = frame        
        self.Robots_buttons = []
        
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_buttons", self.CreateButtons)
        event_manager.subscribe("request_delete_robot_buttons", self.DeleteButtons)
        
        event_manager.subscribe("request_set_robot_radio", self.setRobot)
        event_manager.subscribe("request_change_robot_name", self.ChangeRobotName)

    def GUI(self):
        main_layout = QGridLayout(self.frame)

        title = QLabel("Robots:")
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setStyleSheet(style_label_bold)
        main_layout.addWidget(title,0,0)

        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        scroll.setFixedHeight(300)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll, 1, 0) 
        
        ## Create a frame for the buttons
        frame = QFrame()
        layout_buttons = QVBoxLayout()
        layout_buttons.setSpacing(5)
        layout_buttons.setAlignment(Qt.AlignTop)

        frame.setMaximumWidth(250)
        main_layout.addWidget(frame, 0, 1, 2, 1)
        frame.setLayout(layout_buttons)
        
        button = QPushButton("Add new robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(create_new_robot)
        layout_buttons.addWidget(button)
        
        self.BUTTON_SAVE_ROBOT = QPushButton("Save robot")
        self.BUTTON_SAVE_ROBOT.setStyleSheet(style_button_menu)
        self.BUTTON_SAVE_ROBOT.clicked.connect(lambda: save_robot(True))
        layout_buttons.addWidget(self.BUTTON_SAVE_ROBOT)
         
        button = QPushButton("Send settings")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(self.send_settings)
        layout_buttons.addWidget(button)
        
        button = QPushButton("Delete robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(delete_robot)
        layout_buttons.addWidget(button)
        
        button = QPushButton("Import robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(import_robot)
        layout_buttons.addWidget(button)
        
        button = QPushButton("Export robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(export_robot)
        layout_buttons.addWidget(button)
 
        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(space_widget, 2, 0, 1, 2)      
        
        
    def ChangeRobotName(self, selected_robot, name):
        self.Robots_buttons[selected_robot].setText(name)
        
    def CreateButtons(self, item, robot_name):          
        radio_button = QRadioButton(robot_name)
        radio_button.setChecked(False)
        radio_button.setStyleSheet(style_radiobutton)
        radio_button.toggled.connect(lambda state, btn=radio_button: change_robot(item))
        self.layout_scroll.addWidget(radio_button)
        self.Robots_buttons.append(radio_button)


    def DeleteButtons(self):
        while self.layout_scroll.count():
            item = self.layout_scroll.takeAt(0)  # Take the first item from the layout
            widget = item.widget()   # If it's a widget, delete it
            if widget is not None:
                widget.deleteLater()  # This ensures the widget is properly deleted
            else:
                self.layout_scroll.removeItem(item)  # If it's not a widget, just remove it (e.g., a spacer item)
    
    def setRobot(self, item): 
        for i in range(len(self.Robots_buttons)):
            self.Robots_buttons[i].blockSignals(True)

        self.Robots_buttons[item].setChecked(True)

        for i in range(len(self.Robots_buttons)):
            self.Robots_buttons[i].blockSignals(False)

    def ChangeRobot(self, btn, item):
        if btn.isChecked():
            self.Robots_buttons[item].setReadOnly(True)
            change_robot(item)
            self.Robots_buttons[item].setReadOnly(False)
            
    def send_settings(self):
        send_settings_io()
        send_settings_robot()
    
    
            