from backend.core.event_manager import event_manager


import math

from backend.games import get_result_ttt
from backend.games import print_board_ttt
from backend.games import minimax_ttt
from backend.games import terminial_ttt

from robot_library import Vision

class TicTacToe():
    def __init__(self):
        self.width = 400
        self.height = 400
        self.s = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.vision = Vision()
 
    def DetectBoard(self, color):       
        ### FInd objects
        
        self.Objects = self.vision.FindObject(color=color)
        
        x_average = 0
        y_average = 0  

        if len(self.Objects) == 4:
            x_average = x_average/4
            y_average = y_average/4
            
            for i in range(len(self.Objects)):
                if self.Objects[i][0][0] < x_average and self.Objects[i][1][0] < y_average:
                    # print(f"1pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x1 = self.Objects[i][0][0]
                    y1 = self.Objects[i][1][0]
                    # print(self.Objects[i][0])
                    # print(x1)
                if self.Objects[i][0][0] < x_average and self.Objects[i][1][0] > y_average:
                    # print(f"4pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x4 = self.Objects[i][0][0]
                    y4 = self.Objects[i][1][0]
                if self.Objects[i][0][0] > x_average and self.Objects[i][1][0] < y_average:
                    # print(f"2pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x2 = self.Objects[i][0][0]
                    y2 = self.Objects[i][1][0]
                if self.Objects[i][0][0] > x_average and self.Objects[i][1][0] > y_average:
                    # print(f"3pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x3 = self.Objects[i][0][0]
                    y3 = self.Objects[i][1][0]
                    

            Place_X = x1
            Place_Y = y1
            
            width_board = x2 - x1
            height_board = y4 - y1
                
        board = [Place_X, Place_Y, width_board, height_board]
        print(board)

        return board
                 
    def FindMoveHuman(self, color, board=list):   
        # X Y coordinates board   
        board_x = board[0]
        board_Y = board[1]

        width_board = board[2]
        height_board = board[3]
        
        column_width = width_board / 2
        row_height = height_board / 2
        
        # print(f"col {column_width} row{row_height}")

        objects = self.vision.FindObject(color=color)

        for object in objects:
            object_x = object[0]
            object_y = object[1]
                    
            row = round((object_x - board_x) / column_width)
            if row < 0:
                row = 0
            elif row > 2:
                row = 2
                
            column = round((object_y - board_Y) / row_height)
            if column < 0:
                column = 0
            elif column > 2:
                column = 2
            
            # print(f"X{Xobject_place} Y{Yobject_place}")
            # print(f"column: {column}, row: {row}")
            
            index = 3 * row + column
            self.s = get_result_ttt(self.s, (1, index))
                    
        print_board_ttt(self.s)
 
        event_manager.publish("request_set_pixmap_video", image_RGB)
        
    def GenerateMoveAi(self, board):
        action = minimax_ttt(self.s)
        
        self.s = get_result_ttt(self.s, action[0])
        print_board_ttt(self.s)
        
        
        column = action[0][1] % 3
        row = math.floor(action[0][1]/3)
                    
        Place_X = board[0]
        Place_Y = board[1]
        width_board = board[2]
        height_board = board[3]
 
        column_width = width_board / 2
        row_height = height_board / 2 
        
        # print(f"robot: row {row} column {column} ")     
                    
        Xobject_place = Place_X + (column_width * row)
        Yobject_place = Place_Y + (row_height * column)
                    
        return Xobject_place, Yobject_place
    
    def CheckWinningMove(self):  
        if terminial_ttt(self.s):
            return True
        else:
            return False

            
        

    


            
        