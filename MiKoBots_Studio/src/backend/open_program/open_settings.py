import backend.core.variables as var
import json
from backend.robot_management import get_robots

from backend.core.event_manager import event_manager

from backend.vision import set_square_size_per

from backend.file_managment import get_file_path

def OpenSettings():
    ## open the file with settings
    file_path = get_file_path("/settings/settings.json")   
    
    try:           
        with open(file_path, 'r') as file:
            settings_file = json.load(file)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Error: could not open the settings file")
        settings_file = [None] * 11
        

    
    # 0: get robot port -> not used any more
    # 1: get io port -> not used any more
    # 2: get cam port -> not used any more

    # 3: jog distance
    try:
        event_manager.publish("request_set_jog_distance", settings_file[3])
    except:
        event_manager.publish("request_set_jog_distance", 50)
    
    # 4: selected robot
    try:
        if settings_file[4] is None:
            var.SELECTED_ROBOT = 0
        elif type(settings_file[4]) == int:
            var.SELECTED_ROBOT = settings_file[4]
        else:
            robots = get_robots()
            var.ROBOT_NAME = settings_file[4]
            for i in range(len(robots)):
                if var.ROBOT_NAME == robots[i][0]:
                    var.SELECTED_ROBOT = i

    except:
        var.SELECTED_ROBOT = 0

    # 5: color settings
    try:
        event_manager.publish("request_set_colors", settings_file[5])
    except:
        # when error send None so init values will show
        event_manager.publish("request_set_colors", None)
        
    # 6: Vision settings
    try: 
        event_manager.publish("request_set_vision_settings", settings_file[6])
    except:
        settings = [0, 0, 0, 160, True]
        event_manager.publish("request_set_vision_settings", settings)
    
    # 7: get the sqaure size percentage, for vision settings when not connected to the robot
    try:
        set_square_size_per(settings_file[7])
    except:
        set_square_size_per(0.8)

    # 8: Speed setting
    try:
        event_manager.publish("request_set_speed", settings_file[8])
    except:
        event_manager.publish("request_set_speed", 50)

    # 9: Acceleration settings
    try:
        event_manager.publish("request_set_accel", settings_file[9])
    except:
        event_manager.publish("request_set_accel", 50)
        
    # 10: Controller settings
    try: 
        event_manager.publish("request_set_controller_settings", settings_file[10])
    except:
        event_manager.publish("request_set_controller_settings", None)

