from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

from backend.robot_management.robot_communication import TalkWithRobot
from backend.robot_management.robot_communication import TalkWithIO

from backend.calculations.calculations_vision import calculate_mm_per_pixel

from backend.games.solve_connect4 import SolveConnect4  
from backend.games.solve_tac_tact_toe import solveTicTacToe

from backend.vision.vision_management import VisionManagement
import backend.vision.vision_var as VD

import backend.core.variables as var
from backend.core.event_manager import event_manager




import re
import time
import tkinter.messagebox
import numpy as np
import cv2
import math
import math
import threading
import os

class Move():
    def __init__(self):#, robot):
        self.TalkWithRobot = TalkWithRobot()
        

        
        # for i in range(len(var.ROBOTS)):
        #     if robot == var.ROBOTS[i][0]:
                
        #         if i != var.SELECTED_ROBOT:                   
        #             event_manager.publish("request_set_robot", i)   
                      
    
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
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_AXIS[i]}{pos[i]} "
            
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]
            
        command += f"s{v} a{a}\n"
        
        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            self.TalkWithRobot.SendLineToRobot(command)
    
    def OffsetJ(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return     
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return   
        
        command = "OffsetJ "
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_AXIS[i]}{pos[i]} "
            
        command += f"s{v} a{a}\n"
        
        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            self.TalkWithRobot.SendLineToRobot(command)
        
    def JogJoint(self, pos, v = None, a = None):
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return
        
        command = "jogJ "
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]
            
        command += f"s{v} a{a}\n"
        
        print(command)
        
        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1:      
            if not var.PROGRAM_RUN and var.ROBOT_BUSY:
                return
            self.TalkWithRobot.SendLineToRobot(command)
        
    def MoveL(self, pos, a = 50, v = 50, Origin = None):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return
        
        if Origin:
            pos[0] += Origin[0]
            pos[1] += Origin[1]
            pos[2] += Origin[2]

        command = "OffsetJ "
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_AXIS[i]}{pos[i]} "
            
        command += f"s{v} a{a}\n"      
        
        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            var.ROBOT_BUSY = 1
            self.TalkWithRobot.SendLineToRobot(command)
                
    def OffsetL(self, pos, a = 50, v = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return    
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return   
        
        command = "OffsetL "
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_AXIS[i]}{pos[i]} "
            
        command += f"s{v} a{a}\n"  
        
        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            if not var.PROGRAM_RUN:
                var.ROBOT_BUSY = 1
            self.TalkWithRobot.SendLineToRobot(command)   

    def MoveJointPos(self, pos, a = 50, v = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print("Error, this command MoveJ has more input axis than that are joints")
            event_manager.publish("request_stop_sim")
            return

        command = "MoveJoint "
        for i in range(var.NUMBER_OF_JOINTS):
            command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            
        command += f"s{v} a{a}\n"

        if var.SIM == 1:
            if var.SIM_SHOW_LINE == 1:
                event_manager.publish("simulate_program", True, command)
            else:
                event_manager.publish("simulate_program", False, command)
        else: 
            
            self.TalkWithRobot.SendLineToRobot(command)    
            
    # def origin(self, name, pos):
    #     pass

    def Home(self):
        command = "Home\nEnd\n"
        
        if var.ROBOT_CONNECT == 1:
            self.TalkWithRobot.SendLineToRobot(command)
        else:
            tkinter.messagebox.showerror("Error", "Robot is not connected")
            
class Tool():
    def __init__(self, tool):
        self.tool_number = None
        self.TalkWithIO = TalkWithIO()
        self.TalkWithRobot = TalkWithRobot()
        
        self.IO_BOX = None

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
                     
                settings_tool = ("Set_tools A" + str(tool_pin) + "B" + str(type_tool) + "C" + str(var.TOOLS3D[self.tool_number][8][0]) + "D" + str(var.TOOLS3D[self.tool_number][8][1]) + "\n")      
                         
                tool_frame = "Set_tool_frame "
                letters = ['A','B','C','D','E','F']
                
                for i in range(6):
                    tool_frame += str(letters[i])
                    tool_frame += str(var.TOOLS3D[self.tool_number][5][i])
                    
                tool_frame += "\n"
                    
                if var.SETTINGS['Set_tools'][1] == "IO" and var.IO_CONNECT:
                    self.TalkWithIO.send_to_IO(settings_tool)
                    self.IO_BOX = True
                elif var.ROBOT_CONNECT:
                    self.TalkWithRobot.SendLineToRobot(settings_tool)
                    self.IO_BOX = False   
                           
                # send tool frame only to the robot
                if var.ROBOT_CONNECT:
                    self.TalkWithRobot.SendLineToRobot(tool_frame)
                
                # send the settings of the tool to the robot
                # var.TOOLS3D[i][5] = [0,0,0,0,0,0] # Tool frame
                # var.TOOLS3D[i][6] = "Tool pin 1" # Tool pin number
                # var.TOOLS3D[i][7] = "None" # Type of tool pin (Servo or relay)
                # var.TOOLS3D[i][8] = ["min","max"] # min and max value
                
        if self.tool_number is None:
            print("Do not regonize this tool")
    
    def moveTo(self, pos):
        if self.type_of_tool == "Servo":
            if var.SIM:
                var.TOOL_POS = pos
                event_manager.publish("request_set_tool_pos", pos)
            
            command = f"Tool_move_to pos({pos})\n"
            if var.IO_CONNECT and self.IO_BOX:
                self.TalkWithIO.send_to_IO(command)
            if var.ROBOT_CONNECT and not self.IO_BOX:
                self.TalkWithRobot.SendLineToRobot(command)  
        else:
            print("with this tool you cannot do this command")
    
    def state(self, state):
        print(self.type_of_tool)
        print("state" + state)
        if self.type_of_tool == "Relay" and (state == "HIGH" or state == "LOW"):
            print("test")
            
            if var.SIM:
                if state == "HIGH":
                    event_manager.publish("request_set_tool_state", True)
                elif state == "LOW":
                    event_manager.publish("request_set_tool_state", False)
                    
            command = f"Tool_state ({state})\n"
            if var.IO_CONNECT and self.IO_BOX:
                self.TalkWithIO.send_to_IO(command)
            if var.ROBOT_CONNECT and not self.IO_BOX:
                self.TalkWithRobot.SendLineToRobot(command)
        else:
            print("with this tool you cannot do this command")  
            
class IO():
    def __init__(self, number, type):
        self.TalkWithIO = TalkWithIO()
        self.TalkWithRobot = TalkWithRobot()
        
        self.type = type
        self.IO_BOX = None
        self.IO_number = number
        
        if self.type == "INPUT" or self.type == "OUTPUT":
            # determine the pin number
            IO_pin = var.SETTINGS["Set_io_pin"][0][self.IO_number]
                    
            settings_io = f"Set_IO_pin A{self.IO_number}B{IO_pin}C{self.type}\n"
            
            # send the settings to the IO box or the robot
            if var.SETTINGS["Set_io_pin"][1] == "IO" and var.IO_CONNECT:
                self.TalkWithIO.SendLineToIO(settings_io)
                self.IO_BOX = True
                print("IO box")
            elif var.ROBOT_CONNECT:
                self.TalkWithRobot.SendLineToRobot(settings_io)
                self.IO_BOX = False
                print("no io box")  
        else:
            print("error do not regonize this type, only INPUT or OUTPUT") 
 
        
    def digitalRead(self):
        if self.type == "INPUT":
            
            IO_CHECK = event_manager.publish("request_check_io_state", self.IO_number)[0]
            
            if IO_CHECK:
                return True
            else:
                return False             
    
    
    def digitalWrite(self, state):
        if var.SIM and self.type == "OUTPUT":
            if state == "HIGH":
                event_manager.publish("request_set_io_state", self.IO_number, True)
            elif state == "LOW":
                event_manager.publish("request_set_io_state", self.IO_number, False)
                     
        if self.type == "OUTPUT" and var.IO_CONNECT:        
            if state == "HIGH":
                event_manager.publish("request_set_io_state", self.IO_number, True)
                command = f"IO_digitalWrite P{self.IO_number}S1\n"

                if self.IO_BOX:
                    self.TalkWithIO.SendLineToIO(command)
                elif not self.IO_BOX:
                    self.TalkWithRobot.SendLineToRobot(command)
                                      
            elif state == "LOW":
                event_manager.publish("request_set_io_state", self.IO_number, False)
                command = f"IO_digitalWrite P{self.IO_number}S0\n"
                self.TalkWithIO.SendLineToIO(command)
  
class Gcode():
    def __init__(self):
        self.robot = TalkWithRobot()
        self.move = Move()
        
    def setOrigin(self, X, Y, Z):
        self.X_origin = X
        self.Y_origin = Y
        self.Z_origin = Z
            
    def run(self):        
        new_command = []       
        
        ## get the gcode file information      
        
        Gcode_program = event_manager.publish("request_gcode_text_get")[0]
        print(f"Gcode_program {Gcode_program}")
        lines_gcode = Gcode_program.split('\n')
        
        X = self.X_origin
        Y = self.Y_origin
        Z = self.Z_origin
        
        
        for line in lines_gcode:
            matchX = re.search(r'X(\d+\.\d+|\d+)', line)
            matchY = re.search(r'Y(\d+\.\d+|\d+)', line)
            matchZ = re.search(r'Z(\d+\.\d+|\d+)', line)
            
            if matchX:
                X = round(float(self.X_origin) + float(matchX.group(1)),2)
            
            if matchY:
                Y = round(float(self.Y_origin) + float(matchY.group(1)),2)
            
            if matchZ:    
                Z = round(float(self.Z_origin) + float(matchZ.group(1)),)
            
            y = 90
            p = 0
            r = 180
                
            if X != 0 or Y != 0 or Z != 0:
                words = line.split()
                if words:
                    first_word_1 = words[0]
                    if first_word_1 == "G01":
                        command = f"MoveJ X{X} Y{Y} Z{Z} y{y} p{p} r{r} s{5} a{5}"                                                         
                        new_command.append(command + "\n")
                        if var.SIM:
                            print(command)
                            self.move.MoveJ([X,Y,Z,y,p,r], 10 , 10)
                    elif first_word_1 == "G00":
                        command = f"MoveJ X{X} Y{Y} Z{Z} y{y} p{p} r{r} s{5} a{5}"                                                         
                        new_command.append(command + "\n")
                        if var.SIM:
                            print(command)
                            self.move.MoveJ([X,Y,Z,y,p,r], 10 , 10)
        if var.SIM == 0:                
            self.robot.send_multiple_lines(new_command)
    
class Vision():
    def __init__(self):
        print("vision")
        self.cam = VisionManagement()
        self.move = Move()
          
    def search_area(self, Place = list, Size = list, color = None, shape = None):
        
        mm_per_pixel = calculate_mm_per_pixel(Height=340)
        CamSizeY, CamSizeX, ch = VD.image_RGB.shape
         
        def threadVision():
            frames_X = math.ceil(float(Size[0]) / (CamSizeX * mm_per_pixel))
            frame_X_size = float(Size[0]) / frames_X
            print(f"{frames_X} = {float(Size[0])} * {(CamSizeX * mm_per_pixel)}")
            
            frames_Y = math.ceil(float(Size[1]) / (CamSizeY * mm_per_pixel))
            frame_Y_size = float(Size[1]) / frames_Y
            print(frames_Y)
            
            objects_found = []
            
            for i in range(frames_X):
                X = (0.5 * frame_X_size) + (i * frame_X_size) + Place[0]
                for j in range(frames_Y):
                    Y = (0.5 * frame_Y_size) + (j * frame_Y_size) + Place[1]
                    
                    LINE = f"MoveJ X{X} Y{Y} Z340 y0 p0 r180 s50 a50\n"
                    
                    self.move.MoveJ([X,Y,340,0,0,180],50,50)
                    
                    while round(var.POS_AXIS[1],0) != round(Y,0):
                        time.sleep(0.05)                       
                    
                    new_objects_found = self.find_object(color)
                    objects_found = self.find_uniek_objects(objects_found, new_objects_found)
            
            print(f"number of objexts found {len(objects_found)}")
            
            return objects_found
                
        t_threadVision = threading.Thread(target=threadVision)  
        t_threadVision.start()
        
    def find_uniek_objects(self, objects_found, new_objects):
        new_list = objects_found
        for i in range(len(new_objects)):
            equal = 0
            X_new = new_objects[i][0][0]
            Y_new = new_objects[i][1][0]
                
            for j in range(len(objects_found)):
                X_old = objects_found[j][0][0]
                Y_old = objects_found[j][1][0]

                X_delta = abs(X_old - X_new)
                Y_delta = abs(Y_old - Y_new)
                print(X_delta)
                
                if X_delta < objects_found[i][2][0] and Y_delta < objects_found[i][3][0]:
                    equal = 1
                    break

            if equal == 0:
                new_list.append(new_objects[i])
        
        return new_list

    def drawAxis(self, img, p_, q_, color, scale):
        p = list(p_)
        q = list(q_)

        ## [visualization1]
        angle = math.atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
        hypotenuse = math.sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

        # Here we lengthen the arrow by a factor of scale
        q[0] = p[0] - scale * hypotenuse * math.cos(angle)
        q[1] = p[1] - scale * hypotenuse * math.sin(angle)
        cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

        # create the arrow hooks
        p[0] = q[0] + 9 * math.cos(angle + math.pi / 4)
        p[1] = q[1] + 9 * math.sin(angle + math.pi / 4)
        cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

        p[0] = q[0] + 9 * math.cos(angle - math.pi / 4)
        p[1] = q[1] + 9 * math.sin(angle - math.pi / 4)
        cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
        ## [visualization1]
        
        return img

    def find_object(self, color = None, size = None):       
        mm_per_pixel = calculate_mm_per_pixel()
        
        image_RGB = VD.image_RGB
        cv2.imwrite('input_img.jpg', image_RGB)
        image_GRAY = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2GRAY)
        
        #image_GRAY = cv2.equalizeHist(image_GRAY)
        
        image_GRAY = cv2.adaptiveThreshold(image_GRAY, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 399, 12)
        image_HSV = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        # get the contours of the color
        if color:
            mask_HSV = self.cam.mask(color, image_HSV)
            kernel = np.ones((5, 5), np.uint8)
            mask_HSV = cv2.morphologyEx(mask_HSV, cv2.MORPH_OPEN, kernel)
            contours_HSV, _ = cv2.findContours(mask_HSV, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
   
        # get the contour of the color            
        _, mask_GRAY = cv2.threshold(image_GRAY, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)         
        contours_GRAY, _ = cv2.findContours(mask_GRAY, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
               
        self.height_picture, self.width_picture, ch = image_RGB.shape 
        self.Objects = []    

        new_contours = []
        for contour in contours_GRAY:
            area = cv2.contourArea(contour)
            #print(area)
            if area < 1000 or 100000 < area:
                continue
            
            sz = len(contour)
            data_contour = np.empty((sz, 2), dtype=np.float64)
            for i in range(data_contour.shape[0]):
                data_contour[i,0] = contour[i,0,0]
                data_contour[i,1] = contour[i,0,1]
                
            mean = np.empty((0))
            mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_contour, mean)
            
            center_x_gray = int(mean[0,0])
            center_y_gray = int(mean[0,1])
            #print(f"X {center_x_gray} Y {center_y_gray}")
            
            # check if size is correct
            width = np.sqrt(eigenvalues[0]) * mm_per_pixel
            height = np.sqrt(eigenvalues[1]) * mm_per_pixel
            
            Size = True
            """
            if size:
                if (size[0] < 1.05 * height) or (size[0] > 0.95 * height) or (size[0] < 1.05 * height) or (size[1] > 0.95 * width):
                    Size = True
                else:
                    Size = False
            else:
                Size = True
                
from vision.tic_tac_toe.functions import TicTacToe_functions
from vision.vision_functions import VisionFunctions

vision = VisionFunctions()

vision.find_object(color = None, size = [50,20])
                
            """
            if Size and color: 
                for contour_HSV in contours_HSV:
                    area = cv2.contourArea(contour_HSV)
                    #print(f"area colors {area}")
                    if area > 300 or 100000 < area:
                        x, y, w, h = cv2.boundingRect(contour_HSV)
                        center_x_hsv = x + 1/2 * w
                        center_y_hsv = y + 1/2 * h
                        #cv2.rectangle(image_RGB, (x, y), (x+w, y+h), (200, 200, 200), 2)
                        #print(f"color X {center_x_hsv} Y {center_y_hsv} w {w} h {h}")
                        if center_x_gray < (1/2 * w + center_x_hsv) and center_x_gray > (center_x_hsv - 1/2 * w):
                            if center_y_gray < (1/2 * h + center_y_hsv) and center_y_gray > (center_y_hsv - 1/2 * h):                   
                                new_contours.append(contour)
                                break
            elif not color:
                new_contours.append(contour)
                    
                    
        cv2.drawContours(image_RGB, new_contours, -1, (200, 200, 200), 5)
        
        for contour in new_contours:
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
            
            ## [visualization]
            # Draw the principal components
            cv2.circle(image_RGB, cntr, 3, (255, 0, 255), 2)
            p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
            p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
            image_RGB = self.drawAxis(image_RGB, cntr, p1, (255, 255, 0), 1)
            image_RGB = self.drawAxis(image_RGB, cntr, p2, (0, 0, 255), 5)

            height = round(np.sqrt(eigenvalues[0][0]) * mm_per_pixel, 2)
            width = round(np.sqrt(eigenvalues[1][0]) * mm_per_pixel, 2)

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

            if var.TOOL_TURN_CAM == 1:
                Yobject_place = round(-Yplace_from_center  + float(var.POS_AXIS[1]) - float(var.TOOL_OFFSET_CAM[1]),1)           
                Xobject_place = round(-Xplace_from_center  + float(var.POS_AXIS[0]) - float(var.TOOL_OFFSET_CAM[0]),1)
            else:
                Yobject_place = round(Yplace_from_center  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                Xobject_place = round(Xplace_from_center  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                
            print(f"X {Xobject_place} Y {Yobject_place} width {width} height {height} angle {angle}")
            
            self.Objects.append([[Xobject_place], [Yobject_place], [width], [height], [angle], [color]])

        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        return self.Objects
    
    def move_to_object(self, list_objects = list, number = int, Zdistance = float):
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
        self.vision_management = VisionManagement()
        self.SolveConnect4 = SolveConnect4()
        print("connect4")     
    
    def FindMoveHuman(self, color):                    
        pieces_list = []
        width = 700
        height = 600
        mask, image = self.vision_management.mask_image(color)
        
        rectified_image = cv2.warpPerspective(image, self.board_matrix, (width, height))
        
        mask = self.vision_management.mask(color, rectified_image)
        self.height_picture, self.width_picture, ch = image.shape 

        column_width = round(width / 7)
        row_height = round(height / 6)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        RGB_image = cv2.warpPerspective(VD.image_RGB, self.board_matrix, (width, height))

        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > 300:             
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.6 * h and w < 1.4 * h:
                    position_X = x 
                    position_Y = y 

                    column = 6 - round(position_X / column_width)
                    row = 5 - round(position_Y / row_height)

                    cv2.rectangle(RGB_image, (x, y), (x+w, y+h), (200, 200, 200), 2)
                    print(f"column: {column}, row: {row}")
                    pieces_list.append([[row],[column]])
                    
                    self.SolveConnect4.drop_piece(self.SolveConnect4.board, row, column, self.SolveConnect4.PLAYER_PIECE)
                
        self.SolveConnect4.print_board(self.SolveConnect4.board)

        posx = int(1/2 * column_width)
        print(posx)    
        for i in range(7):
            RGB_image = cv2.line(RGB_image, (posx,0), (posx, height), (255, 0, 0), 2)
            posx = posx + column_width

        posy = int(1/2 * row_height)
        print(posy)
        for i in range(6):
            RGB_image = cv2.line(RGB_image, (0,posy), (width, posy), (255, 0, 0), 2)
            posy = posy + row_height

        event_manager.publish("request_set_pixmap_image", RGB_image)
        
    def DetectBoard(self, color):       
        mask, image = self.vision_management.mask_image(color)
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
        
        RGB_image = VD.image_RGB
        
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
                    cv2.rectangle(RGB_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
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
            
            RGB_image = cv2.warpPerspective(RGB_image, self.board_matrix, (width, height))
            
            column_width = round(width / 7)
            row_height = round(height / 6)

            posx = round(1/2 * column_width)
            for i in range(7):
                RGB_image = cv2.line(RGB_image, (posx,0), (posx, height), (255, 0, 0), 2)
                posx = posx + column_width

            posy = round(1/2 * row_height)
            for i in range(6):
                RGB_image = cv2.line(RGB_image, (0,posy), (width, posy), (255, 0, 0), 2)
                posy = posy + row_height
            
        event_manager.publish("request_set_pixmap_image", RGB_image)
        
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
        self.cam = VisionManagement()
        self.solveTicTacToe = solveTicTacToe()
        self.s = [self.solveTicTacToe.BOARD_EMPTY for _ in range(9)]
 
    def DetectBoard(self, color):       
        mm_per_pixel = calculate_mm_per_pixel()
        
        RGB_image = VD.image_RGB
        image_HSV = cv2.cvtColor(RGB_image, cv2.COLOR_RGB2HSV)

        mask = self.cam.mask(color, image_HSV)
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
                    cv2.rectangle(RGB_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
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
        
        event_manager.publish("request_set_pixmap_image", RGB_image)
        
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
        mm_per_pixel = calculate_mm_per_pixel()
        
        Place_X = board[0]
        Place_Y = board[1]
        width_board = board[2]
        height_board = board[3]
        
        column_width = width_board / 2
        row_height = height_board / 2
        
        print(f"col {column_width} row{row_height}")

        RGB_image = VD.image_RGB
        image_HSV = cv2.cvtColor(RGB_image, cv2.COLOR_RGB2HSV)
                              
        mask = self.cam.mask(color,image_HSV)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > 1000:             
                x, y, w, h = cv2.boundingRect(contour)
                if w > 0.8 * h and w < 1.2 * h:
                    cv2.rectangle(RGB_image, (x, y), (x+w, y+h), (200, 200, 200), 2)
                    
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
                    self.s = self.solveTicTacToe.result(self.s, (1, index))
                    
        self.solveTicTacToe.print_board(self.s)
 
        
        event_manager.publish("request_set_pixmap_video", RGB_image)
        
    def GenerateMoveAi(self, board):
        action = self.solveTicTacToe.minimax(self.s)
        
        self.s = self.solveTicTacToe.result(self.s, action[0])
        self.solveTicTacToe.print_board(self.s)
        
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
        if self.solveTicTacToe.terminal(self.s):
            return True
        else:
            return False

            
        

    


            
        