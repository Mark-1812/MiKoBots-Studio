from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QCursor, QPixmap, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal, QStringListModel, pyqtSlot
from PyQt5.QtWidgets import QCompleter, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
import keyword

from backend.core.event_manager import event_manager

from code import InteractiveConsole

import keyword

#from robot_library import Move, IO, Tool, Vision, Connect4, TicTacToe

from gui.style import *
import re
import os

from backend.core.api import run_blockly_code

import backend.core.variables as var

class ProgramField(QWidget):
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)

        self.font_size = 11
        self.xmlString = "test"
        self.FrameProgramming(frame_layout)
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_program_title", self.SetProgramName)
        event_manager.subscribe("request_program_field_clear", self.ProgramFieldClear)
        event_manager.subscribe("request_program_field_insert", self.ProgramFieldInsert)
        event_manager.subscribe("request_program_field_get", self.ProgramFieldGet)
        event_manager.subscribe("request_program_field_read_only", self.ReadOnlyText)
        event_manager.subscribe("request_get_program_type", self.GetProgramTpe)
        event_manager.subscribe("request_get_blockly_code", self.GetBlocklyCode)
        event_manager.subscribe("request_save_blockly_file", self.save_workspace)
        event_manager.subscribe("request_load_blockly_file", self.load_workspace)
        event_manager.subscribe("request_clear_blockly_file", self.clear_workspace)
    
    
    def ReadOnlyText(self, state):
        self.PROGRAM_TEXT_WIDGET.setReadOnly(state)

    def GetProgramTpe(self):
        if self.CHECKBOX_BLOCKLY.isChecked():
            print("blockly coding")
            return True
        else:
            print("not blockly coding")
            return False 
        
    def GetBlocklyCode(self):
        print("get blockl code")
        self.web_view.page().runJavaScript("python.pythonGenerator.workspaceToCode(workspace);", run_blockly_code)
        
    @pyqtSlot()
    def save_workspace(self):
        # Call the saveWorkspace function in JavaScript and handle the result
        print("save_workspace")
        self.web_view.page().runJavaScript("saveWorkspace();", self.BlocklyConverting)

    def BlocklyConverting(self, xmlString):
        event_manager.publish("request_program_xmlString", xmlString)
        


    @pyqtSlot()
    def load_workspace(self, xmlString):
        try:
            self.web_view.page().runJavaScript(f'loadWorkspace(`{xmlString}`);')
            print("Workspace loaded.")
        except FileNotFoundError:
            print("No saved workspace found.")
            
            
    @pyqtSlot()
    def clear_workspace(self):
        print("Clearing workspace")
        # Run JavaScript to clear the Blockly workspace
        self.web_view.page().runJavaScript("workspace.clear();")  
        

    def FrameProgramming(self, layout):
        self.PROGRAM_NAME = QLabel("Program: New file.miko")
        self.PROGRAM_NAME.setStyleSheet(style_label_title)
        self.PROGRAM_NAME.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.PROGRAM_NAME.setFixedHeight(24)
        layout.addWidget(self.PROGRAM_NAME, 0, 0)
        
        # button_help = QPushButton("i")
        # button_help.setStyleSheet(style_button_help)
        # button_help.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # button_help.clicked.connect(lambda: webbrowser.open('https://www.mikobots.com'))
        # layout.addWidget(button_help,0,0)
        

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
        blockly_path = os.path.abspath(os.path.join(current_directory, '../..', 'blockly', 'blockly.html'))
        self.web_view.setUrl(QUrl.fromLocalFile(blockly_path))  # Make sure to set the correct path to your HTML file
        # Read the HTML file and set it in the QWebEngineView
        # with open(blockly_path, 'r', encoding='utf-8') as file:
        #     blockly_html = file.read()
        #     print(blockly_html)
        #     self.web_view.setHtml(blockly_html)
        #     self.web_view.page().runJavaScript("console.log('Page loaded')")
            
        # Print the absolute path to blockly.html
        #blockly_path = blockly_path.replace('\\', '/')
        
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
        print(current_directory)
        blockly_path = os.path.abspath(os.path.join(current_directory, '../..', 'blockly', 'blockly.html'))
        print(blockly_path)
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


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.console = InteractiveConsole()
        self.python_keywords = keyword.kwlist
        self.completer = QCompleter(self.python_keywords)
        
        self.setupCompleter()
        self.line_count = 0
        
        self.tabs_nr = 0
 
    def setupCompleter(self):
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)    
             
    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0)
        self.completer = completer
        
        
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)
        
    def insertCompletion(self, completion):
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(completion)
        self.setTextCursor(cursor)

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        return cursor.selectedText()
    
    def showCompleter(self):
        if not self.completer.popup().isVisible():
            self.completer.complete(self.cursorRect())

    def get_methods(self, cls):
        """Retrieve method names from the class."""
        return [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith("__")]
      
    def countNumberTabs(self):
        cursor_position = self.textCursor().position()
        full_text = self.toPlainText()

        # Find the last newline character before the cursor
        last_newline_pos = full_text.rfind('\n', 0, cursor_position)
        if last_newline_pos == -1:
            last_newline_pos = 0  # No newline found, start from the beginning

        # Get the text from the last newline to the cursor position       
        current_line = full_text[last_newline_pos:cursor_position]
        current_line = current_line.lstrip('\n')
        current_line += "#"

        self.tabs_nr = 0
        for char in current_line:
            if char == '\t':
                self.tabs_nr += 1
            else:
                break
        
        current_line = current_line.rstrip()
        
        if '#' in current_line:
            current_line = current_line.split('#', 1)[0]
            
        if current_line.endswith(':'):
            self.tabs_nr += 1            
 
    def get_item_right_of_cursor(text_edit):
        cursor = text_edit.textCursor()  # Get the current text cursor
        cursor_position = cursor.position()  # Get the current cursor position
        
        # Get the text to the right of the cursor
        text_right = text_edit.toPlainText()[cursor_position:cursor_position + 1]  # Get one character to the right
        
        return text_right
 
    def GetItemLeftOfCursor(text_edit, number_to_left):
        cursor = text_edit.textCursor()  # Get the current text cursor
        cursor_position = cursor.position()  # Get the current cursor position
        
        # Get the text to the right of the cursor
        text_left = text_edit.toPlainText()[cursor_position -1 - number_to_left :cursor_position -number_to_left]  # Get one character to the right
        
        return text_left
 
    def keyTab(self):
        cursor = self.textCursor()
        
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        
        full_text = self.toPlainText()
        selected_text_with_newlines = full_text[selection_start:selection_end]


        if selected_text_with_newlines:
            # Split the selected text by newlines
            lines = selected_text_with_newlines.split('\n')

            # Add a tab at the beginning and for each line
            indented_lines = ['\t' + line for line in lines]

            # Join the lines back together with newlines
            indented_text = '\n'.join(indented_lines)
            
            print(f"indented_text {indented_text}")

            # Replace the selected text with the indented text
            cursor.insertText(indented_text)
    
    def keyHelpThings(self, event):
        selected_text = self.textCursor().selectedText()    
        madeChange = True

        #print(event.text())
           
        if event.text() in ('"', "'", "(", "[", "{"):
            cursor = self.textCursor()
            if selected_text != "":
                if event.text() == "(":
                    cursor.insertText(f'{event.text()}{selected_text})')
                elif event.text() == "[":
                    cursor.insertText(f'{event.text()}{selected_text}]')
                elif event.text() == "{":
                    cursor.insertText(f"{{{selected_text}}}")
                else:
                    cursor.insertText(f'{event.text()}{selected_text}{event.text()}')
                    
            # if the item right of the cursur is nothing that a double
            elif self.get_item_right_of_cursor() in ("", '"', "'", ")", "]", "}"):   
                if event.text() in "(":
                    cursor.insertText(f'{event.text()})')
                elif event.text() == "[":
                    cursor.insertText(f'{event.text()}]')
                elif event.text() == "{":
                    cursor.insertText('{}')
                else:
                    cursor.insertText(f'{event.text()}{event.text()}')
                cursor.setPosition(cursor.position() - 1)
                self.setTextCursor(cursor)
            else:
                cursor.insertText(f'{event.text()}')
                self.setTextCursor(cursor)
        else:
            madeChange = False
            
        return madeChange    
               
    def keyPressEvent(self, event):  
        
        if self.keyHelpThings(event):
            return

        if event.key() == Qt.Key_Tab:
            self.keyTab()
            
        self.countNumberTabs()
        
        
        hide = False
        
        if self.GetItemLeftOfCursor(0) in ('\t') and event.key() in (Qt.Key_Tab, Qt.Key_Enter, Qt.Key_Return):
            hide = True
         
        super(CustomTextEdit, self).keyPressEvent(event)
        
        if self.GetItemLeftOfCursor(0) == ('\t') and self.GetItemLeftOfCursor(1) == '\n':
            hide = True
           
        if event.text() in ('"', "'", ";", "(", ")", ":", ",", "+", "-", "*", "/", " "):
            self.completer.popup().hide()
            return
        
        if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_Backspace, Qt.Key_Shift):
            self.completer.popup().hide()
            return

        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            cursor = self.textCursor()
            for i in range(self.tabs_nr):
                text = '\t'
                cursor.insertText(text) 
        
        
        if hide == True:
            self.completer.popup().hide()
            return
        
        if self.completer and self.completer.popup().isVisible():
            # Ignore specific keys that interfere with the completer
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                print("oke")
                
                cursor = self.textCursor()
                cursor_position = cursor.position()
                text_before_cursor = cursor.document().toPlainText()[:cursor_position]
                
                print(text_before_cursor)
                print(self.GetItemLeftOfCursor(1))


                prefix = self.completer.completionPrefix()
                num_chars_to_delete = len(prefix)    
                
                if self.GetItemLeftOfCursor(1) == '.':
                   print("delete one more")
                   num_chars_to_delete += 1 

                print(num_chars_to_delete)
                
                if len(text_before_cursor) >= num_chars_to_delete:
                    cursor.setPosition(cursor_position - num_chars_to_delete, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()  # Remove the selected text
                    
                event.ignore()
                self.completer.popup().hide()  # Hide on Escape
                return

        completion_prefix = self.textUnderCursor()
        cursor_position = self.textCursor().position()
        full_text = self.toPlainText()        
        
        cursor_position = self.textCursor().position()
        full_text = self.toPlainText()

        # Find the last newline character before the cursor
        last_newline_pos = full_text.rfind('\n', 0, cursor_position)
        if last_newline_pos == -1:
            last_newline_pos = 0  # No newline found, start from the beginning

        # Get the text from the last newline to the cursor position       
        current_line = full_text[last_newline_pos:cursor_position]
        current_line = current_line.lstrip('\n')
     
        if current_line in ("", "\n"):
            self.completer.popup().hide()
            return 
        
   
        if '.' in current_line:
            #base = current_line.split('.')[0].strip()  # Get the base (the variable name)
            # Attempt to retrieve the corresponding Move instance from the console locals
            pattern = r"[\(\,\n\s]*(\w+)\."
            match = re.search(pattern, current_line)
            if match:
                base = match.group(1)   
            else:
                return

            print(base)
            
            pattern = fr'{base}\s*=\s*(\w+)\(.*\)'
            code = self.toPlainText()
            
            matches = re.findall(pattern, code)
            # find if there is robot be
            
            if matches:
                for match in matches:
                    instance = match
                    ClassRef = globals()[instance]
                    methods = self.get_methods(ClassRef)  # Get methods of the Move class
                    if methods:
                        self.completer.setModel(QStringListModel(methods))
                        self.showCompleter()
        else:
            self.completer.setModel(QStringListModel(self.python_keywords))
    
        if completion_prefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completion_prefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        
        rect = self.cursorRect()
        rect.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(rect)  # Show the completer popup
    

        
