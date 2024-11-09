import backend.core.variables as var
from backend.core.event_manager import event_manager

from backend.robot_management  import send_line_to_robot
from backend.simulation import simulate_program


class Move():
    def __init__(self):
        event_manager.subscribe("request_robot_home", self.Home)   
        event_manager.subscribe("request_robot_jog_joint", self.JogJoint)   
        event_manager.subscribe("request_robot_move_j", self.MoveJ)   
        event_manager.subscribe("request_robot_offset_j", self.OffsetJ)   
        event_manager.subscribe("request_robot_move_joint_pos", self.MoveJointPos)   
    
        self.letters = [chr(i) for i in range(65, 91)]  # A-Z letters
    
    def MoveJ(self, pos, v = None, a = None, Origin = None):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if Origin:
            pos[0] = pos[0] + Origin[0]
            pos[1] = pos[1] + Origin[1]
            pos[2] = pos[2] + Origin[2]
        
        command = "MoveJ "
        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"            
            simulate_program(command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
                
    def OffsetJ(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return     
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return   
        
        command = "OffsetJ "

        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"     
                   
            simulate_program(command)
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            
            send_line_to_robot(command)  
        
    def JogJoint(self, pos, v = None, a = None):
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if var.ROBOT_BUSY:
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]        
        
        command = "jogJ "
        
        
        # check if the simulation is enabled
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            simulate_program(command)
            
        elif var.ROBOT_CONNECT == 1:    
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
        
    def MoveL(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]      

        command = "OffsetJ "
        
        
        # check if it is a simulation
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"                 
            simulate_program(command)
            
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
                
    def OffsetL(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return    
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return   

        
        if var.SIM == 1:
            command = "OffsetL "
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"                 
            simulate_program(command)
            
        elif var.ROBOT_CONNECT == 1 and var.ROBOT_HOME:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)

    def MoveJointPos(self, pos, v = 50, a = 50):
        if not var.ROBOT_HOME and not var.SIM:
            return
        
        if len(pos) > var.NUMBER_OF_JOINTS:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return

        command = "MoveJoint "
        

        # check if the simulation is enables
        if var.SIM == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            
            print(command)
            simulate_program(command)
            
        elif var.ROBOT_CONNECT == 1:
            for i in range(var.NUMBER_OF_JOINTS):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
            
    def Home(self):    
        if var.ROBOT_CONNECT == 1:
            command = "Home\n"
            send_line_to_robot(command)