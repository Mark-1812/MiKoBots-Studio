import asyncio
import backend.core.variables as var

from .communication_com import TalkThroughCOM
from .communication_bt import TalkThroughBT



talk_with_robot_com = TalkThroughCOM(ROBOT=True)
talk_with_io_com = TalkThroughCOM(IO=True)

talk_with_robot_bt = TalkThroughBT(ROBOT = True)
talk_with_io_bt = TalkThroughBT(IO = True)

#########################################
## Communication robot
#########################################

def connect_robot_check():
    if talk_with_robot_bt.connect:
        return True
    if talk_with_robot_com.connect:
        return True
    
    return False

def connect_robot(addres = None ,type = None):
    # if type is True than COM
    # address is com port or bluetooth addres

    if not talk_with_robot_bt.connect and not talk_with_robot_com.connect: 
        # make a connection
        if type: # COM port connection
            talk_with_robot_com.Connect(addres)
        else: # Bluetooth connection
            talk_with_robot_bt.Connect(addres)
    elif talk_with_robot_com.connect:
        # break the connection
        talk_with_robot_com.DisConnect()

    elif talk_with_robot_bt.connect:
        talk_with_robot_bt.Disconnect()
    
def send_line_to_robot(command, Home = False):
    if talk_with_robot_bt.stop or talk_with_robot_com.stop:
        print("Error: Stop mode, press first play")
        return
    
    if talk_with_robot_bt.pauze or talk_with_robot_com.pauze:
        print("Error: Pauze mode, press first play")
        return

    if talk_with_robot_bt.connect:
        if Home and talk_with_robot_bt.robot_home:  # check if the root is home
            talk_with_robot_bt.SendLineCommand(command)
        elif not Home:
            talk_with_robot_bt.SendLineCommand(command)
        else:
            print("Error: the robot is not homed")
    elif talk_with_robot_com.connect:
        if Home and talk_with_robot_com.robot_home:
            talk_with_robot_com.SendLineCommand(command)
        elif not Home:
            talk_with_robot_com.SendLineCommand(command)
        else:
            print("Error: the robot is not homes")
    else:
        print("Error: The robot is not connected")
    
def send_settings_robot():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.SendSettingsRobot()
    elif talk_with_robot_com.connect:
        talk_with_robot_com.SendSettingsRobot()
        
def close_robot():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.Close()
    else:
        talk_with_robot_com.Close()    

def scan_for_robots():
    talk_with_robot_bt.ScanForDevice()


def send_tool_frame():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.SendToolFrame()
    elif talk_with_robot_com.connect:
        talk_with_robot_com.SendToolFrame()
        
        
# play, pauze and stop the robot functions, also the IO??
def pauze_robot():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.PauzeProgram()

    if talk_with_robot_com.connect:
        talk_with_robot_com.PauzeProgram()

def play_robot():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.PlayProgram()

    if talk_with_robot_com.connect:
        talk_with_robot_com.PlayProgram()

def stop_robot():
    if talk_with_robot_bt.connect:
        talk_with_robot_bt.StopProgram()
    elif talk_with_robot_com.connect:
        talk_with_robot_com.StopProgram()  




    
#########################################
## Communication IO
#########################################

def send_line_to_io(command):
    if talk_with_io_bt.connect:
        talk_with_io_bt.SendLineCommand(command)
    elif talk_with_robot_com.connect:
        talk_with_io_com.SendLineCommand(command)
    else:
        print("Error io is not connected")
    
def send_settings_io():
    if talk_with_io_bt.connect:
        talk_with_io_bt.SendSettingsIO()
    elif talk_with_io_com.connect:
        talk_with_io_com.SendSettingsIO()
    else:
        print("Error io is not connected") 
 
def close_io():
    if talk_with_io_bt.connect:
        talk_with_io_bt.Close()
    elif talk_with_io_com.connect:
        talk_with_io_com.Close() 
                
def scan_for_io():
    talk_with_io_bt.ScanForDevice()

def connect_io_check():
    if talk_with_io_bt.connect:
        return True
    if talk_with_io_com.connect:
        return True
    
    return False

def connect_io(addres = None, settings = list,type = None):
    # if type is True than COM
    # address is com port or bluetooth addres

    if not talk_with_io_bt.connect and not talk_with_io_com.connect: 
        # make a connection
        if type: # COM port connection
            print("make com connection")
            talk_with_io_com.Connect(addres, settings)
        else: # Bluetooth connection
            print("make bt connection")
            talk_with_io_bt.Connect(addres, settings)
    elif talk_with_io_com.connect:
        # break the connection
        print("break com connection")
        talk_with_io_com.DisConnect()

    elif talk_with_io_bt.connect:
        print("break bt connection")
        talk_with_io_bt.Disconnect()