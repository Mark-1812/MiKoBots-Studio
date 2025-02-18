import backend.core.variables as var
from backend.core.event_manager import event_manager


import os

from backend.robot_management import change_tool
from backend.robot_management.communication  import send_line_to_io, connect_io_check
from backend.robot_management.communication  import send_line_to_robot, connect_robot_check, send_tool_frame
from backend.simulation import check_simulation_on

import time


class Tool():
    def __init__(self):
        event_manager.subscribe("request_change_pos_tool", self.MoveTo)   
        event_manager.subscribe("request_send_settings_tool", self.SetTool)   
        event_manager.subscribe("request_change_state_tool", self.State)   
        
        self.tool_number = None
        self.IO_BOX = None

    def SetTool(self, tool):
        tool_settings = var.TOOL_SETTINGS

        for i in range(len(tool_settings)):
            if tool == os.path.splitext(tool_settings[i][0])[0]:
                self.tool_number = i

                # if the tool is different than shown in the simulation change tool
                event_manager.publish("request_set_tool_combo", self.tool_number)
                # change_tool(self.tool_number)
                
                
                time.sleep(0.05)
                
                
                self.type_of_tool = var.TOOL_TYPE
                self.servo_values = var.TOOL_SERVO_SETTINGS # even if the tool has no servo type
                tool_pin = var.TOOL_PIN
                                
                                
                if self.type_of_tool == "Servo":
                    type_tool = 0
                if self.type_of_tool == "Relay":
                    type_tool = 1
                if self.type_of_tool == "None":
                    type_tool = 2
                     
                settings_tool = ("Set_tools A" + str(tool_pin) + "B" + str(type_tool) + "C" + str(self.servo_values[0]) + "D" + str(self.servo_values[1]) + "\n")      
                         

                    
                # send settings to IO if this is given in settings
                if var.ROBOT_SETTINGS['Set_tools'][1] == "IO" and connect_io_check():
                    send_line_to_io(settings_tool)
                    self.IO_BOX = True
                    
                # send settings to ROBOT if this is given in settings    
                elif var.ROBOT_SETTINGS['Set_tools'][1] != "IO" and connect_robot_check():
                    send_line_to_robot(settings_tool)
                    self.IO_BOX = False   
                           
                # send always the tool frame only to the robot
                if connect_robot_check():
                    send_tool_frame()
                
        if self.tool_number is None:
            print(var.LANGUAGE_DATA.get("message_tool_not_regonized"))
    
    def MoveTo(self, pos):
        if self.type_of_tool == "Servo":
            # check if the pos is within the reach
            if pos > 100:
                pos = 100
            elif pos < 0:
                pos = 0
                
            var.TOOL_POS = pos
            
            # if simulation is enabled only change the value
            if check_simulation_on():
                event_manager.publish("request_set_tool_pos", pos)
            
            # command for tool to move
            command = f"Tool_move_to pos({pos})\n"
             
            if connect_io_check() and self.IO_BOX:
                send_line_to_io(command)
                
            if connect_robot_check() and not self.IO_BOX:
                send_line_to_robot(command)
        else:
            print(var.LANGUAGE_DATA.get("message_not_move_tool")) 
    
    def State(self, state):
        print(self.type_of_tool)
        if self.type_of_tool == "Relay" and (state == "HIGH" or state == "LOW"):
            
            if check_simulation_on():
                if state == "HIGH":
                    event_manager.publish("request_set_tool_state", True)
                elif state == "LOW":
                    event_manager.publish("request_set_tool_state", False)
                    
            command = f"Tool_state ({state})\n"
            
            if connect_io_check() and self.IO_BOX:
                send_line_to_io(command)
            if connect_robot_check() and not self.IO_BOX:
                send_line_to_robot(command)
        else:
            print(var.LANGUAGE_DATA.get("message_not_state_tool")) 
            