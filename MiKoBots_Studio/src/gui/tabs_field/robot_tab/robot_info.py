from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

class RobotInfo():
    def __init__(self, frame):
        main_layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QVBoxLayout(scroll_widget)
        
        label = QLabel("Import the library:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("from robot_library import Move, Tool, IO")  
        scroll_layout.addWidget(entry)
        
        #### ROBOT MOVE FUNCTIONS
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Robot move functions:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)        
        
        label = QLabel("Declare the robot function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("Robot = Move()")       
        scroll_layout.addWidget(entry)    
         
        
        # MoveJ
        label = QLabel("MoveJ")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.MoveJ(pos = list, v = float, a = float)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("MoveJ is used to move the robot from one point to another when that movement does not have to be in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        
        # MoveL
        label = QLabel("MoveL")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.MoveL(pos = list, v = float, a = float)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("MoveL is used to move the robot from one point to another in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)    
        
        # OffsetJ
        label = QLabel("OffsetJ")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.OffsetJ(pos = list, v = float, a = float)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("OffsetJ is used to move the robot with an offset from it's position to another when that movement does not have to be in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  
        
        # OffsetL
        label = QLabel("OffsetL")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.OffsetL(pos = list, v = float, a = float)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("OffsetL is used to move the robot with an offset from it's position to another in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label) 
        
        #### ROBOT TOOL FUNCTIONS
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Robot tool functions:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
                       
        label = QLabel("Declare the tool function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("Tool_name = Tool('tool')")    
        scroll_layout.addWidget(entry)
        
        label = QLabel("<b>tool:</b> fill here in the tool what you are using")
        label.setStyleSheet(style_label)
        scroll_layout.addWidget(label)
        
        # moveTO is only for 
        label = QLabel("moveTo")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Tool_name.moveTo(pos = int)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("moveTo is used for tools where the servo option is selected, to move the tool to a certain value.<br>"
                "<b>pos:</b> tool position")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         

        # state is only for 
        label = QLabel("state")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Tool_name.state(state = boolean)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("state is used for tools where the relay option is selected, to turn the tool OFF or ON.<br>"
                "<b>state:</b> tool state True or False")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)   
        
        #### ROBOT IO FUNCTIONS
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Robot IO functions:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
                       
        label = QLabel("Declare the IO function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("Input_output = IO(number = int, type = string)")       
        scroll_layout.addWidget(entry)        
        
        label = QLabel("<b>number:</b> number of the IO port")
        label.setStyleSheet(style_label)
        scroll_layout.addWidget(label)
        
        label = QLabel("<b>type:</b> what type INPUT or OUTPUT ")
        label.setStyleSheet(style_label)
        scroll_layout.addWidget(label)
        
        # digitalRead
        label = QLabel("digitalRead")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Input_output.digitalRead()")  
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("digitalRead will return a True of False")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)        


        # digitalWrite
        label = QLabel("digitalWrite")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Input_output.digitalWrite(state = boolean)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("digitalWrite will set the IO pin to HIGH or LOW.<br>"
                "<b>state:</b> 'HIGH' or 'LOW'")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
                
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)