import threading
import time
import serial
import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

class TalkThroughCOM():
    pause_event = threading.Event()
    busy_event = threading.Event()

    def __init__(self, ROBOT = False, IO = False):
        super().__init__()

        self.ROBOT = ROBOT
        self.IO = IO

        self.connect = False
        self.com_port = None
        self.com_ser = None

        self.stop = False
        self.pauze = False

        self.pause_event.clear()
        self.busy_event.clear()

# Connect the robot
    def Connect(self, com_port = None):
        try:        
            self.com_port = com_port
            self.com_ser = serial.Serial(self.com_port, baudrate=115200)#, timeout=1)
            self.com_ser .dtr = False   # Ensure DTR is inactive
            self.com_ser .setRTS(False) # Deactivate RTS first
            time.sleep(0.1)
            self.com_ser .setRTS(True)  # Reactivate RTS to reset
            time.sleep(0.5)
            self.com_ser .dtr = True    # Enable DTR

            t_threadRead = threading.Thread(target=self.ReadDate)  
            t_threadRead.start()

            start_time = time.time()
            while not self.connect:
                time.sleep(0.01)  
                current_time = time.time()
                if current_time - start_time > 4:
                    break

            if self.connect: 
                if self.ROBOT:
                    event_manager.publish("request_robot_connect_button_color", True)
                    self.SendSettingsRobot()
                
                if self.IO:
                    event_manager.publish("request_io_connect_button_color", True)
                    self.SendSettingsIO()

                self.connect = True
            else:
                print(var.LANGUAGE_DATA.get("message_failed_connection_com"))
                self.com_ser.close()
                self.connect = False
        
        except serial.SerialException:
            print(var.LANGUAGE_DATA.get("message_failed_connection_com"))

# disconnect the robot
    def DisConnect(self):
        self.robot_home = False  
        self.com_ser.close()
        self.connect = False 

        if self.ROBOT:
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)
            self.robot_home = False

        if self.IO:
            event_manager.publish("request_io_connect_button_color", False) 

# Close the robot 
    def Close(self):
        if self.connect:
            self.com_ser.close()

# read data
    def ReadDate(self):
        while self.com_ser.is_open:
            try:
                data = self.com_ser.readline().decode('latin-1').rstrip()  # Read a line
            except:
                break

            if data:
                if data == "wait":
                    self.pause_event.set()
                elif data.strip() == "go":
                    self.pause_event.clear()
                elif data.strip() == "ROBOT_CONNECTED":
                    self.connect = True
                    self.busy = False
                elif data.strip() == "IO_CONNECTED" and self.ROBOT:
                    print(var.LANGUAGE_DATA.get("message_robot_instead_of_io"))

                elif data.strip() == "home":
                    self.robot_home = True
                    event_manager.publish("request_robot_home_button_color", True)
                elif data.strip() == "END":
                    self.busy_event.clear()
                    self.busy = 0   
                elif data.startswith("Tool state"):
                    state = data.split()[-1]
                    if state == "HIGH":
                        event_manager.publish("request_set_tool_state", True)
                    elif state == "LOW":
                        event_manager.publish("request_set_tool_state", False)
                    
                elif data.startswith("Input "):
                    parts = data.split()
                    
                    io_number = int(parts[1])
                    io_state = int(parts[2])
                    
                    if io_state == 1:
                        event_manager.publish("request_set_io_state_input", io_number, True)
                    else:
                        event_manager.publish("request_set_io_state_input", io_number, False)    
                elif data.startswith("POS:"):
                    words = data.split()

                    for i in range(len(words)):
                        if words[i] == 'G':
                            var.POS_GRIPPER = float(words[i + 1])
                        
                        event_manager.publish("request_set_tool_pos", var.POS_GRIPPER)
                            
                        for j in range(var.NUMBER_OF_JOINTS):
                            if words[i] == var.NAME_JOINTS[j]:
                                var.POS_JOINT[j] = float(words[i + 1])
                                
                            if words[i] == var.NAME_AXIS[j]:
                                var.POS_AXIS[j] = float(words[i + 1])
                        
                        event_manager.publish("request_label_pos_joint", var.POS_JOINT, var.NAME_JOINTS, var.UNIT_JOINT)
                        event_manager.publish("request_label_pos_axis", var.POS_AXIS, var.NAME_AXIS, var.UNIT_AXIS)

                else:
                    pass
                data_text = "ROBOT: " + data
                print(data_text) 
                    
                data = None


            time.sleep(0.01)
           
        self.DisConnect()  

