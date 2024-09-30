import backend.core.variables as var
import numpy as np
import cv2

import backend.vision.vision_var as VD
import tkinter.messagebox

import time
import threading
import requests

from backend.core.event_manager import event_manager

class VisionManagement():
    def __init__(self):
        super().__init__()       
        self._stop_event = threading.Event() 
        
        self.image_HSV = None 
        self.valid_URL = False
        
        self.cap = None
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_close_cam", self.CloseCam)
       
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

    def ConnectCam(self):
        if var.CAM_CONNECT == 0:
            com_port_adress = event_manager.publish("request_get_cam_port")
            if com_port_adress[0].isdigit():
                self.cap = cv2.VideoCapture(int(com_port_adress[0]))
                print(self.cap)
            elif self.is_valid_url(com_port_adress): 
                #self.url = 'http://192.168.1.184:81/stream'     
                self.cap = cv2.VideoCapture(com_port_adress)
                
            if self.cap.isOpened():
                event_manager.publish("request_cam_connect_button_color", True)
                print("camere opened")
                var.CAM_CONNECT = 1
                self._stop_event.clear()
                self.video()  
                # Proceed with connecting to the camera stream
            else:
                event_manager.publish("request_cam_connect_button_color", False)
                tkinter.messagebox.showinfo("info", "Cannot find the camera, check if you have the right COM port or URL")
            
        else:
            var.CAM_CONNECT = 0
            try:
                self._stop_event.set()
                time.sleep(0.1)
                self.cap.release()
                event_manager.publish("request_cam_connect_button_color", False)
                print("cam disconnect")
            except: 
                print("error relasing cam")
 
    def threadCAM(self):
        while not self._stop_event.is_set():
            time.sleep(0.005)
            try:
                ret, frame = self.cap.read()
                if ret:
                    VD.image_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)              
                    
                    event_manager.publish("request_set_pixmap_video", VD.image_RGB)
            except: 
                pass 
            
    def video(self):            
        t_threadRead = threading.Thread(target=self.threadCAM)  
        t_threadRead.start()

    def mask_image(self, color_name):
        if color_name in var.VISION_COLOR_OPTIONS:
            if len(var.VISION_COLOR_OPTIONS[color_name]) == 2:
                lower_color = np.array(var.VISION_COLOR_OPTIONS[color_name][0])
                upper_color = np.array(var.VISION_COLOR_OPTIONS[color_name][1])
                mask = cv2.inRange(VD.image_HSV, lower_color, upper_color)
            elif len(var.VISION_COLOR_OPTIONS[color_name]) == 4:
                lower_color1 = np.array(var.VISION_COLOR_OPTIONS[color_name][0])
                upper_color1 = np.array(var.VISION_COLOR_OPTIONS[color_name][1]) 
                mask1 = cv2.inRange(VD.image_HSV, lower_color1, upper_color1)
                lower_color2 = np.array(var.VISION_COLOR_OPTIONS[color_name][2])
                upper_color2 = np.array(var.VISION_COLOR_OPTIONS[color_name][3]) 
                mask2 = cv2.inRange(VD.image_HSV, lower_color2, upper_color2)
                
                mask = mask1 + mask2
                
            return mask, VD.image_HSV
        else:
            print("color not found")
        
    def mask(self, color_name, image):
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
            print("color not found")                
                 
    def capture_frame(self, RGB = None):
        ret, frame = var.VISION_CAP.read()
        if ret:
            # Convert BGR to RGB
            if RGB == None:
                image_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                return image_HSV
            else:
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return image_rgb

    def CalibrateVision(self, data):
        var.TOOL_SETTINGS_CAM = data
        
        var.TOOL_SETTINGS_CAM[4] = event_manager.publish("request_label_width_video")[0]
        print(var.TOOL_SETTINGS_CAM)
        
        #event_manager.publish("request_save_robot_button")       