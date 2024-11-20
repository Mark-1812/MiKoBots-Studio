import json
from backend.core.event_manager import event_manager
import backend.core.variables as var

from backend.robot_management import get_selected_robot

from backend.vision import get_square_size_per

def SaveSettings(file_management):
    setting_file = [0]*7
    setting_file[3] = event_manager.publish("request_get_jog_distance")[0]
    setting_file[4] = get_selected_robot()
    setting_file[5] = event_manager.publish("request_get_vision_settings")[0]
    setting_file[6] = get_square_size_per()
        
    file_path = file_management.GetFilePath("/settings/settings.json")  
                
    #print(setting_file)
                
    with open(file_path, 'w') as file:
        json.dump(setting_file, file, indent=4)