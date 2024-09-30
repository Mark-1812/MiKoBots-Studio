from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt


class gcodeInfo():  
    def __init__(self, frame):
        layout = QVBoxLayout(frame)
        
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
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
             
        label = QLabel("Import the library:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("from g_code.functions import GcodeFunctions")
        entry.setStyleSheet("background-color: white")        
        scroll_layout.addWidget(entry)

        spacer = QSpacerItem(5,40)
        scroll_layout.addItem(spacer) 
        
        label = QLabel("G-code functions:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        

        
        label = QLabel("Declare the g-code function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("Gcode_program = GcodeFunctions()")
        entry.setStyleSheet("background-color: white")        
        scroll_layout.addWidget(entry)            
        
        
        # setOrigin
        label = QLabel("<b>setOrigin</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Gcode_program.setOrigin(X = int, Y = int, Z = int)")
        entry.setStyleSheet("background-color: white")  
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("setOrigin, is used to set the zero position of the gcode<br>"
                "<b>X:</b> Position in X<br>"
                "<b>Y:</b> Position in Y<br>"
                "<b>Z:</b> Position in Z")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        # RUN
        label = QLabel("<b>run</b>")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Gcode_program.run()")
        entry.setStyleSheet("background-color: white")  
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setText("run, will execute the gcode<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        spacer_widget = QWidget()
        scroll_layout.addWidget(spacer_widget)
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)