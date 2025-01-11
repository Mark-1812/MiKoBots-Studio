import backend.core.variables as var
from backend.calculations import forwardKinematics, inverseKinematics, matrix_to_xyz


from PyQt5.QtCore import QObject

import numpy as np
import re
import time
import math

from backend.core.event_manager import event_manager

from .robot import change_pos_robot



class SimulationManagement(QObject):
    def __init__(self):
        self.Motion_ok = True
        self.simulation_on = False
        self.simulation_busy = False

        self.number_of_joints = None
          
    def EnableSimulation(self, state):
        if state ==  2:
            self.simulation_on = True
            event_manager.publish("request_change_labels_control", True)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
            event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
            
        else:
            self.simulation_on = False
            event_manager.publish("request_change_labels_control", False)
            event_manager.publish("request_label_pos_axis", var.POS_AXIS, var.NAME_AXIS, var.UNIT_AXIS)
            event_manager.publish("request_label_pos_joint", var.POS_JOINT, var.NAME_JOINTS, var.UNIT_JOINT)
    
    def SimulateProgram(self, program):
        self.program = program
        self.last_position = []

        self.simulation_busy = True     
        words = self.program.split()

        self.number_of_joints = var.NUMBER_OF_JOINTS
        self.extra_joint = var.EXTRA_JOINT

        
        if words[0] == "MoveL": self.MoveL(self.program)
        elif words[0] == "MoveJ": self.MoveJ(self.program)
        elif words[0] == "OffsetJ": self.OffsetJ(self.program)
        elif words[0] == "OffsetL" or words[0] == "jogL": self.OffsetL(self.program)
        elif words[0] == "jogJ": self.jogJ(self.program)
        elif words[0] == "MoveJoint": self.MoveJoint(self.program)
        
        self.simulation_busy = False

    #######################
    # Movements action robot
    
    def jogJ(self, line):     
        if self.number_of_joints == 3:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        else:
            print(var.LANGUAGE_DATA.get("message_no_kinematics")) 
            return
        
        matches = re.search(pattern, line)
        Joint_angles_delta = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]

        Joint_angles_start = var.POS_JOINT_SIM

        # calculate the max movement, and the end position
        max_angle = 0
        Joint_angles_end = [0] * (self.number_of_joints + self.extra_joint)
        for i in range(self.number_of_joints):
            if max_angle < abs(Joint_angles_delta[i]):
                max_angle = abs(Joint_angles_delta[i])
            Joint_angles_end[i] = Joint_angles_delta[i] + var.POS_JOINT_SIM[i]
            
        # check if the robot can reach the position
        self.Motion_ok = self.checkJointPos(Joint_angles_end, True)
        
        # move the robot
        if self.Motion_ok:
            self.JTypeMovement(Joint_angles_start, Joint_angles_end)
            
            matrix = forwardKinematics(self.number_of_joints, var.POS_JOINT_SIM, var.DH_PARAM)
            var.POS_AXIS_SIM = matrix_to_xyz(self.number_of_joints, matrix["TOOL"])   

            
            self.updateLabels()

    def MoveJoint(self, line):
        if self.number_of_joints == 3:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'J1(-?\d+).*J2(-?\d+).*J3(-?\d+).*J4(-?\d+).*J5(-?\d+).*J6(-?\d+)'
        else:
            print(var.LANGUAGE_DATA.get("message_no_kinematics")) 
            return
            
        # find the end postion of the joint angles
        matches = re.search(pattern, line)
        Joint_angles_end = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]
        
                        
        # check if the robot can reach the position
        self.Motion_ok = self.checkJointPos(Joint_angles_end, True)
        Joint_angles_start = var.POS_JOINT_SIM
        
        # move the robot
        if self.Motion_ok:
            # move the robot to the new position
            self.JTypeMovement(Joint_angles_start, Joint_angles_end)
            
            # Calculate the XYZ position of the robot
            matrix = forwardKinematics(self.number_of_joints, var.POS_JOINT_SIM, var.DH_PARAM)
            var.POS_AXIS_SIM = matrix_to_xyz(self.number_of_joints, matrix["TOOL"])   
                
            
            # update the position in the labels
            self.updateLabels()

    def MoveJ(self, line): 
        if self.number_of_joints == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print(var.LANGUAGE_DATA.get("message_no_kinematics")) 
            
        matches = re.search(pattern, line)
        axis_pos_end = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]

        # Check if the robot can reach the position
        Joint_angles_start = var.POS_JOINT_SIM
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)

                      
        if self.Motion_ok:
            # calculate the end position of the joins
            Joint_angles_end = inverseKinematics(self.number_of_joints, axis_pos_end, var.POS_JOINT_SIM)

            
            self.JTypeMovement(Joint_angles_start, Joint_angles_end)

            # update the position in the labels
            var.POS_AXIS_SIM = axis_pos_end
            self.updateLabels()                  
                           
    def OffsetJ(self, line):
        if self.number_of_joints == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print(var.LANGUAGE_DATA.get("message_no_kinematics")) 
        
        # find the delta positions
        matches = re.search(pattern, line)
        axis_pos_delta = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]

        # calculate tha end position of the axis
        for i in range(self.number_of_joints):
            axis_pos_delta[i] += var.POS_AXIS_SIM[i]  
        axis_pos_end = axis_pos_delta
        
        # Check if the robot can reach the position
        Joint_angles_start = var.POS_JOINT_SIM   
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)        

        if self.Motion_ok:
            # calculate the end position of the joints
            Joint_angles_end = inverseKinematics(self.number_of_joints, axis_pos_end, var.POS_JOINT_SIM)

            # move the robot to the new position
            self.JTypeMovement(Joint_angles_start, Joint_angles_end)
                 
            # update the position in the labels      
            var.POS_AXIS_SIM = axis_pos_end
            self.updateLabels()
   
    def MoveL(self, line):
        if self.number_of_joints == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print(var.LANGUAGE_DATA.get("message_no_kinematics")) 
            
        # find the end position of the axis
        matches = re.search(pattern, line)
        axis_pos_end = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]     

        axis_pos_start = var.POS_AXIS_SIM 
        
        # Check if you can reach the end position
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)          
            
        # if the robot can reach the end position
        if self.Motion_ok:
            self.LTypeMovement(axis_pos_start, axis_pos_end)

            self.updateLabels()
                      
    def OffsetL(self, line):
        # read the line
        if self.number_of_joints == 3:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+)'
        elif self.number_of_joints == 5:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+)'
        elif self.number_of_joints == 6:
            pattern = r'X(-?\d+).*Y(-?\d+).*Z(-?\d+).*y(-?\d+).*p(-?\d+).*r(-?\d+)'
        else:
            print("no kinematics yet for this type of robot") 
            
        matches = re.search(pattern, line)
        axis_pos_delta = [float(matches.group(i + 1)) for i in range(self.number_of_joints)]
      
        axis_pos_start = var.POS_AXIS_SIM

        # calculate the max movement
        axis_pos_end = [0] * self.number_of_joints
        for i in range(self.number_of_joints):
            axis_pos_end[i] = axis_pos_start[i] + axis_pos_delta[i]
        
        # check if the robot can reach the position  
        self.Motion_ok = self.checkJointPos(axis_pos_end, False)  
                                
        # move the robot                        
        if self.Motion_ok:
            self.LTypeMovement(axis_pos_start, axis_pos_end)

            self.updateLabels()
 
    #######################
    # functions for moving the robvot in the sim
    
    # Move L commands
    def AxisPosDelta(self, axis_pos_start, axis_pos_end):
        axis_pos_delta = []
        for i in range(self.number_of_joints): 
            axis_pos_delta.append(axis_pos_end[i]-axis_pos_start[i])  
        
        return axis_pos_delta        
   
    def AxisIncrements(self, axis_pos_delta, max_step_size):
        # get the max delta
        max_delta = max(axis_pos_delta, key=abs)
        max_delta = abs(max_delta)
        # print(f"Max delta {max_delta}")

        increments = []
        for i in range(self.number_of_joints + self.extra_joint): 
            try:
                # print(f"{(abs(Joint_angles_delta[i]) / max_delta) * max_step_size} = ({abs(Joint_angles_delta[i])}) / {max_delta} * {max_step_size}")
                step_size = (abs(axis_pos_delta[i]) / max_delta) * max_step_size
                if axis_pos_delta[i] < 0:
                    increments.append(-step_size)
                else:
                    increments.append(step_size)
            except:
                increments.append(0)
            
        return increments

    def LTypeMovement(self, axis_start, axis_end):
        axis_pos_start = axis_start
        axis_pos_end = axis_end
        reached_end = False

        while not reached_end:
            start_time = time.time()
            # get the speed so we can calculate the mm per step
            speed_percentage = float(event_manager.publish("request_get_speed")[0])
            step_size = speed_percentage * 0.01

            axis_pos_delta = self.AxisPosDelta(axis_pos_start, axis_pos_end)
            if abs(max(axis_pos_delta, key=abs)) < step_size:
                step_size = abs(max(axis_pos_delta, key=abs))
                reached_end = True
                if step_size == 0:
                    break

            # detemine the increment
            axis_increments = self.AxisIncrements(axis_pos_delta, step_size)

            # calculate the end position of this step
            axis_pos_start = [a + b for a, b in zip(axis_pos_start, axis_increments)]
            
            Joint_angles_end = inverseKinematics(self.number_of_joints, axis_pos_start, var.POS_JOINT_SIM)

            # check if it can reach the position
            self.Motion_ok = self.checkJointPos(Joint_angles_end, True)

            # calculate the matrix for the position of the sim models
            matrix = forwardKinematics(self.number_of_joints, Joint_angles_end, var.DH_PARAM)
            
            # move the robot in the simulation
            change_pos_robot(matrix, var.NAME_JOINTS, self.number_of_joints, self.extra_joint)

            # calculate the joint increments and calculate the delay between each step
            joint_increments = [a - b for a, b in zip(Joint_angles_end, var.POS_JOINT_SIM)]
            delay = self.CalculateSpeed(joint_increments)

            end_time = time.time()
            delay_calculations = end_time - start_time

            time.sleep(delay - delay_calculations)

            var.POS_JOINT_SIM = Joint_angles_end


        var.POS_AXIS_SIM = axis_pos_start


    # Move J commands
    def JointAnglesDelta(self, Joint_angles_start, Joint_angles_end):
        Joint_angles_delta = []
        for i in range(self.number_of_joints): 
            Joint_angles_delta.append(Joint_angles_end[i]-Joint_angles_start[i])  
        
        return Joint_angles_delta

    def JointIncrements(self, Joint_angles_delta, max_step_size):
        # get the max delta
        max_delta = max(Joint_angles_delta, key=abs)
        max_delta = abs(max_delta)
        # print(f"Max delta {max_delta}")

        increments = []
        for i in range(self.number_of_joints + self.extra_joint): 
            try:
                # print(f"{(abs(Joint_angles_delta[i]) / max_delta) * max_step_size} = ({abs(Joint_angles_delta[i])}) / {max_delta} * {max_step_size}")
                step_size = (abs(Joint_angles_delta[i]) / max_delta) * max_step_size
                if Joint_angles_delta[i] < 0:
                    increments.append(-step_size)
                else:
                    increments.append(step_size)
            except:
                increments.append(0)
            
        return increments
        
    def JTypeMovement(self, Joint_start, Joint_end):
        Joint_angles_start = Joint_start
        Joint_angles_end = Joint_end
        reached_end = False

        while not reached_end:
            #start_time = time.time()

            # get the speed so we can calculate the deg per step
            speed_percentage = float(event_manager.publish("request_get_speed")[0])

            step_size = speed_percentage * 0.01

            Joint_angles_delta = self.JointAnglesDelta(Joint_angles_start, Joint_angles_end)
            # when the step size is greater than the maximum delta change it to the max delta
            if abs(max(Joint_angles_delta, key=abs)) < step_size:
                step_size = abs(max(Joint_angles_delta, key=abs))
                reached_end = True
                if step_size == 0:
                    break
                

            Joints_increments = self.JointIncrements(Joint_angles_delta, step_size)
            # print(f"Joint increments: {Joints_increments}")

            # print(f"Joint start: {Joint_angles_start}")
            # add the increment to the start position
            Joint_angles_start = [a + b for a, b in zip(Joint_angles_start, Joints_increments)]

            # print(f"Joint start: {Joint_angles_start}")
            # print(f"Joint end: {Joint_angles_end}")
            matrix = forwardKinematics(self.number_of_joints, Joint_angles_start, var.DH_PARAM)

            change_pos_robot(matrix, var.NAME_JOINTS, self.number_of_joints, self.extra_joint)
            delay_time = self.CalculateSpeed(Joints_increments)
            # print(f"time delay: {delay_time}")

            #end_time = time.time()
            #delay_calculations = end_time - start_time
            time.sleep(delay_time)

            # print(f"time needed for calculation = {start_time - end_time}")
            # print(f"delay time {delay_time}")



        var.POS_JOINT_SIM = Joint_angles_start




    def CalculateSpeed(self, joint_distances):       
        # need to know the move in degrees of the maximum joint and we need to know the joint
        # we know the max speed per joint
        
        # get the maximum speed per joint
        joint_speed = [0] * self.number_of_joints
        for i in range(self.number_of_joints):
            joint_speed[i] = float(var.MAX_JOINT_SPEED[i * 2])
            if joint_speed[i] == 0:
                joint_speed[i] = 50
        
        # get the speed percentage
        speed_percentage = float(event_manager.publish("request_get_speed")[0])
        
        # calculate the percentage of how much each joint has to travel
        percentage = [0] * self.number_of_joints
        joint_distances_abs = [abs(x) for x in joint_distances]
        max_joint_distance_index = joint_distances_abs.index(max(joint_distances_abs))
        
        for i in range(self.number_of_joints):
            if (joint_distances_abs[i] / max(joint_distances_abs)) < 0.01:
                percentage[i] = 0.01
            else:
                percentage[i] = joint_distances_abs[i] / max(joint_distances_abs)
    
        # calculate the speed of the joint with the maximum travel
        VEL = (speed_percentage/100) * joint_speed[max_joint_distance_index]
        
        # check if an other joint goes over the max speed
        JointMaxSpeed = max_joint_distance_index
        for i in range(self.number_of_joints):
            if (percentage[i] * VEL) > joint_speed[i] * (speed_percentage/100):
                JointMaxSpeed = i
                VEL = (speed_percentage / 100) * (joint_speed[JointMaxSpeed]/percentage[JointMaxSpeed])
        
        # calculate the delay
        delay = (1 / VEL) * max(joint_distances_abs) # 0.005 is the average time needed for calculation
        return delay
       
    # check if the robot can reach the position       
    def checkJointPos(self, joint_angles_end, joint):
        pos = True
        try:
            if not joint:
                joint_angles_end = inverseKinematics(self.number_of_joints, joint_angles_end, var.POS_JOINT_SIM)
                
            for i in range(self.number_of_joints):
                if joint_angles_end[i] < float(var.MAX_JOINT_MOVE[i * 2]):
                    pos = False
                if joint_angles_end[i] > float(var.MAX_JOINT_MOVE[i * 2 + 1]):
                    pos = False
                for i in range(self.number_of_joints):
                    if np.isnan(joint_angles_end[i]):
                        pos = False
        except:
            pos = False
                       
                       
                       
        if pos == False:
            print(var.LANGUAGE_DATA.get("message_cannot_reach_pos")) 
            event_manager.publish("request_stop_sim")
            
        
        return pos
    

    # Update the label in the GUI
    def updateLabelTool(self, line):
        
        match = re.search(r'[-+]?\d+', line)
        if match:
            value = match.group()
            var.TOOL_POS += int(value)
            event_manager.publish("request_set_tool_pos", var.TOOL_POS)     
        
    def updateLabels(self):
        event_manager.publish("request_label_pos_axis", var.POS_AXIS_SIM, var.NAME_AXIS, var.UNIT_AXIS)
        event_manager.publish("request_label_pos_joint", var.POS_JOINT_SIM, var.NAME_JOINTS, var.UNIT_JOINT)
     
 

    
    
 
    
    