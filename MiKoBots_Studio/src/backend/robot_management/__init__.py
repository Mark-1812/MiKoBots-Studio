import backend.core.variables as var
import asyncio

from backend.robot_management.robot_loader import RobotLoader
from backend.robot_management.tool_managment import ToolManagment
from backend.robot_management.robot_communication import TalkWithRobotCOM
from backend.robot_management.robot_communication import TalkWithRobotBT
from backend.robot_management.io_communication import TalkWithIOBT
from backend.robot_management.io_communication import TalkWithIOCOM
from backend.robot_management.robot_3d_model import Robot3dModel


talk_with_robot_com = TalkWithRobotCOM()
talk_with_robot_bt = TalkWithRobotBT()

talk_with_io_com = TalkWithIOCOM()
talk_with_io_bt = TalkWithIOBT()


robot_loader = RobotLoader()
tool_management = ToolManagment()

robot_3d_model = Robot3dModel()

#### robot

def setup_robot():
    robot = robot_loader.SetupRobot(var.SELECTED_ROBOT)
    robot_loader.ChangeRobot(robot)
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()
    
        
def change_robot(robot):
    robot_loader.CloseCurrentRobot()
    robot_loader.ChangeRobot(robot)
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()

def save_robot(info): 
    robot = robot_loader.SaveRobot(info)
    robot_loader.CloseCurrentRobot()
    robot_loader.ChangeRobot(robot)
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()
    
def create_new_robot():
    robot = robot_loader.CreateNewRobot() 
    robot_loader.CloseCurrentRobot()
    robot_loader.ChangeRobot(robot)
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()
    
def delete_robot():
    robot_loader.DeleteRobot()
    robot_loader.CloseCurrentRobot()
    robot_loader.ChangeRobot(0)
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()
    
def send_pos_robot(SIM):
    pos = robot_loader.SendPosRobot(SIM)
    return pos
    
    
def export_robot():
    robot_loader.ExportRobot()
    
def import_robot():
    robot_loader.ImportRobot()
    change_robot(var.SELECTED_ROBOT)
    
#########################################
## Communication robot
#########################################
    
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

def scan_for_robots():
    asyncio.run_coroutine_threadsafe(talk_with_robot_bt.ScanForDevicesBT(), talk_with_robot_bt.loop)

def connect_robot_bt(device = None):
    asyncio.run_coroutine_threadsafe(talk_with_robot_bt.ConnectRobotBT(device), talk_with_robot_bt.loop)


def connect_robot_com(com_port = None):
    talk_with_robot_com.ConnectRobot(com_port)
    
def stop_robot():
    if var.ROBOT_BLUETOOTH:
        talk_with_robot_bt.StopProgram()
    else:
        talk_with_robot_com.StopProgram()  
    
#########################################
## Communication IO
#########################################



def send_line_to_io(command):
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
    

    
#########################################
## 3d model robot
#########################################

def add_new_3d_model():
    robot_3d_model.AddNewModel()

def show_3d_model_settings(item):
    robot_3d_model.Show3dModelSettings(item)
    
def delete_robot_model(item):
    robot_3d_model.DeleteRobotItem(item)
    
def change_origin_3d_model():
    robot_3d_model.ChangeOrigin3dModel()
    
#########################################
## Tool
#########################################

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

def get_tool_info():
    tool_info = tool_management.GetToolInfo()
    return tool_info