from backend.vision import calculate_mm_per_pixel
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
        print("find objects")
        self.frame = get_image_frame()
        image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        image_GRAY = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2GRAY) 
        
        image_GRAY = cv2.adaptiveThreshold(image_GRAY, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 399, 12)
        image_HSV = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)
        
        
        mm_per_pixel = calculate_mm_per_pixel(image_RGB)
        print(mm_per_pixel)
        
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
                print("found objects")
                
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


                print("1")

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
                print(f"angle_camera {angle_camera}")
                print(f"angle {angle}")

                new_angle = angle_camera + angle
                if new_angle > 360:
                    new_angle = new_angle - 360
                    
                print(f"new angle {new_angle}")
                    
                # get x and Y location of the objects
                if new_angle >= 0 and new_angle < 90:
                    print("X positive Y negative")
                    # Y negative X positive
                    
                    angle_radians = math.radians(new_angle)
                    pos_y = radius * math.sin(angle_radians)
                    pos_x = radius * math.cos(angle_radians)
                    
                    pos_y = pos_y * -1 # make y position negative
                    
                elif new_angle >= 90 and new_angle < 180:
                    print("X negative Y negative")
                    # X negative Y negative
                    
                    angle_radians = math.radians(new_angle - 90)
                    pos_x = radius * math.sin(angle_radians)
                    pos_y = radius * math.cos(angle_radians)
                    
                    pos_x = pos_x * -1
                    pos_y = pos_y * -1
                   
                elif new_angle >= 180 and new_angle < 270:
                    print("X negative Y positive")
                    # X negative Y positive
                    
                    angle_radians = math.radians(new_angle - 180)
                    pos_y = radius * math.sin(angle_radians)
                    pos_x = radius * math.cos(angle_radians)
                    
                    print(f"pos x {pos_x}")
                    print(f"pos y {pos_y}")
                    
                    pos_x = pos_x * -1
                    
                    print(f"pos x {pos_x}")
                    print(f"pos y {pos_y}")
                    
                elif new_angle >= 270 and new_angle < 360:
                    print("Y positive X positive")
                    # X negative Y positive
                    
                    angle_radians = math.radians(new_angle - 270)
                    pos_x = radius * math.sin(angle_radians)
                    pos_y = radius * math.cos(angle_radians)
                  
                    
                print(f"pos x {pos_x}")
                print(f"pos y {pos_y}")

                # get the orientation of the position of the camera


                angle = math.atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
                angle = round(math.degrees(angle),2)

                print("3")

                # check if the camera is connected to the camera
                # if not the location of the camera is static
                cam_tool = False

                if cam_tool:
                    # get the rotation of the camera how it is connected to the tool
                    Yobject_place = round(pos_y  + float(var.POS_AXIS[1]) + float(var.TOOL_OFFSET_CAM[1]),1)          
                    Xobject_place = round(pos_x  + float(var.POS_AXIS[0]) + float(var.TOOL_OFFSET_CAM[0]),1)  
                else:
                    # get the cent lace of the camera out of the settings'
                    # get the rotation of the camera out of the settings

                    offset = event_manager.publish("request_get_offset_cam")[0]
                    print(offset)
                    
                    x_offset = offset[0]
                    y_offset = offset[1]
                    
                    Yobject_place = round(pos_y  + y_offset, 1)          
                    Xobject_place = round(pos_x  + x_offset, 1)
                    
                print(f"X {Xobject_place} Y {Yobject_place} width {width} height {height} angle {angle}")
                
                self.Objects.append([[Xobject_place], [Yobject_place], [width], [height], [angle], [color]])

        event_manager.publish("request_set_pixmap_image", image_RGB)
        
        return self.Objects
    
    def MoveToObject(self, list_objects = list, number = 0, Zdistance = None):
        self.RobotCommand = Move()

        POSXYZ = [0]*6
        
        POSXYZ[0] = list_objects[number][0][0] + float(var.TOOL_OFFSET_CAM[0])
        POSXYZ[1] = list_objects[number][1][0]
        POSXYZ[2] = 120
        POSXYZ[3] = 0
        POSXYZ[4] = 0
        POSXYZ[5] = 180        
        

        if (var.POS_AXIS[2] - Zdistance) < 130 or Zdistance == None:
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