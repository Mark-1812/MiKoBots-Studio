from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QCursor, QPixmap, QSyntaxHighlighter, QTextCharFormat,  QDesktopServices, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal, QStringListModel, pyqtSlot
from PyQt5.QtWidgets import QCompleter, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from backend.core.event_manager import event_manager
from gui.style import *
import os

from backend.run_program import run_blockly_code

from backend.file_manager import blockly_save

import backend.core.variables as var

import json

from .highlight_text import HighlightText
from .text_edit import CustomTextEdit

class ProgramField(QWidget):
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)

        self.font_size = 11
        self.FrameProgramming(frame_layout)
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_program_title", self.SetProgramName)
        event_manager.subscribe("request_program_field_clear", self.ProgramFieldClear)
        event_manager.subscribe("request_program_field_insert", self.ProgramFieldInsert)
        event_manager.subscribe("request_program_field_get", self.ProgramFieldGet)
        event_manager.subscribe("request_get_program_type", self.GetProgramTpe)
        event_manager.subscribe("request_get_blockly_code", self.GetBlocklyCode)
        event_manager.subscribe("request_save_blockly_file", self.save_workspace)
        event_manager.subscribe("request_load_blockly_file", self.load_workspace)
        event_manager.subscribe("request_clear_blockly_file", self.clear_workspace)



    def FrameProgramming(self, layout): 
        self.PROGRAM_NAME = QLabel("Program: New file.miko")
        self.PROGRAM_NAME.setStyleSheet(style_label_title)
        self.PROGRAM_NAME.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.PROGRAM_NAME.setFixedHeight(24)
        layout.addWidget(self.PROGRAM_NAME, 0, 0)
        
        self.CHECKBOX_BLOCKLY = QCheckBox("Blockly")
        self.CHECKBOX_BLOCKLY.setStyleSheet(style_checkbox)
        layout.addWidget(self.CHECKBOX_BLOCKLY,1,0)
        self.CHECKBOX_BLOCKLY.stateChanged.connect(lambda state: self.SwitchProgramStle(state))

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0, 0, 1, 2)  # Set margins to zero
        self.h_layout.setSpacing(0)  # Set spacing to zer 

        self.frame = QFrame()
        self.frame.setStyleSheet(style_frame)
        self.frame.setFrameStyle(QFrame.NoFrame)
        self.frame.setLayout(self.h_layout)

        # Create line numbers text area (non-editable)
        self.line_numbers = QTextEdit()
        self.line_numbers.setReadOnly(True)
        self.line_numbers.setFrameStyle(QFrame.NoFrame)  # No frame for better aesthetics
        self.line_numbers.setFixedWidth(40)  # Fixed width for line numbers column
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide vertical scrollbar
        self.line_numbers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar       
        self.line_numbers.setFont(QFont("Consolas", 11))
        self.line_numbers.setStyleSheet("""
            QTextEdit {
                background-color: white;
                padding: 5;
                border-top-right-radius: 0px;  
                border-bottom-right-radius: 0px; 
                border-bottom-left-radius: 5px;   
                border-top-left-radius: 5px;     
                color: black;
            }
            
        """)
        
        self.PROGRAM_TEXT_WIDGET = CustomTextEdit(self) 
        self.PROGRAM_TEXT_WIDGET.setTabStopWidth(20)
        self.PROGRAM_TEXT_WIDGET.setLineWrapMode(QTextEdit.NoWrap)
        self.PROGRAM_TEXT_WIDGET.verticalScrollBar().valueChanged.connect(self.sync_scrollbars)
        self.PROGRAM_TEXT_WIDGET.setFont(QFont("Consolas", 11))
        self.PROGRAM_TEXT_WIDGET.setStyleSheet(style_textedit_program)
        
        
        self.h_layout.addWidget(self.line_numbers)
        self.h_layout.addWidget(self.PROGRAM_TEXT_WIDGET)


        self.button_plus = QPushButton("+")
        self.button_plus.setFixedSize(30,30)
        self.button_plus.setStyleSheet(style_button_zoom)
        self.button_plus.clicked.connect(lambda: self.change_font_size(1))

        self.button_min = QPushButton("-")
        self.button_min.setFixedSize(30,30)
        self.button_min.setStyleSheet(style_button_zoom)
        self.button_min.clicked.connect(lambda: self.change_font_size(-1))

        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(20, 20, 20, 20)  # Set padding around the button
        button_layout.addWidget(self.button_plus)
        button_layout.addWidget(self.button_min)

        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, False)
        self.web_view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, False)



        # Get the current directory of the file
        current_directory = os.path.dirname(__file__)
        blockly_path = os.path.abspath(os.path.join(current_directory, '../../..', 'blockly', 'blockly.html'))
        self.web_view.setUrl(QUrl.fromLocalFile(blockly_path))  # Make sure to set the correct path to your HTML file
        layout.addWidget(self.web_view, 2, 0)


        #self.blockly_frame.hide()
        layout.setRowStretch(1, 1)  # Set the stretch factor for row 0
        layout.setColumnStretch(0, 1)  # Set the stretch factor for column 0


        self.PROGRAM_TEXT_WIDGET.append("from robot_library import Move\n")
        self.PROGRAM_TEXT_WIDGET.append('robot = Move()\n')
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,500,0,90,0],50,50)")
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,300,0,90,0],50,50)\n")  
        
        layout.addWidget(self.frame, 2, 0)
        layout.addLayout(button_layout, 2, 0, alignment=Qt.AlignBottom | Qt.AlignRight)        
        
        self.PROGRAM_TEXT_WIDGET.textChanged.connect(self.update_line_numbers)
       
        self.highlighter = HighlightText(self.PROGRAM_TEXT_WIDGET.document())
        

        layout_question = QHBoxLayout()
        layout_question.setAlignment(Qt.AlignRight)
        layout.addLayout(layout_question,0,0, alignment=Qt.AlignTop | Qt.AlignRight)
        
        button = QPushButton("?")
        button.setStyleSheet(style_button_help)
        button.setFixedSize(20,20)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://mikobots.com/mikobots-studio/help/program-field/")))
        layout_question.addWidget(button)

    def change_font_size(self, size):
        new_size = self.highlighter.font_size + size  # Increase font size by 2
        self.highlighter.update_font_size(new_size)

        
        self.line_numbers.setFontPointSize(new_size)

        self.PROGRAM_TEXT_WIDGET.selectAll()
        cursor = self.PROGRAM_TEXT_WIDGET.textCursor()
        char_format = cursor.charFormat()

        font = QFont(char_format.fontFamily(), new_size)
        char_format.setFont(font)

        cursor.mergeCharFormat(char_format)

        # Deselect the text
        cursor.movePosition(QTextCursor.Start)
        self.PROGRAM_TEXT_WIDGET.setTextCursor(cursor)

 
    def SwitchProgramStle(self, state):
        current_directory = os.path.dirname(__file__)
        blockly_path = os.path.abspath(os.path.join(current_directory, '../..', 'blockly', 'blockly.html'))
        if state:
            self.frame.hide()
            self.button_min.hide()
            self.button_plus.hide()
        else:
            self.frame.show()
            self.button_min.show()
            self.button_plus.show()

    def update_line_numbers(self):
        # Get the number of lines in the text editor
        
        text = self.PROGRAM_TEXT_WIDGET.toPlainText()
        lines = text.split('\n')
        line_count = len(lines)

        # Generate line numbers
        line_number_text = "\n".join(str(i + 1) for i in range(line_count))

        # Set the line numbers text
        self.line_numbers.setText(line_number_text)

        # Sync vertical scrolling of the line numbers with the text editor
        self.line_numbers.verticalScrollBar().setValue(self.PROGRAM_TEXT_WIDGET.verticalScrollBar().value())

    def sync_scrollbars(self):
        # Synchronize the scrollbar values
        self.line_numbers.verticalScrollBar().setValue(self.PROGRAM_TEXT_WIDGET.verticalScrollBar().value())
    
    def ProgramFieldClear(self):
        self.PROGRAM_TEXT_WIDGET.clear()
        
    def ProgramFieldInsert(self, text):
        self.PROGRAM_TEXT_WIDGET.insertPlainText(text)
        
    def ProgramFieldGet(self):
        program = self.PROGRAM_TEXT_WIDGET.toPlainText() 
        return program
    
    def SetProgramName(self, name):
        self.PROGRAM_NAME.setText(f"Program: {name}")

    def GetProgramTpe(self):
        if self.CHECKBOX_BLOCKLY.isChecked():
            return True
        else:
            return False 
        
    def GetBlocklyCode(self):
        self.web_view.page().runJavaScript("python.pythonGenerator.workspaceToCode(workspace);", run_blockly_code)
        
    @pyqtSlot()
    def save_workspace(self):
        # Call the saveWorkspace function in JavaScript and handle the result
        try:
            self.web_view.page().runJavaScript("saveWorkspace();", self.BlocklyConverting)
        except Exception as e:
            print(f"Error running JavaScript: {e}")

    def BlocklyConverting(self, xmlString):
        blockly_save(xmlString)
        
        


    @pyqtSlot()
    def load_workspace(self, xmlString):
        try:
            # Escape xmlString and pass to JavaScript
            escaped_xmlString = json.dumps(xmlString)
            self.web_view.page().runJavaScript(f'loadWorkspace({escaped_xmlString});')
        except FileNotFoundError:
            print(var.LANGUAGE_DATA.get("message_no_blockly_workspace"))
            
            
    @pyqtSlot()
    def clear_workspace(self):
        # Run JavaScript to clear the Blockly workspace
        self.web_view.page().runJavaScript("workspace.clear();")  
        