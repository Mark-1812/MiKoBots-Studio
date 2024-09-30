from PyQt5.QtWidgets import QPushButton, QLabel, QFrame, QTabWidget, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QTextEdit, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt


from gui.tabs_field.gcode.gcode_info import gcodeInfo
from gui.tabs_field.gcode.gcode_program_field import gcodeField

from gui.style import *

class GcodeFrame():
    def __init__(self,frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        title = QLabel("G-code")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        title.setFixedHeight(20)
        frame_layout.addWidget(title, 0, 0)
        
        tabs = QTabWidget()
        frame_layout.addWidget(tabs, 1, 0)
        tabs.setStyleSheet(style_tabs)
        
        
        tab1 = QFrame()
        tab1.setStyleSheet(style_frame)
        tab2 = QFrame()
        tab2.setStyleSheet(style_frame)
        
        tabs.addTab(tab1, "Info")
        tabs.addTab(tab2, "G-code")
        
        gcodeInfo(tab1)
        gcodeField(tab2)