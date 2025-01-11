########### FIle with all the calculation for a six axis robot arm


import numpy as np
import backend.core.variables as var
import math

class ForwardKinematics_5:
    def __init__(self):
        pass
    
    def ToolMatrix(self, TOOL_FRAME):
    # Initialize the toolFrame matrix as a 4x4 identity matrix
        Xval = TOOL_FRAME[0]
        Yval = TOOL_FRAME[1]
        Zval = TOOL_FRAME[2]
        RZval = TOOL_FRAME[3]
        RYval = TOOL_FRAME[4]
        RXval = TOOL_FRAME[5]
    
        toolFrame = np.eye(4)

        # Calculate trigonometric functions
        cosRZ = np.cos(np.radians(RZval))
        sinRZ = np.sin(np.radians(RZval))
        cosRY = np.cos(np.radians(RYval))
        sinRY = np.sin(np.radians(RYval))
        cosRX = np.cos(np.radians(RXval))
        sinRX = np.sin(np.radians(RXval))

        # Assign values to toolFrame
        toolFrame[0][0] = cosRZ * cosRY
        toolFrame[0][1] = cosRZ * sinRY * sinRX - sinRZ * cosRX
        toolFrame[0][2] = cosRZ * sinRY * cosRX + sinRZ * sinRX
        toolFrame[0][3] = Xval

        toolFrame[1][0] = sinRZ * cosRY
        toolFrame[1][1] = sinRZ * sinRY * sinRX + cosRZ * cosRX
        toolFrame[1][2] = sinRZ * sinRY * cosRX - cosRZ * sinRX
        toolFrame[1][3] = Yval

        toolFrame[2][0] = -sinRY
        toolFrame[2][1] = cosRY * sinRX
        toolFrame[2][2] = cosRY * cosRX
        toolFrame[2][3] = Zval

        return toolFrame

    # Function to compute the transformation matrix for a single DH parameter set
    def dh_transform(self, dh_param):
        theta_degrees, alpha_degrees, d, a = dh_param

        alpha_radians = np.deg2rad(alpha_degrees)
        theta_radians = np.deg2rad(theta_degrees)

        cos_theta = np.cos(theta_radians)
        sin_theta = np.sin(theta_radians)
        cos_alpha = np.cos(alpha_radians)
        sin_alpha = np.sin(alpha_radians)

        transformation_matrix = np.array([
            [cos_theta, -sin_theta * cos_alpha, sin_theta * sin_alpha, a * cos_theta],
            [sin_theta, cos_theta * cos_alpha, -cos_theta * sin_alpha, a * sin_theta],
            [0, sin_alpha, cos_alpha, d],
            [0, 0, 0, 1]
        ])
        return transformation_matrix
    
    def run(self, Joint_angle, dh_params):
        dh_params = [[float(value) for value in sublist] for sublist in dh_params]
        
        Joints = ["J1", "J2", "J3", "J4", "J5", "TOOL"]

            
        PositionsJoints = {}
        T =np.eye(4)

        for i in range(5):
            try:
                dh_param = dh_params[i]
            except:
                dh_param = [0,0,0,0]

            dh_param[0] = dh_param[0] + Joint_angle[i]

            T_i = self.dh_transform(dh_param)
            T = np.dot(T, T_i)
            
            PositionsJoints[Joints[i]] = T
            
        Tool_matrix = self.ToolMatrix(var.TOOL_FRAME)
        T = np.dot(T, Tool_matrix)  


        PositionsJoints[Joints[5]] = T
        
        return PositionsJoints
 
 
 
 
class InverseKinematics_5:
    def __init__(self):
        pass
    
    def run(self, pos):
        tool_frame = var.TOOL_FRAME

        tool_X = tool_frame[0]
        tool_Y = tool_frame[1]
        tool_Z = tool_frame[2]
        
        
        X = pos[0] #- tool_X
        Y = pos[1] #- tool_Y
        Z = pos[2] #- tool_Z
        pitch = pos[3]
        roll = pos[4]
        
        #print(f"X {X} Y {Y} Z {Z}")
        dh_param = var.DH_PARAM

        L1 = float(dh_param[0][2])
        L2 = float(dh_param[1][3])
        L3 = float(dh_param[2][3])
        L4 = float(dh_param[4][2]) + tool_Z
        
        #print(f"L1 {L1} L2 {L2} L3 {L3}")
        
        J1 = math.atan(Y / X)
        J1 = math.degrees(J1) 
        
        
        #L4 becomes the lenth of the 
        
        pitch_length = L4 * math.cos(math.radians(pitch))
        # print(f"pitch_lenth {pitch_lenth}")
        pitch_height = L4 * math.sin(math.radians(pitch))
        # print(f"pitch_height {pitch_height}")
        
        r = math.sqrt(X**2 + Y**2) - pitch_length
        # print(f"r: {r}")
        
        D = math.sqrt((Z - L1 - pitch_height)**2 + r**2)
        # print(Z - L1 - pitch_height)
        # print(f"D: {D}")
        
        a1 = math.acos((D**2 + L2**2 - L3**2) / (2 * D * L2))
        # print(f"a1: {math.degrees(a1)}")
        
        a2 = math.atan((Z-L1-pitch_height)/r)
        # print(f"a2: {math.degrees(a2)}")

        J2 = math.degrees(a1) + math.degrees(a2) - 90
        
        # print(D**2 - L3**2 -  L2**2)
        
        J3 = (math.degrees(math.acos((D**2 - L3**2 -  L2**2) / (2 * L3 * L2)))-90) * -1

        J4 = pitch - J2 - J3
        
        J5 = roll

        # print(f"J1: {J1}")
        # print(f"J2: {J2}")
        # print(f"J3: {J3}")
        # print(f"J4: {J4}")
        
        POSJ123 = [J1,J2,J3,J4,J5]
        
        return POSJ123
    



