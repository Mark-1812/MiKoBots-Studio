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


CHARACTERISTIC_UUID_IO = "19680482-86af-4892-ab79-962e98f41045"
SERVICE_UUID_IO = "30a96603-6e34-49d8-9d64-a13f68fefab6"


class TalkWithIOBT(QThread):
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
        characteristics = var.IO_BT_CLIENT.services  
        characteristic_uuids = []
        for char in characteristics:
            characteristic_uuids.append(char.uuid)

        if SERVICE_UUID_IO not in characteristic_uuids:
            await var.IO_BT_CLIENT.disconnect()
            print(var.LANGUAGE_DATA.get("message_wrong_device")) 

    async def ConnectIOBT(self, device_name = None):
        # if the IO is already connected disconnect
        if var.IO_CONNECT:
            await var.IO_BT_CLIENT.disconnect()
            var.IO_CONNECT = False
            event_manager.publish("request_io_connect_button_color", False) 
            var.IO_BLUETOOTH = False
            
        # if the IO is not connected
        else:
            var.IO_BT_CLIENT = BleakClient(device_name)
            
            await var.IO_BT_CLIENT.connect()
            await self.validate_characteristic_uuid()

            if var.IO_BT_CLIENT.is_connected:
                asyncio.run_coroutine_threadsafe(self.SendLineToIO("CONNECT"), self.loop)
                await var.IO_BT_CLIENT.start_notify(CHARACTERISTIC_UUID_IO, self.ReadDataIO)
            else:
                print(var.LANGUAGE_DATA.get("message_faild_connect_bt"))  
            
    async def CloseIO(self):
        # close the io if it is connected
        if var.IO_CONNECT:
            await var.IO_BT_CLIENT.disconnect()    

    async def ReadDataIO(self, sender, data):
        data_text = ""
        try:
            data_text = data.decode('utf-8')
        except UnicodeDecodeError:
            data_text = ""

    
        if data_text.strip() == "END":
            var.IO_BUSY = False
        elif data_text.strip() == "IO_CONNECTED":
            var.IO_BLUETOOTH = True
            var.IO_CONNECT = True
            var.IO_BUSY = False
            event_manager.publish("request_io_connect_button_color", True)
            self.SendSettingsIO()
        elif data_text.strip() == "ROBOT_CONNECTED":
            print(var.LANGUAGE_DATA.get("error_robot_instead_of_io"))
        elif data_text.startswith("Input "):
            parts = data.split()
            
            io_number = int(parts[1])
            io_state = int(parts[2])
            
            if io_state == 1:
                event_manager.publish("request_set_io_state_input", io_number, True)
            else:
                event_manager.publish("request_set_io_state_input", io_number, False)
        elif data_text.startswith("Tool state"):
            state = data_text.split()[-1]
            if state == "HIGH":
                event_manager.publish("request_set_tool_state", True)
            elif state == "LOW":
                event_manager.publish("request_set_tool_state", False)
    
        elif data_text.startswith("POS:"):
            words = data_text.split()

            for i in range(len(words)):
                if words[i] == 'G':
                    var.POS_GRIPPER = float(words[i + 1])
                
                event_manager.publish("request_set_tool_pos", var.POS_GRIPPER)

        else:
            data_text = "ESP32: " + data_text
            print(data_text) 
        
    async def SendLineToIO(self, message):
        while self.pause_event.is_set():
            time.sleep(0.1)
            
        var.IO_BUSY = True
            
        if var.IO_BT_CLIENT.is_connected:
            await var.IO_BT_CLIENT.write_gatt_char(CHARACTERISTIC_UUID_IO, message.encode())
        else:
            await var.IO_BT_CLIENT.disconnect()
            print(var.LANGUAGE_DATA.get("message_lost_connection_io"))
            var.IO_CONNECT = False
            var.IO_BUSY = False
            event_manager.publish("request_robot_connect_button_color", False)       
            
    def run(self):
        self.loop.run_forever()

    def SendSettingsIO(self):
        if not var.IO_BUSY and var.IO_CONNECT:
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
                        command = make_line_ABC(settings[0], category_names[i])
                        asyncio.run_coroutine_threadsafe(self.SendLineToIO(command), self.loop)
                        time.sleep(0.2)
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.IO_BUSY == 1:
                print(var.LANGUAGE_DATA.get("message_io_busy"))

            elif var.ROBOT_CONNECT == 0:
                print(var.LANGUAGE_DATA.get("message_io_not_connected"))




