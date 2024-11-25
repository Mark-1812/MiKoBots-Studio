import time        
from PyQt5.QtWidgets import  QFileDialog, QMessageBox

import threading

import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

from backend.run_program import run_single_line
import pygame
 
class XBox:
    def __init__(self):  
        self.xbox_on = False
      
        self.states = ["State 1", "State 2", "State 3", "State 4"]
        
        self.controller = None
        
        
    def XBoxOn(self):
        if not self.xbox_on:
            self.xbox_on = True
            t_xbox = threading.Thread(target=self.threadXbox)  
            t_xbox.start()
        else:
            self.xbox_on = False
            event_manager.publish("request_button_controller_connect", False)
            
    def threadXbox(self):
        pygame.init()
        
        state = 0

        # Find the Xbox controller
        self.controller = None
        for i in range(pygame.joystick.get_count()):
            if "Xbox" in pygame.joystick.Joystick(i).get_name():
                self.controller = pygame.joystick.Joystick(i)
                self.controller.init()
                break

        if self.controller is None:
            pygame.quit()
            print(var.LANGUAGE_DATA.get("message_not_found_xbox"))
        else:
            event_manager.publish("request_button_controller_connect", True)
            event_manager.publish("request_state_controller_label", self.states[state])
            
            # get the controller settings
            
            controller_settings = event_manager.publish("request_get_controller_settings")[0]
            
            D_PAD_UP = controller_settings['D-PAD up']
            D_PAD_RIGHT = controller_settings['D-PAD Right']
            D_PAD_DOWN = controller_settings['D-PAD Down']
            D_PAD_LEFT = controller_settings['D-PAD Left']
            
            LSB_UP_DOWN = controller_settings['LSB up-down']
            LSB_LEFT_RIGHT = controller_settings['LSB left-right']
            RSB_UP_DOWN = controller_settings['RSB up-down']
            RSB_LEFT_RIGHT = controller_settings['RSB left-right']
            
            

        while self.xbox_on and self.controller:
            pygame.event.pump()
            # get the value of the buttons/ joysticks
            Joystick_Left_stick_LR = int(self.controller.get_axis(0) * 200) 
            Joystick_Left_stick_UD = int(self.controller.get_axis(1) * 200) 
            
            Joystick_Right_stick_UD = int(self.controller.get_axis(3) * 200)  
            Joystick_Right_stick_LR = int(self.controller.get_axis(2) * 200)  
            
            Joystick_Left_Trigger = int(self.controller.get_axis(4) * 200)
            Joystick_Right_Trigger = int(self.controller.get_axis(5) * 200)
            
            JoyStick_Dpad = self.controller.get_hat(0)
            
            Joystick_Right_Bumper = int(self.controller.get_button(5) * 200) 
            Joystick_Left_Bumper = int(self.controller.get_button(4) * 200)
            Joystick_A_Button = int(self.controller.get_button(0))     
                 

            # left and right bumper change state
            if not(Joystick_Right_Bumper > 100 and Joystick_Left_Bumper > 100):
                if Joystick_Right_Bumper > 100 and prev_right_bumper_state == 0:
                    state = (state + 1) % len(self.states)
                    event_manager.publish("request_state_controller_label", self.states[state])    

                prev_right_bumper_state = Joystick_Right_Bumper 
                
                if Joystick_Left_Bumper > 100 and prev_left_bumper_state == 0:
                    state = (state - 1) % len(self.states)
                    event_manager.publish("request_state_controller_label", self.states[state])  
                    
                prev_left_bumper_state = Joystick_Left_Bumper
            
            ##############################################
            # D-PAD buttons    
            ##############################################
            
            # button up
            if JoyStick_Dpad == (-1,0):
                if D_PAD_LEFT[state] == 'Jog dis 1':
                    event_manager.publish("request_set_jog_distance", "1")
                elif D_PAD_LEFT[state] == 'Jog dis 10':
                    event_manager.publish("request_set_jog_distance", "10")
                elif D_PAD_LEFT[state] == 'Jog dis 50':
                    event_manager.publish("request_set_jog_distance", "50")
                elif D_PAD_LEFT[state] == 'Jog dis 100':
                    event_manager.publish("request_set_jog_distance", "100")
                
                    
            # button right
            elif JoyStick_Dpad == (0,1):
                    
                if D_PAD_UP[state] == 'Jog dis 1':
                    event_manager.publish("request_set_jog_distance", "1")
                elif D_PAD_UP[state] == 'Jog dis 10':
                    event_manager.publish("request_set_jog_distance", "10")
                elif D_PAD_UP[state] == 'Jog dis 50':
                    event_manager.publish("request_set_jog_distance", "50")
                elif D_PAD_UP[state] == 'Jog dis 100':
                    event_manager.publish("request_set_jog_distance", "100")
                    
            # button down
            elif JoyStick_Dpad == (1,0):
                if D_PAD_RIGHT[state] == 'Jog dis 1':
                    event_manager.publish("request_set_jog_distance", "1")
                elif D_PAD_RIGHT[state] == 'Jog dis 10':
                    event_manager.publish("request_set_jog_distance", "10")
                elif D_PAD_RIGHT[state] == 'Jog dis 50':
                    event_manager.publish("request_set_jog_distance", "50")
                elif D_PAD_RIGHT[state] == 'Jog dis 100':
                    event_manager.publish("request_set_jog_distance", "100")
                    
                
                
            elif JoyStick_Dpad == (0,-1):
                if D_PAD_DOWN[state] == 'Jog dis 1':
                    event_manager.publish("request_set_jog_distance", "1")
                elif D_PAD_DOWN[state] == 'Jog dis 10':
                    event_manager.publish("request_set_jog_distance", "10")
                elif D_PAD_DOWN[state] == 'Jog dis 50':
                    event_manager.publish("request_set_jog_distance", "50")
                elif D_PAD_DOWN[state] == 'Jog dis 100':
                    event_manager.publish("request_set_jog_distance", "100")
            
                
            # get the jog distance
            jog_distance = float(event_manager.publish("request_get_jog_distance")[0])
                
            
            posXYZ = [0, 0, 0, 0, 0, 0]
            posJoint = [0, 0, 0, 0, 0, 0]
                
                
            ##############################################
            # Joy stick left   
            ##############################################
        
        
            if Joystick_Left_stick_LR > 100:
                if LSB_LEFT_RIGHT[state] == 'X':
                    posXYZ = [jog_distance, 0, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Y':
                    posXYZ = [0, jog_distance, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Z':
                    posXYZ = [0, 0, jog_distance, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'y':
                    posXYZ = [0, 0, 0, jog_distance, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'p':
                    posXYZ = [0, 0, 0, 0, jog_distance, 0]
                elif LSB_LEFT_RIGHT[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, jog_distance]
                    
                elif LSB_LEFT_RIGHT[state] == 'Joint 1':
                    posJoint = [jog_distance, 0, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 2':
                    posJoint = [0, jog_distance, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 3':
                    posJoint = [0, 0, jog_distance, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 4':
                    posJoint = [0, 0, 0, jog_distance, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, jog_distance, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, jog_distance]
                
            if Joystick_Left_stick_LR < -100:
                if LSB_LEFT_RIGHT[state] == 'X':
                    posXYZ = [-jog_distance, 0, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Y':
                    posXYZ = [0, -jog_distance, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Z':
                    posXYZ = [0, 0, -jog_distance, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'y':
                    posXYZ = [0, 0, 0, -jog_distance, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'p':
                    posXYZ = [0, 0, 0, 0, -jog_distance, 0]
                elif LSB_LEFT_RIGHT[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, -jog_distance]
                    
                elif LSB_LEFT_RIGHT[state] == 'Joint 1':
                    posJoint = [-jog_distance, 0, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 2':
                    posJoint = [0, -jog_distance, 0, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 3':
                    posJoint = [0, 0, -jog_distance, 0, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 4':
                    posJoint = [0, 0, 0, -jog_distance, 0, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, -jog_distance, 0]
                elif LSB_LEFT_RIGHT[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, -jog_distance]                
                
            if Joystick_Left_stick_UD > 100:
                if LSB_UP_DOWN[state] == 'X':
                    posXYZ = [jog_distance, 0, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Y':
                    posXYZ = [0, jog_distance, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Z':
                    posXYZ = [0, 0, jog_distance, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'y':
                    posXYZ = [0, 0, 0, jog_distance, 0, 0]
                elif LSB_UP_DOWN[state] == 'p':
                    posXYZ = [0, 0, 0, 0, jog_distance, 0]
                elif LSB_UP_DOWN[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, jog_distance]
                    
                elif LSB_UP_DOWN[state] == 'Joint 1':
                    posJoint = [jog_distance, 0, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 2':
                    posJoint = [0, jog_distance, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 3':
                    posJoint = [0, 0, jog_distance, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 4':
                    posJoint = [0, 0, 0, jog_distance, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, jog_distance, 0]
                elif LSB_UP_DOWN[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, jog_distance]
         
            if Joystick_Left_stick_UD < -100:
                if LSB_UP_DOWN[state] == 'X':
                    posXYZ = [-jog_distance, 0, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Y':
                    posXYZ = [0, -jog_distance, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Z':
                    posXYZ = [0, 0, -jog_distance, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'y':
                    posXYZ = [0, 0, 0, -jog_distance, 0, 0]
                elif LSB_UP_DOWN[state] == 'p':
                    posXYZ = [0, 0, 0, 0, -jog_distance, 0]
                elif LSB_UP_DOWN[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, -jog_distance]
                    
                elif LSB_UP_DOWN[state] == 'Joint 1':
                    posJoint = [-jog_distance, 0, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 2':
                    posJoint = [0, -jog_distance, 0, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 3':
                    posJoint = [0, 0, -jog_distance, 0, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 4':
                    posJoint = [0, 0, 0, -jog_distance, 0, 0]
                elif LSB_UP_DOWN[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, -jog_distance, 0]
                elif LSB_UP_DOWN[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, -jog_distance]
                
              
            ##############################################
            # Joy stick right
            ##############################################              
         
            if Joystick_Right_stick_UD > 100:
                if RSB_UP_DOWN[state] == 'X':
                    posXYZ = [jog_distance, 0, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Y':
                    posXYZ = [0, jog_distance, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Z':
                    posXYZ = [0, 0, jog_distance, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'y':
                    posXYZ = [0, 0, 0, jog_distance, 0, 0]
                elif RSB_UP_DOWN[state] == 'p':
                    posXYZ = [0, 0, 0, 0, jog_distance, 0]
                elif RSB_UP_DOWN[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, jog_distance]
                    
                elif RSB_UP_DOWN[state] == 'Joint 1':
                    posJoint = [jog_distance, 0, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 2':
                    posJoint = [0, jog_distance, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 3':
                    posJoint = [0, 0, jog_distance, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 4':
                    posJoint = [0, 0, 0, jog_distance, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, jog_distance, 0]
                elif RSB_UP_DOWN[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, jog_distance]  
                    
            if Joystick_Right_stick_UD < -100:
                if RSB_UP_DOWN[state] == 'X':
                    posXYZ = [-jog_distance, 0, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Y':
                    posXYZ = [0, -jog_distance, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Z':
                    posXYZ = [0, 0, -jog_distance, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'y':
                    posXYZ = [0, 0, 0, -jog_distance, 0, 0]
                elif RSB_UP_DOWN[state] == 'p':
                    posXYZ = [0, 0, 0, 0, -jog_distance, 0]
                elif RSB_UP_DOWN[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, -jog_distance]
                    
                elif RSB_UP_DOWN[state] == 'Joint 1':
                    posJoint = [-jog_distance, 0, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 2':
                    posJoint = [0, -jog_distance, 0, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 3':
                    posJoint = [0, 0, -jog_distance, 0, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 4':
                    posJoint = [0, 0, 0, -jog_distance, 0, 0]
                elif RSB_UP_DOWN[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, -jog_distance, 0]
                elif RSB_UP_DOWN[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, -jog_distance]

            if Joystick_Right_stick_LR > 100:
                if RSB_LEFT_RIGHT[state] == 'X':
                    posXYZ = [jog_distance, 0, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Y':
                    posXYZ = [0, jog_distance, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Z':
                    posXYZ = [0, 0, jog_distance, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'y':
                    posXYZ = [0, 0, 0, jog_distance, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'p':
                    posXYZ = [0, 0, 0, 0, jog_distance, 0]
                elif RSB_LEFT_RIGHT[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, jog_distance]
                    
                elif RSB_LEFT_RIGHT[state] == 'Joint 1':
                    posJoint = [jog_distance, 0, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 2':
                    posJoint = [0, jog_distance, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 3':
                    posJoint = [0, 0, jog_distance, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 4':
                    posJoint = [0, 0, 0, jog_distance, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, jog_distance, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, jog_distance]
                
            if Joystick_Right_stick_LR < -100:
                if RSB_LEFT_RIGHT[state] == 'X':
                    posXYZ = [-jog_distance, 0, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Y':
                    posXYZ = [0, -jog_distance, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Z':
                    posXYZ = [0, 0, -jog_distance, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'y':
                    posXYZ = [0, 0, 0, -jog_distance, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'p':
                    posXYZ = [0, 0, 0, 0, -jog_distance, 0]
                elif RSB_LEFT_RIGHT[state] == 'r':
                    posXYZ = [0, 0, 0, 0, 0, -jog_distance]
                    
                elif RSB_LEFT_RIGHT[state] == 'Joint 1':
                    posJoint = [-jog_distance, 0, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 2':
                    posJoint = [0, -jog_distance, 0, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 3':
                    posJoint = [0, 0, -jog_distance, 0, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 4':
                    posJoint = [0, 0, 0, -jog_distance, 0, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 5':
                    posJoint = [0, 0, 0, 0, -jog_distance, 0]
                elif RSB_LEFT_RIGHT[state] == 'Joint 6':
                    posJoint = [0, 0, 0, 0, 0, -jog_distance]                
                                               
                
            if posXYZ != [0, 0, 0, 0, 0, 0]:
                posAxis = []
                for i in range(var.NUMBER_OF_JOINTS):
                    posAxis.append(posXYZ[i])
                    
                if posAxis != [0]*var.NUMBER_OF_JOINTS:
                    run_single_line(f"robot.OffsetJ({posAxis}, {var.JOG_SPEED}, {var.JOG_ACCEL})")
                
                
            elif posJoint != [0, 0, 0, 0, 0, 0]:
                posAxis = []
                for i in range(var.NUMBER_OF_JOINTS):
                    posAxis.append(posJoint[i])
                    
                if posAxis != [0]*var.NUMBER_OF_JOINTS:
                    run_single_line(f"robot.JogJoint({posAxis}, {var.JOG_SPEED}, {var.JOG_ACCEL})")
                
                
                
            time.sleep(0.05)
                
        pygame.quit()
        event_manager.publish("request_state_controller_label", "")
                    

