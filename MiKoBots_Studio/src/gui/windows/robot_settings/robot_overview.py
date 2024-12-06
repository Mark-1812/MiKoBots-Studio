from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from backend.core.event_manager import event_manager

from gui.style import *

from backend.robot_management.robot_settings  import save_robot, export_robot, import_robot, delete_robot, create_new_robot, change_robot_settings


class RobotOverview(QFrame):   
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self)   
        self.Robots_buttons = []
        
        self.CreateRobotField()
        self.CreateButtonsField()

        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_buttons", self.CreateButtons)
        event_manager.subscribe("request_delete_robot_buttons", self.DeleteButtons)
        
        event_manager.subscribe("request_set_robot_radio", self.setRobot)
        event_manager.subscribe("request_change_robot_name", self.ChangeRobotName)

    def CreateRobotField(self):
        title = QLabel("Robots:")
        title.setStyleSheet(style_label_title)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title,0,0)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setWidgetResizable(True)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(self.scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area,1,0)  

    def CreateButtonsField(self):
        ## Create a frame for the buttons
        layout_buttons = QVBoxLayout()
        layout_buttons.setSpacing(5)
        layout_buttons.setAlignment(Qt.AlignTop)
    
        frame = QWidget()
        frame.setContentsMargins(0, 0, 0, 0) 
        frame.setFixedWidth(150)
        frame.setStyleSheet(style_widget)
        frame.setLayout(layout_buttons)
        
        button = QPushButton("Add new robot")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(create_new_robot)
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
        layout_buttons.addItem(space_widget) 

        self.layout.addWidget(frame, 0, 1, 2, 1)    

        
    def ChangeRobotName(self, selected_robot, name):
        self.Robots_buttons[selected_robot].setText(name)
        
    def CreateButtons(self, item, robot_name):      
        radio_button = QRadioButton(robot_name, self.scroll_widget)
        radio_button.setChecked(False)
        radio_button.setStyleSheet(style_radiobutton)
        radio_button.toggled.connect(lambda state, btn=radio_button: self.ChangeRobot(btn, item))
        self.layout_scroll.addWidget(radio_button)
        self.Robots_buttons.append(radio_button)

    def DeleteButtons(self):
        for button in self.Robots_buttons:
            self.layout_scroll.removeWidget(button)
            button.setParent(None)
            button.deleteLater()
            button = None

        self.Robots_buttons = []
    
    def setRobot(self, item): 
        self.Robots_buttons[item].setChecked(True)

    def ChangeRobot(self, btn, item):
        if btn.isChecked():
            change_robot_settings(item)