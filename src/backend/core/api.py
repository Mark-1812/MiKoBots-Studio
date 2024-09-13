# backend/api.py

from backend.robot_management.robot_loader import RobotLoader
from backend.robot_management.tool_managment import ToolManagment
from backend.robot_management.robot_3d_model import Robot3dModel
from backend.robot_management.robot_communication import TalkWithRobot
from backend.robot_management.robot_communication import TalkWithIO

from backend.simulation.simulation_management import SimulationManagement
from backend.simulation.simulation_origin_window import SimulationOriginWindow
from backend.simulation.simulation_object_window import SimulationObjectWindow

from robot_library import Move

from backend.core.run_program import RunProgram

from backend.vision.vision_management import VisionManagement

from backend.file_managment.save_open import SaveOpen
from backend.core.close_program import CloseProgram

robot_loader = RobotLoader()
tool_management = ToolManagment()
robot_3d_model = Robot3dModel()
talk_with_robot = TalkWithRobot()
talk_with_io = TalkWithIO()
move = Move()

simulation_management = SimulationManagement()
simulation_origin_window = SimulationOriginWindow()
simulation_object_window = SimulationObjectWindow()

run_program = RunProgram()

vision_management = VisionManagement()

save_open = SaveOpen()

###########################
#   close program
###########################

def close_program():
    CloseProgram()




###########################
#   RunProgram
###########################

def run_script(sim):
    run_program.RunScript(sim)
    
def stop_script():
    run_program.StopScript()

###########################
#   Move
###########################

def home():
    move.Home()

###########################
#   vision_management
###########################

def connect_cam():
    vision_management.ConnectCam()
    
def calibrate_vision(data):
    vision_management.CalibrateVision(data)

###########################
#   io_communication
###########################

def connect_io():
    talk_with_io.ConnectIO()
    
def send_settings_io():
    talk_with_io.SendSettingsIO()

###########################
#   robot_communication
###########################

def connect_robot():
    talk_with_robot.ConnectRobot()
    
def send_settings_robot():
    talk_with_robot.SendSettingsRobot()
    
def send_line_to_robot(line):
    talk_with_robot.SendLineToRobot(line)

###########################
#   Save Open file
##########################

def new_file():
    save_open.NewFile()
    
def save_file():
    save_open.SaveFile()
    
def save_as_file():
    save_open.SaveAsFile()
    
def open_file():
    save_open.OpenFile()
    


####################
#   Simulation management
####################

def enable_simulation(state):
    simulation_management.EnableSimulation(state)

def simulation_move_gui(pos, move):
    simulation_management.SimulationMoveGUI(pos, move)

####################
#   Simulation object
####################
def add_new_object_model():
    simulation_object_window.AddNewObjectModel()
    
def add_object_to_plotter(item):
    simulation_object_window.AddObjectToPlotter(item)
    
def delete_object_plotter(item):
    simulation_object_window.DeleteObjectPlotter(item)

def open_object_models():
    simulation_object_window.OpenObjectModels()
    
def show_pos_object(item):
    simulation_object_window.ShowPosObject(item)
    
def change_pos_object():
    simulation_object_window.ChangePosObject()
    
def show_origin_object(item):
    simulation_object_window.ShowOriginObject(item)
    
def change_origin_object():
    simulation_object_window.ChangeOriginObject()
    
def delete_stl_object_1(item):
    simulation_object_window.DeleteSTLObject1(item)
    
def change_color_object(color, color_code, item):
    simulation_object_window.ChangeColorObject(color, color_code, item)

    

####################
#   Simulation origin
####################
    
def add_origin():
    simulation_origin_window.AddOrigin()
    
def save_origin(item):
    simulation_origin_window.SaveOrigin(item)

def delete_origin(item):
    simulation_origin_window.DeleteOrigin(item)



####################
#   Robot loader
####################

def change_robot(btn, item):
    """API function for the frontend to request a robot change."""
    if btn.isChecked():
        print(item)
        robot_loader.ChangeRobot(item)
        
def save_robot(info):
    robot_loader.SaveRobot(info)
    
def send_pos_robot(SIM):
    pos = robot_loader.SendPosRobot(SIM)
    return pos

def delete_robot():
    robot_loader.DeleteRobot()

def export_robot():
    robot_loader.ExportRobot()
    
def import_robot():
    robot_loader.ImportRobot()
    
def create_new_robot():
    robot_loader.CreateNewRobot()
    
##################
#   3d model robot
####################

def add_new_3d_model():
    robot_3d_model.AddNewModel()

def show_3d_model_settings(item):
    robot_3d_model.Show3dModelSettings(item)
    
def move_robot_model(item, dir):
    robot_3d_model.MovePlotterItem(item, dir)
    
def delete_robot_model(item):
    robot_3d_model.DeleteRobotItem(item)
    
def change_origin_3d_model():
    robot_3d_model.ChangeOrigin3dModel()
    
############
# TOOL

def add_new_tool():
    tool_management.AddNewTool()

def show_tool_settings(tool):
    tool_management.ShowSettings(tool)
    
def update_tool_settings():
    tool_management.UpdateSettings()

def delete_tool(tool):
    tool_management.DeleteTool(tool)
    
def change_tool(tool):
    tool_management.changeTool(tool)

    
    