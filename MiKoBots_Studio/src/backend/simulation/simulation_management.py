import backend.core.variables as var
from backend.calculations.kinematics_6_axis import ForwardKinematics_6, InverseKinmatics_6
from backend.calculations.kinematics_3_axis import ForwardKinematics_3, InverseKinematics_3
from backend.calculations.convert_matrix import MatrixToXYZ

from PyQt5.QtCore import QObject

import numpy as np
import re
import time
import math

from backend.core.event_manager import event_manager

class SimulationManagement(QObject):
    def __init__(self):
        self.forward_kinematics_6 = ForwardKinematics_6()
        self.inverse_kinematics_6 = InverseKinmatics_6()
        
        self.inverse_kinematics_3 = InverseKinematics_3()
        self.forward_kinematics_3 = ForwardKinematics_3()

        self.viewer_busy = 0
        
        self.points = []
        
        self.step_size_deg = 1
        self.step_size_mm = 2
        
        self.Motion_ok = True
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("simulate_program", self.SimulateProgram)   
        event_manager.subscribe("request_set_sim_not_busy", self.SetNotBusy)   
          
    def EnableSimulation(self, state):
        if state ==  2:
            var.SIM = 1
            event_manager.publish("request_change_labels_control", True)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
            event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
            
        else:
            var.SIM = 0
            event_manager.publish("request_change_labels_control", False)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS, var.NAME_AXIS, var.UNIT_AXIS)
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
        def execute_program():
            
            self.viewer_busy = 1
            if type(POS) == list:
                line = Move
                
                for i in range(var.NUMBER_OF_JOINTS):
                    line += (f" {var.NAME_AXIS[i]}{POS[i]}")
            else:
                line = f"{Move} {POS}"
                
            words = line.split()
            if words[0] == "MoveL": self.MoveL(line, False)
            elif words[0] == "MoveJ": self.MoveJ(line, False)
            elif words[0] == "OffsetJ": self.OffsetJ(line, False)
            elif words[0] == "OffsetL" or words[0] == "jogL": self.OffsetL(line, False)
            
            
            elif words[0] == "jogJ": 
                line = Move
                for i in range(var.NUMBER_OF_JOINTS):
                    line += (f" {var.NAME_JOINTS[i]}{POS[i]}")   
                self.jogJ(line, False)
                
            elif words[0] == "MoveJoint":
                line = Move
                for i in range(var.NUMBER_OF_JOINTS):
                    line += (f" {var.NAME_JOINTS[i]}{POS[i]}")              
                self.MoveJoint(line, False)
                
            elif words[0] == "Tool_MoveTo":
                self.updateLabelTool(line)
                
            self.viewer_busy = 0
                                                    

        if self.viewer_busy == 0:
            self.Motion_ok = True
            thread = threading.Thread(target = execute_program)
            thread.start()    

    #######################
    # Movements action robot
    
    def SetNotBusy(self):
        self.viewer_busy = 0
    
    def jogJ(self, line, points):       
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            return
        
        matches = re.search(pattern, line)
        Joint_angles_delta = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]

        Joint_angles_start = var.POS_JOINT_SIM

        # calculate the max movement, and the end position
        max_angle = 0
        Joint_angles_end = [0] * (var.NUMBER_OF_JOINTS + var.EXTRA_JOINT)
        for i in range(var.NUMBER_OF_JOINTS):
            if max_angle < abs(Joint_angles_delta[i]):
                max_angle = abs(Joint_angles_delta[i])
            Joint_angles_end[i] = Joint_angles_delta[i] + var.POS_JOINT_SIM[i]
            
            
 
        # check if the robot can reach the position
        self.Motion_ok = self.checkJointPos(Joint_angles_end, True)
        
        # move the robot
        if self.Motion_ok:
            number_of_steps = math.ceil(max_angle / self.step_size_deg)

            Joints_increments = self.JointAxisIncrements(Joint_angles_delta, number_of_steps)
            self.JTypeMovement(number_of_steps, Joint_angles_start, Joints_increments, points)

            if var.NUMBER_OF_JOINTS == 3:
                matrix = self.forward_kinematics_3.ForwardKinematics(var.POS_JOINT_SIM)
                var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[3]])
            elif var.NUMBER_OF_JOINTS == 6:
                matrix = self.forward_kinematics_6.ForwardKinematics(var.POS_JOINT_SIM)
                var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[6]])      

            
            self.updateLabels()

    def MoveJoint(self, line, points):
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            return
            
        matches = re.search(pattern, line)
        Joint_angles_end = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]
        
        # calculate the max movement
        max_angle = 0 
        for i in range(var.NUMBER_OF_JOINTS):
            if max_angle < abs(var.POS_JOINT_SIM[i] - Joint_angles_end[i]):
                max_angle = abs(var.POS_JOINT_SIM[i] - Joint_angles_end[i])
                        
        # check if the robot can reach the position
        self.Motion_ok = self.checkJointPos(Joint_angles_end, True)
        Joint_angles_start = var.POS_JOINT_SIM
        
        # move the robot
        if self.Motion_ok:
            Joint_angles_delta = self.JointAnglesDelta(Joint_angles_start, Joint_angles_end)
            number_of_steps = math.ceil(max_angle / self.step_size_deg)          
            Joints_increments = self.JointAxisIncrements(Joint_angles_delta, number_of_steps)
            
            # move the robot to the new position
            self.JTypeMovement(number_of_steps, Joint_angles_start, Joints_increments, points)
            
            # Calculate the XYZ position of the robot
            if var.NUMBER_OF_JOINTS == 3:
                matrix = self.forward_kinematics_3.ForwardKinematics(var.POS_JOINT_SIM)
                var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[3]])
            elif var.NUMBER_OF_JOINTS == 6:
                matrix = self.forward_kinematics_6.ForwardKinematics(var.POS_JOINT_SIM)
                var.POS_AXIS_SIM = MatrixToXYZ(matrix[var.NAME_JOINTS[6]])       
            
            # update the position in the labels
            self.updateLabels()

    def MoveJ(self, line, points): 
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            
        matches = re.search(pattern, line)
        axis_pos_end = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]
    
        # calculate the max movement
        max_pos_mm = 0
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(var.POS_AXIS_SIM[i] - axis_pos_end[i]):
                max_pos_mm = abs(var.POS_AXIS_SIM[i] - axis_pos_end[i])

        # Check if the robot can reach the position
        Joint_angles_start = var.POS_JOINT_SIM
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)

                      
        if self.Motion_ok and max_pos_mm > 0.00:
            if var.NUMBER_OF_JOINTS == 6:
                Joint_angles_end = self.inverse_kinematics_6.InverseKinematics(axis_pos_end, var.POS_JOINT_SIM)
            elif var.NUMBER_OF_JOINTS == 3:
                Joint_angles_end = self.inverse_kinematics_3.inverseKinematics(axis_pos_end)
                
            Joint_angles_delta = self.JointAnglesDelta(Joint_angles_start, Joint_angles_end)
            number_of_steps = math.ceil(max_pos_mm / self.step_size_mm)
            Joints_increments = self.JointAxisIncrements(Joint_angles_delta, number_of_steps)
            
            # move the robot to the new position
            self.JTypeMovement(number_of_steps, Joint_angles_start, Joints_increments, points)
                      
            # update the position in the labels
            var.POS_AXIS_SIM = axis_pos_end
            self.updateLabels()                  
                      
    def MoveL(self, line, points):
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            
        matches = re.search(pattern, line)
        axis_pos_end = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]     
            
        max_pos_mm = 0
        pos_xyz_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            if max_pos_mm < (axis_pos_end[i] - var.POS_AXIS_SIM[i]):
                max_pos_mm = (axis_pos_end[i] - var.POS_AXIS_SIM[i])
            pos_xyz_delta.append(axis_pos_end[i] - var.POS_AXIS_SIM[i])  

        # calculate the distance per mm
        number_of_steps = math.ceil(max_pos_mm / self.step_size_mm)
        
        # Check if you can reach the end position
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)          
            
        # if the robot can reach the end position
        if self.Motion_ok:
            pos_xyz_increments = self.JointAxisIncrements(pos_xyz_delta, number_of_steps) 
            self.LTypeMovement(number_of_steps, pos_xyz_increments, points)
             
    def OffsetJ(self, line, points):
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
        
        matches = re.search(pattern, line)
        axis_pos_delta = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]

        # calculate tha max movement, and the end position
        max_pos_mm = 0
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(axis_pos_delta[i]):
                max_pos_mm = abs(axis_pos_delta[i])
            axis_pos_delta[i] += var.POS_AXIS_SIM[i]  
        
        axis_pos_end = axis_pos_delta
        
        # Check if the robot can reach the position
        Joint_angles_start = var.POS_JOINT_SIM   
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)        

        

        if self.Motion_ok:
            if var.NUMBER_OF_JOINTS == 6:
                Joint_angles_end = self.inverse_kinematics_6.InverseKinematics(axis_pos_end, var.POS_JOINT_SIM)
            elif var.NUMBER_OF_JOINTS == 3:
                Joint_angles_end = self.inverse_kinematics_3.inverseKinematics(axis_pos_end)
                
            #print(f"Joint angle end: {Joint_angles_end}")    
                
            Joint_angles_delta = self.JointAnglesDelta(Joint_angles_start, Joint_angles_end)   
            
            
                       
            number_of_steps = math.ceil(abs(max_pos_mm) / self.step_size_mm)
            Joints_increments = self.JointAxisIncrements(Joint_angles_delta, number_of_steps)
            
            #print(f"Joints_increments: {Joints_increments}")
            
            # move the robot to the new position
            self.JTypeMovement(number_of_steps, Joint_angles_start, Joints_increments, points)
                 
            # update the position in the labels      
            var.POS_AXIS_SIM = axis_pos_end
            self.updateLabels()
               
    def OffsetL(self, line, points):
        # read the line
        if var.NUMBER_OF_JOINTS == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif var.NUMBER_OF_JOINTS == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            
        matches = re.search(pattern, line)
        axis_pos_delta = [float(matches.group(i + 1)) for i in range(var.NUMBER_OF_JOINTS)]
      
        
        # calculate the max movement
        max_pos_mm = 0
        axis_pos_end = [0] * var.NUMBER_OF_JOINTS
        for i in range(var.NUMBER_OF_JOINTS):
            if max_pos_mm < abs(axis_pos_delta[i]):
                max_pos_mm = abs(axis_pos_delta[i])
            axis_pos_end[i] = var.POS_AXIS_SIM[i] + axis_pos_delta[i]
        
        # check if the robot can reach the position  
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)  
                                
        # move the robot                        
        if self.Motion_ok:
            number_of_steps =math.ceil(max_pos_mm / self.step_size_mm)
            pos_xyz_increments = self.JointAxisIncrements(axis_pos_delta, number_of_steps)
            
            self.LTypeMovement(number_of_steps, pos_xyz_increments, points)
 
    #######################
    # functions for moving the robvot in the sim
    
    def JointAxisIncrements(self, delta, number_of_steps):
        increments = []
        for i in range(var.NUMBER_OF_JOINTS + var.EXTRA_JOINT): 
            try:
                increments.append(delta[i] / number_of_steps)  
            except:
                increments.append(0)
            
        return increments
 
    def JointAnglesDelta(self, Joint_angles_start, Joint_angles_end):
        Joint_angles_delta = []
        for i in range(var.NUMBER_OF_JOINTS): 
            Joint_angles_delta.append(Joint_angles_end[i]-Joint_angles_start[i])  
        
        return Joint_angles_delta
 
    def CalculateSpeed(self, joint_distances):       
        # need to know the move in degrees of the maximum joint and we need to know the joint
        # we know the max speed per joint
        #print(f"joints distances {joint_distances}")
        
        # get the maximum speed per joint
        var.JOINT_SPEED 
        joint_speed = [0] * var.NUMBER_OF_JOINTS
        for i in range(var.NUMBER_OF_JOINTS):
            joint_speed[i] = float(var.JOINT_SPEED[i * 2])
            if joint_speed[i] == 0:
                joint_speed[i] = 50
        #print(f"max speed of the joints {joint_speed}")
        
        # get the speed percentage
        speed_percentage = float(event_manager.publish("request_get_speed")[0])
        #print(f"speed percentage {speed_percentage}")
        
        # calculate the percentage of how much each joint has to travel
        percentage = [0] * var.NUMBER_OF_JOINTS
        joint_distances_abs = [abs(x) for x in joint_distances]
        max_joint_distance_index = joint_distances_abs.index(max(joint_distances_abs))
        
        #print(f"max_joint_distance_index {joint_distances_abs}")
        
        for i in range(var.NUMBER_OF_JOINTS):
            if (joint_distances_abs[i] / max(joint_distances_abs)) < 0.01:
                percentage[i] = 0.01
            else:
                percentage[i] = joint_distances_abs[i] / max(joint_distances_abs)
        #print(f"percentage of how much each joint has to move {percentage}")
    
        # calculate the speed of the joint with the maximum travel
        VEL = (speed_percentage/100) * joint_speed[max_joint_distance_index]
        
        # check if an other joint goes over the max speed
        JointMaxSpeed = max_joint_distance_index
        for i in range(var.NUMBER_OF_JOINTS):
            if (percentage[i] * VEL) > joint_speed[i] * (speed_percentage/100):
                JointMaxSpeed = i
                VEL = (speed_percentage / 100) * (joint_speed[JointMaxSpeed]/percentage[JointMaxSpeed])
        
        # calculate the delay
        delay = (1 / VEL) * max(joint_distances_abs) # 0.005 is the average time needed for calculation
        #print(f"delay {delay}")
        return delay
         
    def LTypeMovement(self, number_of_steps, pos_xyz_increments, points):
        for i in range(int(number_of_steps)):
            if self.Motion_ok:
                for j in range(var.NUMBER_OF_JOINTS):
                    var.POS_AXIS_SIM[j] += pos_xyz_increments[j]

            if points:    
                try:
                    if var.NUMBER_OF_JOINTS == 6:
                        Joint_angles = self.inverse_kinematics_6.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                    elif var.NUMBER_OF_JOINTS == 3:
                        Joint_angles = self.inverse_kinematics_3.inverseKinematics(var.POS_AXIS_SIM)
                    self.Motion_ok = self.checkJointPos(Joint_angles, True)
                    #matrix = self.forward_kinematics_6.ForwardKinematics(Joint_angles)
                except:    
                    print("Cannot reach this position")
                    text = "Error cannot reach this position"
                    event_manager.publish("request_insert_new_log", text) 
                    self.Motion_ok = False  
                                    
                if self.Motion_ok:
                    X = matrix[var.NAME_JOINTS[6]][0][3]
                    Y = matrix[var.NAME_JOINTS[6]][1][3]
                    Z = matrix[var.NAME_JOINTS[6]][2][3]
                    self.points.append([X,Y,Z])
        
            else:
                if var.NUMBER_OF_JOINTS == 6:
                    Joint_angles = self.inverse_kinematics_6.InverseKinematics(var.POS_AXIS_SIM, var.POS_JOINT_SIM)
                elif var.NUMBER_OF_JOINTS == 3:
                    Joint_angles = self.inverse_kinematics_3.inverseKinematics(var.POS_AXIS_SIM)
                    
                self.Motion_ok = self.checkJointPos(Joint_angles, True)
                
                if var.NUMBER_OF_JOINTS == 6:
                    matrix = self.forward_kinematics_6.ForwardKinematics(Joint_angles)
                elif var.NUMBER_OF_JOINTS == 3: 
                    matrix = self.forward_kinematics_3.ForwardKinematics(Joint_angles)
                                    
                event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
                joint_increments = [a - b for a, b in zip(Joint_angles, var.POS_JOINT_SIM)]
                delay = self.CalculateSpeed(joint_increments)
                time.sleep(delay)

            if self.Motion_ok:
                var.POS_JOINT_SIM = Joint_angles
                self.updateLabels()
 
    def JTypeMovement(self, number_of_steps, Joint_angles_start, Joints_increments, points):
        #print(f"number of steps {number_of_steps}")
        start_time = time.time()
        for i in range(int(number_of_steps)):
            
            
            for j in range(var.NUMBER_OF_JOINTS + var.EXTRA_JOINT):
                Joint_angles_start[j] += Joints_increments[j]   
                
            if points:
                if var.NUMBER_OF_JOINTS == 6:
                    matrix = self.forward_kinematics_6.ForwardKinematics(Joint_angles_start)
                elif var.NUMBER_OF_JOINTS == 3: 
                    matrix = self.forward_kinematics_3.ForwardKinematics(Joint_angles_start)
                X = matrix[var.NAME_JOINTS[6]][0][3]
                Y = matrix[var.NAME_JOINTS[6]][1][3]
                Z = matrix[var.NAME_JOINTS[6]][2][3]
                self.points.append([X,Y,Z])
            
            else:
                if var.NUMBER_OF_JOINTS == 6:
                    matrix = self.forward_kinematics_6.ForwardKinematics(Joint_angles_start)
                elif var.NUMBER_OF_JOINTS == 3: 
                    matrix = self.forward_kinematics_3.ForwardKinematics(Joint_angles_start)
                    
                event_manager.publish("request_move_robot", matrix, var.NAME_JOINTS, var.NUMBER_OF_JOINTS, var.EXTRA_JOINT)
                delay_time = self.CalculateSpeed(Joints_increments)
                time.sleep(delay_time)
                
            var.POS_JOINT_SIM = Joint_angles_start
            
        #end_time = time.time()
        #execution_time = end_time - start_time - delay_time
        #print(execution_time)
       
       
    def updateLabelTool(self, line):
        
        match = re.search(r'[-+]?\d+', line)
        if match:
            value = match.group()
            var.TOOL_POS += int(value)
            event_manager.publish("request_set_tool_pos", var.TOOL_POS)     
        
    def updateLabels(self):
        event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
        event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
     
    def checkJointPos(self, end_pos, joint):
        pos = True
        try:
            if not joint:
                if var.NUMBER_OF_JOINTS == 6:
                    end_pos = self.inverse_kinematics_6.InverseKinematics(end_pos, var.POS_JOINT_SIM)
                elif var.NUMBER_OF_JOINTS == 3:
                    end_pos = self.inverse_kinematics_3.inverseKinematics(end_pos)
            for i in range(var.NUMBER_OF_JOINTS):
                if end_pos[i] < float(var.ROBOT_JOINT_MOVE[i * 2]):
                    pos = False
                if end_pos[i] > float(var.ROBOT_JOINT_MOVE[i * 2 + 1]):
                    pos = False
                for i in range(var.NUMBER_OF_JOINTS):
                    if np.isnan(end_pos[i]):
                        pos = False
        except:
            pos = False
                       
        if pos == False:
            print(var.NUMBER_OF_JOINTS)
            text = "Error cannot reach this position"
            event_manager.publish("request_insert_new_log", text) 
            event_manager.publish("request_stop_sim")
            
        
        return pos
    
        
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
    
    
 
    
    