import backend.core.variables as var

from backend.robot_management.robot_loader import RobotLoader
from backend.robot_management.tool_managment import ToolManagment
from backend.robot_management.robot_3d_model import Robot3dModel



robot_loader = RobotLoader()
tool_management = ToolManagment()

robot_3d_model = Robot3dModel()

#### robot

def get_selected_robot():
    return robot_loader.selected_robot

def get_selected_tool():
    return tool_management.selected_tool

def get_selected_robot_name():
    return robot_loader.robots[robot_loader.selected_robot][0]

def set_selected_robot(robot):
    print("set the selected robot")
    print(robot)
    robot_loader.selected_robot = robot
    print(get_selected_robot())

def setup_robot():
    robot_loader.SetupRobot()
    robot_loader.ChangeRobot()
    robot_3d_model.setup()
    tool_management.SetupTool()
    tool_management.changeTool(0)
    robot_loader.AddRobotToPlotter()
    robot_loader.CreateNewButtons()
    
        
def change_robot(robot = None):
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
    change_robot()
    

    

    
#########################################
## 3d model robot
#########################################

def add_new_3d_model():
    robot = get_selected_robot()
    robot_name = get_selected_robot_name()
    robot_3d_model.AddNewModel(robot, robot_name)

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
    robot = get_selected_robot()
    robot_name = get_selected_robot_name()
    tool_management.AddNewTool(robot, robot_name)

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