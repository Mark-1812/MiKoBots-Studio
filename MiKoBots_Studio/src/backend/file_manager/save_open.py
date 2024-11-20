from PyQt5.QtWidgets import QPushButton, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import os
import ast

import backend.core.variables as var


from gui.windows.message_boxes import ErrorMessage, SaveProgramMessage

from backend.core.event_manager import event_manager

from backend.robot_management import change_robot, get_selected_robot, get_selected_robot_name

from backend.run_program import check_program_run

from backend.simulation.object import open_object_file, close_object_file, get_objects_sim
from backend.simulation.origins import open_origins_file, close_origins_file, get_origins_file

import threading
import time
         
class SaveOpen:
    def __init__(self):
        self.MikoFile = [
                    "Program text",
                    "Gcode",
                    "3D models",
                    "origins",
                    "Selected robot",
                    "Selected tool",
                    "Program blockly"
                    
        ]
        #self.file_dialog = QFileDialog()
        
        self.program_path = ""
        self.program_folder = ""

           
    def NewFile(self):
        if  check_program_run():    
            return
            
        answer = SaveProgramMessage(var.LANGUAGE_DATA.get("message_ask_save_program"))

        if answer == 1:
            self.SaveFile() 
                    
        self.CloseFile()
        self.MikoFile = [
                "",
                "",
                [],
                [],
                get_selected_robot(),
                var.SELECTED_TOOL,
                ""
        ]
        self.SetProgram()


                  
    def SaveFile(self):
        def ThreadSave():
            self.MikoFile[6] = ""
            self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
            #self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
            self.MikoFile[2] = get_objects_sim()
            self.MikoFile[3] = get_origins_file()
            self.MikoFile[4] = get_selected_robot_name()
            self.MikoFile[5] = var.SELECTED_TOOL
            event_manager.publish("request_save_blockly_file")
            
            while self.MikoFile[6] == "":
                time.sleep(0.01)
            
            try:
                if self.program_path:
                    event_manager.publish("request_set_program_title", os.path.basename(self.program_path))       
                    with open(self.program_path, "w") as file:
                        file.write(str(self.MikoFile))
                else:
                    
                    self.SaveAsFile()
            except:
                self.SaveAsFile()
                
        t_threadRead = threading.Thread(target=ThreadSave)  
        t_threadRead.start()

    def SaveAsFile(self):
        if check_program_run():    
            return

        self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
        #self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
        self.MikoFile[2] = get_objects_sim()
        self.MikoFile[3] = get_origins_file()
        self.MikoFile[4] = get_selected_robot_name()
        self.MikoFile[5] = var.SELECTED_TOOL
        event_manager.publish("request_save_blockly_file")
        
        
        options = QFileDialog.Options()
        
        self.program_path, _  = QFileDialog.getSaveFileName(None, "Save .miko File", str(self.program_folder), "MiKo Files (*.miko);;All Files (*)", options=options)
    
    
        if self.program_path:
            self.program_folder = os.path.dirname(self.program_path)            
            event_manager.publish("request_set_program_title", os.path.basename(self.program_path))
            with open(self.program_path, "w") as file:
                file.write(str(self.MikoFile))          
                
    def OpenFileFromPath(self, file_path):

        self.program_path = file_path

        
        self.CloseFile()
        
        self.program_folder = os.path.dirname(self.program_path)
            
        event_manager.publish("request_set_program_title", os.path.basename(self.program_path))
        with open(self.program_path, "r") as file:
            program = file.read()
            self.MikoFile = ast.literal_eval(program)      
            self.SetProgram()
            
            if len(self.MikoFile) == 6:
                self.MikoFile.append("Blockly")      
      
                
    def OpenFile(self):
        if check_program_run():  
            return
        
        answer = SaveProgramMessage(var.LANGUAGE_DATA.get("title_save"), var.LANGUAGE_DATA.get("message_ask_save_program"))

        if answer == 1:
            self.SaveFile()    
            
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.program_path, _ = QFileDialog.getOpenFileName(None, "Open .miko File", str(self.program_folder), "MiKo Files (*.miko);;All Files (*)", options=options)
        
        if not self.program_path:
            return
        
        self.CloseFile()
        
        self.program_folder = os.path.dirname(self.program_path)
            
        event_manager.publish("request_set_program_title", os.path.basename(self.program_path))
        with open(self.program_path, "r") as file:
            program = file.read()
            self.MikoFile = ast.literal_eval(program)      
            self.SetProgram()
            
            if len(self.MikoFile) == 6:
                self.MikoFile.append("Blockly")
        
            
    
    def SetProgram(self):
            
        # Program text
        event_manager.publish("request_program_field_insert", self.MikoFile[0])
        
        # Blockly program
        try:
            event_manager.publish("request_load_blockly_file", self.MikoFile[6])
        except:
            pass
        
        # 3d models
        try:
            open_object_file(self.MikoFile[2])
        except:
            ErrorMessage(var.LANGUAGE_DATA.get("message_not_open_3dmodel"))

        # Origin
        open_origins_file(self.MikoFile[3])
        
        
        # Robot
        try:           
            change_robot(self.MikoFile[4])
            # Tool
            event_manager.publish("request_set_tool_combo", self.MikoFile[5])
        except:
            change_robot(0)
            event_manager.publish("request_set_tool_combo", 0)
            ErrorMessage(var.LANGUAGE_DATA.get("message_not_open_robot"))
            
             
    def CloseFile(self):            
        event_manager.publish("request_program_field_clear")     
        event_manager.publish("request_gcode_text_clear")
        close_object_file()
        close_origins_file()
        event_manager.publish("request_clear_blockly_file")
        
        
        
    def BlocklyConverting(self, xmlString):
        self.MikoFile[6] = xmlString 
        
        if self.MikoFile[6] == "":
            self.MikoFile[6] = "None"

                
