import threading
import sys
from threading import Event

import io

import ctypes  # Import ctypes module for thread manipulation
from PyQt5.QtCore import pyqtSignal,  QObject, QTimer
import backend.core.variables as var
from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage
from backend.simulation import simulation_not_busy, check_simulation_on

from backend.robot_management.communication import connect_robot_check, connect_io_check

import gc

class RunProgram():
    def __init__(self):
        self.script_thread = None
        self.program_running = False
        
        self.globals_delete = []

        self.output_stream = OutputStream()
        self.output_stream.textWritten.connect(self.update_output)
        #sys.stdout = self.output_stream

        

    def RunScript(self, sim):     
        if sim and check_simulation_on() and not self.program_running:
            if event_manager.publish("request_get_program_type")[0]:
                event_manager.publish("request_get_blockly_code")
            else:
                script = event_manager.publish("request_program_field_get")[0]
                self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
                self.script_thread.start()          
        elif not sim and (connect_robot_check() or connect_io_check()) and not self.program_running:
            if event_manager.publish("request_get_program_type")[0]:
                event_manager.publish("request_get_blockly_code")
            else:
                script = event_manager.publish("request_program_field_get")[0]
                self.script_thread = threading.Thread(target=self.execute_script, args=(script,))
                self.script_thread.start()            
        else:
            if not self.program_running and not sim:
                print(var.LANGUAGE_DATA.get("message_robot_not_connected"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_robot_not_connected"))
            else:
                print(var.LANGUAGE_DATA.get("message_program_running"))
                ErrorMessage(var.LANGUAGE_DATA.get("message_program_running"))

    def RunBlocklyCode(self, code):
        try:
            program = "from robot_library import Move, Tool, Vision, IO\nrobot = Move()\nvision = Vision()\ntool = Tool()\nIO = IO()\n"
            program += code
            self.script_thread = threading.Thread(target=self.execute_script, args=(program,))
            self.script_thread.start() 
        except Exception as e:
            print(f"Error executing code: {e}")
            
    def RunSingleLine(self, line):
        if not self.program_running:
            program = "from robot_library import Move, Tool, Vision, IO\nrobot = Move()\nvision = Vision()\ntool = Tool()\nIO = IO()\n"
            program += line
            
                
            self.script_thread = threading.Thread(target=self.execute_script, args=(program,))
            self.script_thread.start() 
            
    
    def execute_script(self, script):       
        
        
        try:
            self.program_running = True
            event_manager.publish("request_enable_tool_combo", False)
            exec(script, globals(), locals())

            # Identify and print global variables to be cleared related to Tool, Move, and Vision
            related_classes = {"Tool", "Move", "Vision", "IO"}  # Class names to remove

            # Check globals for both class instances and the classes themselves
            for name, value in globals().items():
                # If the variable name is in `related_classes` or the value is an instance of those classes
                if name in related_classes or any(cls in str(type(value)) for cls in related_classes):
                    self.globals_delete.append(name)            
            
            for name in self.globals_delete:
                del globals()[name]
            
            locals().clear()
            
            self.program_running = False
            event_manager.publish("request_enable_tool_combo", True)
        except Exception as e:
            print("An error occurred:", e)
            self.program_running = False
            event_manager.publish("request_enable_tool_combo", True)
        finally:
            pass

            

    def update_output(self, text):
        event_manager.publish("request_insert_new_log", text)

    def StopScript(self):                
        if self.program_running:
            thread_id = int(self.script_thread.ident)
            
            if thread_id == -1:
                return
            
            if check_simulation_on():
                event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
                event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
                
            
            self.program_running = False
            
            event_manager.publish("request_enable_tool_combo", True)
            simulation_not_busy()
            
            
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
                

            
              
class OutputStream(QObject):
    textWritten = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self._in_write = False  # Flag to prevent recursion
        
    def write(self, text):
        if self._in_write:
            return  # Prevent recursion if we're already inside a write
        
        # Prevent emitting the signal while inside the write method
        self._in_write = True
        self.textWritten.emit(str(text))  # Emit the text
        self._in_write = False  # Reset the flag after emitting the signal