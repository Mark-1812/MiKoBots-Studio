from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt, pyqtSignal, QRegularExpression, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
from PyQt5.QtGui import  QTextCursor, QSyntaxHighlighter, QTextCharFormat, QFont, QColor

from keyword import kwlist  # For example, you could highlight Python keywords too

from backend.core.event_manager import event_manager

from datetime import datetime

from gui.style import *
   
class LogField:
    log_signal = pyqtSignal(str)
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)
        
        self.FrameLog() 
        self.subscribeToEvents()  

        self.parent_frame.setLayout(self.layout)
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_insert_new_log", self.InsertLog)        
    
    def FrameLog(self):       
        title = QtWidgets.QLabel("Log")
        title.setStyleSheet(style_label_title)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title, 0, 0, 1, 2)
        
        self.LOG_TEXT_WIDGET = QTextEdit()
        self.LOG_TEXT_WIDGET.setReadOnly(True)
        self.LOG_TEXT_WIDGET.setStyleSheet(style_textedit)
        self.layout.addWidget(self.LOG_TEXT_WIDGET, 1,0)
        self.highlighter = HighlightText(self.LOG_TEXT_WIDGET.document())
        
        self.log_text_scrollbar = QScrollBar()
        self.layout.addWidget(self.log_text_scrollbar, 1,1)

        self.LOG_TEXT_WIDGET.setVerticalScrollBar(self.log_text_scrollbar)
        
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
        current_place = self.log_text_scrollbar.value()
        
        if current_place == self.log_text_scrollbar.maximum():
            #self.LOG_TEXT_WIDGET.append(log_message)
            self.log_text_scrollbar.setValue(self.log_text_scrollbar.maximum())
        else:
            #self.LOG_TEXT_WIDGET.append(log_message)
            self.log_text_scrollbar.setValue(current_place)
            
        self.LOG_TEXT_WIDGET.setReadOnly(True)
                


class HighlightText(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(HighlightText, self).__init__(parent)

        self.highlighting_rules = []

        # Normal text format
        normal_text_format = QTextCharFormat()
        normal_text_format.setForeground(Qt.black)
        normal_text_format.setFont(QFont("Consolas", 11))
        # Match any text that doesn't contain 'error'
        self.highlighting_rules.append((QRegularExpression(r'^(?!.*error).*'), normal_text_format))

        # Error messages format (whole line red)
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("red"))
        error_format.setFont(QFont("Consolas", 11))
        # Match the entire line if it contains the word "error"
        self.highlighting_rules.append((QRegularExpression(r'.*error.*', QRegularExpression.CaseInsensitiveOption), error_format))

    def highlightBlock(self, text):
        # Apply formatting based on the highlighting rules
        for pattern, text_format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), text_format)

