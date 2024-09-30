import json

from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator

from gui.style import *

class Connect4():
    def __init__(self, frame):
        layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QVBoxLayout(scroll_widget)        
       
        label = QLabel("Import the connect4 library:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setStyleSheet(style_entry)
        entry.setText("from robot_library import Connect4")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Connect4 functions:")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the connect4 function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setStyleSheet(style_entry)
        entry.setText("connect4 = Connect4()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("Find board")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("board = connect.DetectBoard(color = str)")
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
        
        entry = QLineEdit("connect4.FindMoveHuman(color, board)")
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
        label = QLabel("<b>Generate move AI")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("TicTacToe.GenerateMoveAi(board)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("This function will calculate the best move for the robot, and retrun the position.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>"               
                "<b>column:</b> the place in X directions.<br>"
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  

        # CheckWinningMove
        label = QLabel("Winning move")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("Winner = connect4.WinningMove(AI)")
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("This function will return True or False.<br>"
                "<b>AI:</b> if true, check winning move robot, else player<br>"     
                "<b>Winner:</b> if winner is True game is over<br>"  
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         
        
                    
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)