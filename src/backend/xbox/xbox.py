import time        
import tkinter.messagebox  
import pygame
import threading
from backend.robot_management.robot_commands import Move
import frontend.dynamic_widgets as DW
import backend.core.variables as v
 
class XBox:
    def __init__(self, button, label, jog_entry, program_lines):
        self.xbox_on = 0
        self.current_state_index = 0
        
        self.states = ["Move X Y Z", "Move y p r", "Move J1 J2 J3", "Move J4 J5 J6"]
        self.button = button
        self.label = label
        
        self.ProgramLines = program_lines    
        self.jog_entry = jog_entry
        self.robot_move = Move()
        
        self.controller = None
        
        
    def XBoxOn(self):
        if self.xbox_on == 0:
            self.xbox_on = 1
            self.xbox()
        else:
            self.button.setStyleSheet("background-color: orange;")
            self.xbox_on = 0

    def xbox(self):
        def threadXbox():
            pygame.init()

            # Find the Xbox controller
            self.controller = None
            for i in range(pygame.joystick.get_count()):
                if "Xbox" in pygame.joystick.Joystick(i).get_name():
                    self.controller = pygame.joystick.Joystick(i)
                    self.controller.init()
                    break
                
            print(self.controller)

            if self.controller is None:
                print("Xbox controller not found. Make sure it's connected.")
                pygame.quit()
                tkinter.messagebox.showinfo("Connection","Cannot find the xbox controller")
            else:
                self.button.setStyleSheet("background-color: green;")
                self.label.setText(self.states[self.current_state_index])
                
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
                    self.jog_entry.setText("1")
                elif JoyStick_Dpad == (0,1):
                    self.jog_entry.setText("10")
                elif JoyStick_Dpad == (1,0):
                    self.jog_entry.setText("50")
                elif JoyStick_Dpad == (0,-1):
                    self.jog_entry.setText("100")               
                
                if Joystick_A_Button and prev_A_Button == 0:
                    LINE = f"MoveJ X{round(v.POS_AXIS_SIM[0],1)} Y{round(v.POS_AXIS_SIM[1],1)} Z{round(v.POS_AXIS_SIM[2],1)} y{round(v.POS_AXIS_SIM[3],1)} p{round(v.POS_AXIS_SIM[4],1)} r{round(v.POS_AXIS_SIM[5],1)} s50 a50"
                
                prev_A_Button = Joystick_A_Button
                
                if not(Joystick_Right_Bumper > 100 and Joystick_Left_Bumper > 100):
                    if Joystick_Right_Bumper > 100 and prev_right_bumper_state == 0:
                        self.current_state_index = (self.current_state_index + 1) % len(self.states)
                        new_state = self.states[self.current_state_index]   
                        self.label.setText(new_state)     

                    prev_right_bumper_state = Joystick_Right_Bumper 
                    
                    if Joystick_Left_Bumper > 100 and prev_left_bumper_state == 0:
                        self.current_state_index = (self.current_state_index - 1) % len(self.states)
                        new_state = self.states[self.current_state_index]
                        self.label.setText(new_state)
                        
                    prev_left_bumper_state = Joystick_Left_Bumper
                
                   
                if Joystick_Left_Trigger > 100:
                    #self.ProgramLines.ProgramJogGripper(1)
                    pass
                
                if Joystick_Right_Trigger > 100:
                    #self.ProgramLines.ProgramJogGripper(0)
                    pass
                    
                if self.current_state_index == 0:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [float(v.JOG_DISTANCE),0,0,0,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [-float(v.JOG_DISTANCE),0,0,0,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,float(v.JOG_DISTANCE),0,0,0,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,-float(v.JOG_DISTANCE),0,0,0,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,float(v.JOG_DISTANCE),0,0,0]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,-float(v.JOG_DISTANCE),0,0,0]
                    
                    if len(pos) > 0:
                        self.robot_move.OffsetJ(pos,v.JOG_SPEED,v.JOG_ACCEL)
                
                elif self.current_state_index == 1:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [0,0,0,float(v.JOG_DISTANCE),0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [0,0,0,-float(v.JOG_DISTANCE),0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,0,0,0,float(v.JOG_DISTANCE),0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,0,0,0,-float(v.JOG_DISTANCE),0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,0,0,0,float(v.JOG_DISTANCE)]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,0,0,0,-float(v.JOG_DISTANCE)]
                    
                    if len(pos) > 0:
                        self.robot_move.OffsetJ(pos,v.JOG_SPEED,v.JOG_ACCEL)
                            
                elif self.current_state_index == 2:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [0,0,0,float(v.JOG_DISTANCE),0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [0,0,0,-float(v.JOG_DISTANCE),0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,0,0,0,float(v.JOG_DISTANCE),0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,0,0,0,-float(v.JOG_DISTANCE),0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,0,0,0,float(v.JOG_DISTANCE)]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,0,0,0,-float(v.JOG_DISTANCE)]
                        
                    if len(pos) > 0:
                        self.robot_move.JogJoint(pos,v.JOG_SPEED,v.JOG_ACCEL)
                                          
                elif self.current_state_index == 3:
                    pos = []
                    if Joystick_Left_stick_LR > 100:
                        pos = [float(v.JOG_DISTANCE),0,0,0,0,0]
                    elif Joystick_Left_stick_LR < -100:
                        pos = [-float(v.JOG_DISTANCE),0,0,0,0,0]
                    elif Joystick_Left_stick_UD > 100:
                        pos = [0,float(v.JOG_DISTANCE),0,0,0,0]
                    elif Joystick_Left_stick_UD < -100:
                        pos = [0,-float(v.JOG_DISTANCE),0,0,0,0]
                    elif Joystick_Right_stick_UD > 100:
                        pos = [0,0,float(v.JOG_DISTANCE),0,0,0]
                    elif Joystick_Right_stick_UD < -100:
                        pos = [0,0,-float(v.JOG_DISTANCE),0,0,0]
                        
                    if len(pos) > 0:
                        self.robot_move.JogJoint(pos,v.JOG_SPEED,v.JOG_ACCEL)
                             

                
                time.sleep(0.05)
                    
            pygame.quit()
            self.label.setText("")
            print("quit pi game")
                    
        t_xbox = threading.Thread(target=threadXbox)  
        t_xbox.start()
