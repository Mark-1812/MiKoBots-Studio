from PyQt5.QtWidgets import QFileDialog

import json
import backend.core.variables as var
import numpy as np
import os
import stat
import shutil
import zipfile
from pathlib import Path

from backend.calculations.kinematics_6_axis import ForwardKinematics_6, InverseKinmatics_6
from backend.calculations.kinematics_3_axis import ForwardKinematics_3, InverseKinematics_3

from backend.file_managment.file_management import FileManagement

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import ErrorMessage, WarningMessageRe


class RobotSettings:
    def __init__(self):
        super().__init__()
        
        self.ForwardKinematics_6 = ForwardKinematics_6()
        self.ForwardKinematics_3 = ForwardKinematics_3()
        self.InverseKinematics_6 = InverseKinmatics_6()
        self.InverseKinematics_3 = InverseKinematics_3()

        self.file_management = FileManagement()
        
        #a list with all the robots that exsist
        self.robotFile = []    
        self.selected_robot = None
        self.selected_robot_name = None
        
        self.robots = []

        self.settings_current_robot = None
       
    # function reletad to settings of the robot
    def GetRobotSettings(self):
        # Platform for file path
        file = self.file_management.GetFilePath("/Robot_library/" + self.robots[self.selected_robot][0] + "/settings.json") 
        
        # if the robot already exsist open the file of the robot
        try:
            with open(file, 'r') as file:
                settings_file = json.load(file)
        except FileNotFoundError:
            print(var.LANGUAGE_DATA.get("message_not_open_robot"))

        general_setting = settings_file['Settings']
        robot_model_settings = settings_file['3Dfiles']
        robot_tool_settings = settings_file['Tools']    
        self.selected_robot_name = settings_file['Name']   
        
        number_of_joints = int(general_setting['Set_number_of_joints'][0])
        extra_joint = int(general_setting['Set_extra_joint'][0])
        dh_param = general_setting['Set_dh_par'][0]
        
        # set all the settings
        if not 'Set_robot_name' in general_setting:
            self.selected_robot_name = {'Set_robot_name': [self.selected_robot_name,""]}
            general_setting = {**self.selected_robot_name, **general_setting}

        return [general_setting, robot_model_settings, robot_tool_settings, number_of_joints, dh_param]
                     
    def CreateNewRobot(self):
        # first save the current robot
        if len(self.robots) > 0:
            # look how many robots already exsist, and create a new robot
            item = len(self.robots)
            
            # check if the name of the robot all exsist
            robot_name = f"robot {item}"
            for i in range(len(self.robots)):
                if self.robots[i][0] == robot_name:
                    robot_name += "_1"
                    i = 0
                    
        else:
            item = 0
            robot_name = f"robot 0"

        settings_robot = {
            "Set_motor_pin": [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],""],
            "Set_switch_pin": [["0", "0", "0", "0", "0", "0"],""],
            "Set_max_pos": [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],""],
            "Set_lim_pos": [["0", "0", "0", "0", "0", "0"],""],
            "Set_step_deg": [["0", "0", "0", "0", "0", "0"],""],
            "Set_dir_joints": [["0", "0", "0", "0", "0", "0"],""], 
            "Set_speed": [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],""], 
            "Set_home_settings": [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],""],
            "Set_dh_par": [[["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"]],""],
            "Set_number_of_joints": ["6", ""],
            "Set_extra_joint": [0, ""],
            'Set_robot_name': [robot_name, ""],
            'Set_tools': [["0", "0", "0", "0", "0", "0"],""], 
            'Set_io_pin': [["0", "0", "0", "0", "0", "0"],""]
            }     

        self.robots.append([robot_name, settings_robot, [], [], "IO settings"])
        
        # make a new folder structure for the robot
        new_folder_robot = self.file_management.GetFilePath("/Robot_library/" + self.robots[item][0])
        new_folder_robot = self.file_management.GetFilePath("/Robot_library/" + self.robots[item][0] + "/ROBOT_STL")
        new_folder_tools = self.file_management.GetFilePath("/Robot_library/" + self.robots[item][0] + "/TOOLS_STL")
               
        os.makedirs(new_folder_robot, exist_ok=True)
        os.makedirs(new_folder_robot, exist_ok=True)
        os.makedirs(new_folder_tools, exist_ok=True)
        
        # give the new robot default values

        
        # Save all the information of this robot in a files
        settings_file = {}
        
        setting_names = ["Name", "Settings", "3Dfiles", "Tools", "IOSettings"]
        for i in range(len(setting_names)):
            settings_file[setting_names[i]] = self.robots[item][i]

        # Change the name of the folder, if the name of the robot is changed
        file = self.file_management.GetFilePath("/Robot_library/" + self.robots[item][0] + "/settings.json")
        
        with open(file, 'w') as file:
            json.dump(settings_file, file, indent=4)  


        # create radio button, and text fiels for the new robot
        event_manager.publish("request_robot_buttons", item, robot_name)

        # change the robot
        event_manager.publish("request_set_robot_radio", self.selected_robot)
        event_manager.publish("request_add_robot_combo", robot_name)

    def SaveRobot(self,settings_robot, settings_3d_model = list, settings_tool = list):
        # Get all the settings in the textboxes in the var.Settings
        
        robot_name = settings_robot['Set_robot_name'][0]

        # Change the name of the folder, if the name of the robot is changed
        old_name = self.file_management.GetFilePath("/Robot_library/" + self.robots[self.selected_robot][0]) 
        new_name = self.file_management.GetFilePath("/Robot_library/" + robot_name)

        os.rename(old_name, new_name)

        # change the name in the robot oververiew
        event_manager.publish("request_change_robot_name", self.selected_robot, robot_name)


        for i in range(len(settings_3d_model)):
            settings_3d_model[i][1] = settings_3d_model[i][1].replace(self.robots[self.selected_robot][0], robot_name)
            settings_3d_model[i][2] = settings_3d_model[i][2].replace(self.robots[self.selected_robot][0], robot_name)
        
        for i in range(len(settings_tool)):
            settings_tool[i][1] = settings_tool[i][1].replace(self.robots[self.selected_robot][0], robot_name)
            settings_tool[i][2] = settings_tool[i][2].replace(self.robots[self.selected_robot][0], robot_name)
        
        # save everything of the robot in one file, and store the in a settings file
        self.robots[self.selected_robot][0] = robot_name
        self.robots[self.selected_robot][1] = settings_robot
        self.robots[self.selected_robot][2] = settings_3d_model
        self.robots[self.selected_robot][3] = settings_tool
        
        # Save all the information of this robot in a files
        settings_file = {}
        
        setting_names = ["Name", "Settings", "3Dfiles", "Tools", "IOSettings"]
        for i in range(len(setting_names)):
            settings_file[setting_names[i]] = self.robots[self.selected_robot][i]

        # Change the name of the folder, if the name of the robot is changed
        file = self.file_management.GetFilePath("/Robot_library/" + self.robots[self.selected_robot][0] + "/settings.json")
        
        with open(file, 'w') as file:
            json.dump(settings_file, file, indent=4)    
        
        
        # Save all the names of the robots that exsist also in a file
        settings_file = {}
        for i in range(len(self.robots)):
            settings_file[i] = self.robots[i][0]
            
        return self.selected_robot
            
    def DeleteRobot(self):
        response = WarningMessageRe(var.LANGUAGE_DATA.get("message_sure_delete_robot"))
        
        if response:
            pass
        
        if len(self.robots) <= 1:
            ErrorMessage(var.LANGUAGE_DATA.get("message_delete_last_robot"))
            return

        
        ROBOT_DELETE = self.selected_robot
        
        # Make the first the selected robot
        self.selected_robot = 0
        
        event_manager.publish("request_set_robot_radio", self.selected_robot)       
        

        # Delete the folder with the robots informations
        folder_name =  self.robots[ROBOT_DELETE][0]
        
        # Platform for file path
        folder = self.file_management.GetFilePath("/Robot_library/" + folder_name)
        
        # Remove the folder and its contents
        try:
            for root, dirs, files in os.walk(folder):
                for dir in dirs:
                    os.chmod(os.path.join(root, dir), stat.S_IRWXU)
                for file in files:
                    os.chmod(os.path.join(root, file), stat.S_IRWXU)                
            shutil.rmtree(folder)
        except OSError as e:
            try:
                os.chmod(folder, stat.S_IRWXU)
                shutil.rmtree(folder)
            except:
                ErrorMessage(var.LANGUAGE_DATA.get("message_not_delete_folder"), folder)

        del self.robots[ROBOT_DELETE]
                
        # delete all the current buttons
        event_manager.publish("request_delete_robot_buttons")
        event_manager.publish("request_delete_robot_combo")
    
        # Create new buttons
        for i in range(len(self.robots)):
            robot_name = self.robots[i][0]
            event_manager.publish("request_robot_buttons", i, robot_name)
            event_manager.publish("request_add_robot_combo", robot_name)
            
    def ImportRobot(self):
        # select the zip that you want to import
        file_path_zip, _ = QFileDialog.getOpenFileName(None, "Select a File", "", "All Files (*)")
        
        if not file_path_zip:
            return
        
        folder_robots = self.file_management.GetFilePath("/Robot_library")
        zip_file = os.path.basename(file_path_zip)
        robot_name = os.path.splitext(zip_file)[0]
        robot_name_old = robot_name
        duplicate = False

        for i in range(len(self.robots)):
            if robot_name == self.robots[i][0]:
                duplicate = True
                robot_name = robot_name + "_1"
                i = 0
             
                
        robot_folder = os.path.join(folder_robots, robot_name)
        os.makedirs(folder_robots, exist_ok=True)

        # Create a temporary folder to extract the original folder contents
        with zipfile.ZipFile(file_path_zip, 'r') as zip_ref:
            temp_folder = os.path.join(folder_robots, 'temp_extracted')
            os.makedirs(temp_folder, exist_ok=True)
            zip_ref.extractall(temp_folder)

            for item in os.listdir(temp_folder):
                item_path = os.path.join(temp_folder, item)
                if os.path.isdir(item_path):
                    shutil.move(item_path, os.path.join(robot_folder, os.path.basename(item)))
                elif os.path.isfile(item_path):
                    shutil.move(item_path, robot_folder)

            # Remove the temporary directory
            shutil.rmtree(temp_folder)

            macosx_folder = os.path.join(robot_folder, "__MACOSX")
            if os.path.exists(macosx_folder):
                shutil.rmtree(macosx_folder)  

        # if there is a duplicate also change the name in the settings
        if duplicate:
            json_file = self.file_management.GetFilePath("/Robot_library/" + robot_name + "/settings.json")

            with open(json_file, 'r') as file:
                json_data = json.load(file)
                
            json_data['Name'] = robot_name
            json_data["Settings"]["Set_robot_name"][0] = robot_name

            # Convert JSON data to string for replacement
            json_str = json.dumps(json_data)

            # Replace all instances of "/MiKo/" with "/MiKo_1/"
            json_str = json_str.replace("/" + robot_name_old + "/", "/" + robot_name + "/")

            # Convert back to JSON
            modified_json_data = json.loads(json_str)

            with open(json_file, 'w') as file:
                json.dump(modified_json_data, file, indent=4)
        
        item = len(self.robots)
                
        # # add the robot to the menu
        self.robots.append([robot_name, [], [], "tools", "IO settings"])   
            
        event_manager.publish("request_robot_buttons", item, robot_name)
        event_manager.publish("request_delete_robot_combo")
    
        # Create new buttons
        for i in range(len(self.robots)):
            robot_name = self.robots[i][0]
            event_manager.publish("request_add_robot_combo", robot_name)




        
    def ExportRobot(self):
        # make a zip file of the selected robot
        
        
        folder_robot = self.file_management.GetFilePath("/Robot_library/" + self.robots[self.selected_robot][0])
        # Set options to disable the native dialog
       
        folder_output = QFileDialog.getExistingDirectory(None, "Select Output Folder")
        
        if folder_output:
            os.makedirs(folder_output, exist_ok=True)
            output_zip_path = os.path.join(folder_output, self.robots[self.selected_robot][0])
            shutil.make_archive(output_zip_path, 'zip', folder_robot)
            
            
            

    
    

                    
    
                            


        

         

     
               
 


            