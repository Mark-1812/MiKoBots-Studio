import backend.core.variables as var
from backend.core.event_manager import event_manager

from backend.robot_management.communication  import send_line_to_robot, connect_robot_check
from backend.simulation import simulate_program, check_simulation_on


class Move():
    def __init__(self):
        event_manager.subscribe("request_robot_home", self.Home)   
        event_manager.subscribe("request_robot_jog_joint", self.JogJoint)   
        event_manager.subscribe("request_robot_move_j", self.MoveJ)   
        event_manager.subscribe("request_robot_offset_j", self.OffsetJ)   
        event_manager.subscribe("request_robot_move_joint_pos", self.MoveJointPos)   
    
        self.letters = [chr(i) for i in range(65, 91)]  # A-Z letters

        self.number_of_joints = var.NUMBER_OF_JOINTS
        self.dh_param = var.DH_PARAM

    
    def MoveJ(self, pos, v = None, a = None, Origin = None):
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if Origin:
            pos[0] = pos[0] + Origin[0]
            pos[1] = pos[1] + Origin[1]
            pos[2] = pos[2] + Origin[2]
        
        command = "MoveJ "
        
        # check if the simulation is enabled
        if check_simulation_on():
            for i in range(self.number_of_joints):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"            
            simulate_program(command)
        else:
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command, Home=True)
                
    def OffsetJ(self, pos, v = 50, a = 50):       
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return   
        
        command = "OffsetJ "

        # check if the simulation is enabled
        if check_simulation_on():
            for i in range(self.number_of_joints):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"     
            simulate_program(command)
        else:
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            
            send_line_to_robot(command, True)  
        
    def JogJoint(self, pos, v = None, a = None):
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]        
        
        command = "jogJ "
        
        
        # check if the simulation is enabled
        if check_simulation_on():
            for i in range(self.number_of_joints):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            simulate_program(command)
            
        else:    
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
        
    def MoveL(self, pos, v = 50, a = 50):
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return
        
        if v == None:
            v = event_manager.publish("request_get_speed")[0]
        if a == None: 
            a = event_manager.publish("request_get_accel")[0]      

        command = "OffsetJ "
        
        
        # check if it is a simulation
        if check_simulation_on():
            for i in range(self.number_of_joints):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"                 
            simulate_program(command)
            
        else:
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command, Home=True)
                
    def OffsetL(self, pos, v = 50, a = 50):
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return   

        command = "OffsetL "
        
        if check_simulation_on():
            
            for i in range(self.number_of_joints):
                command += f"{var.NAME_AXIS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"                 
            simulate_program(command)
            
        else:
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command, True)

    def MoveJointPos(self, pos, v = 50, a = 50):
        if len(pos) is not self.number_of_joints:
            print(var.LANGUAGE_DATA.get("message_more_values_than_joints"))
            event_manager.publish("request_stop_sim")
            return

        command = "MoveJoint "
        

        # check if the simulation is enables
        if check_simulation_on():
            for i in range(self.number_of_joints):
                command += f"{var.NAME_JOINTS[i]}{pos[i]} "
            command += f"s{v} a{a}\n"
            
            simulate_program(command)
            
        else:
            for i in range(self.number_of_joints):
                command += str(self.letters[i]) + str(pos[i])
            command += f"{self.letters[i+1]}{v}{self.letters[i+2]}{a}\n"
            send_line_to_robot(command)
            
    def Home(self):    
        command = "Home\n"
        send_line_to_robot(command)