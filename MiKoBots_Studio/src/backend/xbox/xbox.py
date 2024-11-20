import time        
from PyQt5.QtWidgets import  QFileDialog, QMessageBox

import threading

import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage
 
class XBox:
    def __init__(self):  
        self.xbox_on = 0
        self.current_state_index = 0
      
        self.states = ["Move X Y Z", "Move y p r", "Move J1 J2 J3", "Move J4 J5 J6"]
        
        self.controller = None
        
        
    def XBoxOn(self):
        if self.xbox_on == 0:
            self.xbox_on = 1
            self.xbox()
        else:
            self.xbox_on = 0
            event_manager.publish("request_button_controller_connect", False)
            
    def xbox(self):
        def threadXbox():
            import pygame
            pygame.init()

            # Find the Xbox controller
            self.controller = None
            for i in range(pygame.joystick.get_count()):
                if "Xbox" in pygame.joystick.Joystick(i).get_name():
                    self.controller = pygame.joystick.Joystick(i)
                    self.controller.init()
                    break

            if self.controller is None:
                pygame.quit()
                ErrorMessage(var.LANGUAGE_DATA.get("message_not_found_xbox"))

            else:
                event_manager.publish("request_button_controller_connect", True)
                event_manager.publish("request_state_controller_label", self.states[self.current_state_index])
              
            while self.xbox_on == 1 and self.controller:
                pygame.event.pump()
                Joystick_Left_stick_LR = int(self.controller.get_axis(0) * 200)  # Scale the value to match your motor position range
                Joystick_Left_stick_UD = int(self.controller.get_axis(1) * 200)  # Scale the value to match your motor position range
                Joystick_Right_stick_UD = int(self.controller.get_axis(3) * 200)  # Scale the value to match your motor position range
                
                Joystick_Left_Trigger = int(self.controller.get_axis(4) * 200)
                Joystick_Right_Trigger = int(self.controller.get_axis(5) * 200)
                
                JoyStick_Dpad = self.controller.get_hat(0)
                
                Joystick_Right_Bumper = int(self.controller.get_button(5) * 200) 
                Joystick_Left_Bumper = int(self.controller.get_button(4) * 200)
                Joystick_A_Button = int(self.controller.get_button(0))     
               
                           
                              
                if JoyStick_Dpad == (-1,0):
                    event_manager.publish("request_set_jog_distance", "1")
                elif JoyStick_Dpad == (0,1):
                    event_manager.publish("request_set_jog_distance", "10")
                elif JoyStick_Dpad == (1,0):
                    event_manager.publish("request_set_jog_distance", "50")
                elif JoyStick_Dpad == (0,-1):
                    event_manager.publish("request_set_jog_distance", "100")       
                
                if Joystick_A_Button and prev_A_Button == 0:
                    LINE = f"MoveJ X{round(var.POS_AXIS_SIM[0],1)} Y{round(var.POS_AXIS_SIM[1],1)} Z{round(var.POS_AXIS_SIM[2],1)} y{round(var.POS_AXIS_SIM[3],1)} p{round(var.POS_AXIS_SIM[4],1)} r{round(var.POS_AXIS_SIM[5],1)} s50 a50"
                
                prev_A_Button = Joystick_A_Button
                
                if not(Joystick_Right_Bumper > 100 and Joystick_Left_Bumper > 100):
                    if Joystick_Right_Bumper > 100 and prev_right_bumper_state == 0:
                        self.current_state_index = (self.current_state_index + 1) % len(self.states)
                        event_manager.publish("request_state_controller_label", self.states[self.current_state_index])    

                    prev_right_bumper_state = Joystick_Right_Bumper 
                    
                    if Joystick_Left_Bumper > 100 and prev_left_bumper_state == 0:
                        self.current_state_index = (self.current_state_index - 1) % len(self.states)
                        event_manager.publish("request_state_controller_label", self.states[self.current_state_index])  
                        
                    prev_left_bumper_state = Joystick_Left_Bumper
                
                   
                if Joystick_Left_Trigger > 100:
                    #self.ProgramLines.ProgramJogGripper(1)
                    pass
              
                if Joystick_Right_Trigger > 100:
                    #self.ProgramLines.ProgramJogGripper(0)
                    pass
                    
                jog_distance = float(event_manager.publish("request_get_jog_distance")[0])
                    
                if self.current_state_index == 0:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [jog_distance,0,0,0,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [-jog_distance,0,0,0,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,jog_distance,0,0,0,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,-jog_distance,0,0,0,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,jog_distance,0,0,0]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,-jog_distance,0,0,0]
                    
                    if len(pos) > 0:
                        event_manager.publish("request_robot_offset_j", pos)  
           
                elif self.current_state_index == 1:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [0,0,0,jog_distance,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [0,0,0,-jog_distance,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,0,0,0,jog_distance,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,0,0,0,-jog_distance,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,0,0,0,jog_distance]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,0,0,0,-jog_distance]
                    
                    if len(pos) > 0:
                        event_manager.publish("request_robot_offset_j", pos)  
                        
                elif self.current_state_index == 2:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [jog_distance,0,0,0,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [-jog_distance,0,0,0,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,jog_distance,0,0,0,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,-jog_distance,0,0,0,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,jog_distance,0,0,0]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,-jog_distance,0,0,0]
                        
                    if len(pos) > 0:
                        event_manager.publish("request_robot_jog_joint", pos) 
                            
                elif self.current_state_index == 3:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [0,0,0,jog_distance,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [0,0,0,-jog_distance,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,0,0,0,jog_distance,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,0,0,0,-jog_distance,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,0,0,0,jog_distance]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,0,0,0,-jog_distance]
                        
                    if len(pos) > 0:
                        event_manager.publish("request_robot_jog_joint", pos) 
               
                time.sleep(0.05)
                    
            pygame.quit()
            event_manager.publish("request_state_controller_label", "")
                    
        t_xbox = threading.Thread(target=threadXbox)  
        t_xbox.start()
