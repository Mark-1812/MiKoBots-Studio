import math 
import time
import random

class tic_tac_toe:
    def __init__(self):
        print("start")
        self.BOARD = []
        self.ROBOT = "X"
        self.PLAYER = "O"
        
        self.create_board()
        self.print_board()

    def print_board(self):
        for i in range(3):
            str = ""
            for j in range(3):
                str += self.BOARD[i][j] + " "
            print(str)
        print("\n")

    def create_board(self): 
        for i in range(3):
            self.BOARD.append([])
            for j in range(3):
                self.BOARD[i].append("_")
    
    def check_winning_move(self, board):
        Winner = None
        open_spots = 0
        i = 0
        j = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    open_spots += 1
                          
        ## horizontal
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2]:
                if board[i][0] == self.PLAYER:
                    Winner = self.PLAYER
                elif board[i][0] == self.ROBOT:
                    Winner = self.ROBOT
                    
        # vertical
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i]:
                if board[0][i] == self.PLAYER:
                    Winner = self.PLAYER
                elif board[0][i] == self.ROBOT:
                    Winner = self.ROBOT
                    
        # diagonal
        if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
            if board[1][1] == self.PLAYER:
                Winner = self.PLAYER
            elif board[1][1] == self.ROBOT:
                Winner = self.ROBOT       
                            
        if open_spots == 0:
            Winner = "Tie"
                                        
        return Winner
        
    def scores(self, score):
        if score == self.ROBOT:
            return 1
        elif score == self.PLAYER:
            return -1
        elif score == "Tie":
            return 0
         
    def minimax(self, board, depth, maximizing):
        result = self.check_winning_move(board)
        
        if result is not None:
            return self.scores(result)
        
        if maximizing:
            Best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "_":
                        board[i][j] = self.ROBOT
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = "_"  
                        if score is not None:
                            Best_score = max(score, Best_score)

            return Best_score
        else:
            Best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "_":
                        board[i][j] = self.PLAYER
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = "_"
                        if score is not None:
                            Best_score = min(score, Best_score)
            return Best_score
      
    def FindBestMove(self):
        # first find all the moves that the robot can do
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if self.BOARD[i][j] == "_":
                    self.BOARD[i][j] = self.ROBOT
                    score = self.minimax(self.BOARD, 0, False)
                    self.BOARD[i][j] = "_"
                    if score is not None:
                        if score > best_score:
                            best_score = score
                            best_move = [i,j]
        
        return best_move
    
    def set_move(self, i, j, ROBOT):
        if ROBOT:
            self.BOARD[i][j] = self.ROBOT
        else:
            self.BOARD[i][j] = self.PLAYER
        
        self.print_board()
        
    def game_over(self):
        result = self.check_winning_move(self.BOARD)
        if result == self.ROBOT:
            return True
        elif result == self.PLAYER:
            return True
        else:
            return False
        
ttt = tic_tac_toe()
turn_Player = random.randint(0, 1)
turn = 0

while True and turn < 9:
    time.sleep(0.05)
    if turn_Player:
        print("PLAYER turn")
        column = int(input("enter the columnm:"))
        row = int(input("enter the row"))
        ttt.set_move(row, column, False)
        
        if ttt.game_over():
            print("player has won")
            break
        
        turn_Player = False
        turn += 1
        
    else:
        print("ROBOT turn")
        best_move = ttt.FindBestMove()
        ttt.set_move(best_move[0],best_move[1],True)
        
        if ttt.game_over():
            print("robot has won")
            break
        
        turn_Player = True
        turn += 1 
        
if turn == 9:
    print("it's a tie")
    