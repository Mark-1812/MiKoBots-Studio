import backend.core.variables as var
import json

def OpenSettings(file_mangement):
    ## open the file with settings
    file_path = file_mangement.GetFilePath("/settings/settings.json")   
    
    try:           
        with open(file_path, 'r') as file:
            settings_file = json.load(file)
    except:
        settings_file = ["0", "0", "0", "0", "0"]
        var.SELECTED_ROBOT = 0
    
    
    ## get the selected robot  
    try:
        var.SELECTED_ROBOT = settings_file[4] 
    except:
        var.SELECTED_ROBOT = 0
        
        
    ## get color settings
    try: 
        var.COLOR_RANGE = settings_file[5] 
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
    
    var.SETTINGS_FILE = settings_file   