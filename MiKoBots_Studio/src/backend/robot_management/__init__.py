from .robot_loader import RobotLoader

robot_loader = RobotLoader()

def SetupRobot():
    robot_loader.SetupRobot()
    
def ChangeRobot(robot):
    robot_loader.ChangeRobot(robot)
    
