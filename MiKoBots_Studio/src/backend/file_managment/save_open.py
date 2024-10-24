from PyQt5.QtWidgets import QPushButton, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import os
import ast

import tkinter.messagebox
import backend.core.variables as var

from gui.save_window import AskSave


from backend.core.event_manager import event_manager

import xmltodict
import json
         
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
           
    def NewFile(self):
        if  var.PROGRAM_RUN:    
            return
            
        answer = AskSave()
        if answer == "Yes":
            self.SaveFile() 
        elif answer == "No":
            pass
        elif answer == "Cancel":
            return
                    
        self.CloseFile()
        self.MikoFile = [
                "",
                "",
                [],
                [],
                var.SELECTED_ROBOT,
                var.SELECTED_TOOL,
                
        ]
        self.SetProgram()


                  
    def SaveFile(self):
        self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
        self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
        self.MikoFile[2] = event_manager.publish("request_get_objects_plotter")[0]
        self.MikoFile[3] = event_manager.publish("request_get_origins_plotter")[0]
        self.MikoFile[4] = event_manager.publish("request_get_current_robot_nr")[0]
        self.MikoFile[5] = event_manager.publish("request_get_tool_nr")[0]
        event_manager.publish("request_save_blockly_file")
        
        try:
            if self.program_path:
                event_manager.publish("request_set_program_title", os.path.basename(self.program_path))       
                with open(self.program_path, "w") as file:
                    file.write(str(self.MikoFile))
            else:
                self.SaveAsFile()
        except:
            self.SaveAsFile()

    def SaveAsFile(self):
        if var.PROGRAM_RUN:    
            return

        self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
        self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
        self.MikoFile[2] = event_manager.publish("request_get_objects_plotter")[0]
        self.MikoFile[3] = event_manager.publish("request_get_origins_plotter")[0]
        self.MikoFile[4] = event_manager.publish("request_get_current_robot_nr")[0]
        self.MikoFile[5] = event_manager.publish("request_get_tool_nr")[0]
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
        
        answer = AskSave()
        if answer == "Yes":
            self.SaveFile() 
        elif answer == "No":
            pass
        elif answer == "Cancel":
            return
            
            
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
            print("error old file")
            
        # Gcode
        event_manager.publish("request_gcode_text_insert", self.MikoFile[1])
        
        # 3d models
        print(self.MikoFile[2])
        #try:
        event_manager.publish("request_open_doc_objects", self.MikoFile[2])
        #except:
            #tkinter.messagebox.showerror("Waring", "could not open the 3d models")

        # Origin
        event_manager.publish("request_open_doc_origins", self.MikoFile[3])
        
        # Robot
        try:           
            event_manager.publish("request_change_robot", self.MikoFile[4])
            # Tool
            event_manager.publish("request_set_tool_combo", self.MikoFile[5])
        except:
            event_manager.publish("request_change_robot", 0)
            event_manager.publish("request_set_tool_combo", 0)
            tkinter.messagebox.showerror("Waring", "could not open the robot, from the file")
            
             
    def CloseFile(self):            
        event_manager.publish("request_program_field_clear")     
        event_manager.publish("request_gcode_text_clear")
        event_manager.publish("request_close_doc_objects")
        event_manager.publish("request_close_doc_origins")
        # Close all the objects in the plotter
        
    def BlocklyConverting(self, xmlString):
        
        print(xmlString)
        # dict_data = xmltodict.parse(xmlString)
        # json_data = json.dumps(dict_data, indent=4)
        # print(json_data)      
        self.MikoFile[6] = xmlString 

                
