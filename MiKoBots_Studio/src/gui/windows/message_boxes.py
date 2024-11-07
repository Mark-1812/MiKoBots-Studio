from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QLineEdit, QMessageBox, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import Qt


def WarningMessageRe(text, text_info = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText(text)
    if text_info:
        msg.setInformativeText(text_info)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    # Show the message box and wait for user response
    result = msg.exec_()

    if result == QMessageBox.Ok:
        return True
    else:
        return False
    
def InfoMessage(title, text, text_info = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(text)
    if text_info:
        msg.setInformativeText(text_info)
    msg.setStandardButtons(QMessageBox.Ok)

    # Show the message box
    msg.exec_()

def ErrorMessage(text, text_info = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)  # Set the icon to Critical for error messages
    msg.setWindowTitle("Error")  # Set the title of the dialog
    msg.setText(text)  # Set the main error message
    msg.setStandardButtons(QMessageBox.Ok)  # Add an "Ok" button

    # Execute the message box
    msg.exec_()

def SaveProgramMessage(text, text_info = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)  # Set the icon to Critical for error messages
    msg.setWindowTitle("Save")  # Set the title of the dialog
    msg.setText(text)  # Set the main error message
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # Add an "Ok" button

    # Execute the message box
    reply = msg.exec_()
    
    if reply == QMessageBox.Yes:
        print("Program closed with saving")
        return True
    elif reply == QMessageBox.No:
        print("Program closed without saving")
        return False


def CloseProgramMessage(title, text, text_info = None):
    msg_box = QMessageBox()
    msg_box.setText("Do you want to save the program?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowFlags(Qt.Dialog |  Qt.WindowTitleHint)

    # Execute and get the result
    reply = msg_box.exec_()

    if reply == QMessageBox.Yes:
        print("Program closed with saving")
        return 1
    elif reply == QMessageBox.No:
        print("Program closed without saving")
        return 0
    elif reply == QMessageBox.Cancel:
        return -1