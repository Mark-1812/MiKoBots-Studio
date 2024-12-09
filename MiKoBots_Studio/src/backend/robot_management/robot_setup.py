import backend.core.variables as var
import os
from pathlib import Path

from backend.file_managment import get_file_path
from backend.core.event_manager import event_manager


def SetupRobot():
    folder_path = get_file_path("/Robot_library") 
    folders = []
    

    folder_path = Path(folder_path)
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        folders = []

        for folder in folder_path.iterdir():
            if folder.is_dir():  # Check if the item is a directory
                folders.append(folder.name)
        folders = sorted(folders)
    else:
        os.makedirs(folder_path, exist_ok=True)

    event_manager.publish("request_delete_robot_combo")
    robots = []

    for i in range(len(folders)):
        robots.append([f"robot", "settings", [], "tools", "IOSettings"])
        robots[i][0] = folders[i]
        
        event_manager.publish("request_add_robot_combo", robots[i][0])

    event_manager.publish("request_set_robot_combo", var.ROBOT_NAME)

    if len(folders) > 0:
        return robots
    else:
        print(var.LANGUAGE_DATA.get("message_no_robot_found"))    