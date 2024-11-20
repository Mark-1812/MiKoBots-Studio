from backend.vision import calculate_mm_per_pixel

import backend.core.variables as var
from backend.core.event_manager import event_manager


import cv2
import math
from backend.vision import get_image_frame
from backend.vision import get_mask

from backend.games import get_result_ttt
from backend.games import print_board_ttt
from backend.games import minimax_ttt
from backend.games import terminial_ttt


class TicTacToe():
    def __init__(self):
        self.width = 400
        self.height = 400
        self.s = [0, 0, 0, 0, 0, 0, 0, 0, 0]
 
    def DetectBoard(self, color):       
        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image_HSV = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)

        mm_per_pixel = calculate_mm_per_pixel(image_RGB)
        mask = get_mask(color, image_HSV)
        
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.height_picture, self.width_picture, ch = image_HSV.shape
        
        self.Objects = []
        x_average = 0
        y_average = 0   
        
        for contour in contours:
            # Filter out small contours
            
            if cv2.contourArea(contour) > 100:
                # Get the bounding box of the contour
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.7 * h and w < 1.3 * h:
                    cv2.rectangle(image_RGB, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    width_object = w * mm_per_pixel
                    height_object = h * mm_per_pixel
                    
                    Ycenter = x + (1/2) * w
                    if Ycenter > (self.width_picture / 2):
                        Yplace_from_center = (Ycenter - (self.width_picture / 2)) * mm_per_pixel
                    else:
                        Yplace_from_center = -((self.width_picture / 2) - Ycenter) * mm_per_pixel
                        
                    Xcenter = y + (1/2) * h
                    if Xcenter > (self.height_picture / 2):    
                        Xplace_from_center = (Xcenter - (self.height_picture / 2)) * mm_per_pixel
                    else:
                        Xplace_from_center = -((self.height_picture / 2) - Xcenter) * mm_per_pixel    
                        

                    # needs degrees not tool_turn_cam

                    # if var.TOOL_TURN_CAM == 1:
                    #     Yobject_place = round(-Yplace_from_center  + float(var.POS_AXIS[1]) - float(var.TOOL_OFFSET_CAM[1]),1)           
                    #     Xobject_place = round(-Xplace_from_center  + float(var.POS_AXIS[0]) - float(var.TOOL_OFFSET_CAM[0]),1)
                    # else:
                    #     Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                    #     Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                    
                    
                    # x_average = x_average + Xobject_place
                    # y_average = y_average + Yplace_from_center
                                        
                    
                    # self.Objects.append([[Xobject_place],[Yobject_place],[width_object],[height_object]])             
        
        event_manager.publish("request_set_pixmap_image", image_RGB)
        
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
                
                   
                


        return [Place_X, Place_Y, width_board, height_board]
                 
    def FindMoveHuman(self, color, board=list):      
        Place_X = board[0]
        Place_Y = board[1]
        width_board = board[2]
        height_board = board[3]
        
        column_width = width_board / 2
        row_height = height_board / 2
        
        # print(f"col {column_width} row{row_height}")

        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image_HSV = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        mm_per_pixel = calculate_mm_per_pixel(image_RGB)
                              
        mask = get_mask(color,image_HSV)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > 1000:             
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.8 * h and w < 1.2 * h:
                    cv2.rectangle(image_RGB, (x, y), (x+w, y+h), (200, 200, 200), 2)
                    
                    Ycenter = x + (1/2) * w
                    if Ycenter > (self.width_picture / 2):
                        Yplace_from_center = (Ycenter - (self.width_picture / 2)) * mm_per_pixel
                    else:
                        Yplace_from_center = -((self.width_picture / 2) - Ycenter) * mm_per_pixel
                        
                    Xcenter = y + (1/2) * h
                    # print(Xcenter)
                    if Xcenter > (self.height_picture / 2):    
                        Xplace_from_center = (Xcenter - (self.height_picture / 2)) * mm_per_pixel
                    else:
                        Xplace_from_center = -((self.height_picture / 2) - Xcenter) * mm_per_pixel    

                    # needs degrees not tool_turn_cam

                    # if var.TOOL_TURN_CAM == 1:
                    #     Yobject_place = round(-Yplace_from_center  + float(var.POS_AXIS[1]) - float(var.TOOL_OFFSET_CAM[1]),1)           
                    #     Xobject_place = round(-Xplace_from_center  + float(var.POS_AXIS[0]) - float(var.TOOL_OFFSET_CAM[0]),1)
                    # else:
                    #     Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                    #     Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                    
                    
                    # row = round((Xobject_place - Place_X) / column_width)
                    # if row < 0:
                    #     row = 0
                    # elif row > 2:
                    #     row = 2
                        
                    # column = round((Yobject_place - Place_Y) / row_height)
                    # if column < 0:
                    #     column = 0
                    # elif column > 2:
                    #     column = 2
                    
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

            
        

    


            
        