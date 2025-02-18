import threading
import time
import serial
import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

class TalkThroughCOM():
    pause_event = threading.Event()

    def __init__(self, ROBOT = False, IO = False):
        super().__init__()

        self.ROBOT = ROBOT
        self.IO = IO

        self.connect = False
        self.com_port = None
        self.com_ser = None

        self.stop = False
        self.pauze = False
        self.busy = False

        self.pause_event.clear()

        self.settings = None

# Connect the robot
    def Connect(self, com_port = None, settings = None):
        try:        
            self.com_port = com_port
            self.com_ser = serial.Serial(self.com_port, baudrate=57600)#, timeout=1)
            self.com_ser .dtr = False   # Ensure DTR is inactive
            self.com_ser .setRTS(False) # Deactivate RTS first
            time.sleep(0.2)
            self.com_ser .setRTS(True)  # Reactivate RTS to reset
            time.sleep(0.8)
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
                self.settings = settings
                if self.ROBOT:
                    event_manager.publish("request_robot_connect_button_color", True)
                    self.SendToolFrame()
                    self.SendSettingsRobot()
                
                if self.IO:
                    print("Send IO settings")
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
        try:
            self.com_ser.close()
        except: pass
        self.connect = False 
        self.busy = False

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
                    
                elif data.strip() == "ROBOT_CONNECTED" and self.ROBOT:
                    self.connect = True
                    self.busy = False
                elif data.strip() == "ROBOT_CONNECTED" and self.IO:
                    self.DisConnect()
                    print(var.LANGUAGE_DATA.get("message_robot_instead_of_io"))
                    
                elif data.strip() == "IO_CONNECTED" and self.IO:
                    print("IO connefcted")
                    self.connect = True
                    self.busy = False
                elif data.strip() == "IO_CONNECTED" and self.ROBOT:
                    self.DisConnect()
                    print(var.LANGUAGE_DATA.get("message_robot_instead_of_io"))

                elif data.strip() == "home":
                    self.robot_home = True
                    event_manager.publish("request_robot_home_button_color", True)
                elif data.strip() == "END":
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
                            var.TOOL_POS = float(words[i + 1])
                        
                        event_manager.publish("request_set_tool_pos", var.TOOL_POS)
                    
                            
                        for j in range(var.NUMBER_OF_JOINTS):
                            if words[i] == var.NAME_JOINTS[j]:
                                var.POS_JOINT[j] = float(words[i + 1])
                                
                            if words[i] == var.NAME_AXIS[j]:
                                var.POS_AXIS[j] = float(words[i + 1])
                        
                        event_manager.publish("request_label_pos_joint", var.POS_JOINT, var.NAME_JOINTS, var.UNIT_JOINT)
                        event_manager.publish("request_label_pos_axis", var.POS_AXIS, var.NAME_AXIS, var.UNIT_AXIS)

                else:
                
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
            # print(command)
            self.com_ser.write(command.encode())
        except:
            self.DisConnect()
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
                letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

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
                robot_settings = var.ROBOT_SETTINGS
                
                print(robot_settings)

                # sent first the number of joints
                command = f'Set_number_of_joints A{var.NUMBER_OF_JOINTS}\n'
                self.SendLineCommand(command)
                
                settings = robot_settings['Set_motor_type']
                command = make_line_ABC(settings[0], 'Set_motor_type')
                self.SendLineCommand(command)
                
                if var.EXTRA_JOINT:
                    command = f'Set_extra_joint A1\n'
                    self.SendLineCommand(command) 
                    
                           
                for category in robot_settings:
                    settings = robot_settings[category]
                    if settings[1] == "" and  category != 'Set_extra_joint' and category != 'Set_motor_type'  and  category != 'Set_io_pin'and  category != 'Set_robot_name' and  category != "Set_tools":
                        
                        command = make_line_ABC(settings[0], category)
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
                robot_settings = var.ROBOT_SETTINGS

                # send all the settings to the robot except for the settings where the IO_box is checked
                for category in robot_settings:
                    category_names.append(category)
                    
                for i, setting in enumerate(robot_settings):
                    settings = robot_settings[category_names[i]]
                    if settings[1] == "IO":
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

    def SendToolFrame(self):
        if not self.busy and self.connect:
            tool_frame = var.TOOL_FRAME
            command = "Set_tool_frame "
            letters = ['A','B','C','D','E','F']
            

            for i in range(6):
                command += str(letters[i])
                command += str(tool_frame[i])
                
            command += "\n"
                
            self.SendLineCommand(command)


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


