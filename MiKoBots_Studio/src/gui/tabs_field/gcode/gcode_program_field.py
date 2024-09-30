from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QTabWidget, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QTextEdit, QFileDialog, QSpacerItem, QSizePolicy

from backend.core.event_manager import event_manager

from gui.style import *

class gcodeField():  
    def __init__(self, frame):
        self.layout = QGridLayout(frame)
        self.GUI()
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_gcode_text_clear", self.GcodeTextClear)
        event_manager.subscribe("request_gcode_text_insert", self.GcodeTextInsert)
        event_manager.subscribe("request_gcode_text_get", self.GcodeTextGet)
        
    def GUI(self):
        self.GCODE_TEXT_WIDGET = QTextEdit()
        self.GCODE_TEXT_WIDGET.setStyleSheet(style_textedit)
        self.layout.addWidget(self.GCODE_TEXT_WIDGET,1,0,1,2)
        
        button = QPushButton("Open")
        button.setMaximumWidth(80)
        button.setStyleSheet(style_button)
        button.clicked.connect(lambda: self.OpenGcode())
        self.layout.addWidget(button,2,0)
             
        
    def GcodeTextClear(self):
        self.GCODE_TEXT_WIDGET.clear()
        
    def GcodeTextInsert(self, text):
        self.GCODE_TEXT_WIDGET.insertPlainText(text)
        
    def GcodeTextGet(self):
        program = self.GCODE_TEXT_WIDGET.toPlainText() 
        return program
        
    def OpenGcode(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        file_path, _ = QFileDialog.getOpenFileName(None, "Open .gcode File", "", "MiKo Files (*.gcode);;All Files (*)", options=options)
        
        if file_path:
            with open(file_path, "r") as file:
                self.GCODE_TEXT_WIDGET.clear()
                for line in file:
                    self.GCODE_TEXT_WIDGET.insertPlainText(line.rstrip() + "\n")