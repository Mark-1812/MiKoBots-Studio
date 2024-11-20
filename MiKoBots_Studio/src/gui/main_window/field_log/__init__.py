from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt, pyqtSignal, QRegularExpression, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
from PyQt5.QtGui import  QTextCursor, QSyntaxHighlighter, QTextCharFormat, QFont, QColor

from keyword import kwlist  # For example, you could highlight Python keywords too

from backend.core.event_manager import event_manager

from datetime import datetime

from gui.style import *
   
from .highlight_text import HighlightText

class LogField(QWidget):
    log_signal = pyqtSignal(str)
    
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        
        self.FrameLog(frame_layout) 
        
        self.subscribeToEvents()   
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_insert_new_log", self.InsertLog)        
    
    def FrameLog(self, layout):       
        title = QtWidgets.QLabel("Log")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.addWidget(title)
        
        self.LOG_TEXT_WIDGET = QTextEdit()
        self.LOG_TEXT_WIDGET.setReadOnly(True)
        self.LOG_TEXT_WIDGET.setStyleSheet(style_textedit)
        layout.addWidget(self.LOG_TEXT_WIDGET)
        self.highlighter = HighlightText(self.LOG_TEXT_WIDGET.document())
        
        # self.log_text_scrollbar = QScrollBar()
        # layout.addWidget(self.log_text_scrollbar, 1,1)

        # self.LOG_TEXT_WIDGET.setVerticalScrollBar(self.log_text_scrollbar)
        
    def InsertLog(self, text):

        if not text.strip():
            return
        
        current_time = datetime.now().strftime("%H:%M:%S")
        log_message = f"{current_time} -> {text}"

        QMetaObject.invokeMethod(
            self.LOG_TEXT_WIDGET,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, log_message)
        )
        
        #self.LOG_TEXT_WIDGET.setReadOnly(False)
        #current_place = self.log_text_scrollbar.value()
        current_place = self.LOG_TEXT_WIDGET.verticalScrollBar().value()
        
        if current_place == self.LOG_TEXT_WIDGET.verticalScrollBar().maximum():
            #self.LOG_TEXT_WIDGET.append(log_message)
            self.LOG_TEXT_WIDGET.verticalScrollBar().setValue(current_place)
            #self.log_text_scrollbar.setValue(self.log_text_scrollbar.maximum())
        else:
            #self.LOG_TEXT_WIDGET.append(log_message)
            self.LOG_TEXT_WIDGET.verticalScrollBar().setValue(current_place)
            
        self.LOG_TEXT_WIDGET.setReadOnly(True)