import json
from backend.core.event_manager import event_manager
import backend.core.variables as var

def SaveSettings(file_management):
    setting_file = ["0", "0", "0", "0", "0", "0"]
    setting_file[3] = event_manager.publish("request_get_jog_distance")[0]
    setting_file[4] = var.SELECTED_ROBOT
    setting_file[5] = var.COLOR_RANGE
        
    file_path = file_management.GetFilePath("/settings/settings.json")  
                
    #print(setting_file)
                
    with open(file_path, 'w') as file:
        json.dump(setting_file, file, indent=4)