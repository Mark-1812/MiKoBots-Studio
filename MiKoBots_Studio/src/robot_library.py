




from backend.calculations.calculations_vision import calculate_mm_per_pixel

from backend.games.solve_connect4 import SolveConnect4  

import backend.core.variables as var
from backend.core.event_manager import event_manager


import re
import time
import numpy as np
import cv2
import math
import math
import os

from backend.core.api import send_line_to_io
from backend.core.api import send_line_to_robot
from backend.core.api import get_image_frame
from backend.core.api import get_mask
from backend.core.api import draw_axis

from backend.core.api import get_result_ttt
from backend.core.api import print_board_ttt
from backend.core.api import minimax_ttt
from backend.core.api import terminial_ttt

class Move():
    def __init__(self):
        event_manager.subscribe("request_robot_home", self.Home)   
        event_manager.subscribe("request_robot_jog_joint", self.JogJoint)   
        event_manager.subscribe("request_robot_move_j", self.MoveJ)   
        event_manager.subscribe("request_robot_offset_j", self.OffsetJ)   
        event_manager.subscribe("request_robot_move_joint_pos", self.MoveJointPos)   
    
        self.letters = [chr(i) for i in range(65, 91)]  # A-Z letters
    
    def MoveJ(self, pos, v = None, a = None, Origin = None):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(len(pos))
            print(var.NUMBER_OF_JOINTS)
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return
        
        if Origin:
            pos[0] = pos[0] + Origin[0]
            pos[1] = pos[1] + Origin[1]
            pos[2] = pos[2] + Origin[2]
        
        command = "MoveJ "
        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"            
            event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
                
    
    def OffsetJ(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return     
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return   
        
        command = "OffsetJ "

        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"            
            event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            
            send_line_to_robot(command)
        
        
    def JogJoint(self, pos, v = None, a = None):
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return
        
        if var.ROBOT_BUSY:
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]        
        
        command = "jogJ "
        
        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            event_manager.publish("simulate_program", False, command)
            
        elif var.ROBOT_CONNECT == 1:    
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
                
            send_line_to_robot(command)
        
    def MoveL(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]      

        command = "OffsetJ "
        
        
        # check if it is a simulation
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"                 
            event_manager.publish("simulate_program", False, command) 
            
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
                
    def OffsetL(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return    
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return   
        
        
            
        command += f"s{v} a{a}\n"  
        
        if var.SIM == 1:
            command = "OffsetL "
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            event_manager.publish("simulate_program", False, command)
            
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)

    def MoveJointPos(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return

        command = "MoveJoint "
        

        # check if the simulation is enables
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
            

    def Home(self):    
        if var.ROBOT_CONNECT == 1:
            command = "Home\n"
            send_line_to_robot(command)
            
class Tool():
    def __init__(self):
        event_manager.subscribe("request_change_pos_tool", self.MoveTo)   
        event_manager.subscribe("request_send_settings_tool", self.SetTool)   
        event_manager.subscribe("request_change_state_tool", self.State)   
        
        self.tool_number = None
        self.IO_BOX = None

    def SetTool(self, tool):
        for i in range(len(var.TOOLS3D)):
            if tool == os.path.splitext(var.TOOLS3D[i][0])[0]:
                self.tool_number = i
                
                self.type_of_tool = var.TOOLS3D[self.tool_number][7]
                if self.type_of_tool == "Servo":
                    self.servo_values = var.TOOLS3D[self.tool_number][8] 
                # if the tool is different than shown in the simulation change tool
                
                event_manager.publish("request_set_tool_combo", self.tool_number)
                
                # determine the pin number
                string_tool_nr = var.TOOLS3D[self.tool_number][6]
                number = int(string_tool_nr.split()[-1]) - 1
                tool_pin = var.SETTINGS["Set_tools"][0][number]
                                
                                
                if var.TOOLS3D[self.tool_number][7] == "Servo":
                    type_tool = 0
                if var.TOOLS3D[self.tool_number][7] == "Relay":
                    type_tool = 1
                if var.TOOLS3D[self.tool_number][7] == "None":
                    type_tool = 2
                     
                settings_tool = ("Set_tools A" + str(tool_pin) + "B" + str(type_tool) + "C" + str(var.TOOLS3D[self.tool_number][8][0]) + "D" + str(var.TOOLS3D[self.tool_number][8][1]) + "\n")      
                         
                tool_frame = "Set_tool_frame "
                letters = ['A','B','C','D','E','F']
                
                for i in range(6):
                    tool_frame += str(letters[i])
                    tool_frame += str(var.TOOLS3D[self.tool_number][5][i])
                    
                tool_frame += "\n"
                    
                # send settings to IO if this is given in settings
                if var.SETTINGS['Set_tools'][1] == "IO" and var.IO_CONNECT:
                    send_line_to_io(settings_tool)
                    self.IO_BOX = True
                    
                # send settings to ROBOT if this is given in settings    
                elif var.SETTINGS['Set_tools'][1] != "IO" and var.ROBOT_CONNECT:
                    send_line_to_robot(settings_tool)
                    self.IO_BOX = False   
                           
                # send always the tool frame only to the robot
                if var.ROBOT_CONNECT:
                    send_line_to_robot(tool_frame)
                
        if self.tool_number is None:
            print("Error: Do not regonize this tool")
    
    def MoveTo(self, pos):
        if self.type_of_tool == "Servo":
            # if simulation is enabled only change the value
            if var.SIM:
                var.TOOL_POS = pos
                event_manager.publish("request_set_tool_pos", pos)
            
            # command for tool to move
            command = f"Tool_move_to pos({pos})\n"
             
            if var.IO_CONNECT and self.IO_BOX:
                send_line_to_io(command)
                
            if var.ROBOT_CONNECT and not self.IO_BOX:
                send_line_to_robot(command)
        else:
            event_manager.publish("request_insert_new_log", var.LANGUAGE_DATA.get("message_not_move_tool")) 
    
    def State(self, state):
        if self.type_of_tool == "Relay" and (state == "HIGH" or state == "LOW"):
            
            if var.SIM:
                if state == "HIGH":
                    event_manager.publish("request_set_tool_state", True)
                elif state == "LOW":
                    event_manager.publish("request_set_tool_state", False)
                    
            command = f"Tool_state ({state})\n"
            
            if var.IO_CONNECT and self.IO_BOX:
                print("test1")
                send_line_to_io(command)
            if var.ROBOT_CONNECT and not self.IO_BOX:
                print("test2")
                send_line_to_robot(command)
        else:
            event_manager.publish("request_insert_new_log", var.LANGUAGE_DATA.get("message_not_state_tool")) 
            
class IO():
    def __init__(self):
        self.type = None
        self.IO_BOX = None

    
    def SetIO(self, pin_number, type):
        self.type = type
        self.IO_BOX = None
        
        if self.type == "INPUT" or self.type == "OUTPUT":
            # determine the pin number
            IO_pin = var.SETTINGS["Set_io_pin"][0][pin_number]
                    
            settings_io = f"Set_io_pin A{pin_number}B{IO_pin}C{self.type}\n"
            
            # send the settings to the IO box or the robot
            if var.SETTINGS["Set_io_pin"][1] == "IO" and var.IO_CONNECT:
                send_line_to_io(settings_io)
                self.IO_BOX = True
            elif var.SETTINGS["Set_io_pin"][1] != "IO" and var.ROBOT_CONNECT:
                send_line_to_robot(settings_io)
                self.IO_BOX = False
        else:
            print("error do not regonize this type, only INPUT or OUTPUT")        
    
    def digitalRead(self, pin_number):
        if self.type == "INPUT":
            
            IO_CHECK = event_manager.publish("request_check_io_state", pin_number)[0]
            
            if IO_CHECK:
                return True
            else:
                return False             
    
    
    def digitalWrite(self, pin_number, state):
        if self.type == "OUTPUT":
            if state == "HIGH":
                event_manager.publish("request_set_io_state", pin_number, True)
            elif state == "LOW":
                event_manager.publish("request_set_io_state", pin_number, False)
           
        if (not var.SIM and self.IO_BOX and var.IO_CONNECT) or (not var.SIM and not self.IO_BOX and var.ROBOT_CONNECT):       
            if self.type != "OUTPUT":   
                return
                     
            if state == "HIGH":
                # change the value of the IO pin in the control menu
                event_manager.publish("request_set_io_state", pin_number, True)
                
                command = f"IO_digitalWrite P{pin_number}S1\n"

                if self.IO_BOX:
                    send_line_to_io(command)
                elif not self.IO_BOX:
                    send_line_to_robot(command)
                                    
            elif state == "LOW":
                # change the value of the IO pin in the control menu
                event_manager.publish("request_set_io_state", pin_number, False)
                
                command = f"IO_digitalWrite P{pin_number}S0\n"
                
                if self.IO_BOX:
                    send_line_to_io(command)
                    
                elif not self.IO_BOX:
                    send_line_to_robot(command)
    
class Vision():
    def __init__(self):
        self.move = Move()
        self.Objects = None

    def FindObject(self, color = None):       
        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image_GRAY = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2GRAY) 
        
        image_GRAY = cv2.adaptiveThreshold(image_GRAY, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 399, 12)
        image_HSV = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        mm_per_pixel = calculate_mm_per_pixel(image_RGB)
        
        self.height_picture, self.width_picture, ch = image_RGB.shape 
        
        # get the contours of the color
        if color:
            mask_HSV = get_mask(color, image_HSV)
            kernel = np.ones((5, 5), np.uint8)
            mask_HSV = cv2.morphologyEx(mask_HSV, cv2.MORPH_OPEN, kernel)
            contours_HSV, _ = cv2.findContours(mask_HSV, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        self.Objects = []
        
        for contour in contours_HSV:
            # Filter out small contours
            sz = len(contour)
            data_contour = np.empty((sz, 2), dtype=np.float64)
            for i in range(data_contour.shape[0]):
                data_contour[i,0] = contour[i,0,0]
                data_contour[i,1] = contour[i,0,1]     
                
            mean = np.empty((0))
            mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_contour, mean)  
            
            cntr = (int(mean[0,0]), int(mean[0,1]))
            Xcenter = cntr[1]
            Ycenter = cntr[0]         

            height = round(np.sqrt(eigenvalues[0][0]) * mm_per_pixel, 2)
            width = round(np.sqrt(eigenvalues[1][0]) * mm_per_pixel, 2)
            
            if height > 5 and width > 5:
                
                ## [visualization]
                # Draw the principal components
                cv2.circle(image_RGB, cntr, 3, (255, 0, 255), 2)
                p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
                p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
                image_RGB = draw_axis(image_RGB, cntr, p1, (255, 255, 0), 1)
                image_RGB = draw_axis(image_RGB, cntr, p2, (0, 0, 255), 5)

                # here is the location found of the object in the camera, X and Y distance from center
                if Ycenter > (self.width_picture / 2):
                    Yplace_from_center = (Ycenter - (self.width_picture / 2)) * mm_per_pixel
                else:
                    Yplace_from_center = -((self.width_picture / 2) - Ycenter) * mm_per_pixel
                    
                if Xcenter > (self.height_picture / 2):    
                    Xplace_from_center = (Xcenter - (self.height_picture / 2)) * mm_per_pixel
                else:
                    Xplace_from_center = -((self.height_picture / 2) - Xcenter) * mm_per_pixel    


                # get the orientation of the position of the camera


                angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
                angle = round(math.degrees(angle),2)


                Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                
                    
                print(f"X {Xobject_place} Y {Yobject_place} width {width} height {height} angle {angle}")
                
                self.Objects.append([[Xobject_place], [Yobject_place], [width], [height], [angle], [color]])

        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        return self.Objects
    
    def MoveToObject(self, list_objects = list, number = int, Zdistance = float):
        self.RobotCommand = Move()

        POSXYZ = [0]*6
        
        POSXYZ[0] = list_objects[number][0][0] + float(var.TOOL_OFFSET_CAM[0])
        POSXYZ[1] = list_objects[number][1][0]
        POSXYZ[2] = 120
        POSXYZ[3] = 0
        POSXYZ[4] = 0
        POSXYZ[5] = 180        
        
        if (var.POS_AXIS[2] - Zdistance) < 130:
            POSXYZ[2] = Zdistance
            self.RobotCommand.MoveJ(pos=POSXYZ, v=50, a=50) 
        
        else:
            POSXYZ[2] = 120 + Zdistance
            
            print(f"position to move to {POSXYZ}")
            # move to the object stay 150 mm above
            self.RobotCommand.MoveJ(pos=POSXYZ, v=50, a=50)
            
            color = list_objects[0][5][0]
            
            time.sleep(0.5)
            objects = self.find_object(color)
            print(f"new X location {objects[0][0][0]}")
            print(f"new Y location {objects[0][1][0]}")

            X = list_objects[number][0][0]
            Y = list_objects[number][1][0]        
                    
            for i in range(len(objects)):
                X_object = objects[i][0][0] 
                Y_object = objects[i][1][0] 
                
                X_delta = abs(X - X_object)
                Y_delta = abs(Y - Y_object)
                print(f"X delta {X_delta} Y delta {Y_delta}")
                print(f"X size {list_objects[number][2][0]} Y size {list_objects[number][3][0]}")
                
                if X_delta < list_objects[number][2][0] * 3 and Y_delta < list_objects[number][3][0] * 3:
                    object_nr = i
                    break
            
            POSXYZ[0] = objects[object_nr][0][0]
            POSXYZ[1] = objects[object_nr][1][0]
            POSXYZ[2] = Zdistance
            print(f"position to move to {POSXYZ}")
            self.RobotCommand.MoveJ(pos=POSXYZ, v=50, a=50)   
     
