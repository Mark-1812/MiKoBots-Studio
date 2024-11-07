# backend/api.py
import asyncio
from backend.robot_management.robot_loader import RobotLoader
from backend.robot_management.tool_managment import ToolManagment
from backend.robot_management.robot_3d_model import Robot3dModel
from backend.robot_management.robot_communication import TalkWithRobotCOM
from backend.robot_management.robot_communication import TalkWithRobotBT

from backend.robot_management.io_communication import TalkWithIOCOM
from backend.robot_management.io_communication import TalkWithIOBT

from backend.simulation.simulation_management import SimulationManagement
from backend.simulation.simulation_origin_window import SimulationOriginWindow
from backend.simulation.simulation_object_window import SimulationObjectWindow

from backend.xbox.xbox import XBox


from backend.core.run_program import RunProgram

from backend.vision.vision_management import VisionManagement


from backend.games.solve_tac_tact_toe import solveTicTacToe


import backend.core.variables as var

talk_with_robot_com = TalkWithRobotCOM()
talk_with_robot_bt = TalkWithRobotBT()

robot_loader = RobotLoader()
tool_management = ToolManagment()
robot_3d_model = Robot3dModel()

talk_with_io_com = TalkWithIOCOM()
talk_with_io_bt = TalkWithIOBT()


simulation_management = SimulationManagement()
simulation_origin_window = SimulationOriginWindow()
simulation_object_window = SimulationObjectWindow()

xbox = XBox()

run_program = RunProgram()

vision_management = VisionManagement()


solve_tic_tac_toe = solveTicTacToe()


###########################
#   RunProgram
###########################

def run_script(sim):
    run_program.RunScript(sim)
    
def stop_script():
    run_program.StopScript()
    if var.ROBOT_CONNECT and var.ROBOT_BLUETOOTH:
        talk_with_robot_bt.StopProgram()
    if var.ROBOT_CONNECT and not var.ROBOT_BLUETOOTH:
        talk_with_robot_com.StopProgram()

def run_blockly_code(code):
    run_program.RunBlocklyCode(code)
    
def run_single_line(code):
    run_program.RunSingleLine(code)


###########################
#   Xbox
###########################    

def xbox_on():
    xbox.XBoxOn()


###########################
#   vision_management
###########################

def close_cam():
    vision_management.CloseCam()

def connect_cam(com_port = None):
    vision_management.ConnectCam(com_port)

def get_image_frame():
    return vision_management.GetImageFrame()

def get_mask(color, image):
    return vision_management.GetMask(color, image)

def draw_axis(img, p_, q_, color, scale):
    return vision_management.DrawAxis(img, p_, q_, color, scale)


###########################
#   io_communication
###########################
def send_line_to_io(command):
    print("send line or dead")
    if var.IO_BLUETOOTH:
        asyncio.run_coroutine_threadsafe(talk_with_io_bt.SendLineToIO(command), talk_with_io_bt.loop)
    else:
        talk_with_io_com.SendLineToIO(command)
        
def send_settings_io():
    if var.ROBOT_BLUETOOTH:
        talk_with_io_bt.SendSettingsIO()
    else:
        talk_with_io_com.SendSettingsIO()
 
def close_io():
    if var.IO_BLUETOOTH:
        asyncio.run_coroutine_threadsafe(talk_with_io_bt.CloseIO(), talk_with_io_bt.loop)
    else:
        talk_with_io_com.CloseIO()  
                
## bluetooth

def scan_for_io():
    asyncio.run_coroutine_threadsafe(talk_with_io_bt.ScanForDevicesBT(), talk_with_robot_bt.loop)

def connect_io_bt(device = None):
    asyncio.run_coroutine_threadsafe(talk_with_io_bt.ConnectIOBT(device), talk_with_robot_bt.loop)
    


## com
def connect_io_com(com_port = None):
    talk_with_io_com.ConnectIO(com_port)
    

###########################
#   robot_communication
###########################

def send_line_to_robot(command):
    
    if var.ROBOT_BLUETOOTH:
        asyncio.run_coroutine_threadsafe(talk_with_robot_bt.SendLineToRobot(command), talk_with_robot_bt.loop)
    else:
        talk_with_robot_com.SendLineToRobot(command)
        
def send_settings_robot():
    if var.ROBOT_BLUETOOTH:
        talk_with_robot_bt.SendSettingsRobot()
    else:
        talk_with_robot_com.SendSettingsRobot()
        
def close_robot():
    if var.ROBOT_BLUETOOTH:
        asyncio.run_coroutine_threadsafe(talk_with_robot_bt.CloseRobot(), talk_with_robot_bt.loop)
    else:
        talk_with_robot_com.CloseRobot()    

## bluetooth

def scan_for_robots():
    asyncio.run_coroutine_threadsafe(talk_with_robot_bt.ScanForDevicesBT(), talk_with_robot_bt.loop)

def connect_robot_bt(device = None):
    asyncio.run_coroutine_threadsafe(talk_with_robot_bt.ConnectRobotBT(device), talk_with_robot_bt.loop)


## com

def connect_robot_com(com_port = None):
    talk_with_robot_com.ConnectRobot(com_port)
    




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

def change_robot(item):
    """API function for the gui to request a robot change."""
    robot_loader.ChangeRobot(item)
    tool_management.SetupTool()
    
        
def save_robot(info):
    robot_loader.SaveRobot(info)
    
def send_pos_robot(SIM):
    pos = robot_loader.SendPosRobot(SIM)
    return pos

def delete_robot():
    robot_loader.DeleteRobot()
    tool_management.SetupTool()

def export_robot():
    robot_loader.ExportRobot()
    
def import_robot():
    robot_loader.ImportRobot()
    tool_management.SetupTool()
    
def create_new_robot():
    robot_loader.CreateNewRobot()
    tool_management.SetupTool()
    
def setup_robot():
    robot_loader.SetupRobot()
    tool_management.SetupTool()
    
##################
#   3d model robot
####################

def add_new_3d_model():
    robot_3d_model.AddNewModel()

def show_3d_model_settings(item):
    robot_3d_model.Show3dModelSettings(item)
    
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
    
    # check if the robot is conneted if than send tool settings
    

def get_tool_info():
    tool_info = tool_management.GetToolInfo()
    return tool_info

################
# tictactoe
    
def get_result_ttt():
    result = solve_tic_tac_toe.GetResult()
    return result
    
def print_board_ttt(board):
    solve_tic_tac_toe.print_board(board)

def minimax_ttt(board):
    result = solve_tic_tac_toe.minimax(board)
    return result

def terminial_ttt(board):
    result = solve_tic_tac_toe.terminal(board)
    return result