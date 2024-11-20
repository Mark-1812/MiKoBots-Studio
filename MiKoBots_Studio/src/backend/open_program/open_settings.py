import backend.core.variables as var
import json

from backend.robot_management import set_selected_robot

from backend.core.event_manager import event_manager

from backend.vision import set_square_size_per

def OpenSettings(file_mangement):
    ## open the file with settings
    file_path = file_mangement.GetFilePath("/settings/settings.json")   
    
    try:           
        with open(file_path, 'r') as file:
            settings_file = json.load(file)
    except:
        settings_file = [0] * 10
        print("Error: could not open the settings file")
    
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
        set_selected_robot(settings_file[4])
    except:
        set_selected_robot(0)

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
        event_manager.publish("request_set_accel", settings_file[8])
    except:
        event_manager.publish("request_set_accel", 50)

