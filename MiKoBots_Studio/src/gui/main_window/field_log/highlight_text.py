from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt, pyqtSignal, QRegularExpression, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
from PyQt5.QtGui import  QTextCursor, QSyntaxHighlighter, QTextCharFormat, QFont, QColor

from keyword import kwlist  # For example, you could highlight Python keywords too

from backend.core.event_manager import event_manager

from datetime import datetime

from gui.style import *
 
                


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

