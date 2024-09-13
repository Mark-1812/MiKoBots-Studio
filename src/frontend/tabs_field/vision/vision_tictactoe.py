from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

class TicTacToe():
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
       
        label = QLabel("Import the Tic-Tac-Toe library:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("from vision.tic_tac_toe.functions import TicTacToeFunctions")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Tic-Tac-Toe functions:")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the Tic-Tac-Toe function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("TicTacToe = TicTacToeFunctions()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("<b>Find board</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("board = TicTacToe.DetectBoard(color = str)")
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
        
        entry = QLineEdit("TicTacToe.FindMoveHuman(color, board)")
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
        
        entry = QLineEdit("X_place, Y_place = TicTacToe.GenerateMoveAi(board)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("This function will calculate the best move for the robot, and retrun the position.<br>"
                "<b>board:</b> the board from, DetectBoard.<br>"               
                "<b>X_place:</b> the place in X directions.<br>"
                "<b>Y_place:</b> the place in Y directions.<br>"
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)  

        # CheckWinningMove
        label = QLabel("<b>Check winning move</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("Winner = TicTacToe.CheckWinningMove()")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("This function will return True or False.<br>"
                "<b>Winner:</b> if winner is True game is over."  
                )
        label.setWordWrap(True)
        scroll_layout.addWidget(label)         
        
                    
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)

        

