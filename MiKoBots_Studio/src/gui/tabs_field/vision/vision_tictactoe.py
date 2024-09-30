from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

from gui.style import *

class TicTacToe():
    def __init__(self, frame):
        layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QVBoxLayout(scroll_widget)        
       
        label = QLabel("Import the Tic-Tac-Toe library:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setStyleSheet(style_entry)
        entry.setText("from vision.tic_tac_toe.functions import TicTacToeFunctions")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Tic-Tac-Toe functions:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the Tic-Tac-Toe function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setStyleSheet(style_entry)
        entry.setText("TicTacToe = TicTacToeFunctions()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("Find board")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("board = TicTacToe.DetectBoard(color = str)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("find the game board<br>"
                "<b>color:</b> color of the 4 corner stones<br>"
                "<b>board:</b> is a list that contains the information of the board:<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        # Find move human
        label = QLabel("Find move human")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("TicTacToe.FindMoveHuman(color, board)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("Find the move that the playes has made<br>"
                "<b>color:</b> the color of the players stones.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         

        # GenerateMoveAi
        label = QLabel("Generate move AI")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("X_place, Y_place = TicTacToe.GenerateMoveAi(board)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("This function will calculate the best move for the robot, and retrun the position.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>"               
                "<b>X_place:</b> the place in X directions.<br>"
                "<b>Y_place:</b> the place in Y directions.<br>"
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  

        # CheckWinningMove
        label = QLabel("Check winning move>")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("Winner = TicTacToe.CheckWinningMove()")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("This function will return True or False.<br>"
                "<b>Winner:</b> if winner is True game is over."  
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         
        
                    
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)

        

