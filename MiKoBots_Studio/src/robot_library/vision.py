from backend.vision import calculate_mm_per_pixel
import backend.core.variables as var
from backend.core.event_manager import event_manager

import time
import numpy as np
import cv2
import math

from backend.vision import get_image_frame, check_cam_tool_connect
from backend.vision import get_mask
from backend.vision import draw_axis

from robot_library import Move

 
   
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

            x, y, bounding_w, bounding_h = cv2.boundingRect(contour)

            height = round(bounding_h * mm_per_pixel, 2)
            width = round(bounding_w * mm_per_pixel, 2)
            
            
            
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

                if Yplace_from_center > 0 and Xplace_from_center > 0:
                    angle_xy = math.atan(abs(Xplace_from_center) / abs(Yplace_from_center))
                    angle = 270 + math.degrees(angle_xy)

                elif Yplace_from_center > 0 and Xplace_from_center < 0:
                    angle_xy = math.atan(abs(Yplace_from_center) / abs(Xplace_from_center))
                    angle = 180 + math.degrees(angle_xy)

                elif Yplace_from_center < 0 and Xplace_from_center < 0:
                    angle_xy = math.atan(abs(Xplace_from_center) / abs(Yplace_from_center))
                    angle = 90 + math.degrees(angle_xy)

                elif Yplace_from_center < 0 and Xplace_from_center > 0:
                    angle_xy = math.atan(abs(Yplace_from_center) / abs(Xplace_from_center))
                    angle = math.degrees(angle_xy)

                radius = math.sqrt(pow(Xplace_from_center, 2) + pow(Yplace_from_center, 2))

                camera_settings = event_manager.publish("request_get_offset_cam")[0]
                angle_camera = camera_settings[2]

                new_angle = angle_camera + angle
                if new_angle > 360:
                    new_angle = new_angle - 360
                    
                # get x and Y location of the objects
                if new_angle >= 0 and new_angle < 90:
                    # Y negative X positive
                    
                    angle_radians = math.radians(new_angle)
                    pos_y = radius * math.sin(angle_radians)
                    pos_x = radius * math.cos(angle_radians)
                    
                    pos_x = pos_x * -1 # make x position negative
                    
                elif new_angle >= 90 and new_angle < 180:
                    # X negative Y negative
                    
                    angle_radians = math.radians(new_angle - 90)
                    pos_x = radius * math.sin(angle_radians)
                    pos_y = radius * math.cos(angle_radians)
                   
                elif new_angle >= 180 and new_angle < 270:
                    # X negative Y positive
                    
                    angle_radians = math.radians(new_angle - 180)
                    pos_y = radius * math.sin(angle_radians)
                    pos_x = radius * math.cos(angle_radians)
                    
                    pos_y = pos_y * -1
                    
                elif new_angle >= 270 and new_angle < 360:
                    # X negative Y positive
                    
                    angle_radians = math.radians(new_angle - 270)
                    pos_x = radius * math.sin(angle_radians)
                    pos_y = radius * math.cos(angle_radians)

                    pos_y = pos_y * -1
                    pos_x = pos_x * -1

                # get the orientation of the position of the camera

 
                angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
                angle = round(math.degrees(angle),2)

                # check if the camera is connected to the camera
                # if not the location of the camera is static

                cam_tool = check_cam_tool_connect()

                if cam_tool:
                    # get the rotation of the camera how it is connected to the tool
                    Yobject_place = round(pos_y  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                    Xobject_place = round(pos_x  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                else:
                    # get the cent lace of the camera out of the settings'
                    # get the rotation of the camera out of the settings

                    offset = event_manager.publish("request_get_offset_cam")[0]
                    
                    x_offset = offset[0]
                    y_offset = offset[1]
                    
                    Yobject_place = round(pos_y  + y_offset, 1)          
                    Xobject_place = round(pos_x  + x_offset, 1)
                
                print(f"x {Xobject_place}, y {Yobject_place}, height {height}, width {width}")

                self.Objects.append([Xobject_place, Yobject_place, width, height, angle, color])
                
                
        # check if there are no dounbles is the object list
        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        return self.Objects
    
    def MoveToObject(self, list_objects = list, Zdistance = int, vel = 50, accel = 50, check = None):
        self.RobotCommand = Move()
        number_of_joints = var.NUMBER_OF_JOINTS

        if number_of_joints == 6:
            POSXYZ = [0]*6
            
            POSXYZ[0] = list_objects[0]
            POSXYZ[1] = list_objects[1]
            POSXYZ[2] = Zdistance
            POSXYZ[3] = 0
            POSXYZ[4] = 0
            POSXYZ[5] = 180     
        elif number_of_joints == 3:
            POSXYZ = [0]*3
            
            POSXYZ[0] = list_objects[0]
            POSXYZ[1] = list_objects[1]
            POSXYZ[2] = Zdistance             
        
        
        # check if the camera is connected to the tool
        if not check_cam_tool_connect() or not check:
            # Move to the object with the given Z distance
            self.RobotCommand.MoveJ(pos=POSXYZ, v = vel, a = accel) 
        else:
            # Do an extra check at 120 mm above the given z distance
            POSXYZ[2] += 120
            self.RobotCommand.MoveJ(pos=POSXYZ, v = vel, a = accel)
            
            # check the color of the object out of the lsit
            color = list_objects[0][5]
            
            time.sleep(0.5)
            objects = self.FindObject(color)

            X = list_objects[0]
            Y = list_objects[1]        
                    
            # if it sees multiples object pick the object that is closed to the object
            for i in range(len(objects)):
                X_object = objects[i][0]
                Y_object = objects[i][1] 
                
                X_delta = abs(X - X_object)
                Y_delta = abs(Y - Y_object)
                # print(f"X delta {X_delta} Y delta {Y_delta}")
                # print(f"X size {list_objects[number][2]} Y size {list_objects[number][3]}")
                
                if X_delta < list_objects[2] * 3 and Y_delta < list_objects[3] * 3:
                    object_nr = i
                    break
                
            # when the object is found move to the location of the obejct
            POSXYZ[0] = objects[object_nr][0]
            POSXYZ[1] = objects[object_nr][1]
            POSXYZ[2] = Zdistance
            self.RobotCommand.MoveJ(pos=POSXYZ, v = vel, a = accel)   