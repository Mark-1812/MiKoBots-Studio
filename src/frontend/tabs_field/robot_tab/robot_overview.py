from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from backend.core.event_manager import event_manager

from backend.core.api import change_robot
from backend.core.api import send_settings_io
from backend.core.api import send_settings_robot
from backend.core.api import save_robot
from backend.core.api import export_robot
from backend.core.api import import_robot
from backend.core.api import delete_robot
from backend.core.api import create_new_robot

class RobotOverview(QWidget):   
    def __init__(self, frame):
        super().__init__()
        self.frame = frame        
        self.Robots_buttons = []
        
        self.SetupUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_robot_buttons", self.CreateButtons)
        event_manager.subscribe("request_delete_robot_buttons", self.DeleteButtons)
        
        event_manager.subscribe("request_set_robot", self.setRobot)
        event_manager.subscribe("request_save_robot_button", self.ButtonSaveRobot)
        event_manager.subscribe("request_get_robot_name", self.GetRobotName)


    def SetupUI(self):
        main_layout = QVBoxLayout(self.frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(
                #"QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
                "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
                "QPushButton:hover { background-color: white; }"
                "QPushButton:pressed { background-color: darkorange; }"+
                "QCheckBox {  background-color: white; }"+
                "QLabel {font-size: 12px; font-family: Arial;}"+
                "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QLineEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        self.layout_robots = QGridLayout(scroll_widget)
        
        
        title = QLabel("Robots:")
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        self.layout_robots.addWidget(title,0,0)
        
        scroll_area2 = QScrollArea()
        scroll_area2.setWidgetResizable(True)
        scroll_area2.setFixedWidth(350)
        self.layout = QGridLayout(scroll_area2)
        
        self.layout_robots.addWidget(scroll_area2,1,0,7,1) 
        
        button = QPushButton("Add new robot")
        button.setFixedSize(100,25)
        button.clicked.connect(create_new_robot)
        self.layout_robots.addWidget(button, 0,1)
        
        self.BUTTON_SAVE_ROBOT = QPushButton("Save robot")
        self.BUTTON_SAVE_ROBOT.setFixedSize(100,25)
        self.BUTTON_SAVE_ROBOT.clicked.connect(lambda: save_robot(True))
        self.layout_robots.addWidget(self.BUTTON_SAVE_ROBOT, 1,1)
        
        button = QPushButton("Send settings")
        button.setFixedSize(100,25)
        button.clicked.connect(self.send_settings)
        self.layout_robots.addWidget(button, 2,1)
        
        button = QPushButton("Delete robot")
        button.setFixedSize(100,25)
        button.clicked.connect(delete_robot)
        self.layout_robots.addWidget(button, 3,1)
        
        button = QPushButton("Import robot")
        button.setFixedSize(100,25)
        button.clicked.connect(import_robot)
        self.layout_robots.addWidget(button, 4,1)
        
        button = QPushButton("Export robot")
        button.setFixedSize(100,25)
        button.clicked.connect(export_robot)
        self.layout_robots.addWidget(button, 5,1)
        
        spacer_widget = QWidget()
        self.layout_robots.addWidget(spacer_widget, 6, 1)
        
        spacer_widget = QWidget()
        self.layout_robots.addWidget(spacer_widget, self.layout_robots.rowCount(), 2)
                
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)        

    def ButtonSaveRobot(self):
        self.BUTTON_SAVE_ROBOT.click()
        
    def GetRobotName(self, selected_robot):
        name = self.Robots_buttons[selected_robot][1].text()
        return name
        
    def CreateButtons(self, item, robot_name):          
        self.Robots_buttons.append([[],[]])
               
        radio_button = QRadioButton()
        radio_button.setChecked(False)
        radio_button.toggled.connect(lambda state, btn=radio_button: change_robot(btn, item))
        self.layout.addWidget(radio_button, item, 0)
        self.Robots_buttons[item][0] = radio_button
        
        #self.send_signal_change_robot.connect(self.controller.ChangeRobot)
            
        entry = QLineEdit(robot_name)
        entry.setMinimumWidth(60)
        entry.setReadOnly(True)
        self.layout.addWidget(entry, item, 1)
        self.Robots_buttons[item][1] = entry
            
        spacer_widget = QWidget()
        self.layout.addWidget(spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())
        
    def DeleteButtons(self):
        for i in range(len(self.Robots_buttons)):
            for j in range(2):
                self.Robots_buttons[i][j].setParent(None)
                self.Robots_buttons[i][j].deleteLater()
        
        self.Robots_buttons = []        
   
    def setRobot(self, item): 
        self.Robots_buttons[item][0].setChecked(True)

    def ChangeRobot(self, btn, item):
        if btn.isChecked():
            change_robot(item)

    def send_settings(self):
        send_settings_io
        send_settings_robot
    
    
            