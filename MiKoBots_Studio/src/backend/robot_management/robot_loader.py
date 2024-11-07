from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog

import json
import backend.core.variables as var
import numpy as np
import os
import stat
import shutil
import zipfile
from pathlib import Path

from backend.calculations.kinematics_6_axis import ForwardKinematics_6
from backend.calculations.kinematics_3_axis import ForwardKinematics_3
from backend.calculations.convert_matrix import MatrixToXYZ

from backend.file_managment.file_management import FileManagement

from backend.core.event_manager import event_manager

from gui.windows.message_boxes import InfoMessage, ErrorMessage, WarningMessageRe


class RobotLoader(QObject):

    def __init__(self):
        super().__init__()
        
        self.ForwardKinematics_6 = ForwardKinematics_6()
        self.ForwardKinematics_3 = ForwardKinematics_3()
        self.file_management = FileManagement()
                 
        var.SELECTED_ROBOT = 0
        
         #a list with all the robots that exsist
        self.robotFile = []    
             
    def SetupRobot(self):
        # Platform for file path
        folder_path = self.file_management.GetFilePath("/Robot_library") 
        folders = []

        folder_path = Path(folder_path)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            folders = []

            for folder in folder_path.iterdir():
                if folder.is_dir():  # Check if the item is a directory
                    folders.append(folder.name)

            folders = sorted(folders)
            print(f"folders... {folders}")
        else:
            os.makedirs(folder_path, exist_ok=True)

        for i in range(len(folders)):
            var.ROBOTS.append([f"robot", "settings", [], "tools", "IOSettings"])
            var.ROBOTS[i][0] = folders[i]
            
            event_manager.publish("request_robot_buttons", i, var.ROBOTS[i][0])
            event_manager.publish("request_add_robot_combo", var.ROBOTS[i][0])

        if len(folders) > 0:
            try:
                event_manager.publish("request_set_robot_radio", var.SELECTED_ROBOT)
                event_manager.publish("request_set_robot_combo", var.SELECTED_ROBOT)
                self.ChangeRobot(var.SELECTED_ROBOT)
            except:
                event_manager.publish("request_set_robot_radio", 0)
                event_manager.publish("request_set_robot_combo", 0)
                self.ChangeRobot(0)
                var.SELECTED_ROBOT = 0
        else:
            print("NO robots found")
 
    def ChangeRobot(self, robot):  
        if type(robot) == int:
            pass
        else:
            for i in range(len(var.ROBOTS)):
                if robot == var.ROBOTS[i][0]:
                    robot = i
                    return
        
        
        event_manager.publish("request_delete_robot_plotter")
        event_manager.publish("request_delete_buttons_joint")
        event_manager.publish("request_delete_buttons_axis")
        event_manager.publish("request_delete_buttons_move")
        event_manager.publish("request_delete_settings_fields")
        
        event_manager.publish("request_set_robot_combo", robot)
        event_manager.publish("request_set_robot_radio", robot)
          
        var.SELECTED_ROBOT = robot
        
        var.POS_AXIS_SIM = [0,0,0,0,0,0]
        var.POS_JOINT_SIM = [0,0,0,0,0,0]
        
        print(var.ROBOTS)

        # Platform for file path
        file = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[var.SELECTED_ROBOT][0] + "/settings.json") 
        
        # if the robot already exsist open the file of the robot
        try:
            with open(file, 'r') as file:
                settings_file = json.load(file)

                var.SETTINGS = settings_file['Settings']
                var.ROBOT3D = settings_file['3Dfiles']
                var.TOOLS3D = settings_file['Tools']    
                var.ROBOT_NAME = settings_file['Name']   
                
                var.NUMBER_OF_JOINTS = int(var.SETTINGS['Set_number_of_joints'][0])
                var.EXTRA_JOINT = int(var.SETTINGS['Set_extra_joint'][0])
                
                print(f"Number of joints: {var.NUMBER_OF_JOINTS}")
                print(f"Extra joint: {var.EXTRA_JOINT}")
                event_manager.publish("request_create_settings_fields", var.NUMBER_OF_JOINTS)
                    
                # set all the settings
                event_manager.publish("request_set_robot_settings", var.SETTINGS)
                
                settings_DH = var.SETTINGS['Set_dh_par']
                var.DH_PARAM = settings_DH[0]
                
                settings_max_pos = var.SETTINGS['Set_max_pos']
                var.ROBOT_JOINT_MOVE = settings_max_pos[0] 
                
                var.JOINT_SPEED = var.SETTINGS['Set_speed'][0]
                
                if var.NUMBER_OF_JOINTS == 3:
                    matrix = self.ForwardKinematics_3.ForwardKinematics([0,0,0])
                    XYZ = MatrixToXYZ(matrix[var.NAME_JOINTS[3]])
                    var.POS_AXIS_SIM = XYZ
                elif var.NUMBER_OF_JOINTS == 6:
                    matrix = self.ForwardKinematics_6.ForwardKinematics([0,0,0,0,0,0])
                    XYZ = MatrixToXYZ(matrix[var.NAME_JOINTS[5]])
                    var.POS_AXIS_SIM = XYZ
                
                # create the buttons
                event_manager.publish("request_create_buttons_joint", var.NUMBER_OF_JOINTS)
                event_manager.publish("request_create_buttons_axis", var.NUMBER_OF_JOINTS)  
                event_manager.publish("request_create_buttons_move", var.NUMBER_OF_JOINTS, var.NAME_JOINTS, var.NAME_AXIS)        
                
                # delete the old robot and load the new robot buttons
                event_manager.publish("setup_3d_model")
                
                for i in range(len(var.ROBOT3D)):
                    file_path = self.file_management.GetFilePath(var.ROBOT3D[i][2])   
                    data = [file_path, var.ROBOT3D[i][3], np.eye(4), np.eye(4), var.ROBOT3D[i][5]]
                    event_manager.publish("request_add_robot_to_plotter", data)
                  
                if var.NUMBER_OF_JOINTS == 6:
                    matrix = self.ForwardKinematics_6.ForwardKinematics([0,0,0,0,0,0])
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
                elif var.NUMBER_OF_JOINTS == 3:
                    matrix = self.ForwardKinematics_3.ForwardKinematics([0,0,0])
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
                else:
                    print("no kinematics yet for this type of robot")
                
                                
                event_manager.publish("set_camera_pos_plotter", 3)


        except FileNotFoundError:
            print("No File Found")
        
      
    # send position robot
    def SendPosRobot(self, SIM):
        if SIM:
            pos = [var.POS_AXIS_SIM, var.POS_JOINT_SIM]
            return pos
        else:
            pos = [var.POS_AXIS, var.POS_JOINT]
            return pos
       
    # Button actions you can do                                       
    def CreateNewRobot(self):
        # first save the current robot
        if len(var.ROBOTS) > 0:
            # look how many robots already exsist, and create a new robot
            item = len(var.ROBOTS)
            
            # check if the name of the robot all exsist
            robot_name = f"robot {item}"
            for i in range(len(var.ROBOTS)):
                if var.ROBOTS[i][0] == robot_name:
                    robot_name += "_1"
                    i = 0
                    
        else:
            item = 0
            robot_name = f"robot 0"
        
        var.ROBOTS.append([robot_name, [], [], "tools", "IO settings"])
        
        # make a new folder structure for the robot
        new_folder_robot = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[item][0])
        new_folder_robot = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[item][0] + "/ROBOT_STL")
        new_folder_tools = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[item][0] + "/TOOLS_STL")
               
        os.makedirs(new_folder_robot, exist_ok=True)
        os.makedirs(new_folder_robot, exist_ok=True)
        os.makedirs(new_folder_tools, exist_ok=True)
        
        # give the new robot default values
        var.SETTINGS = {
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
            "Set_extra_joint": [0, ""]
            } 
        var.ROBOT3D = []
        var.TOOLS3D = []
        
        # create radio button, and text fiels for the new robot
        event_manager.publish("request_robot_buttons", item, robot_name)

        # Save the robot, create a file for it
        var.SELECTED_ROBOT = item
        self.SaveRobot()        
        
        # change the robot
        
        event_manager.publish("request_set_robot_radio", var.SELECTED_ROBOT)
        event_manager.publish("request_set_robot_combo", var.SELECTED_ROBOT)
        self.ChangeRobot(var.SELECTED_ROBOT)

    def SaveRobot(self, Info = None):
        # Change the name of the folder, if the name of the robot is changed
        robot_name = event_manager.publish("request_get_robot_name", var.SELECTED_ROBOT)
        
        old_name = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[var.SELECTED_ROBOT][0]) 
        new_name = self.file_management.GetFilePath("/Robot_library/" + robot_name[0])
            
        os.rename(old_name, new_name)

        for i in range(len(var.ROBOT3D)):
            var.ROBOT3D[i][1] = var.ROBOT3D[i][1].replace(var.ROBOTS[var.SELECTED_ROBOT][0], robot_name[0])
            var.ROBOT3D[i][2] = var.ROBOT3D[i][2].replace(var.ROBOTS[var.SELECTED_ROBOT][0], robot_name[0])
        
        for i in range(len(var.TOOLS3D)):
            var.TOOLS3D[i][1] = var.TOOLS3D[i][1].replace(var.ROBOTS[var.SELECTED_ROBOT][0], robot_name[0])
            var.TOOLS3D[i][2] = var.TOOLS3D[i][2].replace(var.ROBOTS[var.SELECTED_ROBOT][0], robot_name[0])
            
        
        # Get all the settings in the textboxes in the var.Settings
        settings_robot = event_manager.publish("request_get_robot_settings")
        
        # save everything of the robot in one file, and store the in a settings file
        var.ROBOTS[var.SELECTED_ROBOT][0] = robot_name[0]
        var.ROBOTS[var.SELECTED_ROBOT][1] = settings_robot[0]
        var.ROBOTS[var.SELECTED_ROBOT][2] = var.ROBOT3D
        var.ROBOTS[var.SELECTED_ROBOT][3] = var.TOOLS3D
        
        print(var.ROBOT3D)
        
        # Save all the information of this robot in a files
        settings_file = {}
        
        setting_names = ["Name", "Settings", "3Dfiles", "Tools", "IOSettings"]
        for i in range(len(setting_names)):
            settings_file[setting_names[i]] = var.ROBOTS[var.SELECTED_ROBOT][i]

        # Change the name of the folder, if the name of the robot is changed
        file = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[var.SELECTED_ROBOT][0] + "/settings.json")
        
        with open(file, 'w') as file:
            json.dump(settings_file, file, indent=4)    
        
        
        # Save all the names of the robots that exsist also in a file
        settings_file = {}
        for i in range(len(var.ROBOTS)):
            settings_file[i] = var.ROBOTS[i][0]
            
        self.ChangeRobot(var.SELECTED_ROBOT)
        
        if Info:
            InfoMessage(var.LANGUAGE_DATA.get("title_Settings_saved"), var.LANGUAGE_DATA.get("changes_been_saved"))
            
    def DeleteRobot(self):
        response = WarningMessageRe(var.LANGUAGE_DATA.get("message_sure_delete_robot"))
        
        if response:
            pass
        
        if len(var.ROBOTS) <= 1:
            ErrorMessage(var.LANGUAGE_DATA.get("message_delete_last_robot"))
            return

        
        ROBOT_DELETE = var.SELECTED_ROBOT
        
        # Make the first the selected robot
        var.SELECTED_ROBOT = 0
        event_manager.publish("request_set_robot_radio", var.SELECTED_ROBOT)
        event_manager.publish("request_set_robot_combo", var.SELECTED_ROBOT)
        self.ChangeRobot(var.SELECTED_ROBOT)
        self.SaveRobot()           
        

        # Delete the folder with the robots informations
        folder_name =  var.ROBOTS[ROBOT_DELETE][0]
        
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
            print(f"Folder '{folder}' and its contents have been deleted.")
        except OSError as e:
            try:
                os.chmod(folder, stat.S_IRWXU)
                shutil.rmtree(folder)
            except:
                ErrorMessage(var.LANGUAGE_DATA.get("message_not_delete_folder"), folder)

        var.ROBOTS[ROBOT_DELETE] = []    
        robots_old = var.ROBOTS
        var.ROBOTS = []
        
        # Delete the current robot out the list of robots and make a new list
        for i in range(len(robots_old)):
            if robots_old[i] != []:
                var.ROBOTS.append(robots_old[i])
                
        # delete all the current buttons
        event_manager.publish("request_delete_robot_buttons")
    
        # Create new buttons
        for i in range(len(var.ROBOTS)):
            robot_name = var.ROBOTS[i][0]
            event_manager.publish("request_robot_buttons", i, robot_name)
            
            

    def ImportRobot(self):
        # select the zip that you want to import
        file_path_zip, _ = QFileDialog.getOpenFileName(None, "Select a File", "", "All Files (*)")
        
        if not file_path_zip:
            return
        
        folder_robot = self.file_management.GetFilePath("/Robot_library")
        zip_file = os.path.basename(file_path_zip)
        robot_name = os.path.splitext(zip_file)[0]
        robot_name_old = robot_name
        duplicate = False

        for i in range(len(var.ROBOTS)):
            if robot_name == var.ROBOTS[i][0]:
                duplicate = True
                robot_name = robot_name + "_1"
                i = 0
                
        # Create a temporary folder to extract the original folder contents
        temp_folder = os.path.join(folder_robot, 'temp_extracted')
        os.makedirs(temp_folder, exist_ok=True)
        
        with zipfile.ZipFile(file_path_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)
            
        new_folder_path = os.path.join(folder_robot, robot_name)

        shutil.move(temp_folder, new_folder_path)
        
        # if there is a duplicate also change the name in the settings
        if duplicate:
            json_file = self.file_management.GetFilePath("/Robot_library/" + robot_name + "/settings.json")
            with open(json_file, 'r') as file:
                json_data = json.load(file)
                
            json_data['Name'] = robot_name

            # Convert JSON data to string for replacement
            json_str = json.dumps(json_data)

            # Replace all instances of "/MiKo/" with "/MiKo_1/"
            json_str = json_str.replace("/" + robot_name_old + "/", "/" + robot_name + "/")

            # Convert back to JSON
            modified_json_data = json.loads(json_str)

            # Print the modified JSON
            print(json.dumps(modified_json_data, indent=4))
            
                
            with open(json_file, 'w') as file:
                json.dump(modified_json_data, file, indent=4)
        
        item = len(var.ROBOTS)
                
        # # add the robot to the menu
        var.ROBOTS.append([robot_name, [], [], "tools", "IO settings"])   
            
        event_manager.publish("request_robot_buttons", item, robot_name)

        # # Save the robot, create a file for it
        var.SELECTED_ROBOT = item
                
        
        # # change the robot
        event_manager.publish("request_set_robot_radio", var.SELECTED_ROBOT)
        event_manager.publish("request_set_robot_combo", var.SELECTED_ROBOT)       
        self.ChangeRobot(var.SELECTED_ROBOT)
        self.SaveRobot()
        
    def ExportRobot(self):
        # make a zip file of the selected robot
        
        
        folder_robot = self.file_management.GetFilePath("/Robot_library/" + var.ROBOTS[var.SELECTED_ROBOT][0])
        # Set options to disable the native dialog
       
        folder_output = QFileDialog.getExistingDirectory(None, "Select Output Folder")
        
        if folder_output:
            os.makedirs(folder_output, exist_ok=True)
            output_zip_path = os.path.join(folder_output, var.ROBOTS[var.SELECTED_ROBOT][0])
            shutil.make_archive(output_zip_path, 'zip', folder_robot)
            
            
            

    
    

                    
    
                            


        

         

     
               
 


            