class TalkWithIOCOM:
    def __init__ (self):
        self.data = ""
       
    def CloseIO(self):
        if var.IO_CONNECT:
            var.IO_SER.close() 
    
    def ConnectIO(self, com_port = None):
        if var.IO_CONNECT == 1 and var.IO_BUSY == 0:
            var.IO_CONNECT = False     
            var.IO_SER.close()
            print("disconnect IO")
            event_manager.publish("request_io_connect_button_color", False) 
            
            
        elif not var.IO_CONNECT and var.IO_COM:
            try:    
                var.IO_COM = com_port
                var.IO_SER = serial.Serial(var.IO_COM, baudrate=115200, timeout=1)
                var.IO_SER .dtr = False   # Ensure DTR is inactive
                var.IO_SER .setRTS(False) # Deactivate RTS first
                time.sleep(0.1)
                var.IO_SER .setRTS(True)  # Reactivate RTS to reset
                time.sleep(0.5)
                var.IO_SER .dtr = True    # Enable DTR
                
                t_threadRead = threading.Thread(target=self.ReadDataIO)  
                t_threadRead.start()
                
                start_time = time.time()
                while var.IO_CONNECT == 0:
                    time.sleep(0.01)  
                    current_time = time.time()
                    if current_time - start_time > 4:
                        break
                if var.IO_CONNECT: 
                    event_manager.publish("request_io_connect_button_color", True)
                    self.SendSettingsIO()
                else:
                    print(var.LANGUAGE_DATA.get("message_failed_connection_com"))
                    var.IO_SER.close()
                
            except serial.SerialException:
                print(var.LANGUAGE_DATA.get("message_failed_connection_com"))
                       
        else:
            if var.IO_BUSY == 1:
                print(var.LANGUAGE_DATA.get("message_io_busy"))

    def CloseIO(self):
        if var.IO_CONNECT:
            var.IO_SER.close()

    def SendSettingsIO(self):
        if not var.IO_BUSY and var.IO_CONNECT:
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
                        
                        self.SendLineToIO(command)
                          
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.IO_BUSY == 1:
                print(var.LANGUAGE_DATA.get("message_io_busy"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_io_busy"))
            elif var.IO_CONNECT == 0:
                print(var.LANGUAGE_DATA.get("message_io_not_connected"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_io_not_connected"))

    def SendLineToIO(self, command):          
        var.IO_BUSY = True
        try:
            var.IO_SER.write(command.encode())
        except:
            self.CloseIO()
            print(var.LANGUAGE_DATA.get("message_lost_connection_io"))
            
        time.sleep(0.2)
                                      
    def ReadDataIO(self):
        while var.IO_SER.is_open:
            try:
                if var.IO_SER.in_waiting > 0:
                    data = var.IO_SER.readline().decode('utf-8').rstrip()  # Read a line
            except:
                break
            
            if data:
                if data.strip() == "END":
                    var.IO_BUSY = False
                elif data.strip() == "IO_CONNECTED":
                    var.IO_CONNECT = True
                    var.IO_BUSY = False
                elif data.strip() == "ROBOT_CONNECTED":
                    print(var.LANGUAGE_DATA.get("message_io_instead_of_robot"))
                    ErrorMessage(var.LANGUAGE_DATA.get("message_io_instead_of_robot"))
                elif data.startswith("Input "):
                    parts = data.split()
                    
                    io_number = int(parts[1])
                    io_state = int(parts[2])
                    
                    if io_state == 1:
                        event_manager.publish("request_set_io_state_input", io_number, True)
                    else:
                        event_manager.publish("request_set_io_state_input", io_number, False)
                elif data.startswith("Tool state"):
                    state = data.split()[-1]
                    if state == "HIGH":
                        event_manager.publish("request_set_tool_state", True)
                    elif state == "LOW":
                        event_manager.publish("request_set_tool_state", False)
            
                elif data.startswith("POS:"):
                    words = data.split()

                    for i in range(len(words)):
                        if words[i] == 'G':
                            var.POS_GRIPPER = float(words[i + 1])
                        
                        event_manager.publish("request_set_tool_pos", var.POS_GRIPPER)
                            
                else:
                    print(data)

            time.sleep(0.01)    
            
        var.IO_CONNECT = 0
        var.IO_BUSY = 0            
        event_manager.publish("request_io_connect_button_color", False)
            


