import json

from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator


class Connect4():
    def __init__(self, frame):
        layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(
                "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
                "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
                "QPushButton:hover { background-color: white; }"
                "QPushButton:pressed { background-color: darkorange; }"+
                "QCheckBox {  background-color: white; }"+
                "QLabel {font-size: 12px; font-family: Arial;}"+
                "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QLineEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        scroll_layout = QVBoxLayout(scroll_widget)        
       
        label = QLabel("Import the connect4 library:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("from vision.connect4.functions import Connect4Functions")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Connect4 functions:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the connect4 function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("connect4 = Connect4Functions()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("<b>Find board</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("board = connect.DetectBoard(color = str)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("find the game board<br>"
                "<b>color:</b> color of the 4 corner stones<br>"
                "<b>board:</b> is a list that contains the information of the board:<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        # Find move human
        label = QLabel("<b>Find move human</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("connect4.FindMoveHuman(color, board)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("Find the move that the playes has made<br>"
                "<b>color:</b> the color of the players stones.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         

        # GenerateMoveAi
        label = QLabel("<b>Generate move AI</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("TicTacToe.GenerateMoveAi(board)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("This function will calculate the best move for the robot, and retrun the position.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>"               
                "<b>column:</b> the place in X directions.<br>"
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  

        # CheckWinningMove
        label = QLabel("<b>Winning move</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("Winner = connect4.WinningMove(AI)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("This function will return True or False.<br>"
                "<b>AI:</b> if true, check winning move robot, else player<br>."     
                "<b>Winner:</b> if winner is True game is over<br>."  
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         
        
                    
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)