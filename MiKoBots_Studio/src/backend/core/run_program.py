import threading
import sys
from threading import Event



import ctypes  # Import ctypes module for thread manipulation
from PyQt5.QtCore import pyqtSignal,  QObject, QTimer
import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage

import gc

class RunProgram():
    def __init__(self):
        self.script_thread = None
        
        self.globals_delete = []

        self.output_stream = OutputStream()
        self.output_stream.textWritten.connect(self.update_output)

        

    def RunScript(self, sim):     
        if sim and var.SIM and not var.PROGRAM_RUN:
            if event_manager.publish("request_get_program_type")[0]:
                event_manager.publish("request_get_blockly_code")
            else:
                script = event_manager.publish("request_program_field_get")[0]
                self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
                self.script_thread.start()          
        elif not sim and (var.ROBOT_CONNECT or var.IO_CONNECT) and not var.PROGRAM_RUN:
            if event_manager.publish("request_get_program_type")[0]:
                event_manager.publish("request_get_blockly_code")
            else:
                script = event_manager.publish("request_program_field_get")[0]
                self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
                self.script_thread.start()            
        else:
            if not var.PROGRAM_RUN and not sim:
                event_manager.publish("request_insert_new_log", var.LANGUAGE_DATA.get("message_robot_not_connected"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_robot_not_connected"))
            else:
                event_manager.publish("request_insert_new_log", var.LANGUAGE_DATA.get("message_program_running"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_program_running"))

    def RunBlocklyCode(self, code):
        try:
            program = "from robot_library import Move, Tool, Vision, IO\nrobot = Move()\nvision = Vision()\ntool = Tool()\nIO = IO()\n"
            program += code
            print(f"Blockly program\n {program}")
            self.script_thread = threading.Thread(target=self.execute_script, args=(program,))
            self.script_thread.start() 
        except Exception as e:
            print(f"Error executing code: {e}")
            
    def RunSingleLine(self, line):
        if not var.PROGRAM_RUN:
            program = "from robot_library import Move, Tool, Vision, IO\nrobot = Move()\nvision = Vision()\ntool = Tool()\nIO = IO()\n"
            program += line
            
            self.script_thread = threading.Thread(target=self.execute_script, args=(program,))
            self.script_thread.start() 
            
    
    def execute_script(self, script):
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = self.output_stream
        
        try:
            var.PROGRAM_RUN = True
            event_manager.publish("request_enable_tool_combo", False)
            event_manager.publish("request_program_field_read_only", True)
            print("start program")
            exec(script, globals(), locals())

            # Identify and print global variables to be cleared related to Tool, Move, and Vision
            related_classes = {"Tool", "Move", "Vision", "IO"}  # Class names to remove

            # Check globals for both class instances and the classes themselves
            for name, value in globals().items():
                # If the variable name is in `related_classes` or the value is an instance of those classes
                if name in related_classes or any(cls in str(type(value)) for cls in related_classes):
                    print(f"{name}: {value}")
                    self.globals_delete.append(name)            
                                  
            print("end program")
            
            for name in self.globals_delete:
                del globals()[name]
            
            locals().clear()
            
            var.PROGRAM_RUN = False
            event_manager.publish("request_enable_tool_combo", True)
            event_manager.publish("request_program_field_read_only", False)
        except Exception as e:
            print("An error occurred:", e)
            var.PROGRAM_RUN = False
            event_manager.publish("request_enable_tool_combo", True)
            event_manager.publish("request_program_field_read_only", False)
        finally:
            sys.stdout = original_stdout
            gc.collect()
            
            for name in {"tool", "robot", "vision"}:
                if name in globals():
                    print(f"Remaining references to {name}: {len(gc.get_referrers(globals()[name]))}")
            

            

    def update_output(self, text):
        event_manager.publish("request_insert_new_log", text)

    def StopScript(self):                
        if var.PROGRAM_RUN:
            thread_id = int(self.script_thread.ident)
            
            if thread_id == -1:
                return
            
            if var.SIM:
                event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
                event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
                
            
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
        