# send command   
    def SendLineCommand(self, command):
        while self.pause_event.is_set():
            time.sleep(0.1)
        
        self.busy = 1   

        try:
            self.com_ser.write(command.encode())
        except:
            self.CloseRobot()
            print(var.LANGUAGE_DATA.get("message_lost_connection_robot"))
            
        start_time = time.time()
        while self.busy: 
            if time.time() - start_time >= 10:
                break 
            time.sleep(0.03)
                   
# send settings  
    def SendSettingsRobot(self):
        if not self.busy and self.connect:
            category_names = []

            def make_line_ABC(settings_values, command_name):
                letters = [chr(i) for i in range(65, 91)]  # A-Z letters

                if isinstance(settings_values[0], list):
                    column = len(settings_values)
                else:
                    column = 1
                    
                    
                formatted_settings = f"{command_name} "
                if column == 1:
                    for i, value in enumerate(settings_values):
                        formatted_settings += letters[i] + str(value)
                else:
                    for i in range(column):
                        for j in range(len(settings_values[0])):
                            value = settings_values[i][j]
                            formatted_settings += letters[j + (len(settings_values[0])) * i] + str(value)
                
                formatted_settings += "\n"
                return formatted_settings
            
            def threadSettings():
                # send all the settings to the robot except for the settings where the IO_box is checked
                for category in var.SETTINGS:
                    category_names.append(category)
                           
                # sent first the number of joints
                command = f'Set_number_of_joints A{var.NUMBER_OF_JOINTS}\n'
                self.SendLineCommand(command)
                time.sleep(0.2)
                
                if var.SETTINGS["Set_extra_joint"][0] == 1:
                    command = f'Set_extra_joint A1\n'
                    self.SendLineCommand(command)
                    time.sleep(0.2)
                           
                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]

                    if settings[1] == "" and  category_names[i] != 'Set_extra_joint':
                        command = make_line_ABC(settings[0], category_names[i])
                        self.SendLineCommand(command)
                                  
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if self.busy == 1:
                print(var.LANGUAGE_DATA.get("message_robot_busy")) 
            elif not self.connect:
                print(var.LANGUAGE_DATA.get("message_robot_not_connected")) 
                ErrorMessage(var.LANGUAGE_DATA.get("message_robot_not_connected"))
    
    def SendSettingsIO(self):
        if not self.busy and self.connect:
            category_names = []

            def make_line_ABC(settings_values, command_name):
                letters = [chr(i) for i in range(65, 91)]  # A-Z letters

                if isinstance(settings_values[0], list):
                    column = len(settings_values)
                else:
                    column = 1
                formatted_settings = f"{command_name} "
                if column == 1:
                    for i, value in enumerate(settings_values):
                        formatted_settings += letters[i] + str(value)
                else:
                    for i in range(column):
                        for j in range(len(settings_values[0])):
                            value = settings_values[i][j]
                            formatted_settings += letters[j + (len(settings_values[0])) * i] + str(value)
                
                formatted_settings += "\n"
                return formatted_settings
            
            def threadSettings():
                # send all the settings to the robot except for the settings where the IO_box is checked
                for category in var.SETTINGS:
                    category_names.append(category)
                    
                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]
                    if settings[1] == "IO":
                        print("settings...." + category_names[i])
                        print(settings[0])
                        command = make_line_ABC(settings[0], category_names[i])
                        
                        self.SendLineCommand(command)
                          
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if self.busy == 1:
                print(var.LANGUAGE_DATA.get("message_io_busy"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_io_busy"))
            elif self.connect == 0:
                print(var.LANGUAGE_DATA.get("message_io_not_connected"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_io_not_connected"))

## play pauze stop the robot
    def StopProgram(self):
        # send all the settings to the robot except for the settings where the IO_box is checked
        command = "stop\n"
        if self.com_ser:
            self.com_ser.write(command.encode())

        self.busy = False
        self.stop = True

    def PlayProgram(self):
        # send all the settings to the robot except for the settings where the IO_box is checked
        command = "play\n"
        if self.com_ser:
            self.com_ser.write(command.encode())

        self.stop = False
        self.pauze = False

    def PauzeProgram(self):
        # send all the settings to the robot except for the settings where the IO_box is checked
        command = "pauze\n"
        if self.com_ser:
            self.com_ser.write(command.encode())

        self.pauze = True

