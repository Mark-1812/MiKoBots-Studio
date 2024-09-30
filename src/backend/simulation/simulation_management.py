import backend.core.variables as var
from backend.calculations.inverse_kinematics import InverseKinmatics
from backend.calculations.forward_kinematics import ForwardKinematics
from PyQt5.QtCore import QObject

import numpy as np
import re
import time
import math

from backend.calculations.convert_matrix import MatrixToXYZ
from backend.calculations.convert_matrix import XYZToMatrix

from backend.core.event_manager import event_manager

class SimulationManagement(QObject):
    def __init__(self):
        self.forward_kin = ForwardKinematics()
        self.inverse_kin = InverseKinmatics()
        
        self.viewer_busy = 0
        
        self.points = []
        
        self.step_size_deg = 2
        self.step_size_mm = 2
        
        self.Motion_ok = True
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("simulate_program", self.SimulateProgram)   
        
        
    def EnableSimulation(self, state):
        if state ==  2:
            var.SIM = 1
            event_manager.publish("request_change_labels_control", True)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_JOINT)
            event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
            
        else:
            var.SIM = 0
            event_manager.publish("request_change_labels_control", False)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS, var.NAME_AXIS, var.UNIT_JOINT)
            event_manager.publish("request_label_pos_joint", var.POS_JOINT, var.NAME_JOINTS, var.UNIT_JOINT)
    
    def SimulateProgram(self, line, program):
        self.program = program
        self.step = 0
        self.last_position = []

        self.viewer_busy = 1         
        words = self.program.split()
        
        if words[0] == "MoveL": self.MoveL(self.program, line)
        elif words[0] == "MoveJ": self.MoveJ(self.program, line)
        elif words[0] == "OffsetJ": self.OffsetJ(self.program, line)
        elif words[0] == "OffsetL" or words[0] == "jogL": self.OffsetL(self.program, line)
        #elif words[0] == "Gripper": self.Gripper(self.program)
        elif words[0] == "jogJ": self.jogJ(self.program, line)
        #elif words[0] == "MoveJoint": self.MoveJont(self.program, line)

        if line and self.points != []:
            #self.Createline()
            last_points = self.points[-1]
            self.points = []
            self.points.append(last_points)
        
        self.step += 1
        self.viewer_busy = 0
                                 
    def SimulationMoveGUI(self, POS, Move):
        import threading
        print("SimulationMoveGUI")
        
        
        def execute_program():
            self.viewer_busy = 1
            line = f"{Move} X{POS[0]} Y{POS[1]} Z{POS[2]} y{POS[3]} p{POS[4]} r{POS[5]}"

            words = line.split()
            if words[0] == "MoveL": self.MoveL(line, False)
            elif words[0] == "MoveJ": self.MoveJ(line, False)
            elif words[0] == "OffsetJ": self.OffsetJ(line, False)
            elif words[0] == "OffsetL" or words[0] == "jogL": self.OffsetL(line, False)
            
            
            elif words[0] == "jogJ": 
                line = f"{Move} J1{POS[0]} J2{POS[1]} J3{POS[2]} J4{POS[3]} J5{POS[4]} J6{POS[5]}"
                self.jogJ(line, False)
            elif words[0] == "MoveJoint":
                line = f"{Move} J1{POS[0]} J2{POS[1]} J3{POS[2]} J4{POS[3]} J5{POS[4]} J6{POS[5]}"
                self.MoveJoint(line, False)
                
            self.viewer_busy = 0
                                                    

        if self.viewer_busy == 0:
            self.Motion_ok = True
            thread = threading.Thread(target = execute_program)
            thread.start()    
    
    '''
    
    def Createline(self):
        coordinates = np.array(self.points)  
        line = pv.PolyData()
        line.points = coordinates
        
        lines = np.full((len(coordinates)-1, 3), 2, dtype=np.int_)
        lines[:, 1] = np.arange(0, len(coordinates)-1)
        lines[:, 2] = np.arange(1, len(coordinates))

        line.lines = lines
        SV.LINE.append(plotter.add_mesh(line, color="black", line_width=2)) 
        
    def DeleteLine(self):
        import threading
        def deleteLine():
            for i in range(len(SV.LINE)):
                plotter.remove_actor(SV.LINE[i])
                
        thread = threading.Thread(target = deleteLine)
        thread.start() 
    
    '''
    
    def jogJ(self, line, points):
        pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        POSJ123 = []
        matches = re.search(pattern, line)
        for i in range(6):
            POSJ123.append(float(matches.group(1 + i)))
        
        for i in range(var.NUMBER_OF_JOINTS):
            POSJ123[i] += var.POS_JOINT_SIM[i]
            
 
        self.Motion_ok = self.checkJointPos(POSJ123)


        Joint_angles_start = var.POS_JOINT_SIM
        
        Joint_angles_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            Joint_angles_delta.append(Joint_angles_start[i] - POSJ123[i])                

        max_angle = max(map(abs, Joint_angles_delta))
        number_of_steps = math.ceil(max_angle / self.step_size_deg)

        Joints_increments = []
        for i in range(var.NUMBER_OF_JOINTS): 
            try:
                Joints_increments.append(Joint_angles_delta[i] / number_of_steps)  
            except:
                Joints_increments.append(0)

        if self.Motion_ok:
            for i in range(int(number_of_steps)):
                for j in range(var.NUMBER_OF_JOINTS):
                    Joint_angles_start[j] -= Joints_increments[j]
                if points:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    X = matrix[var.NAME_JOINTS[5]][0][3]
                    Y = matrix[var.NAME_JOINTS[5]][1][3]
                    Z = matrix[var.NAME_JOINTS[5]][2][3]
                    self.points.append([X,Y,Z])
                else:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)
                    time.sleep(0.01)
                var.POS_JOINT_SIM = Joint_angles_start
                matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[6]])
                self.updateLabels()

    def MoveJoint(self, line, points):
        pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        POSJ123 = []
        matches = re.search(pattern, line)
        for i in range(6):
            POSJ123.append(float(matches.group(1 + i)))

        Joint_angles_start = var.POS_JOINT_SIM
        
        Joint_angles_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            Joint_angles_delta.append(Joint_angles_start[i] - POSJ123[i])                

        max_angle = max(map(abs, Joint_angles_delta))       
        number_of_steps = math.ceil(max_angle / self.step_size_deg)
        
        self.Motion_ok = self.checkJointPos(Joint_angles_delta)
        
        if number_of_steps > 0 and self.Motion_ok:
            Joints_increments = []
            for i in range(var.NUMBER_OF_JOINTS): 
                Joints_increments.append(Joint_angles_delta[i] / number_of_steps)  

            for i in range(int(number_of_steps)):
                for j in range(var.NUMBER_OF_JOINTS):
                    Joint_angles_start[j] -= Joints_increments[j]
                    
                if points:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    X = matrix[var.NAME_JOINTS[5]][0][3]
                    Y = matrix[var.NAME_JOINTS[5]][1][3]
                    Z = matrix[var.NAME_JOINTS[5]][2][3]
                    self.points.append([X,Y,Z])
                else:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)
                    time.sleep(self.CalculateSpeed())
        
            var.POS_JOINT_SIM = Joint_angles_start
            matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
            var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[6]])
            self.updateLabels()

    def MoveJ(self, line, points): 
        # read the line
        pattern = r"[XYZypr]-?\d+(?:\.\d+)?"
        matches = re.findall(pattern, line)       
        POSXYZ = [float(match[1:]) for match in matches]
        
        max_pos_mm = 0
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(var.POS_AXIS_SIM[i] - POSXYZ[i]):
                max_pos_mm = abs(var.POS_AXIS_SIM[i] - POSXYZ[i])
                
        # Check if the robot can reach the position
        try:
            Joint_angles_start = var.POS_JOINT_SIM
            Joint_angles_end = self.inverse_kin.InverseKinematics(POSXYZ, var.POS_JOINT_SIM)  
            self.Motion_ok = self.checkJointPos(Joint_angles_end)
            
            for i in range(var.NUMBER_OF_JOINTS):
                if np.isnan(Joint_angles_end[i]):
                    self.Motion_ok = False

            number_of_steps = math.ceil(max_pos_mm / self.step_size_mm)        
        except:     
            self.Motion_ok = False
 
                                
        # If the robot can reach the position        
        if self.Motion_ok and max_pos_mm > 0.00:
            Joint_angles_delta = []
            for i in range(var.NUMBER_OF_JOINTS): 
                Joint_angles_delta.append(Joint_angles_start[i]-Joint_angles_end[i])                

            # calculate the joint increments per step
            Joints_increments = []
            for i in range(var.NUMBER_OF_JOINTS): 
                Joints_increments.append(Joint_angles_delta[i] / number_of_steps)  
            
            # change the posotion of the robot arm per step   
            for i in range(int(number_of_steps)):
                for j in range(var.NUMBER_OF_JOINTS):
                    Joint_angles_start[j] -= Joints_increments[j]    
                                
                if points:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    X = matrix[var.NAME_JOINTS[6]][0][3]
                    Y = matrix[var.NAME_JOINTS[6]][1][3]
                    Z = matrix[var.NAME_JOINTS[6]][2][3]
                    self.points.append([X,Y,Z])
                else:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)
                    time.sleep(self.CalculateSpeed()) 
                var.POS_JOINT_SIM = Joint_angles_start
                var.POS_AXIS_SIM = POSXYZ
                self.updateLabels()
                       
    def MoveL(self, line, points):
        pattern = r"[XYZypr]-?\d+(?:\.\d+)?"
        matches = re.findall(pattern, line)       
        pos_xyz_end = [float(match[1:]) for match in matches]
            
        max_pos_mm = 0
        pos_xyz_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            if max_pos_mm < (pos_xyz_end[i] - var.POS_AXIS_SIM[i]):
                max_pos_mm = (pos_xyz_end[i] - var.POS_AXIS_SIM[i])
            pos_xyz_delta.append(pos_xyz_end[i] - var.POS_AXIS_SIM[i])  

        # calculate the distance per mm
        number_of_steps = math.ceil(max_pos_mm / self.step_size_mm)
        
        pos_xyz_increments = []
        for i in range(var.NUMBER_OF_JOINTS): 
            pos_xyz_increments.append(pos_xyz_delta[i] / number_of_steps)  
            
        # Check if you can reach the end position
        try:
            Joint_angles = self.inverse_kin.InverseKinematics(pos_xyz_end, var.POS_JOINT_SIM)
            self.Motion_ok = self.checkJointPos(Joint_angles)
        except:
            print("Cannot reach this position")
            self.Motion_ok = False            
            
        # if the robot can reach the end position
        if self.Motion_ok:
            for i in range(int(number_of_steps)):
                if self.Motion_ok:
                    for j in range(var.NUMBER_OF_JOINTS):
                        var.POS_AXIS_SIM[j] += pos_xyz_increments[j]

                if points:
                    try:
                        Joint_angles = self.inverse_kin.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                        self.Motion_ok = self.checkJointPos(Joint_angles)
                        matrix = self.forward_kin.ForwardKinematics(Joint_angles)
                    except:  
                        print("Cannot reach this position")
                        self.Motion_ok = False
                        
                    if self.Motion_ok:
                        X = matrix[var.NAME_JOINTS[6]][0][3]
                        Y = matrix[var.NAME_JOINTS[6]][1][3]
                        Z = matrix[var.NAME_JOINTS[6]][2][3]
                        self.points.append([X,Y,Z])                    
                else:
                    try:
                        Joint_angles = self.inverse_kin.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                        matrix = self.forward_kin.ForwardKinematics(Joint_angles)
                    except:     
                        print("Cannot reach this position")
                        self.Motion_ok = False   
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)       
                    time.sleep(self.CalculateSpeed())
                    
                if self.Motion_ok:      
                    var.POS_JOINT_SIM = Joint_angles
                    self.updateLabels()
             
    def OffsetJ(self, line, points):
        pattern = r"[XYZypr]-?\d+(?:\.\d+)?"
        matches = re.findall(pattern, line)      
        POSXYZ = [float(match[1:]) for match in matches]
        max_pos_mm = 0
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(POSXYZ[i]):
                max_pos_mm = abs(POSXYZ[i])
            POSXYZ[i] += var.POS_AXIS_SIM[i]  
        

        try: 
            Joint_angles_start = var.POS_JOINT_SIM
            Joint_angles_end = self.inverse_kin.InverseKinematics(POSXYZ, var.POS_JOINT_SIM)   
            self.Motion_ok = self.checkJointPos(Joint_angles_end)        
        except:  
            print("Cannot reach this position")
            self.Motion_ok = False
            
        if self.Motion_ok:
            # Calculate the distance per step
            Joint_angles_delta = []
            for i in range(var.NUMBER_OF_JOINTS): 
                Joint_angles_delta.append(Joint_angles_start[i]-Joint_angles_end[i])                

            number_of_steps = math.ceil(abs(max_pos_mm) / self.step_size_mm)
            
            Joints_increments = []
            for i in range(var.NUMBER_OF_JOINTS): 
                Joints_increments.append(Joint_angles_delta[i] / number_of_steps)  
             
            for i in range(int(number_of_steps)):       
                for j in range(var.NUMBER_OF_JOINTS):
                    Joint_angles_start[j] -= Joints_increments[j]
                
                if points:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    X = matrix[var.NAME_JOINTS[6]][0][3]
                    Y = matrix[var.NAME_JOINTS[6]][1][3]
                    Z = matrix[var.NAME_JOINTS[6]][2][3]
                    self.points.append([X,Y,Z])
                else:
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles_start)
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)                    
                    time.sleep(self.CalculateSpeed())


            var.POS_JOINT_SIM = Joint_angles_start
            var.POS_AXIS_SIM = POSXYZ 
            self.updateLabels()
             
    def OffsetL(self, line, points):
        pattern = r"[XYZypr]-?\d+(?:\.\d+)?"
        matches = re.findall(pattern, line)   
        pos_xyz_end = [float(match[1:]) for match in matches]
        max_pos_mm = 0
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(pos_xyz_end[i]):
                max_pos_mm = abs(pos_xyz_end[i])
            pos_xyz_end[i] += var.POS_AXIS_SIM[i]    
        
        pos_xyz_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            pos_xyz_delta.append(pos_xyz_end[i] - var.POS_AXIS_SIM[i])  

        number_of_steps =math.ceil(max_pos_mm / self.step_size_mm)
        
        pos_xyz_increments = []
        for i in range(var.NUMBER_OF_JOINTS): 
            pos_xyz_increments.append(pos_xyz_delta[i] / number_of_steps)  
 
        try:
            Joint_angles = self.inverse_kin.InverseKinematics(pos_xyz_end, var.POS_JOINT_SIM)
            self.Motion_ok = self.checkJointPos(Joint_angles)
            matrix = self.forward_kin.ForwardKinematics(Joint_angles)
        except:   
            print("Cannot reach this position")
            self.Motion_ok = False  
                                
        if self.Motion_ok:
            for i in range(int(number_of_steps)):
                if self.Motion_ok:
                    for j in range(var.NUMBER_OF_JOINTS):
                        var.POS_AXIS_SIM[j] += pos_xyz_increments[j]

                if points:    
                    try:
                        Joint_angles = self.inverse_kin.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                        self.Motion_ok = self.checkJointPos(Joint_angles)
                        matrix = self.forward_kin.ForwardKinematics(Joint_angles)
                    except:    
                        print("Cannot reach this position")
                        self.Motion_ok = False  
                                        
                    if self.Motion_ok:
                        X = matrix[var.NAME_JOINTS[6]][0][3]
                        Y = matrix[var.NAME_JOINTS[6]][1][3]
                        Z = matrix[var.NAME_JOINTS[6]][2][3]
                        self.points.append([X,Y,Z])
            
                else:
                    Joint_angles = self.inverse_kin.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                    self.Motion_ok = self.checkJointPos(Joint_angles)
                    matrix = self.forward_kin.ForwardKinematics(Joint_angles)
                    event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS)
                    time.sleep(self.CalculateSpeed())

                if self.Motion_ok:
                    var.POS_JOINT_SIM = Joint_angles
                    self.updateLabels()
 
    def CalculateSpeed(self):
        min_delay = 0.01
        max_delay = 0.2
        delay_step = (max_delay - min_delay)/100
        delay = max_delay - (delay_step * float(var.JOG_SPEED))
        # min delay = 0.005
        # max delay = 0.05
        return delay
        
    def updateLabels(self):
        event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
        event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)

            
    def checkJointPos(self, joint_angles):
        pos = True
        for i in range(var.NUMBER_OF_JOINTS):
            if joint_angles[i] < float(var.ROBOT_JOINT_MOVE[i * 2]):
                pos = False
            if joint_angles[i] > float(var.ROBOT_JOINT_MOVE[i * 2 + 1]):
                pos = False
        if pos == False:
            print("Cannot reach this position")
        return pos