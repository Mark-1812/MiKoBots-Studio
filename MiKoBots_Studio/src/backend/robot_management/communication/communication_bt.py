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

CHARACTERISTIC_UUID_IO = "19680482-86af-4892-ab79-962e98f41045"
SERVICE_UUID_IO = "30a96603-6e34-49d8-9d64-a13f68fefab6"

class TalkThroughBT(QThread):
    pause_event = threading.Event()
    busy_event = threading.Event()

    def __init__(self, ROBOT=False, IO=False):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.pause_event.clear()
        self.busy_event.clear()
        self.start()

        self.ROBOT = ROBOT
        self.IO = IO

        self.client_bt = None
        self.connect = False
        self.robot_home = False
        self.busy = False
        self.stop = False

    def ScanForDevice(self):
        asyncio.run_coroutine_threadsafe(self._ScanForDevices(), self.loop)
    
    async def _ScanForDevices(self):
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
        characteristics = self.client_bt.services
        characteristic_uuids = []
        for char in characteristics:
            characteristic_uuids.append(char.uuid)

        if self.ROBOT and (SERVICE_UUID_ROBOT not in characteristic_uuids):
            print(var.LANGUAGE_DATA.get("message_wrong_device")) 
            return False

        if self.IO and (SERVICE_UUID_IO not in characteristic_uuids):
            #print(var.LANGUAGE_DATA.get("message_wrong_device")) 
            return False

        return True

    def Connect(self, addres):
        asyncio.run_coroutine_threadsafe(self._Connect(addres), self.loop)


        start_time = time.time()
        while not self.connect:
            time.sleep(0.01)  
            current_time = time.time()
            if current_time - start_time > 4:
                break
        
        if self.ROBOT and self.connect:
            event_manager.publish("request_robot_connect_button_color", self.connect)
        if self.IO and self.connect:
            event_manager.publish("request_io_connect_button_color", self.connect)

    async def _Connect(self, addres):
        self.client_bt = BleakClient(addres)

        await self.client_bt.connect()
        device = await self.validate_characteristic_uuid()
        
        if self.ROBOT and self.client_bt.is_connected and device:
            await self.client_bt.start_notify(CHARACTERISTIC_UUID_ROBOT, self.ReadData) # start reading data
            self.busy = False
            self.SendLineCommand("CONNECT")   
        elif self.IO and self.client_bt.is_connected and device:
            await self.client_bt.start_notify(CHARACTERISTIC_UUID_IO, self.ReadData) # start reading data
            self.busy = False
            self.SendLineCommand("CONNECT")   
        else:
            print(var.LANGUAGE_DATA.get("message_faild_connect_bt")) 
            

    def Disconnect(self):
        asyncio.run_coroutine_threadsafe(self._Disconnect(), self.loop)

    async def _Disconnect(self):
        await self.client_bt.disconnect()
        self.connect = False

        if self.ROBOT:
            self.robot_home = False  
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)


        if self.ROBOT:
            event_manager.publish("request_io_connect_button_color", False)

    def Close(self):     
        asyncio.run_coroutine_threadsafe(self._Close(), self.loop)
                
    async def _Close(self):
        # close the robot if it is connected    
        if self.connect:
            print("disconnect trobot try")
            await self.client_bt.disconnect()

    async def ReadData(self, sender, data):
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
            if self.ROBOT:
                self.connect = True
                self.busy = False
                #event_manager.publish("request_robot_connect_button_color", True)
                self.SendSettingsRobot()    
            if self.IO:
                print(var.LANGUAGE_DATA.get("message_io_instead_of_robot"))
                self.disconnect()


        elif data_text.strip() == "IO_CONNECTED":
            if self.ROBOT:
                #print(var.LANGUAGE_DATA.get("message_robot_instead_of_io"))
                print(" error")
                self.disconnect()
            
            if self.IO:
                self.connect = True
                self.busy = False
                event_manager.publish("request_robot_connect_button_color", True)
                self.SendSettingsIO()   


        elif data_text.strip() == "home":
            self.robot_home = True
            event_manager.publish("request_robot_home_button_color", True)
        elif data_text.strip() == "END":
            self.busy_event.clear()
            self.busy = False
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
            pass
        data_text = "ROBOT: " + data_text
        print(data_text) 

    def SendLineCommand(self, command):
        while self.pause_event.is_set():
            time.sleep(0.1)

        start_time = time.time()
        while self.busy: 
            if time.time() - start_time >= 10:
                break 
            time.sleep(0.03)
            
        self.busy = True
        asyncio.run_coroutine_threadsafe(self._SendLineCommand(command), self.loop)

    async def _SendLineCommand(self, message):
        if self.ROBOT and self.client_bt.is_connected:
            print(f"sent: {message}")
            await self.client_bt.write_gatt_char(CHARACTERISTIC_UUID_ROBOT, message.encode())
        elif self.IO and self.client_bt.is_connected:
            print(f"sent: {message}")
            await self.client_bt.write_gatt_char(CHARACTERISTIC_UUID_IO, message.encode())
        else:
            print(var.LANGUAGE_DATA.get("message_lost_connection_robot"))
            self.disconnect()    
            


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
                
                return formatted_settings
            
            def threadSettings():
                # send all the settings to the robot except for the settings where the IO_box is checked
                for category in var.SETTINGS:
                    category_names.append(category)
                           
                # sent first the number of joints
                command = f'Set_number_of_joints A{var.NUMBER_OF_JOINTS}'
                self.SendLineCommand(command)
                
                if var.SETTINGS["Set_extra_joint"][0] == 1:
                    command = f'Set_extra_joint A1'
                    self.SendLineCommand(command)           

                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]
                    if settings[1] == "" and  category_names[i] != 'Set_extra_joint' and  category_names[i] != 'Set_io_pin'and  category_names[i] != 'Set_robot_name':
                        
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
                        command = make_line_ABC(settings[0], category_names[i])
                        ready = asyncio.run_coroutine_threadsafe(self.SendLineCommand(command), self.loop)
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if self.busy == 1:
                print(var.LANGUAGE_DATA.get("message_io_busy"))

            elif self.connect == 0:
                print(var.LANGUAGE_DATA.get("message_io_not_connected"))

    def StopProgram(self):
        if self.client_bt.is_connected:
            asyncio.run_coroutine_threadsafe(self._SendLineCommand("stop"), self.loop)
            
        self.busy = False
        self.stop = True

    def PlayProgram(self):
        if self.client_bt.is_connected:
            asyncio.run_coroutine_threadsafe(self._SendLineCommand("play"), self.loop)



    def run(self):
        self.loop.run_forever()