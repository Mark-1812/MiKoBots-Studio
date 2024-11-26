

from backend.games.solve_connect4 import SolveConnect4  

import backend.core.variables as var
from backend.core.event_manager import event_manager

import numpy as np
import cv2
import math

from backend.vision import get_image_frame
from backend.vision import get_mask

class Connect4():
    def __init__(self):
        self.SolveConnect4 = SolveConnect4()
    
    def FindHumanMove(self, color):                    
        pieces_list = []
        width = 700
        height = 600
        
        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        mask = get_mask(color, image)
        
        
        rectified_image = cv2.warpPerspective(image, self.board_matrix, (width, height))
        
        mask = get_mask(color, rectified_image)
        self.height_picture, self.width_picture, ch = image.shape 

        column_width = round(width / 7)
        row_height = round(height / 6)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        image_RGB = cv2.warpPerspective(image_RGB, self.board_matrix, (width, height))

        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > 300:             
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.6 * h and w < 1.4 * h:
                    position_X = x 
                    position_Y = y 

                    column = 6 - round(position_X / column_width)
                    row = 5 - round(position_Y / row_height)

                    cv2.rectangle(image_RGB, (x, y), (x+w, y+h), (200, 200, 200), 2)
                    print(f"column: {column}, row: {row}")
                    pieces_list.append([[row],[column]])
                    
                    self.SolveConnect4.drop_piece(self.SolveConnect4.board, row, column, self.SolveConnect4.PLAYER_PIECE)
                
        self.SolveConnect4.print_board(self.SolveConnect4.board)

        posx = int(1/2 * column_width)
        for i in range(7):
            image_RGB = cv2.line(image_RGB, (posx,0), (posx, height), (255, 0, 0), 2)
            posx = posx + column_width

        posy = int(1/2 * row_height)
        for i in range(6):
            image_RGB = cv2.line(image_RGB, (0,posy), (width, posy), (255, 0, 0), 2)
            posy = posy + row_height

        event_manager.publish("request_set_pixmap_image", image_RGB)
        
    def DetectBoard(self, color): 
        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        mask = get_mask(color, image)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.height_picture, self.width_picture, ch = image.shape 

        x_mark = []
        y_mark = []
        
        width_mark = []
        height_mark = []
        
        x_average = 0
        y_average = 0
            

        width = 700
        height = 600         
            
        i = 0
        
        for contour in contours:
            if cv2.contourArea(contour) > 500 and cv2.contourArea(contour) < 12000:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.6 * h and w < 1.4 * h:
                    x_average = x_average + x
                    y_average = y_average + y
                    x_mark.append(x+(1/2*w)) 
                    y_mark.append(y+(1/2*h))
                    
                    width_mark.append(w)
                    height_mark.append(h)
                    
                    print(f"pos x: {x_mark[i]} pos y {y_mark[i]} size:{w*h}")
                    cv2.rectangle(image_RGB, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    i = i + 1
                    print(f"number of contours found {i}")
                
        stones = i
        if i == 4:
            x_average = x_average/4
            y_average = y_average/4

            j = 0
            for j in range(i):
                if x_mark[j] < x_average and y_mark[j] < y_average:
                    print(f"1pos x: {x_mark[j]} pos y {y_mark[j]}")
                    x1 = x_mark[j] - 1/2 * width_mark[j]
                    y1 = y_mark[j] - 1/2 * height_mark[j]
                if x_mark[j] < x_average and y_mark[j] > y_average:
                    print(f"2pos x: {x_mark[j]} pos y {y_mark[j]}")
                    x4 = x_mark[j] - 1/2 * width_mark[j]
                    y4 = y_mark[j] + 1/2 * height_mark[j]
                if x_mark[j] > x_average and y_mark[j] < y_average:
                    print(f"3pos x: {x_mark[j]} pos y {y_mark[j]}")
                    x2 = x_mark[j] + 1/2 * width_mark[j]
                    y2 = y_mark[j] - 1/2 * height_mark[j]
                if x_mark[j] > x_average and y_mark[j] > y_average:
                    print(f"4pos x: {x_mark[j]} pos y {y_mark[j]}")
                    x3 = x_mark[j] + 1/2 * width_mark[j]
                    y3 = y_mark[j] + 1/2 * height_mark[j]

            

            pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
            pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
            self.board_matrix = cv2.getPerspectiveTransform(pts1, pts2)
            
            image_RGB = cv2.warpPerspective(image_RGB, self.board_matrix, (width, height))
            
            column_width = round(width / 7)
            row_height = round(height / 6)

            posx = round(1/2 * column_width)
            for i in range(7):
                image_RGB = cv2.line(image_RGB, (posx,0), (posx, height), (255, 0, 0), 2)
                posx = posx + column_width

            posy = round(1/2 * row_height)
            for i in range(6):
                image_RGB = cv2.line(image_RGB, (0,posy), (width, posy), (255, 0, 0), 2)
                posy = posy + row_height
            
        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        if stones == 4:
            return True
        else:
            return False
        
    def GenerateMoveAi(self):
        col, minimax_score = self.SolveConnect4.minimax(self.SolveConnect4.board, 5, -math.inf, math.inf, True) 
        row = self.SolveConnect4.get_next_open_row(self.SolveConnect4.board, col)
        self.SolveConnect4.drop_piece(self.SolveConnect4.board, row, col, self.SolveConnect4.AI_PIECE)
        return col
                
    def CheckWinningMove(self):
        if self.SolveConnect4.winning_move(self.SolveConnect4.board, self.SolveConnect4.AI_PIECE):
            return True
        elif self.SolveConnect4.winning_move(self.SolveConnect4.board, self.SolveConnect4.PLAYER_PIECE):
            return True
        else:
            return False