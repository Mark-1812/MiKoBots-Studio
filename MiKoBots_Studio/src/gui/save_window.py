from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSplitter, QMessageBox, QMainWindow, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import *


def AskSave():
    msg_box = QMessageBox()
    msg_box.setText("Do you want to save the program?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
    msg_box.setStyleSheet(style_messagebox)

    # Execute and get the result
    reply = msg_box.exec_()
    
    if reply == QMessageBox.Yes:
        msg_box.close()
        return "Yes"
    elif reply == QMessageBox.No:
        msg_box.close()
        return "Close"
    elif reply == QMessageBox.Cancel:
        msg_box.close()
        return "Cancel"
    
    