from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
import keyword

from backend.core.event_manager import event_manager

from code import InteractiveConsole

class ProgramField(QWidget):
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        self.FrameProgramming(frame_layout)
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_program_title", self.SetProgramName)
        event_manager.subscribe("request_program_field_clear", self.ProgramFieldClear)
        event_manager.subscribe("request_program_field_insert", self.ProgramFieldInsert)
        event_manager.subscribe("request_program_field_get", self.ProgramFieldGet)
    
    def FrameProgramming(self, layout):
        self.PROGRAM_NAME = QtWidgets.QLabel("Program: New file.miko")
        self.PROGRAM_NAME.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.PROGRAM_NAME.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.PROGRAM_NAME, 0, 0, 1, 2)

        self.PROGRAM_TEXT_WIDGET = CustomTextEdit()
        
        self.PROGRAM_TEXT_WIDGET.setTabStopWidth(20)
        #self.program_text.setStyleSheet("background-color: #272822; color: #F8F8F2; font-family: Consolas; font-size: 11pt;")
        self.PROGRAM_TEXT_WIDGET.setLineWrapMode(QTextEdit.NoWrap)
        
        layout.addWidget(self.PROGRAM_TEXT_WIDGET)
        
        self.PROGRAM_TEXT_WIDGET.append("from robot.commands import Move\n")
        self.PROGRAM_TEXT_WIDGET.append("robot = Move()\n")
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,500,0,90,0],50,50)")
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,300,0,90,0],50,50)")     

        self.console = InteractiveConsole()
        self.console.locals['app'] = QApplication.instance()
        self.console.locals['window'] = self
       
        self.highlighter = HighlightText(self.PROGRAM_TEXT_WIDGET.document())
    
    def ProgramFieldClear(self):
        self.PROGRAM_TEXT_WIDGET.clear()
        
    def ProgramFieldInsert(self, text):
        self.PROGRAM_TEXT_WIDGET.insertPlainText(text)
        
    def ProgramFieldGet(self):
        program = self.PROGRAM_TEXT_WIDGET.toPlainText() 
        return program
    
    def SetProgramName(self, name):
        self.PROGRAM_NAME.setText(f"Program: {name}")

class HighlightText(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(HighlightText, self).__init__(parent)

        self.highlighting_rules = []
        # Normal text
        normal_text_format = QTextCharFormat()
        normal_text_format.setForeground(Qt.black)
        normal_text_format.setFont(QFont("Consolas", 11))
        self.highlighting_rules.append((QRegularExpression(r'[^\s]+'), normal_text_format))  # Match any non-whitespace characters

        # Python keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#339c9a"))
        keyword_format.setFont(QFont("Consolas", 11))  # Change the font here
        keyword_list = keyword.kwlist
        self.highlighting_rules.extend([(r'\b%s\b' % keyword, keyword_format) for keyword in keyword_list])

        # Multi-line strings
        string_format = QTextCharFormat()
        string_format.setForeground(Qt.lightGray)
        string_format.setFont(QFont("Consolas", 11))  # Change the font here
        self.highlighting_rules.append((QRegularExpression(r'""".*"""'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'''.*'''"), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)
        comment_format.setFont(QFont("Consolas", 11))  # Change the font here
        self.highlighting_rules.append((QRegularExpression(r'#[^\n]*'), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
                match = expression.match(text, match.capturedEnd())

                
class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.text() == '"':
            cursor = self.textCursor()
            cursor.insertText('""')
            cursor.setPosition(cursor.position() - 1)
            self.setTextCursor(cursor)
        elif event.text() == '(':
            cursor = self.textCursor()
            cursor.insertText('()')
            cursor.setPosition(cursor.position() - 1)
            self.setTextCursor(cursor)
        elif event.text() == '[':
            cursor = self.textCursor()
            cursor.insertText('[]')
            cursor.setPosition(cursor.position() - 1)
            self.setTextCursor(cursor)
        else:
            super().keyPressEvent(event)