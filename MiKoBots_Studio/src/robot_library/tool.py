import backend.core.variables as var
from backend.core.event_manager import event_manager


import os

from backend.robot_management  import send_line_to_io
from backend.robot_management  import send_line_to_robot



class Tool():
    def __init__(self):
        event_manager.subscribe("request_change_pos_tool", self.MoveTo)   
        event_manager.subscribe("request_send_settings_tool", self.SetTool)   
        event_manager.subscribe("request_change_state_tool", self.State)   
        
        self.tool_number = None
        self.IO_BOX = None

    def SetTool(self, tool):
        for i in range(len(var.TOOLS3D)):
            if tool == os.path.splitext(var.TOOLS3D[i][0])[0]:
                self.tool_number = i
                
                self.type_of_tool = var.TOOLS3D[self.tool_number][7]
                if self.type_of_tool == "Servo":
                    self.servo_values = var.TOOLS3D[self.tool_number][8] 
                # if the tool is different than shown in the simulation change tool
                
                event_manager.publish("request_set_tool_combo", self.tool_number)
                
                # determine the pin number
                string_tool_nr = var.TOOLS3D[self.tool_number][6]
                number = int(string_tool_nr.split()[-1]) - 1
                tool_pin = var.SETTINGS["Set_tools"][0][number]
                                
                                
                if var.TOOLS3D[self.tool_number][7] == "Servo":
                    type_tool = 0
                if var.TOOLS3D[self.tool_number][7] == "Relay":
                    type_tool = 1
                if var.TOOLS3D[self.tool_number][7] == "None":
                    type_tool = 2
                     
                settings_tool = ("Set_tools A" + str(tool_pin) + "B" + str(type_tool) + "C" + str(var.TOOLS3D[self.tool_number][8][0]) + "D" + str(var.TOOLS3D[self.tool_number][8][1]) + "\n")      
                         
                tool_frame = "Set_tool_frame "
                letters = ['A','B','C','D','E','F']
                
                for i in range(6):
                    tool_frame += str(letters[i])
                    tool_frame += str(var.TOOLS3D[self.tool_number][5][i])
                    
                tool_frame += "\n"
                    
                # send settings to IO if this is given in settings
                if var.SETTINGS['Set_tools'][1] == "IO" and var.IO_CONNECT:
                    send_line_to_io(settings_tool)
                    self.IO_BOX = True
                    
                # send settings to ROBOT if this is given in settings    
                elif var.SETTINGS['Set_tools'][1] != "IO" and var.ROBOT_CONNECT:
                    send_line_to_robot(settings_tool)
                    self.IO_BOX = False   
                           
                # send always the tool frame only to the robot
                if var.ROBOT_CONNECT:
                    send_line_to_robot(tool_frame)
                
        if self.tool_number is None:
            print(var.LANGUAGE_DATA.get("message_tool_not_regonized"))
    
    def MoveTo(self, pos):
        if self.type_of_tool == "Servo":
            # if simulation is enabled only change the value
            if var.SIM:
                var.TOOL_POS = pos
                event_manager.publish("request_set_tool_pos", pos)
            
            # command for tool to move
            command = f"Tool_move_to pos({pos})\n"
             
            if var.IO_CONNECT and self.IO_BOX:
                send_line_to_io(command)
                
            if var.ROBOT_CONNECT and not self.IO_BOX:
                send_line_to_robot(command)
        else:
            print(var.LANGUAGE_DATA.get("message_not_move_tool")) 
    
    def State(self, state):
        if self.type_of_tool == "Relay" and (state == "HIGH" or state == "LOW"):
            
            if var.SIM:
                if state == "HIGH":
                    event_manager.publish("request_set_tool_state", True)
                elif state == "LOW":
                    event_manager.publish("request_set_tool_state", False)
                    
            command = f"Tool_state ({state})\n"
            
            if var.IO_CONNECT and self.IO_BOX:
                send_line_to_io(command)
            if var.ROBOT_CONNECT and not self.IO_BOX:
                send_line_to_robot(command)
        else:
            print(var.LANGUAGE_DATA.get("message_not_state_tool")) 
            