from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
from PyQt5.QtGui import  QTextCursor

from backend.core.event_manager import event_manager
   
class LogField(QWidget):
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        self.FrameLog(frame_layout) 
        
        self.subscribeToEvents()   
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_insert_new_log", self.InsertLog)        
    
    def FrameLog(self, layout):       
        title = QtWidgets.QLabel("Log")
        title.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.addWidget(title, 0, 0, 1, 2)
        
        def scrolling( *args):
            self.LOG_TEXT_WIDGET.verticalScrollBar().setValue(args[0])

        self.LOG_TEXT_WIDGET = QTextEdit()
        self.LOG_TEXT_WIDGET.setDisabled(False)
        self.LOG_TEXT_WIDGET.setStyleSheet("background-color: " + "white")
        layout.addWidget(self.LOG_TEXT_WIDGET, 1,0)
        
        self.log_text_scrollbar = QScrollBar()
        self.log_text_scrollbar.valueChanged.connect(scrolling)
        layout.addWidget(self.log_text_scrollbar, 1,1)

        self.LOG_TEXT_WIDGET.setVerticalScrollBar(self.log_text_scrollbar)
        
    def InsertLog(self, text):
        self.LOG_TEXT_WIDGET.moveCursor(QTextCursor.End)
        self.LOG_TEXT_WIDGET.insertPlainText(text)
        self.LOG_TEXT_WIDGET.ensureCursorVisible()
