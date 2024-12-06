import backend.core.variables as var
from backend.core.event_manager import event_manager

from backend.robot_management.communication  import send_line_to_io, send_line_to_robot, connect_robot_check, connect_io_check

from backend.simulation import check_simulation_on


class IO():
    def __init__(self):
        self.type = None
        self.IO_BOX = None

    
    def SetIO(self, pin_number, type):
        self.type = type
        self.IO_BOX = None
        
        if self.type == "INPUT" or self.type == "OUTPUT":
            # determine the pin number
            IO_pin = var.ROBOT_SETTINGS["Set_io_pin"][0][pin_number]
                    
            settings_io = f"Set_io_pin A{pin_number}B{IO_pin}C{self.type}\n"
            
            # send the settings to the IO box or the robot
            if var.ROBOT_SETTINGS["Set_io_pin"][1] == "IO" and connect_io_check():
                send_line_to_io(settings_io)
                self.IO_BOX = True
            elif var.ROBOT_SETTINGS["Set_io_pin"][1] != "IO" and connect_robot_check():
                send_line_to_robot(settings_io)
                self.IO_BOX = False
        else:
            print("error do not regonize this type, only INPUT or OUTPUT")        
    
    def digitalRead(self, pin_number):
        if self.type == "INPUT":
            
            IO_CHECK = event_manager.publish("request_check_io_state", pin_number)[0]
            
            if IO_CHECK:
                return True
            else:
                return False             
    
    def digitalWrite(self, pin_number, state):
        if self.type == "OUTPUT":
            if state == "HIGH":
                event_manager.publish("request_set_io_state", pin_number, True)
            elif state == "LOW":
                event_manager.publish("request_set_io_state", pin_number, False)
           
        if (not check_simulation_on() and self.IO_BOX and connect_io_check()) or (not check_simulation_on() and not self.IO_BOX and connect_robot_check()):       
            if self.type != "OUTPUT":   
                return
                     
            if state == "HIGH":
                # change the value of the IO pin in the control menu
                event_manager.publish("request_set_io_state", pin_number, True)
                
                command = f"IO_digitalWrite P{pin_number}S1\n"

                if self.IO_BOX:
                    send_line_to_io(command)
                elif not self.IO_BOX:
                    send_line_to_robot(command)
                                    
            elif state == "LOW":
                # change the value of the IO pin in the control menu
                event_manager.publish("request_set_io_state", pin_number, False)
                
                command = f"IO_digitalWrite P{pin_number}S0\n"
                
                if self.IO_BOX:
                    send_line_to_io(command)
                    
                elif not self.IO_BOX:
                    send_line_to_robot(command)
 