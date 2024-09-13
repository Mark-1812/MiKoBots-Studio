from PyQt5.QtWidgets import QPushButton, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import os
import ast

import tkinter.messagebox
import backend.core.variables as var


from backend.core.event_manager import event_manager
         
class SaveOpen:
    def __init__(self):
        self.MikoFile = [
                    "Program text",
                    "Gcode",
                    "3D models",
                    "origins",
                    "Selected robot",
                    "Selected tool",
                    
        ]
        self.file_dialog = QFileDialog()
        
        self.program_path = ""
        self.program_folder = ""
           
    def NewFile(self):
        if not var.PROGRAM_RUN:    
            answer = tkinter.messagebox.askquestion("Warning", message="Do you want to save the current file?")
            if answer == "yes":
                self.SaveFile() 
    
            self.CloseFile()
                  
    def SaveFile(self):
        self.MikoFile[0] = event_manager.publish("request_program_field_get")[0]
        self.MikoFile[1] = event_manager.publish("request_gcode_text_get")[0]
        self.MikoFile[2] = event_manager.publish("request_get_objects_plotter")[0]
        self.MikoFile[3] = event_manager.publish("request_get_origins_plotter")[0]
        self.MikoFile[4] = event_manager.publish("request_get_current_robot_nr")[0]
        self.MikoFile[5] = event_manager.publish("request_get_tool_nr")[0]
        
        if self.program_path:
            event_manager.publish("request_set_program_title", os.path.basename(self.program_path))       
            with open(self.program_path, "w") as file:
                file.write(str(self.MikoFile))
        else:
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
        
        answer = tkinter.messagebox.askquestion("Warning", message="Do you want to save the current file?")
        if answer == "yes":
            self.SaveFile() 
            
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.program_path, _ = QFileDialog.getOpenFileName(None, "Open .miko File", str(self.program_folder), "MiKo Files (*.miko);;All Files (*)", options=options)
        
        if self.program_path:
            self.CloseFile()
            
            self.program_folder = os.path.dirname(self.program_path)
                
            event_manager.publish("request_set_program_title", os.path.basename(self.program_path))
            with open(self.program_path, "r") as file:
                program = file.read()
                self.MikoFile = ast.literal_eval(program)      
                
                # Program text
                event_manager.publish("request_program_field_insert", self.MikoFile[0])
                
                # Gcode
                event_manager.publish("request_gcode_text_insert", self.MikoFile[1])
                
                # 3d models
                event_manager.publish("request_open_doc_objects", self.MikoFile[2])

                # Origin
                event_manager.publish("request_open_doc_origins", self.MikoFile[3])
                
                # Robot
                event_manager.publish("request_change_robot", self.MikoFile[4])

                # Tool
                #event_manager.publish("request_change_robot", self.MikoFile[5])
                #cur_file.CURRENT_TOOL = self.MikoFile[5]
                #self.robot_frame.RobotTools.changeTool(cur_file.CURRENT_TOOL)           
             
    def CloseFile(self):            
        event_manager.publish("request_program_field_clear")     
        event_manager.publish("request_gcode_text_clear")
        event_manager.publish("request_close_doc_objects")
        event_manager.publish("request_close_doc_origins")
        # Close all the objects in the plotter
        
                

                
