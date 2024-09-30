import threading
import tkinter.messagebox
import tkinter as tk
import time
import serial
import backend.core.variables as var
from serial.serialutil import SerialException
import re

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
        event_manager.subscribe("request_stop_program", self.StopProgram)
        event_manager.subscribe("request_send_command", self.SendLineToRobot)
       
    def CloseRobot(self):
        if var.ROBOT_CONNECT:
            var.ROBOT_SER.close()
        
    def ConnectRobot(self):   
        var.ROBOT_COM = event_manager.publish("request_get_robot_port")[0]
        
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
                    time.sleep(2)
                    self.ReadDataRobot()
                    command = "CONNECT\n"
                    self.SendLineToRobot(command)  
                    
                    start_time = time.time()
                    while var.ROBOT_CONNECT == 0:
                        time.sleep(0.01)  
                        current_time = time.time()
                        if current_time - start_time > 2:
                            break
                        
                    if var.ROBOT_CONNECT: 
                        event_manager.publish("request_robot_connect_button_color", True)
                        self.SendSettingsRobot()
                    else:
                        var.ROBOT_SER.close()
            
            except serial.SerialException:
                tkinter.messagebox.showinfo("info", "cannot find the robot, check if you have the right COM port")
                        
        else:
            if var.ROBOT_COM == "":
                tkinter.messagebox.showinfo("info", "fill in the COM port")
            if var.ROBOT_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Robot is busy performing a task, stop task or wait to be finished")            
    
    def StopProgram(self):
        def threadStop():
            # send all the settings to the robot except for the settings where the IO_box is checked
            command = "stop\n"
            if var.ROBOT_SER:
                var.ROBOT_SER.write(command.encode())
            
            if var.IO_SER:
                var.IO_SER.write(command.encode())
                
            print("stop robot")
            time.sleep(2)
            
            var.ROBOT_BUSY = 0
            command = "play\n"
            
            if var.ROBOT_SER:
                var.ROBOT_SER.write(command.encode())            
            
            if var.IO_SER:
                var.IO_SER.write(command.encode())  
                                                
        t_threadStop = threading.Thread(target=threadStop)  
        t_threadStop.start()   
            
    def SendLineToRobot(self, command):
        while self.pause_event.is_set():
            time.sleep(0.1)
            print("waiting")
        
        var.ROBOT_BUSY = 1   
        time.sleep(0.2)
        
        try:
            print(f"send to robot {command}")
            var.ROBOT_SER.write(command.encode())
        except:
            self.CloseRobot()
            print("lost connection")
                   
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
                   
    def ReadDataRobot(self):
        print("start reading data")
        def threadReadRobot():
            while var.ROBOT_SER.is_open == 1:
                try:
                    data = var.ROBOT_SER.readline().decode(encoding='latin-1').strip()
                except SerialException as e:
                    tkinter.messagebox.showwarning(title="Warning", message="Lost connection with the robot")
                    break                    
                    
                print(data)
                if data.strip() == "wait":
                    self.pause_event.set()
                elif data.strip() == "go":
                    self.pause_event.clear()
                elif data.strip() == "ROBOT_CONNECTED":
                    var.ROBOT_CONNECT = 1
                    var.ROBOT_BUSY = 0 
                elif data.strip() == "IO_CONNECTED":
                    tkinter.messagebox.showwarning(title="Warning", message="This is the IO module not the robot!\n Check if you have the right com port")
                elif data.strip() == "home":
                    var.ROBOT_HOME = True
                    event_manager.publish("request_robot_home_button_color", True)
                elif data.strip() == "END":
                    self.busy_event.clear()
                    var.ROBOT_BUSY = 0   
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
                    event_manager.publish("request_insert_new_log", data)  
                    
                time.sleep(0.1)
                
            var.ROBOT_BUSY = 0
            var.ROBOT_CONNECT = 0
            event_manager.publish("request_robot_connect_button_color", False)
                
        t_threadRead = threading.Thread(target=threadReadRobot)  
        t_threadRead.start()

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
                           
                for i, setting in enumerate(var.SETTINGS):
                    settings = var.SETTINGS[category_names[i]]

                    if settings[1] == "" and  category_names[i] != 'Set_extra_joint':
                        command = make_line_ABC(settings[0], category_names[i])
                        self.SendLineToRobot(command)
                                  
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
        var.IO_COM = event_manager.publish("request_get_io_port")[0]
                 
        if var.IO_CONNECT == 1 and var.ROBOT_BUSY == 0:
            var.IO_CONNECT = False     
            var.IO_SER.close()
            print("disconnect IO")
            event_manager.publish("request_io_connect_button_color", False) 
            
            
        elif not var.IO_CONNECT and var.IO_COM:
            try:   
                var.IO_SER = serial.Serial('COM'+ var.IO_COM, 19200)

                if var.IO_SER.is_open:
                    time.sleep(2)
                    self.ReadDataIO()
                    command = "CONNECT\n"
                    self.SendLineToIO(command)  
                    
                    start_time = time.time()
                    while var.IO_CONNECT == 0:
                        time.sleep(0.01)  
                        current_time = time.time()
                        if current_time - start_time > 2:
                            break
                        
                    if var.IO_CONNECT: 
                        event_manager.publish("request_io_connect_button_color", True)
                        self.SendSettingsIO()
                    else:
                        var.IO_SER.close()
            
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
                        self.SendLineToIO(command)
                          
                
            t_threadSettings = threading.Thread(target=threadSettings)  
            t_threadSettings.start()         
            
            
        else:
            if var.IO_BUSY == 1:
                tkinter.messagebox.showwarning(title="Warning", message="Input output module is busy performing a task")
            elif var.ROBOT_CONNECT == 0:
                tkinter.messagebox.showwarning(title="Warning", message="Input output module is not connected")  
    
    def SendLineToIO(self, command):   
        print(f"send to io {command}")
        var.IO_SER.write(command.encode())
        time.sleep(0.15)
                                      
    def ReadDataIO(self):
        def threadRead():
            while var.IO_SER.is_open:
                try:
                    data = var.IO_SER.readline().decode(encoding='latin-1').strip()
                except:
                    if var.IO_CONNECT:
                        tkinter.messagebox.showwarning(title="Warning", message="Lost connection with the io")
                    var.IO_BUSY = False
                    var.IO_CONNECT = True
                    break                      
                
                print(data)

                if data.strip() == "END":
                    var.IO_BUSY = False
                elif data.strip() == "IO_CONNECTED":
                    var.IO_CONNECT = True
                    var.IO_BUSY = False
                elif data.strip() == "ROBOT_CONNECTED":
                    tkinter.messagebox.showwarning(title="Warning", message="This is the robot!")
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
                            
                time.sleep(0.01)    
                
            var.IO_CONNECT = 0
            var.IO_BUSY = 0            
            event_manager.publish("request_io_connect_button_color", False)
            
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
