from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QHBoxLayout, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 


from backend.core.event_manager import event_manager
 
# 
from gui.main_window.field_control.control_axis import ControlAxis  
from gui.main_window.field_control.control_joint import ControlJoint
from gui.main_window.field_control.control_io import ControlIO
from gui.main_window.field_control.control_tool import ControlTool
from gui.main_window.field_control.control_move import ControlMove


class ControlField(QWidget):   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setStyleSheet(style_widget)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(5)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) 
        scroll_area.setStyleSheet(style_scrollarea)
        

        # Create the child widget and layout
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: #E8E8E8;")
        self.scroll_layout = QHBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll_layout.setSpacing(10)
        
        self.createFrames()
        self.subscribeToEvents()

        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        self.setLayout(self.layout)

    def subscribeToEvents(self):
        event_manager.subscribe("request_change_labels_control", self.ChangeTitles)

    def createFrames(self):
        self.ControlJoint = ControlJoint()
        self.scroll_layout.addWidget(self.ControlJoint)

        self.ControlAxis = ControlAxis()
        self.scroll_layout.addWidget(self.ControlAxis) 

        self.frameMove = ControlMove()
        self.scroll_layout.addWidget(self.frameMove) 

        self.FrameTool = ControlTool()
        self.scroll_layout.addWidget(self.FrameTool) 

        self.frameIO = ControlIO()
        self.scroll_layout.addWidget(self.frameIO)


    def ChangeTitles(self, sim):
        if sim:
            self.simulation = True
            self.ControlJoint.title.setText("Jog Joint (sim)")
            self.ControlAxis.title.setText("Jog Axis (sim)")
            self.frameMove.title.setText("Move (sim)")
            self.FrameTool.title.setText("Tool (sim)")
            self.frameIO.title.setText("IO (sim)")  

            self.ControlJoint.simulation = True
            self.ControlAxis.simulation = True
            self.frameMove.simulation = True
            self.FrameTool.simulation = True
            self.frameIO.simulation = True

        else:
            self.simulation = False
            
            self.ControlJoint.title.setText("Jog Joint")
            self.ControlAxis.title.setText("Jog Axis")
            self.frameMove.title.setText("Move")
            self.FrameTool.title.setText("Tool")
            self.frameIO.title.setText("IO")  

            self.ControlJoint.simulation = False
            self.ControlAxis.simulation = False
            self.frameMove.simulation = False
            self.FrameTool.simulation = False
            self.frameIO.simulation = False       
