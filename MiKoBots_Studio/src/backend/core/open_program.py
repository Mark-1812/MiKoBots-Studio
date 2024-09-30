import os
import json
from backend.file_managment.file_management import FileManagement
from backend.core.event_manager import event_manager
import backend.core.variables as var
import zipfile
import sys


def OpenSettings():
    file_mangement = FileManagement()
    
    file_path = file_mangement.GetFilePath("/settings/settings.json")   
        
    try:           
        with open(file_path, 'r') as file:
            settings_file = json.load(file)
        var.SELECTED_ROBOT = settings_file[4]
        
    except:
        settings_file = ["0", "0", "0", "0", "0"]
        var.SELECTED_ROBOT = 0
    
    return settings_file   

def FolderCheck():
    file_mangement = FileManagement()
    
    file_path = file_mangement.GetFilePath("")
    if not os.path.isdir(file_path):
        # get the file path of the zip file with the data
        try:
            # When running as a PyInstaller bundle, _MEIPASS is created
            #base_path = sys._MEIPASS
            base_path = os.path.dirname(sys.executable)
            zip_file_path = os.path.join(base_path, 'assets', 'MiKoBots_data', 'MiKoBots.zip')
            zip_file_path = os.path.normpath(zip_file_path)
            var.Test = zip_file_path
        except:
            current_directory = os.path.dirname(__file__)
            zip_file_path = os.path.join(current_directory, '..', 'assets', 'MiKoBots_data', 'MiKoBots.zip')
            zip_file_path = os.path.normpath(zip_file_path)


        print(f"zip_file_path {zip_file_path}")

        file_path = file_mangement.GetPathFolder()
        os.makedirs(file_path, exist_ok=True)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(file_path)
        
    # check if all the folders are present 
    
    
    
    
    
    
    ## settings folder
    folder_path = file_mangement.GetFilePath("/settings")
    if not (os.path.exists(folder_path) and os.path.isfile(folder_path)):
        os.makedirs(folder_path, exist_ok=True)
        
    file_path = file_mangement.GetFilePath("/settings/settings.json")
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        setting_file = ["0", "0", "0", "0", "0"]
        print("test iets vwerkefvdsc")
        with open(file_path, 'w') as file:
            json.dump(setting_file, file, indent=4)
                    
    # simulation folder
    folder_path = file_mangement.GetFilePath("/Simulation_library")
    if not (os.path.exists(folder_path) and os.path.isfile(folder_path)):
        os.makedirs(folder_path, exist_ok=True)
    
    file_path = file_mangement.GetFilePath("/Simulation_library/settings.json")
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        setting_file = []
        with open(file_path, 'w') as file:
            json.dump(setting_file, file, indent=4)
            
    # robot folder
    folder_path = file_mangement.GetFilePath("/Robot_library")
    if not (os.path.exists(folder_path) and os.path.isfile(folder_path)):
        os.makedirs(folder_path, exist_ok=True)
    