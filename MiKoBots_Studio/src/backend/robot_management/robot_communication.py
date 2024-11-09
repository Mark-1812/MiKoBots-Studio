import threading
import time
import serial
import backend.core.variables as var
from serial.serialutil import SerialException
import re
from bleak import BleakScanner, BleakClient
import asyncio
from backend.core.event_manager import event_manager
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QMetaObject
import json

from gui.windows.message_boxes import ErrorMessage

CHARACTERISTIC_UUID_ROBOT = "c42e42e4-8214-420c-944d-e127cc0f20ba"  # Replace with your actual characteristic UUID
SERVICE_UUID_ROBOT = "a917e658-9c1a-4901-bbb8-92d54cfa2fdd"

class TalkWithRobotBT(QThread):
    pause_event = threading.Event()
    busy_event = threading.Event()

    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.pause_event.clear()
        self.busy_event.clear()
        self.start()

    async def ScanForDevicesBT(self):
        devices = await BleakScanner.discover()

        device_found = []
        for device in devices:
            if device.name == None:
                pass
            else:
                device_found.append(device)

        event_manager.publish("request_bt_channels", device_found)
        
    async def validate_characteristic_uuid(self):
        # check if it is the right device you try to connect
        characteristics = var.ROBOT_BT_CLIENT.services
        characteristic_uuids = []
        for char in characteristics:
            characteristic_uuids.append(char.uuid)
        
        if SERVICE_UUID_ROBOT not in characteristic_uuids:
            await var.ROBOT_BT_CLIENT.disconnect()
            print(var.LANGUAGE_DATA.get("message_wrong_device")) 

    async def ConnectRobotBT(self, device_name = None):
        # if robot is connected disconnect
        if var.ROBOT_CONNECT:
            event_manager.publish("request_disable_robot_button", True)
            await var.ROBOT_BT_CLIENT.disconnect()
            var.ROBOT_CONNECT = False
            var.ROBOT_HOME = False  
            var.ROBOT_BLUETOOTH = False  
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)
            event_manager.publish("request_disable_robot_button", False)
        # if robot is not connected connect
        else:
            event_manager.publish("request_disable_robot_button", True)
            var.ROBOT_BT_CLIENT = BleakClient(device_name)

            await var.ROBOT_BT_CLIENT.connect()
            await self.validate_characteristic_uuid()
            
            if var.ROBOT_BT_CLIENT.is_connected:
                asyncio.run_coroutine_threadsafe(self.SendLineToRobot("CONNECT"), self.loop)
                await var.ROBOT_BT_CLIENT.start_notify(CHARACTERISTIC_UUID_ROBOT, self.ReadDataRobot) # start reading data
            else:
                print(var.LANGUAGE_DATA.get("message_faild_connect_bt")) 
                
            event_manager.publish("request_disable_robot_button", False)
                
    async def CloseRobot(self):
        # close the robot if it is connected    
        if var.ROBOT_CONNECT:
            print("disconnect trobot try")
            await var.ROBOT_BT_CLIENT.disconnect()

    async def ReadDataRobot(self, sender, data):
        # read the data that is send from the robot
        data_text = ""
        try:
            data_text = data.decode('utf-8')
        except UnicodeDecodeError:
            data_text = ""


        if data_text == "wait":
            self.pause_event.set()
        elif data_text.strip() == "go":
            self.pause_event.clear()
        elif data_text.strip() == "ROBOT_CONNECTED":
            var.ROBOT_BLUETOOTH = True
            var.ROBOT_CONNECT = True
            var.ROBOT_BUSY = False
            event_manager.publish("request_robot_connect_button_color", True)
            event_manager.publish("request_show_connection")
            self.SendSettingsRobot()    
        elif data_text.strip() == "IO_CONNECTED":
            print(var.LANGUAGE_DATA.get("message_io_instead_of_robot"))
        elif data_text.strip() == "home":
            var.ROBOT_HOME = True
            event_manager.publish("request_robot_home_button_color", True)
        elif data_text.strip() == "END":
            self.busy_event.clear()
            var.ROBOT_BUSY = False
        elif data_text.startswith("Tool state"):
            state = data_text.split()[-1]
            if state == "HIGH":
                event_manager.publish("request_set_tool_state", True)
            elif state == "LOW":
                event_manager.publish("request_set_tool_state", False)
            
        elif data_text.startswith("Input "):
            parts = data_text.split()
            
            io_number = int(parts[1])
            io_state = int(parts[2])
            
            if io_state == 1:
                event_manager.publish("request_set_io_state_input", io_number, True)
            else:
                event_manager.publish("request_set_io_state_input", io_number, False)       
        elif data_text.startswith("POS:"):
            words = data_text.split()

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
            data_text = "ROBOT: " + data_text
            print(data_text) 

    async def SendLineToRobot(self, message):
        while self.pause_event.is_set():
            time.sleep(0.1)
            
        time.sleep(0.2)
        var.ROBOT_BUSY = True

        
        if var.ROBOT_BT_CLIENT and var.ROBOT_BT_CLIENT.is_connected:
            #print(f"Message send {message}")
            await var.ROBOT_BT_CLIENT.write_gatt_char(CHARACTERISTIC_UUID_ROBOT, message.encode())
        else:
            await var.ROBOT_BT_CLIENT.disconnect()
            print(var.LANGUAGE_DATA.get("message_lost_connection_robot"))
            var.ROBOT_BLUETOOTH = False
            var.ROBOT_CONNECT = False
            var.ROBOT_HOME = False  
            var.ROBOT_BUSY = False
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)
            
    def run(self):
        self.loop.run_forever()

    def SendSettingsRobot(self):
        if not var.ROBOT_BUSY and var.ROBOT_CONNECT:
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
                
                return formatted_settings
            
            def threadSettings():
                # send all the settings to the robot except for the settings where the IO_box is checked
                for category in var.SETTINGS:
                    category_names.append(category)
                           
                # sent first the number of joints
                command = f'Set_number_of_joints A{var.NUMBER_OF_JOINTS}'
                asyncio.run_coroutine_threadsafe(self.SendLineToRobot(command), self.loop)
                time.sleep(0.2)
                
                if var.SETTINGS["Set_extra_joint"][0] == 1:
                    command = f'Set_extra_joint A1'
                    asyncio.run_coroutine_threadsafe(self.SendLineToRobot(command), self.loop)
                    time.sleep(0.2)
                           

                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]
                    if settings[1] == "" and  category_names[i] != 'Set_extra_joint' and  category_names[i] != 'Set_io_pin':
                        
                        command = make_line_ABC(settings[0], category_names[i])
                        asyncio.run_coroutine_threadsafe(self.SendLineToRobot(command), self.loop)
                        time.sleep(0.2)

            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.ROBOT_BUSY == 1:
                print(var.LANGUAGE_DATA.get("message_robot_busy")) 
                
            elif var.ROBOT_CONNECT == 0: 
                print(var.LANGUAGE_DATA.get("message_robot_not_connected")) 
                ErrorMessage(var.LANGUAGE_DATA.get("message_robot_not_connected"))
      
    def StopProgram(self):
        if var.ROBOT_BT_CLIENT.is_connected:
            asyncio.run_coroutine_threadsafe(self.SendLineToRobot("stop"), self.loop)
            
        print("Stop robot, wait 3 seconds before sending new command.")
        time.sleep(3)
        var.ROBOT_BUSY = 0
        
        if var.ROBOT_BT_CLIENT.is_connected:
            asyncio.run_coroutine_threadsafe(self.SendLineToRobot("play"), self.loop)         




