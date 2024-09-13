from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QTabWidget, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QTextEdit, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt


from frontend.tabs_field.gcode.gcode_info import gcodeInfo
from frontend.tabs_field.gcode.gcode_program_field import gcodeField

class GcodeFrame():
    def __init__(self,frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        title = QLabel("G-code")
        title.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        title.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        title.setFixedHeight(20)
        frame_layout.addWidget(title, 0, 0)
        
        tabs = QTabWidget()
        frame_layout.addWidget(tabs, 1, 0)
        
        
        tabs.setStyleSheet(
                "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
                "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
                "QPushButton:hover { background-color: white; }"
                "QPushButton:pressed { background-color: darkorange; }"+
                "QCheckBox {  background-color: white; }"+
                "QLabel {font-size: 12px; font-family: Arial;}"+
                "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        tab1 = QWidget()
        tab2 = QWidget()
        
        tabs.addTab(tab1, "Info")
        tabs.addTab(tab2, "G-code")
        
        gcodeInfo(tab1)
        gcodeField(tab2)