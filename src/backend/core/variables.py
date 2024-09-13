PROGRAM_RUN = False

SIM = 0
SIM_SHOW_LINE = 0
POS_JOINT_SIM = [0,0,0,0,0,0]
POS_AXIS_SIM = [400,0,500,0,90,0]

LOG_DATA = []

XBOX_USE = 0
XBOX_STATE = 0

NAME_JOINTS = ["J1","J2","J3","J4","J5","J6", "TOOL"]
UNIT_JOINT = ["deg","deg","deg","deg","deg","deg"]

NAME_AXIS = ["X","Y","Z","y","p","r"]
UNIT_AXIS = ["mm","mm","mm","deg","deg","deg"]

POS_GRIPPER = "0"

SPEED = "50"
ACCEL = "50"

JOG_DISTANCE = "10"
JOG_SPEED = "50"
JOG_ACCEL = "50"


CAM_CONNECT = 0
CAM_PORT = 0

FILE_PATH = None


######### robot config

NAME = None

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

DH_PARAM = []

# Position of the Simulation
POS_JOINT_SIM = [0.01,0.01,0.01,0.01,0.01,0.01]
POS_AXIS_SIM = [400,0,500,0,90,0]

# Position of the robot
POS_AXIS = [400,0,300,0,0,0]
POS_JOINT = [0,0,0,0,0,0]
TOOL_POS = 0
SELECTED_ROBOT = None
SELECTED_TOOL = None

# variables related to the connection of the robot
ROBOT_CONNECT = False
ROBOT_BUSY = False
ROBOT_HOME = False
ROBOT_SER = None
ROBOT_PAUZE = False
ROBOT_COM = "3"
ROBOT_JOINT_MOVE = None

# variables related to the connection of the robot
TOOL_FRAME = [0,0,0,0,0,0]
TOOL_PIN_NUMBER = None
TOOL_TYPE = None # relay or servo
TOOL_RELAY_POS = None

TOOL_OFFSET_CAM = None
TOOL_TURN_CAM = None
TOOL_SETTINGS_CAM = None

# variables related to vision
VISION_CAP = ""
VISION_COLOR_OPTIONS = {"RED": [[0, 50, 105], [25, 255, 255], [165, 50, 10], [179, 255, 255]], "GREEN": [[30, 80, 30], [85, 255, 255]], "BLUE": [[95, 95, 100], [135, 255, 255]], "YELLOW": [[20, 100, 100], [35, 255, 255]], "ORAGNE": [[10, 100, 100], [20, 255, 255]], "PURPLE": [[130, 100, 100], [160, 255, 255]], "PINK": [[140, 100, 100], [180, 255, 255]], "CYAN": [[85, 100, 100], [100, 255, 255]], "WHITE": [[0, 0, 200], [179, 50, 255]], "BLACK": [[0, 0, 0], [179, 255, 30]]}


# variables related to the connection of the robot
IO_CONNECT = False
IO_BUSY = False
IO_SER = None
IO_COM = "5"

ORIGIN = []

ROBOT_PLOTTER = []
TOOL_PLOTTER = [None, None, None, None]

SAVED = False