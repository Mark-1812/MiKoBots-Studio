POS_JOINT_SIM = [0,0,0,0,0,0]
POS_AXIS_SIM = [400,0,500,0,90,0]

NAME_JOINTS = ["J1","J2","J3","J4","J5","J6", "TOOL"]
UNIT_JOINT = ["deg","deg","deg","deg","deg","deg"]

NAME_AXIS = ["X","Y","Z","y","p","r"]
UNIT_AXIS = ["mm","mm","mm","deg","deg","deg"]

POS_GRIPPER = "0"

JOG_SPEED = "50"
JOG_ACCEL = "50"

FILE_PATH = None


######### robot config

# Settings
SETTINGS = []         
    # RV.TOOLS3D[i][0] = name
    # RV.TOOLS3D[i][1] = (f"/Robot_library/{folder_name}/TOOLS_STL/ORIGINAL_{name}")
    # RV.TOOLS3D[i][2] = (f"/Robot_library/{folder_name}/TOOLS_STL/{name}")
    # RV.TOOLS3D[i][3] = "red"
    # RV.TOOLS3D[i][4] = [0,0,0,0,0,0] # Position origin
    # RV.TOOLS3D[i][5] = [0,0,0,0,0,0] # Tool frame
    # RV.TOOLS3D[i][6] = "Tool pin 1" # Tool pin number
    # RV.TOOLS3D[i][7] = "None" # Type of tool pin (Servo or relay)
    # RV.TOOLS3D[i][8] = ["min","max"] # min and max value
    # RV.TOOLS3D[i][9] = [0,0,0] # Offset XYZ tool
    # RV.TOOLS3D[i][10] = 0 # Turn camera 180 degrees
    # RV.TOOLS3D[i][11] = [0,0,0,0,0] # RV.TOOL_SETTINGS_CAM[0], RV.TOOL_SETTINGS_CAM[1], RV.TOOL_SETTINGS_CAM[2], RV.TOOL_SETTINGS_CAM[3], RV.TOOL_SETTINGS_CAM[4]

ROBOT3D = []
TOOLS3D = []


NUMBER_OF_JOINTS = 6
EXTRA_JOINT = 0

DH_PARAM = []
JOINT_SPEED = []

# Position of the Simulation
POS_JOINT_SIM = [0.01,0.01,0.01,0.01,0.01,0.01]
POS_AXIS_SIM = [400,0,500,0,90,0]

# Position of the robot
POS_AXIS = [400,0,300,0,0,0]
POS_JOINT = [0,0,0,0,0,0]
TOOL_POS = 0

# variables related to the connection of the robot
ROBOT_JOINT_MOVE = None
ROBOT_NAME = ""

# variables related to the connection of the robot
TOOL_FRAME = [0,0,0,0,0,0]

TOOL_OFFSET_CAM = None
TOOL_SETTINGS_CAM = None


LANGUAGE = 'en'
LANGUAGE_DATA =None 