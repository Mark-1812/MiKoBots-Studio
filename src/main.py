import sys
import json

from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow

from backend.file_managment.file_management import FileManagement
from backend.core.event_manager import event_manager

import robot_library
import zipfile
import os


def main():
    app = QApplication(sys.argv)
    file_mangement = FileManagement()
    
    file_path = file_mangement.GetFilePath("")
    if not os.path.isdir(file_path):
        # get the file path of the zip file with the data
        current_directory = os.path.dirname(__file__)
        zip_file_path = os.path.join(current_directory, '..', 'assets', 'MiKoBots data', 'MiKoBots.zip')
        zip_file_path = os.path.normpath(zip_file_path)

        file_path = file_mangement.GetPathFolder()
        os.makedirs(file_path, exist_ok=True)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(file_path)

    window = MainWindow()
    window.show()
    

    try:
        file_path = file_mangement.GetFilePath("/settings/settings.json")
                 
        with open(file_path, 'r') as file:
            settings_file = json.load(file)
            
        event_manager.publish("request_set_robot_port", settings_file[0])
        event_manager.publish("request_set_io_port", settings_file[1])
        event_manager.publish("request_set_cam_port", settings_file[2])
        event_manager.publish("request_set_jog_distance", settings_file[3])
        
    except:
        event_manager.publish("request_set_robot_port", "0")
        event_manager.publish("request_set_io_port", "0")
        event_manager.publish("request_set_cam_port", "0")
        event_manager.publish("request_set_jog_distance", "0")
        

    
    event_manager.publish("setup_robot")
    
    sys.exit(app.exec_()) 
 

                    
if __name__ == "__main__":
    main()