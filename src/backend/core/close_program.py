from backend.core.event_manager import event_manager

import backend.core.variables as var

from backend.file_managment.file_management import FileManagement


import json

file_management = FileManagement()

def CloseProgram():

    
    event_manager.publish("request_close_plotter")
    event_manager.publish("request_close_plotter_3d_model")
    event_manager.publish("request_close_plotter_tool")
    
    event_manager.publish("request_close_robot")
    event_manager.publish("request_close_io")
    event_manager.publish("request_close_cam")
    
             
    setting_file = ["0", "0", "0", "0"]
    setting_file[0] = event_manager.publish("request_get_robot_port")[0]
    setting_file[1] = event_manager.publish("request_get_io_port")[0]
    setting_file[2] = event_manager.publish("request_get_cam_port")[0]
    setting_file[3] = event_manager.publish("request_get_jog_distance")[0]
        
    file_path = file_management.GetFilePath("/settings/settings.json")  
                
    print(setting_file)
                
    with open(file_path, 'w') as file:
        json.dump(setting_file, file)
        print("saved")
