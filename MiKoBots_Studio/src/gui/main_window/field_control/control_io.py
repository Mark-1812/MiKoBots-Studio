from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

from backend.core.event_manager import event_manager


class ControlIO:
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)
        self.layout.setContentsMargins(5, 3, 5, 3)

        self.simulation = False

        self.FrameIo()
        self.subscribeToEvents()

        self.parent_frame.setLayout(self.layout)
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_check_io_state", self.CheckIOState)
        event_manager.subscribe("request_set_io_state", self.SetIoStateOutput)
        event_manager.subscribe("request_set_io_state_input", self.SetIoStateInput)

    # Frame IO 
    def FrameIo(self):
        self.title = QLabel("IO", self.parent_frame)
        self.title.setStyleSheet(style_label_title)
        self.title.setMaximumHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.title, 0, 0)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget(self.parent_frame)
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QGridLayout(scroll_widget) 
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(5)
        scroll_layout.setAlignment(Qt.AlignTop)
            
        scroll.setWidget(scroll_widget)
        self.layout.addWidget(scroll) 
        
        self.CHECKBOX_IO_INPUT = []
        self.CHECKBOX_IO_OUTPUT = []
        
        for i in range(10):
            label = QLabel(f"IO pin {i}")
            label.setStyleSheet(style_label)
            scroll_layout.addWidget(label, 1 + i, 0)
            
            checkbox = QCheckBox("IN")
            checkbox.setStyleSheet(style_checkbox_io)
            scroll_layout.addWidget(checkbox, 1 + i, 2)
            self.CHECKBOX_IO_INPUT.append(checkbox)
            
            checkbox = QCheckBox("OUT")
            checkbox.setStyleSheet(style_checkbox_io)
            scroll_layout.addWidget(checkbox, 1 + i, 3)
            self.CHECKBOX_IO_OUTPUT.append(checkbox)
           
    def CheckIOState(self, io_number):
        if self.CHECKBOX_IO_INPUT[io_number].isChecked():
            return True
        else:
            return False
           
    def SetIoStateInput(self, io_number, state):
        self.CHECKBOX_IO_INPUT[io_number].setChecked(state)
        
    def SetIoStateOutput(self, io_number, state):
        self.CHECKBOX_IO_OUTPUT[io_number].setChecked(state)
            
