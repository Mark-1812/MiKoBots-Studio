import backend.core.variables as var
import numpy as np
import cv2

import math

import time
import threading
import requests

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

class VisionManagement():
    def __init__(self):
        super().__init__()       
        self._stop_event = threading.Event() 
        
        self.valid_URL = False
        
        self.cap = None
        self.stop = False   
        
        self.image_HSV = None
       
    def CloseCam(self):
        if var.CAM_CONNECT:
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

    def ConnectCam(self, addres = None):
        if var.CAM_CONNECT == 0:
            com_port_adress = addres
            if self.is_valid_url(com_port_adress):    
                self.cap = cv2.VideoCapture(com_port_adress)
            else:
                self.cap = cv2.VideoCapture(addres)
            
            
            if self.cap.isOpened():
                event_manager.publish("request_cam_connect_button_color", True)
                var.CAM_CONNECT = 1
                self._stop_event.clear()
                self.video()  
                # Proceed with connecting to the camera stream
            else:
                event_manager.publish("request_cam_connect_button_color", False)
                ErrorMessage(var.LANGUAGE_DATA.get("message_not_find_cam"))

                
                
        else:
            var.CAM_CONNECT = 0
            try:
                time.sleep(0.1)
                self._stop_event.set()
                self.cap.release()
                
                event_manager.publish("request_cam_connect_button_color", False)
                print(var.LANGUAGE_DATA.get("message_camera_connected"))
            except: 
                print(var.LANGUAGE_DATA.get("message_error_releasing_cam"))
 
    def threadCAM(self):
        while not self._stop_event.is_set() and self.cap.isOpened():
            try:
                time.sleep(0.01)
                if self.cap.isOpened():  # Check the stop condition
                    ret, self.frame = self.cap.read()
                    if not ret:
                        print(var.LANGUAGE_DATA.get("message_failed_grab_frame"))
                        continue
                    image_RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)   
                               
                    if var.CAM_SQUARE:
                        self.ShowCalSquare(image_RGB)
                               
                    event_manager.publish("request_set_pixmap_video", image_RGB)
            except Exception as e:
                print(f"Error in threadCAM: {e}")
  
            
    def ShowCalSquare(self, image):
        self.height_picture, self.width_picture, ch = image.shape 
        
        y_1 = int(0.1 * self.height_picture)
        h_1 = int(0.8 * self.height_picture)
        
        w_1 = int(0.8 * self.height_picture)
        x_1 = int((self.width_picture - w_1) / 2)
        
        self.square_size_pixel = 0.8 * self.height_picture
        
        cv2.rectangle(image, (x_1, y_1), (x_1+w_1, y_1+h_1), (0, 255, 0), 2)
        
        return image
            
    def GetImageFrame(self):
        return self.frame
            
    def video(self):            
        t_threadRead = threading.Thread(target=self.threadCAM)  
        t_threadRead.start()

        
    def GetMask(self, color_name, image):
        if color_name in var.VISION_COLOR_OPTIONS:
            if len(var.VISION_COLOR_OPTIONS[color_name]) == 2:
                lower_color = np.array(var.VISION_COLOR_OPTIONS[color_name][0])
                upper_color = np.array(var.VISION_COLOR_OPTIONS[color_name][1])
                mask = cv2.inRange(image, lower_color, upper_color)
            elif len(var.VISION_COLOR_OPTIONS[color_name]) == 4:
                lower_color1 = np.array(var.VISION_COLOR_OPTIONS[color_name][0])
                upper_color1 = np.array(var.VISION_COLOR_OPTIONS[color_name][1])  
                mask1 = cv2.inRange(image, lower_color1, upper_color1)
                lower_color2 = np.array(var.VISION_COLOR_OPTIONS[color_name][2])
                upper_color2 = np.array(var.VISION_COLOR_OPTIONS[color_name][3]) 
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