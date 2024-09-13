import threading
import tkinter.messagebox
import tkinter as tk
import time
import serial
import backend.core.variables as var
from serial.serialutil import SerialException

from backend.core.event_manager import event_manager

class TalkWithRobot:
    pause_event = threading.Event()
    busy_event = threading.Event()
    
    def __init__ (self):
        self.pause_event.clear()
        self.busy_event.clear()
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_close_robot", self.CloseRobot)
       
    def CloseRobot(self):
        if var.ROBOT_CONNECT:
            var.ROBOT_SER.close()
        
    def ConnectRobot(self):   
        if var.ROBOT_CONNECT and not var.ROBOT_BUSY:
            var.ROBOT_CONNECT = False
            var.ROBOT_HOME = False  
            var.ROBOT_SER.close()
            print("disconnect robot")
            event_manager.publish("request_robot_connect_button_color", False)
            event_manager.publish("request_robot_home_button_color", False)
            
        elif not var.ROBOT_CONNECT and var.ROBOT_COM:
            print("try to connect")
            try:        
                var.ROBOT_SER = serial.Serial('COM'+ var.ROBOT_COM, 19200)
                if var.ROBOT_SER.is_open:
                    event_manager.publish("request_robot_connect_button_color", True)
                    while True and var.ROBOT_CONNECT == 0:
                        line = var.ROBOT_SER.readline().decode(encoding='latin-1').strip()
                        print(line)
                        if "start robot" in line:
                            var.ROBOT_CONNECT = 1
                            self.read_data_robot()
                            self.send_settings()
                                                        

            except serial.SerialException:
                tkinter.messagebox.showinfo("info", "cannot find the robot, check if you have the right COM port")
        else:
            if var.ROBOT_COM == "":
                tkinter.messagebox.showinfo("info", "fill in the COM port")
            if var.ROBOT_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is busy performing a task, stop task or wait to be finished")            
    
    def SendLineToRobot(self, command):
        while self.pause_event.is_set():
            time.sleep(0.1)
            print(f"self.pauze_event {self.pause_event}")
            print("waiting")
        
        var.ROBOT_BUSY = 1   
        print(f"send to robot {command}")
        
        try:
            var.ROBOT_SER.write(command.encode())
        except:
            print("lost connection")
            
        start_time = time.time()
        while var.ROBOT_BUSY: 
            if time.time() - start_time >= 10:
                break 
            time.sleep(0.03)
            
    # for now only used for Gcode        
    def send_multiple_lines(self, commandos):
        self.current_line_index = 0
        self.pause_event.clear()
        
        def ThreadSendLines():
            var.ROBOT_BUSY = 1
            while self.current_line_index < len(commandos):
                while self.pause_event.is_set():
                    time.sleep(0.1)
                    
                command = commandos[self.current_line_index]
                try:
                    print(command)
                    var.ROBOT_SER.write(command.encode())
                    self.current_line_index += 1
                except:
                    tkinter.messagebox.showwarning(title="Warning", message="Lost connection with the robot")
                time.sleep(0.1)
            
            if self.current_line_index == len(commandos):
                var.ROBOT_BUSY = 0
                self.pause_event.clear()

        t_ThreadSendLines = threading.Thread(target=ThreadSendLines)  
        t_ThreadSendLines.start()  
                   
    def read_data_robot(self):
        print("start reading data")
        def threadReadRobot():
            while var.ROBOT_CONNECT == 1:
                try:
                    data = var.ROBOT_SER.readline().decode(encoding='latin-1').strip()
                    print(data)
                    if data.strip() == "wait":
                        self.pause_event.set()
                        print(f"self.pauze_event {self.pause_event}")
                    elif data.strip() == "go":
                        self.pause_event.clear()
                    elif data.strip() == "home":
                        var.ROBOT_HOME = 1
                        event_manager.publish("request_robot_home_button_color", True)
                    elif data.strip() == "END":
                        self.busy_event.clear()
                        print("read END")
                        var.ROBOT_BUSY = 0
                        
                    elif data.startswith("POS:"):
                        words = data.split()

                        try:
                            for i in range(len(words)):
                                if words[i] == 'G':
                                    var.POS_GRIPPER = float(words[i + 1])
                                    
                                for j in range(var.NUMBER_OF_JOINTS):
                                    if words[i] == var.NAME_JOINTS[j]:
                                        var.POS_JOINT[j] = float(words[i + 1])
                                        event_manager.publish("request_label_pos_joint", float(words[i + 1]), var.NAME_JOINTS[j], var.UNIT_JOINT[j])

                                for j in range(var.NUMBER_OF_JOINTS):
                                    if words[i] == var.NAME_AXIS[j]:
                                        var.POS_AXIS[j] = float(words[i + 1])
                                        event_manager.publish("request_label_pos_axis", float(words[i + 1]), var.NAME_AXIS[j], var.UNIT_AXIS[j])
                        except:
                            pass
                except SerialException as e:
                    tkinter.messagebox.showwarning(title="Warning", message="Lost connection with the robot")
                    var.ROBOT_BUSY = 0
                    var.ROBOT_CONNECT = 0
                    break
                
                time.sleep(0.03)
                
        t_threadRead = threading.Thread(target=threadReadRobot)  
        t_threadRead.start()

    def SendSettingsRobot(self):
        print("talky")
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
                    print(category)
                    
                    
                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]
                    if settings[1] == "":
                        command = make_line_ABC(settings[0], category_names[i])
                        self.send_to_robot_one_line(command)
                          
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.ROBOT_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is busy performing a task")
            elif var.ROBOT_CONNECT == 0:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is not connected")       
      
    # if a tool change than send again the settings related to the tool
    def send_tool_settings(self, TOOL):
        if var.ROBOT_BUSY == 0 and var.ROBOT_CONNECT == 1:
            def make_line_ABC(settings_values, command_name):
                letters = [chr(i) for i in range(65, 91)]  # A-Z letters
                formatted_settings = f"{command_name} "


                for i, value in enumerate(settings_values):
                    formatted_settings += letters[i] + str(value)

                formatted_settings += "\n"
                return formatted_settings
        
            try:
                with open(f"settings/settings_tool{TOOL}.json", 'r') as file:
                    settings_file = json.load(file)
                    settings = []
                    for i in range (1, len(settings_file)):
                        settings.append(settings_file[i])
                        
                    command = make_line_ABC(settings, "Set_tool")
                    self.TalkWithRobot.send_to_robot_one_line(command)
            except:
                pass       
        else:
            if var.ROBOT_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is busy performing a task")
            elif var.ROBOT_CONNECT == 0:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is not connected")       

