import threading
import tkinter.messagebox
import sys

import ctypes  # Import ctypes module for thread manipulation
from PyQt5.QtCore import pyqtSignal,  QObject

import backend.core.variables as var

from backend.core.event_manager import event_manager

class RunProgram():
    def __init__(self):
        self.script_thread = None

        self.output_stream = OutputStream()
        self.output_stream.textWritten.connect(self.update_output)
        

    def RunScript(self, sim):     
        if sim and var.SIM and not var.PROGRAM_RUN:
            if event_manager.publish("request_get_program_tpe")[0]:
                # blockly code
                # get the blockly code
                event_manager.publish("request_get_blockly_code")
                pass
            else:
                script = event_manager.publish("request_program_field_get")[0]
                self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
                self.script_thread.start()          
        elif not sim and (var.ROBOT_CONNECT or var.IO_CONNECT) and not var.PROGRAM_RUN:
            script = event_manager.publish("request_program_field_get")[0]
            self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
            self.script_thread.start()            
        else:
            if not var.PROGRAM_RUN and not sim:
                tkinter.messagebox.showerror("Error", "Connect the robot")
            else:
                tkinter.messagebox.showerror("Error", "Program is already running")

    def RunBlocklyCode(self, code):
        print(code)
        try:
            program = "from robot_library import Move\nrobot = Move()\n"
            program += code
            print(program)
            exec(program)  # Warning: Use exec with caution as it can execute arbitrary code
            self.script_thread = threading.Thread(target=self.execute_script, args=(program,))
            self.script_thread.start() 
        except Exception as e:
            print(f"Error executing code: {e}")
    
    def execute_script(self, script):
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = self.output_stream
        
        try:
            var.PROGRAM_RUN = True
            event_manager.publish("request_enable_tool_combo", False)
            event_manager.publish("request_program_field_read_only", True)
            exec(script)
            var.SIM_SHOW_LINE = 0
            var.PROGRAM_RUN = False
            event_manager.publish("request_enable_tool_combo", True)
            event_manager.publish("request_program_field_read_only", False)
        except Exception as e:
            print("An error occurred:", e)
            var.SIM_SHOW_LINE = 0
            var.PROGRAM_RUN = False
            event_manager.publish("request_enable_tool_combo", True)
            event_manager.publish("request_program_field_read_only", False)
        finally:
            sys.stdout = original_stdout

    def update_output(self, text):
        event_manager.publish("request_insert_new_log", text)

    def StopScript(self):
        if var.ROBOT_CONNECT and not var.PROGRAM_RUN:
            event_manager.publish("request_stop_program")
                
        if var.PROGRAM_RUN:
            thread_id = int(self.script_thread.ident)
            
            if thread_id == -1:
                return
            
            if var.SIM:
                event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
                event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
            else:
                event_manager.publish("request_stop_program")
                
            
            var.PROGRAM_RUN = False
            var.SIM_SHOW_LINE = 0      
            
            event_manager.publish("request_enable_tool_combo", True)
            event_manager.publish("request_set_sim_not_busy")  
            
            print("Program ended.")   
            
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
                

            
              
class OutputStream(QObject):
    textWritten = pyqtSignal(str)
    
    def write(self, text):
        self.textWritten.emit(str(text))
        
