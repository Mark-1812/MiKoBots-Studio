from backend.calculations.calculations_vision import calculate_mm_per_pixel
import backend.core.variables as var
from backend.core.event_manager import event_manager

import time
import numpy as np
import cv2
import math

from backend.vision import get_image_frame
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
            
            # print(f"position to move to {POSXYZ}")
            # move to the object stay 150 mm above
            self.RobotCommand.MoveJ(pos=POSXYZ, v=50, a=50)
            
            color = list_objects[0][5][0]
            
            time.sleep(0.5)
            objects = self.find_object(color)
            # print(f"new X location {objects[0][0][0]}")
            # print(f"new Y location {objects[0][1][0]}")

            X = list_objects[number][0][0]
            Y = list_objects[number][1][0]        
                    
            for i in range(len(objects)):
                X_object = objects[i][0][0] 
                Y_object = objects[i][1][0] 
                
                X_delta = abs(X - X_object)
                Y_delta = abs(Y - Y_object)
                # print(f"X delta {X_delta} Y delta {Y_delta}")
                # print(f"X size {list_objects[number][2][0]} Y size {list_objects[number][3][0]}")
                
                if X_delta < list_objects[number][2][0] * 3 and Y_delta < list_objects[number][3][0] * 3:
                    object_nr = i
                    break
            
            POSXYZ[0] = objects[object_nr][0][0]
            POSXYZ[1] = objects[object_nr][1][0]
            POSXYZ[2] = Zdistance
            # print(f"position to move to {POSXYZ}")
            self.RobotCommand.MoveJ(pos=POSXYZ, v=50, a=50)   