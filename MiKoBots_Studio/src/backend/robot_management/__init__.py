import backend.core.variables as var

from backend.robot_management.robot_loader import RobotLoader
from backend.robot_management.robot_setup import SetupRobot

from backend.robot_management.robot_settings import robot_settings

from .communication import send_tool_frame

robot_loader = RobotLoader()

#### robot







def setup_robot():
    robots = SetupRobot()
    robot_settings.robots = robots
    change_robot()

    
        
def change_robot(robot = None):
    robots = SetupRobot()

    if robot is not None:
        var.SELECTED_ROBOT = robot

    if type(var.SELECTED_ROBOT) == int:
        pass
    else:
        robot_found = False
        var.ROBOT_NAME = var.SELECTED_ROBOT
        for i in range(len(robots)):
            if var.ROBOT_NAME == robots[i][0]:
                var.SELECTED_ROBOT = i
                robot_found = True
        
        if not robot_found:
            var.SELECTED_ROBOT = 0
    var.ROBOT_NAME = robots[var.SELECTED_ROBOT][0]



    robot_loader.CloseCurrentRobot()
    robot_loader.ChangeRobot()
    try:
        
        change_tool(0)
        robot_loader.AddRobotToPlotter()
    except:
        pass
    robot_loader.CreateNewButtons() 
    robot_loader.ShowPosRobot()

    

def change_tool(tool):
    robot_loader.changeTool(tool)
    send_tool_frame()
    

### robot 
def get_pos_robot(SIM):
    if SIM:
        return [robot_loader.pos_axis_sim, robot_loader.pos_joint_sim]
    else:
        return [robot_loader.pos_axis, robot_loader.pos_joint]
    
def set_pos_robot(SIM, axis, joint):
    if SIM:
        robot_loader.pos_axis_sim = axis
        robot_loader.pos_joint_sim = joint
    else:
        robot_loader.pos_axis = axis
        robot_loader.pos_joint = joint        


    
def get_robots():
    robots = SetupRobot()
    

    return robots










    