class TalkWithIO:
    def __init__ (self):
        self.data = ""
        self.subscribeToEvents()
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_close_io", self.CloseIO)
       
 
    def CloseIO(self):
        if var.ROBOT_CONNECT:
            var.ROBOT_SER.close() 
    
    def ConnectIO(self):     
        if var.IO_CONNECT == 1 and var.ROBOT_BUSY == 0:
            var.IO_CONNECT = 0      
            var.IO_SER.close()
            print("disconnect IO")
            event_manager.publish("request_io_connect_button_color", False)
        elif var.IO_CONNECT == 0 and var.IO_COM:
            try:   
                var.IO_SER = serial.Serial('COM'+var.IO_COM, 19200)
                if var.IO_SER.is_open:
                    event_manager.publish("request_io_connect_button_color", True)
        
                    while True and var.IO_CONNECT == 0:
                        line = var.IO_SER.readline().decode(encoding='latin-1').strip()
                        print(line)
                        if "start io" in line:
                            var.IO_CONNECT = 1
                    self.read_data_IO()
                    #self.send_settings

            except serial.SerialException:
                tkinter.messagebox.showinfo("info", "cannot find the IO, check if you have the right COM port")
        else:
            if var.IO_COM == "":
                tkinter.messagebox.showinfo("info", "fill in the COM port")
            if var.ROBOT_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is busy performing a task, stop task or wait to be finished")            
    
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
                        self.send_to_IO(command)
                          
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.IO_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Input output module is busy performing a task")
            elif var.ROBOT_CONNECT == 0:
                tkinter.messagebox.showwarning(title="Warning", message="Input output module is not connected")  
    
    # if a tool change than send again the settings related to the tool
    def send_tool_settings(self):
        pass
    
    def send_to_IO(self, command):   
        print(f"send to io {command}")
        var.IO_SER.write(command.encode())
        time.sleep(0.15)
                                      
    def read_data_IO(self):
        def threadRead():
            while var.IO_CONNECT == 1:
                try:
                    if var.IO_SER.in_waiting:
                        self.data = var.IO_SER.readline().decode(encoding='latin-1').strip()
                        if self.data.startswith("Input_"):
                           pass
                        else:
                            print(self.data)
                            
                except SerialException as e:
                    tkinter.messagebox.showwarning(title="Warning", message="Lost connection with the robot")
                    var.ROBOT_BUSY = 0
                    var.ROBOT_CONNECT = 0
                    break
                time.sleep(0.1)    
                
        t_threadRead = threading.Thread(target=threadRead)  
        t_threadRead.start()

    def data_read(self, input):
        if var.IO_SER.in_waiting:
            self.data = var.IO_SER.readline().decode(encoding='latin-1').strip()
        if self.data == f"Input_{input}":
            self.data = ""
            return 1
        else:
            return 0

    def PlayPauzeRobot(self):
        if var.ROBOT_CONNECT:
            if var.ROBOT_PAUZE:
                command = f"play\n"
                self.ser.write(command.encode())
                time.sleep(0.2)
                var.ROBOT_PAUZE = False
            elif not var.ROBOT_PAUZE:
                command = f"pauze\n"
                self.ser.write(command.encode())
                time.sleep(0.2)
                var.ROBOT_PAUZE = True
        else:
            tkinter.messagebox.showwarning(title="Warning", message="Robot is not connected") 
