from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

from gui.style import *

class gcodeInfo():  
    def __init__(self, frame):
        layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QVBoxLayout(scroll_widget)
             
        label = QLabel("Import the library:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setText("from robot_library import Gcode")
        entry.setStyleSheet(style_entry)        
        scroll_layout.addWidget(entry)

        spacer = QSpacerItem(5,40)
        scroll_layout.addItem(spacer) 
        
        label = QLabel("G-code functions:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        
        label = QLabel("Declare the g-code function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setText("Gcode_program = Gcode()")
        entry.setStyleSheet(style_entry)        
        scroll_layout.addWidget(entry)            
        
        
        # setOrigin
        label = QLabel("setOrigin")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Gcode_program.setOrigin(X = int, Y = int, Z = int)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)  
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("setOrigin, is used to set the zero position of the gcode<br>"
                "<b>X:</b> Position in X<br>"
                "<b>Y:</b> Position in Y<br>"
                "<b>Z:</b> Position in Z")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        # RUN
        label = QLabel("run")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit("Gcode_program.run()")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)  
        scroll_layout.addWidget(entry) 
        
        label = QLabel()
        label.setStyleSheet(style_label_bold)
        label.setText("run, will execute the gcode<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        scroll_layout.addWidget(spacer_widget)
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)