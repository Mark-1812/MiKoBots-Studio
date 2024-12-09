import json
from backend.core.event_manager import event_manager
import backend.core.variables as var


from backend.vision import get_square_size_per
from backend.file_managment import get_file_path

def SaveSettings():
    setting_file = [0] * 11

    # 0: get robot port -> not used any more
    # 1: get io port -> not used any more
    # 2: get cam port -> not used any more

    # 3: jog distance
    setting_file[3] = event_manager.publish("request_get_jog_distance")[0]

    # 4: selected robot
    setting_file[4] = var.ROBOT_NAME

    # 5: color settings
    setting_file[5] = event_manager.publish("request_get_colors")[0]

    # 6: vision settings
    setting_file[6] = event_manager.publish("request_get_vision_settings")[0]

    # 7: get the sqaure size percentage, for vision settings when not connected to the robot
    setting_file[7] = get_square_size_per()
        
    # 8: Speed setting
    setting_file[8] = event_manager.publish("request_get_speed")[0]

    # 9: Acceleration settings
    setting_file[9] = event_manager.publish("request_get_accel")[0]
    
    # 10: controller settings
    setting_file[10] = event_manager.publish("request_get_controller_settings")[0]


    try:
        file_path = get_file_path("/settings/settings.json")  
        with open(file_path, 'w') as file:
            json.dump(setting_file, file, indent=4)
    except:
        print("Error: could not save the settings")