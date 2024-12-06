from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QCursor, QPixmap, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal, QStringListModel, pyqtSlot
from PyQt5.QtWidgets import QCompleter, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
from backend.core.event_manager import event_manager

import keyword

from gui.style import *

class HighlightText(QSyntaxHighlighter):
    def __init__(self, document, font="Consolas", font_size=11):
        super(HighlightText, self).__init__(document)
        
        self.font = font
        self.font_size = font_size
        self.highlighting_rules = []

        # Initialize text formats
        self.normal_text_format = QTextCharFormat()
        self.keyword_format = QTextCharFormat()
        self.string_format = QTextCharFormat()
        self.comment_format = QTextCharFormat()
        self.brown_format = QTextCharFormat()
        
        # Set font and foreground for each format
        self.set_formats()

        # Normal text
        self.highlighting_rules.append((QRegularExpression(r'[^\s]+'), self.normal_text_format))  # Match any non-whitespace characters

        # Python keywords
        keyword_list = keyword.kwlist
        self.highlighting_rules.extend([(QRegularExpression(r'\b%s\b' % keyword), self.keyword_format) for keyword in keyword_list])

        # Multi-line strings
        self.highlighting_rules.append((QRegularExpression(r'""".*?"""'), self.string_format))
        self.highlighting_rules.append((QRegularExpression(r"'''.*?'''"), self.string_format))

        # Comments
        self.highlighting_rules.append((QRegularExpression(r'#[^\n]*'), self.comment_format))

        # Highlight text between double quotes in brown
        self.highlighting_rules.append((QRegularExpression(r'"(.*?)"'), self.brown_format))
        self.highlighting_rules.append((QRegularExpression(r"'(.*?)'"), self.brown_format))

    def set_formats(self):
        """Set the font size and color for each QTextCharFormat."""
        self.normal_text_format.setForeground(Qt.black)
        self.normal_text_format.setFont(QFont(self.font, self.font_size))
        
        self.keyword_format.setForeground(QColor("#339c9a"))
        self.keyword_format.setFont(QFont(self.font, self.font_size))
        
        self.string_format.setForeground(Qt.lightGray)
        self.string_format.setFont(QFont(self.font, self.font_size))
        
        self.comment_format.setForeground(Qt.darkGreen)
        self.comment_format.setFont(QFont(self.font, self.font_size))
        
        self.brown_format.setForeground(QColor(139, 69, 19))
        self.brown_format.setFont(QFont(self.font, self.font_size))

    def highlightBlock(self, text):
        # Apply formatting even to empty lines
        self.setFormat(0, len(text), self.normal_text_format)
        
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
                match = expression.match(text, match.capturedEnd())

        if text.strip() == "":
            self.setFormat(0, len(text), self.normal_text_format)  # Ensure empty lines have the default format
            

    def update_font_size(self, new_size):


        self.font_size = new_size
        self.set_formats()  # Update formats with the new font size
        self.rehighlight()  # Rehighlight the text with the updated formats