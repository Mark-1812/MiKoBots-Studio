from PyQt5.QtWidgets import QPushButton, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import os
import ast

import backend.core.variables as var


from gui.windows.message_boxes import ErrorMessage, SaveProgramMessage

from backend.core.event_manager import event_manager

from backend.core.api import change_robot

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
        self.file_dialog = QFileDialog()
        
        self.program_path = ""
        self.program_folder = ""
           
        event_manager.subscribe("request_program_xmlString", self.BlocklyConverting)
           
    def NewFile(self):
        if  var.PROGRAM_RUN:    
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
                var.SELECTED_ROBOT,
                var.SELECTED_TOOL,
                ""
        ]
        self.SetProgram()


                  
    def SaveFile(self):
        def ThreadSave():
            self.MikoFile[6] = ""
            self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
            #self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
            self.MikoFile[2] = event_manager.publish("request_get_objects_plotter")[0]
            self.MikoFile[3] = event_manager.publish("request_get_origins_plotter")[0]
            self.MikoFile[4] = var.ROBOTS[var.SELECTED_ROBOT][0] # robot name
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
        if var.PROGRAM_RUN:    
            return

        self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
        #self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
        self.MikoFile[2] = event_manager.publish("request_get_objects_plotter")[0]
        self.MikoFile[3] = event_manager.publish("request_get_origins_plotter")[0]
        self.MikoFile[4] = var.ROBOTS[var.SELECTED_ROBOT][0]
        self.MikoFile[5] = var.SELECTED_TOOL
        event_manager.publish("request_save_blockly_file")
        
        options = QFileDialog.Options()
        
        self.program_path, _  = QFileDialog.getSaveFileName(None, "Save .miko File", str(self.program_folder), "MiKo Files (*.miko);;All Files (*)", options=options)
    
    
        if self.program_path:
            self.program_folder = os.path.dirname(self.program_path)            
            event_manager.publish("request_set_program_title", os.path.basename(self.program_path))
            with open(self.program_path, "w") as file:
                file.write(str(self.MikoFile))          
                
    def OpenFile(self):
        if var.PROGRAM_RUN:  
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
                print("Old file")
                self.MikoFile.append("Blockly")
                print(self.MikoFile)
            
    
    def SetProgram(self):
            
        # Program text
        event_manager.publish("request_program_field_insert", self.MikoFile[0])
        
        # Blockly program
        try:
            print(self.MikoFile[6])
            event_manager.publish("request_load_blockly_file", self.MikoFile[6])
        except:
            pass
            
        # Gcode
        #event_manager.publish("request_gcode_text_insert", self.MikoFile[1])
        
        # 3d models
        print(self.MikoFile[2])
        try:
            event_manager.publish("request_open_doc_objects", self.MikoFile[2])
        except:
            ErrorMessage(var.LANGUAGE_DATA.get("message_not_open_3dmodel"))

        # Origin
        event_manager.publish("request_open_doc_origins", self.MikoFile[3])
        
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
        event_manager.publish("request_close_doc_objects")
        event_manager.publish("request_close_doc_origins")
        event_manager.publish("request_clear_blockly_file")
        
        
        
    def BlocklyConverting(self, xmlString):
        self.MikoFile[6] = xmlString 
        
        if self.MikoFile[6] == "":
            self.MikoFile[6] = "None"

                
