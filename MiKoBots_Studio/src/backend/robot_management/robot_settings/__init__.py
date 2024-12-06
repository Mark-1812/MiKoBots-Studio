from backend.simulation.robot import delete_robot_preview
from backend.core.event_manager import event_manager

from backend.robot_management.robot_settings.tool_managment import ToolManagment
from backend.robot_management.robot_settings.robot_3d_model import Robot3dModel
from backend.robot_management.robot_settings.robot_settings import RobotSettings

robot_settings = RobotSettings()
tool_management = ToolManagment()
robot_3d_model = Robot3dModel()


def set_robots(robots):
    robot_settings.robots = robots

def change_robot_settings(robot):
    robot_settings.selected_robot = robot
    settings_file = robot_settings.GetRobotSettings()

    # delete the current settings
    delete_robot_preview()
    event_manager.publish("request_delete_settings_fields") 

    # set the new settings
    event_manager.publish("request_set_robot_settings", settings_file[3], settings_file[0])
    tool_management.SetSettings(settings_file[2])
    robot_3d_model.SetSettings(settings_file[1])
    robot_3d_model.ShowRobotPreview(settings_file[3], settings_file[4])

def save_robot(): 
    delete_robot_preview()
    settings_3d_model = robot_3d_model.settings_3d_models
    settings_tool = tool_management.settings_tools
    settings_robot = event_manager.publish("request_get_robot_settings")[0]
    
    robot_settings.SaveRobot(settings_robot, settings_3d_model, settings_tool)

    settings_file = robot_settings.GetRobotSettings()
    robot_3d_model.ShowRobotPreview(settings_file[3], settings_file[4])
    
def create_new_robot():
    robot_settings.CreateNewRobot() 

def delete_robot():

    robot_settings.DeleteRobot()
    # what if the deleted robot is the selected robot in the simulation??
    
def export_robot():
    robot_settings.ExportRobot()
    
def import_robot():
    robot_settings.ImportRobot()

    
#########################################
## 3d model robot
#########################################

def add_new_3d_model():
    robot = robot_settings.selected_robot
    robot_name = robot_settings.selected_robot_name
    robot_3d_model.AddNewModel(robot, robot_name)
    save_robot()

def show_3d_model_settings(item):
    robot_3d_model.Show3dModelSettings(item)
    
def delete_robot_model(item):
    robot_3d_model.DeleteRobotItem(item)
    save_robot()
    
def change_origin_3d_model():
    robot_3d_model.ChangeOrigin3dModel()

def change_color_3d_model(item, color):
    robot_3d_model.ChangeColor(item, color)

def change_link_3d_model(item, link):
    robot_3d_model.ChangeLink(item, link)
    
    
    
    
#########################################
## Tool
#########################################

def add_new_tool():
    robot = robot_settings.selected_robot
    robot_name = robot_settings.selected_robot_name
    tool_management.AddNewTool(robot, robot_name)
    save_robot()

def show_tool_settings(tool):
    tool_management.ShowSettings(tool)
     
def update_tool_settings():
    tool_management.UpdateSettings()

def delete_tool(tool):
    tool_management.DeleteTool(tool)
    save_robot()

def change_color_tool(item, color):
    tool_management.ChangeColor(item, color)
