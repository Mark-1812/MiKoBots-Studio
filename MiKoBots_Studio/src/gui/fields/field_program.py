from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal, QStringListModel
from PyQt5.QtWidgets import QCompleter, QHBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget
import keyword

from backend.core.event_manager import event_manager

from code import InteractiveConsole

import keyword

from robot_library import Move, IO, Tool, Vision, Connect4, TicTacToe, Gcode

from gui.style import *

import re

import backend.core.variables as var

class ProgramField(QWidget):
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)

        self.FrameProgramming(frame_layout)
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_program_title", self.SetProgramName)
        event_manager.subscribe("request_program_field_clear", self.ProgramFieldClear)
        event_manager.subscribe("request_program_field_insert", self.ProgramFieldInsert)
        event_manager.subscribe("request_program_field_get", self.ProgramFieldGet)
        event_manager.subscribe("request_program_field_read_only", self.ReadOnlyText)
    
    def ReadOnlyText(self, state):
        self.PROGRAM_TEXT_WIDGET.setReadOnly(state)
            
    def FrameProgramming(self, layout):
        self.PROGRAM_NAME = QLabel("Program: New file.miko")
        self.PROGRAM_NAME.setStyleSheet(style_label_title)
        self.PROGRAM_NAME.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.PROGRAM_NAME, 0, 0, 1, 2)
        
        
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        h_layout.setSpacing(0)  # Set spacing to zer
        
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
            }
        """)
        
        self.PROGRAM_TEXT_WIDGET = CustomTextEdit(self) 
        self.PROGRAM_TEXT_WIDGET.setTabStopWidth(20)
        self.PROGRAM_TEXT_WIDGET.setLineWrapMode(QTextEdit.NoWrap)
        self.PROGRAM_TEXT_WIDGET.verticalScrollBar().valueChanged.connect(self.sync_scrollbars)
        self.PROGRAM_TEXT_WIDGET.setFont(QFont("Consolas", 11))
        self.PROGRAM_TEXT_WIDGET.setStyleSheet("""
            QTextEdit {
                padding: 5;
                background-color: white;
                border-top-right-radius: 5px;  
                border-bottom-right-radius: 5px;  
                border-bottom-left-radius: 0px;   
                border-top-left-radius: 0px;      
            }
        """)
        
        
        h_layout.addWidget(self.line_numbers)
        h_layout.addWidget(self.PROGRAM_TEXT_WIDGET)
        
        layout.addLayout(h_layout, 1, 0)
        
        self.PROGRAM_TEXT_WIDGET.append("from robot_library import Move\n")
        self.PROGRAM_TEXT_WIDGET.append('robot = Move()\n')
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,500,0,90,0],50,50)")
        self.PROGRAM_TEXT_WIDGET.append("robot.MoveJ([400,20,300,0,90,0],50,50)\n")  
        
        
        self.PROGRAM_TEXT_WIDGET.textChanged.connect(self.update_line_numbers)
       
        self.highlighter = HighlightText(self.PROGRAM_TEXT_WIDGET.document())
 
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
    def __init__(self, parent=None):
        super(HighlightText, self).__init__(parent)
        
        font = "Consolas"
        font_size = 11

        self.highlighting_rules = []
        # Normal text
        normal_text_format = QTextCharFormat()
        normal_text_format.setForeground(Qt.black)
        normal_text_format.setFont(QFont(font, font_size))
        self.highlighting_rules.append((QRegularExpression(r'[^\s]+'), normal_text_format))  # Match any non-whitespace characters

        # Python keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#339c9a"))
        keyword_format.setFont(QFont(font, font_size))  # Change the font here
        keyword_list = keyword.kwlist
        self.highlighting_rules.extend([(r'\b%s\b' % keyword, keyword_format) for keyword in keyword_list])

        # Multi-line strings
        string_format = QTextCharFormat()
        string_format.setForeground(Qt.lightGray)
        string_format.setFont(QFont(font, font_size))  # Change the font here
        self.highlighting_rules.append((QRegularExpression(r'""".*"""'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'''.*'''"), string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)
        comment_format.setFont(QFont(font, font_size))  # Change the font here
        self.highlighting_rules.append((QRegularExpression(r'#[^\n]*'), comment_format))

        # Highlight text between double quotes in brown
        brown_format = QTextCharFormat()
        brown_format.setForeground(QColor(139, 69, 19))  # Brown color
        brown_format.setFont(QFont(font, font_size))
        self.highlighting_rules.append((QRegularExpression(r'"(.*?)"'), brown_format))
        
        # Highlight text between double quotes in brown
        brown_format = QTextCharFormat()
        brown_format.setForeground(QColor(139, 69, 19))  # Brown color
        brown_format.setFont(QFont(font, font_size))
        self.highlighting_rules.append((QRegularExpression(r"'(.*?)'"), brown_format))
        

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
    

        
