import os
import json
from backend.file_managment.file_management import FileManagement
import zipfile
import sys
import platform

def FolderCheck(file_mangement):
    file_path = file_mangement.GetFilePath("")

    if not os.path.isdir(file_path):
        # get the file path of the zip file with the data
        try:
            # When running as a PyInstaller bundle, _MEIPASS is created
            #base_path = sys._MEIPASS
            os_system = platform.system()

            if os_system == "Windows":
                base_path = os.path.dirname(sys.executable)
                zip_file_path = os.path.join(base_path, 'assets', 'MiKoBots_data', 'MiKoBots.zip')
                zip_file_path = os.path.normpath(zip_file_path)
            elif os_system == "Darwin":
                base_path = os.path.dirname(os.path.dirname(sys.executable))
                zip_file_path = os.path.join(base_path,'Resources', 'assets', 'MiKoBots_data', 'MiKoBots.zip')
                zip_file_path = os.path.normpath(zip_file_path)
        except:
            current_directory = os.path.dirname(__file__)
            zip_file_path = os.path.join(current_directory, '..', 'assets', 'MiKoBots_data', 'MiKoBots.zip')
            zip_file_path = os.path.normpath(zip_file_path)

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
    

    ## get language files