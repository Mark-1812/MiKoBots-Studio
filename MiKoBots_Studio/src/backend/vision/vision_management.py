import backend.core.variables as var
import numpy as np
import cv2

import math

import time
import threading
import requests

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

from backend.robot_management import get_selected_tool

class VisionManagement():
    def __init__(self):
        super().__init__()       
        self._stop_event = threading.Event() 
        
        self.valid_URL = False
        
        self.cap = None
        self.stop = False   
        self.connect = False
        self.image_HSV = None
        
        self.cam_tool = False
        
        self.show_square_tool = False
        self.show_square = False
        self.square_size_per = 0.8
        self.square_width_px = 0
        
        
       
    def CloseCam(self):
        if self.connect:
            self._stop_event.set()
            time.sleep(0.1)
            #self.cap.release()
                   
    def is_valid_url(self, url):
        try:
            event_manager.publish("request_cam_connect_button_color", False)
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.head(url, headers=headers)
            return True            
        except requests.RequestException:
            return False

    def DisconnectCam(self):
        self.connect = False
        self._stop_event.set()
        #self.cap.release()
        event_manager.publish("request_cam_connect_button_color", False)
        #print(var.LANGUAGE_DATA.get("message_camera_connected"))
        


    def ConnectCam(self, addres = None):
        com_port_adress = addres
        if self.is_valid_url(com_port_adress):    
            self.cap = cv2.VideoCapture(com_port_adress)
        else:
            print(" try to connect")
            self.cap = cv2.VideoCapture(addres)
            print(" test")
        
        
        if self.cap.isOpened():
            event_manager.publish("request_cam_connect_button_color", True)
            self.connect = True
            self._stop_event.clear()
            self.video()  
            # Proceed with connecting to the camera stream
        else:
            event_manager.publish("request_cam_connect_button_color", False)
            ErrorMessage(var.LANGUAGE_DATA.get("message_not_find_cam"))

    def calculate_mm_per_pixel(self, image = None, Height = None):
        mm_per_pixel = 0

        print(f"self.cam_tool {self.cam_tool}")


        if self.cam_tool:

            tool = get_selected_tool

            settings_cam = var.TOOLS3D[tool][11]
            
            z1 = float(settings_cam[0]) # Z distance big square
            z2 = float(settings_cam[1]) # Z distance small square
            
            size1 = float(settings_cam[2]) # size big square
            size2 = float(settings_cam[3]) # size small square
            
            Zdelta = z1 - z2
            Xdelta = size1 - size2
            
            Ratio_height_width = Xdelta/Zdelta
            
            if Height == None:    
                new_Zdelta = z1 - float(var.POS_AXIS[2])
            else:
                new_Zdelta = z1 - Height
                
            height_picture, width_picture, ch = image.shape 
                
            square_width_pixel = width_picture * 0.8
                
            mm_per_pixel = (size1 - (new_Zdelta * Ratio_height_width)) / square_width_pixel
        else:
            square_size_mm = event_manager.publish("request_get_square_size")[0]
            print(f"percentage square = {self.square_size_per}")


            h, w, ch = image.shape

            print(f"square size mm {square_size_mm}")

            print(f"square height: {h}")

            mm_per_pixel = square_size_mm / (self.square_size_per * h)
            # get square size
            
        return mm_per_pixel
 
    def threadCAM(self):
        while not self._stop_event.is_set() and self.cap.isOpened():
            if self.cap.isOpened():  # Check the stop condition
                try:
                    ret, self.frame = self.cap.read()
                    if not ret:
                        print(var.LANGUAGE_DATA.get("message_failed_grab_frame"))
                        self.DisconnectCam()
                        continue
                    
                except Exception as e:
                    print(f"Error in threadCAM: {e}")
                
                image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)   
                            
                if self.show_square_tool:
                    image_RGB = self.ShowCalSquareTool(image_RGB)
                if self.show_square:
                    image_RGB = self.ShowCalSquare(image_RGB)
                    
                event_manager.publish("request_set_pixmap_video", image_RGB)
                
                time.sleep(0.01)
        
        self.cap.release()
  
    def ShowCalSquare(self, image):
        height_picture, self.width_picture, ch = image.shape 
        
        offset = (1 - self.square_size_per) / 2
        
        y_1 = int(offset * height_picture)
        h_1 = int(self.square_size_per * height_picture)
        
        w_1 = int(self.square_size_per * height_picture)
        x_1 = int((self.width_picture - w_1) / 2)
        
        self.square_width_px = h_1
        
        cv2.rectangle(image, (x_1, y_1), (x_1+w_1, y_1+h_1), (0, 255, 0), 2)
        return image
    
    def ChangeSizeSquare(self, dir):
        if dir:
            self.square_size_per += 0.02
        else:
            self.square_size_per -= 0.02
             
    def ShowCalSquareTool(self, image):
        height_picture, self.width_picture, ch = image.shape 
        
        y_1 = int(0.1 * height_picture)
        h_1 = int(0.8 * height_picture)
        
        w_1 = int(0.8 * height_picture)
        x_1 = int((self.width_picture - w_1) / 2)
        
        self.square_size_pixel = 0.8 * height_picture
        
        cv2.rectangle(image, (x_1, y_1), (x_1+w_1, y_1+h_1), (0, 255, 0), 2)
        return image
          
    def GetImageFrame(self):
        return self.frame
            
    def video(self):            
        t_threadRead = threading.Thread(target=self.threadCAM)  
        t_threadRead.start()
       
    def GetMask(self, color_name, image):
        print("1")
        color_range = event_manager.publish("request_get_colors")[0]
        print(color_range)
        print(color_name)

        print(color_range[color_name])

        if color_name in color_range:
            if len(color_range[color_name]) == 2:
                lower_color = np.array(color_range[color_name][0])
                upper_color = np.array(color_range[color_name][1])
                mask = cv2.inRange(image, lower_color, upper_color)
            elif len(color_range[color_name]) == 4:
                lower_color1 = np.array(color_range[color_name][0])
                upper_color1 = np.array(color_range[color_name][1])  
                mask1 = cv2.inRange(image, lower_color1, upper_color1)
                lower_color2 = np.array(color_range[color_name][2])
                upper_color2 = np.array(color_range[color_name][3]) 
                mask2 = cv2.inRange(image, lower_color2, upper_color2)
                
                mask = mask1 + mask2
                
            return mask
        else:
            print(var.LANGUAGE_DATA.get("message_no_colors"))                

    def DrawAxis(self, img, p_, q_, color, scale):
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