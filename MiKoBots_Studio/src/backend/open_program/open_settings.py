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
        settings_file = ["0", "0", "0", "0", "0"]
        set_selected_robot(0)
    
    
    ## get the selected robot  
    try:
        set_selected_robot(settings_file[4])
    except:
        set_selected_robot(0)
        
        
    ## set vision settings
    try: 
        print(settings_file[5])
        event_manager.publish("request_set_vision_settings", settings_file[5])
        var.COLOR_RANGE = settings_file[5][5] 
    except:
        var.COLOR_RANGE = {
            "RED": [[0, 50, 100], [25, 255, 255]],  #0, 10, 100, 255, 100, 255
            "GREEN": [[35, 100, 100], [85, 255, 255]],
            "BLUE": [[100, 100, 100], [130, 255, 255]],
            "YELLOW": [[20, 100, 100], [30, 255, 255]],
            "ORANGE": [[10, 100, 100], [20, 255, 255]],
            "BLACK": [[0, 0, 0], [180, 255, 50]],
            "GRAY": [[0, 0, 50], [180, 50, 200]],     
            "WHITE": [[0, 0, 200], [180, 50, 255]],    
        }
        settings = [0, 0, 0, 160, True, var.COLOR_RANGE]
        
        event_manager.publish("request_set_vision_settings", settings)
    
    try:
        set_square_size_per(settings_file[6])
    except:
        set_square_size_per(0.8)
    
    var.SETTINGS_FILE = settings_file   