class Connect4():
    def __init__(self):
        self.SolveConnect4 = SolveConnect4()
        print("connect4")     
    
    def FindMoveHuman(self, color):                    
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
        print(posx)    
        for i in range(7):
            image_RGB = cv2.line(image_RGB, (posx,0), (posx, height), (255, 0, 0), 2)
            posx = posx + column_width

        posy = int(1/2 * row_height)
        print(posy)
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
                
    def WinningMove(self, AI):
        if AI == True:
            if self.SolveConnect4.winning_move(self.SolveConnect4.board, self.SolveConnect4.AI_PIECE):
                return True
            else:
                return False
        elif AI == False:
            if self.SolveConnect4.winning_move(self.SolveConnect4.board, self.SolveConnect4.PLAYER_PIECE):
                return True
            else:
                return False

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
        
        print(len(contours))
        
        for contour in contours:
            # Filter out small contours
            
            if cv2.contourArea(contour) > 100:
                # Get the bounding box of the contour
                print("ok")
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
                        
                    if var.TOOL_TURN_CAM == 1:
                        Yobject_place = round(-Yplace_from_center  + float(var.POS_AXIS[1]) - float(var.TOOL_OFFSET_CAM[1]),1)           
                        Xobject_place = round(-Xplace_from_center  + float(var.POS_AXIS[0]) - float(var.TOOL_OFFSET_CAM[0]),1)
                    else:
                        Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                        Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                    
                    
                    x_average = x_average + Xobject_place
                    y_average = y_average + Yplace_from_center
                                        
                    
                    self.Objects.append([[Xobject_place],[Yobject_place],[width_object],[height_object]])             
        
        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        if len(self.Objects) == 4:
            x_average = x_average/4
            y_average = y_average/4
            
            print(f"average X {x_average} Y{y_average}")
            
            for i in range(len(self.Objects)):
                if self.Objects[i][0][0] < x_average and self.Objects[i][1][0] < y_average:
                    print(f"1pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x1 = self.Objects[i][0][0]
                    y1 = self.Objects[i][1][0]
                    print(self.Objects[i][0])
                    print(x1)
                if self.Objects[i][0][0] < x_average and self.Objects[i][1][0] > y_average:
                    print(f"4pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x4 = self.Objects[i][0][0]
                    y4 = self.Objects[i][1][0]
                if self.Objects[i][0][0] > x_average and self.Objects[i][1][0] < y_average:
                    print(f"2pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
                    x2 = self.Objects[i][0][0]
                    y2 = self.Objects[i][1][0]
                if self.Objects[i][0][0] > x_average and self.Objects[i][1][0] > y_average:
                    print(f"3pos x: {self.Objects[i][0]} pos y {self.Objects[i][1]}")
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
        
        print(f"col {column_width} row{row_height}")

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
                    print(Xcenter)
                    if Xcenter > (self.height_picture / 2):    
                        Xplace_from_center = (Xcenter - (self.height_picture / 2)) * mm_per_pixel
                    else:
                        Xplace_from_center = -((self.height_picture / 2) - Xcenter) * mm_per_pixel    
                        
                    if var.TOOL_TURN_CAM == 1:
                        Yobject_place = round(-Yplace_from_center  + float(var.POS_AXIS[1]) - float(var.TOOL_OFFSET_CAM[1]),1)           
                        Xobject_place = round(-Xplace_from_center  + float(var.POS_AXIS[0]) - float(var.TOOL_OFFSET_CAM[0]),1)
                    else:
                        Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                        Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                    
                    
                    row = round((Xobject_place - Place_X) / column_width)
                    if row < 0:
                        row = 0
                    elif row > 2:
                        row = 2
                        
                    column = round((Yobject_place - Place_Y) / row_height)
                    if column < 0:
                        column = 0
                    elif column > 2:
                        column = 2
                    
                    print(f"X{Xobject_place} Y{Yobject_place}")
                    print(f"column: {column}, row: {row}")
                    
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
        
        print(f"robot: row {row} column {column} ")     
                    
        Xobject_place = Place_X + (column_width * row)
        Yobject_place = Place_Y + (row_height * column)
                    
        return Xobject_place, Yobject_place
    
    def CheckWinningMove(self):  
        if terminial_ttt(self.s):
            return True
        else:
            return False

            
        

    


            
        