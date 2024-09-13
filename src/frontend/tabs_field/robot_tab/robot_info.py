from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

class RobotInfo():
    def __init__(self, frame):
        main_layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(
                "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
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
        scroll_layout = QVBoxLayout(scroll_widget)
        
        label = QLabel("Import the library:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("from robot.commands import Move, Tool, IO")  
        scroll_layout.addWidget(entry)
        
        #### ROBOT MOVE FUNCTIONS
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Robot move functions:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)        
        
        label = QLabel("Declare the robot function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("Robot = Move()")       
        scroll_layout.addWidget(entry)    
         
        
        # MoveJ
        label = QLabel("<b>MoveJ</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.MoveJ(pos = list, v = float, a = float)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("MoveJ is used to move the robot from one point to another when that movement does not have to be in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        
        # MoveL
        label = QLabel("<b>MoveL</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.MoveL(pos = list, v = float, a = float)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("MoveL is used to move the robot from one point to another in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)    
        
        # OffsetJ
        label_OffsetJ = QLabel("<b>OffsetJ</b>")
        scroll_layout.addWidget(label_OffsetJ)
        
        entry = QLineEdit("robot.OffsetJ(pos = list, v = float, a = float)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("OffsetJ is used to move the robot with an offset from it's position to another when that movement does not have to be in a straight line.<br>"
                "<b>Pos:</b> joint positions<br>"
                "<b>v:</b> joint speed<br>"
                "<b>a:</b> joint acceleration")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  
        
        # OffsetL
        label = QLabel("<b>OffsetL</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("robot.OffsetL(pos = list, v = float, a = float)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
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
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
                       
        label = QLabel("Declare the tool function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("Tool_name = Tool('tool')")    
        scroll_layout.addWidget(entry)
        
        label = QLabel("<b>tool:</b> fill here in the tool what you are using")
        scroll_layout.addWidget(label)
        
        # moveTO is only for 
        label = QLabel("<b>moveTo</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Tool_name.moveTo(pos = int)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("moveTo is used for tools where the servo option is selected, to move the tool to a certain value.<br>"
                "<b>pos:</b> tool position")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         

        # state is only for 
        label = QLabel("<b>state</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Tool_name.state(state = boolean)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("state is used for tools where the relay option is selected, to turn the tool OFF or ON.<br>"
                "<b>state:</b> tool state True or False")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)   
        
        #### ROBOT IO FUNCTIONS
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Robot IO functions:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
                       
        label = QLabel("Declare the IO function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("Input_output = IO(number = int, type = string)")       
        scroll_layout.addWidget(entry)        
        
        label = QLabel("<b>number:</b> number of the IO port")
        scroll_layout.addWidget(label)
        label = QLabel("<b>type:</b> what type INPUT or OUTPUT ")
        scroll_layout.addWidget(label)
        
        # digitalRead
        label = QLabel("<b>digitalRead</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Input_output.digitalRead()")  
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("digitalRead will return a True of False")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)        


        # digitalWrite
        label = QLabel("<b>digitalWrite</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Input_output.digitalWrite(state = boolean)")
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("digitalWrite will set the IO pin to HIGH or LOW.<br>"
                "<b>state:</b> 'HIGH' or 'LOW'")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
                
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)