class TalkWithRobotCOM():
    pause_event = threading.Event()
    busy_event = threading.Event()

    def __init__(self):
        super().__init__()
        self.pause_event.clear()
        self.busy_event.clear()

    def ConnectRobot(self, com_port = None):
        if var.ROBOT_CONNECT and not var.ROBOT_BUSY:
            event_manager.publish("request_disable_robot_button", True)
            var.ROBOT_CONNECT = False
            var.ROBOT_HOME = False  
            var.ROBOT_SER.close()
            print("Disconnect robot")
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)
            event_manager.publish("request_disable_robot_button", False)

        elif not var.ROBOT_CONNECT and var.ROBOT_COM:
            try:        
                var.ROBOT_COM = com_port
                var.ROBOT_SER = serial.Serial(var.ROBOT_COM, baudrate=115200)#, timeout=1)
                var.ROBOT_SER .dtr = False   # Ensure DTR is inactive
                var.ROBOT_SER .setRTS(False) # Deactivate RTS first
                time.sleep(0.1)
                var.ROBOT_SER .setRTS(True)  # Reactivate RTS to reset
                time.sleep(0.5)
                var.ROBOT_SER .dtr = True    # Enable DTR

                t_threadRead = threading.Thread(target=self.ReadDataRobot)  
                t_threadRead.start()

                start_time = time.time()
                while var.ROBOT_CONNECT == 0:
                    time.sleep(0.01)  
                    current_time = time.time()
                    if current_time - start_time > 4:
                        break
                if var.ROBOT_CONNECT: 
                    event_manager.publish("request_robot_connect_button_color", True)
                    self.SendSettingsRobot()
                else:
                    print(var.LANGUAGE_DATA.get("message_failed_connection_com"))
                    var.ROBOT_SER.close()
            
            except serial.SerialException:
                print(var.LANGUAGE_DATA.get("message_failed_connection_com"))
                        
        else:
            if var.ROBOT_BUSY == 1:       
                print(var.LANGUAGE_DATA.get("message_robot_busy")) 
  
    def CloseRobot(self):
        if var.ROBOT_CONNECT:
            var.ROBOT_SER.close()
            var.ROBOT_HOME = False
    
    def StopProgram(self):
        def threadStop():
            # send all the settings to the robot except for the settings where the IO_box is checked
            command = "stop\n"
            if var.ROBOT_SER:
                var.ROBOT_SER.write(command.encode())
                
            print("Stop robot, wait 3 seconds before sending new command.")
            time.sleep(3)
            
            var.ROBOT_BUSY = 0
            command = "play\n"
            
            if var.ROBOT_SER:
                var.ROBOT_SER.write(command.encode())            
                                                
        t_threadStop = threading.Thread(target=threadStop)  
        t_threadStop.start()   
            
    def SendLineToRobot(self, command):
        while self.pause_event.is_set():
            time.sleep(0.1)
        
        var.ROBOT_BUSY = 1   

        try:
            var.ROBOT_SER.write(command.encode())
        except:
            self.CloseRobot()
            print(var.LANGUAGE_DATA.get("message_lost_connection_robot"))
            
        time.sleep(0.3)
                   
    def ReadDataRobot(self):
        while var.ROBOT_SER.is_open:
            try:
                data = var.ROBOT_SER.readline().decode('latin-1').rstrip()  # Read a line
            except:
                break

            if data:
                if data == "wait":
                    self.pause_event.set()
                elif data.strip() == "go":
                    self.pause_event.clear()
                elif data.strip() == "ROBOT_CONNECTED":
                    var.ROBOT_CONNECT = True
                    var.ROBOT_BUSY = False
                elif data.strip() == "IO_CONNECTED":
                    print(var.LANGUAGE_DATA.get("message_robot_instead_of_io"))

                elif data.strip() == "home":
                    var.ROBOT_HOME = True
                    event_manager.publish("request_robot_home_button_color", True)
                elif data.strip() == "END":
                    self.busy_event.clear()
                    var.ROBOT_BUSY = 0   
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
                    data_text = "ROBOT: " + data
                    print(data_text) 
                    
                data = None


            time.sleep(0.01)
           
            
        var.ROBOT_BUSY = 0
        var.ROBOT_CONNECT = 0
        event_manager.publish("request_robot_connect_button_color", False)
                
    def SendSettingsRobot(self):
        if not var.ROBOT_BUSY and var.ROBOT_CONNECT:
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
                self.SendLineToRobot(command)
                time.sleep(0.2)
                
                if var.SETTINGS["Set_extra_joint"][0] == 1:
                    command = f'Set_extra_joint A1\n'
                    self.SendLineToRobot(command)
                    time.sleep(0.2)
                           
                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]

                    if settings[1] == "" and  category_names[i] != 'Set_extra_joint':
                        command = make_line_ABC(settings[0], category_names[i])
                        self.SendLineToRobot(command)
                                  
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.ROBOT_BUSY == 1:
                print(var.LANGUAGE_DATA.get("message_robot_busy")) 
            elif var.ROBOT_CONNECT == 0:
                print(var.LANGUAGE_DATA.get("message_robot_not_connected")) 
                ErrorMessage(var.LANGUAGE_DATA.get("message_robot_not_connected"))
      

