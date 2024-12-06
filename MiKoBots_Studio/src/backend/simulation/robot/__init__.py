from .robot_sim import RobotSimulation

robot_simulation = RobotSimulation()

def setup_renderer_robot(renderer, plotter, interactor):
    robot_simulation.SetupRenderer(renderer, plotter, interactor)

def add_robot_sim(data):
    robot_simulation.AddRobotToPlotter(data)

def delete_robot_sim():
    robot_simulation.DeleteRobotPlotter()

def add_tool_sim(data):
    robot_simulation.AddToolToPlotter(data)

def delete_tool_sim():
    robot_simulation.DeleteToolPlotter()

def change_pos_robot(matrix, name_joints, number_of_joints, extra_joint):
    robot_simulation.ChangePosRobot(matrix, name_joints, number_of_joints, extra_joint)

robot_simulation_preview = RobotSimulation()

def setup_renderer_robot_preview(renderer, plotter, interactor):
    robot_simulation_preview.SetupRenderer(renderer, plotter, interactor)

def add_robot_preview(data):
    robot_simulation_preview.AddRobotToPlotter(data)

def delete_robot_preview():
    robot_simulation_preview.DeleteRobotPlotter()

def add_tool_preview(data):
    robot_simulation_preview.AddToolToPlotter(data)

def delete_tool_preview():
    robot_simulation_preview.DeleteToolPlotter()

def change_pos_preview(matrix, name_joints, number_of_joints, extra_joint):
    robot_simulation_preview.ChangePosRobot(matrix, name_joints, number_of_joints, extra_joint)