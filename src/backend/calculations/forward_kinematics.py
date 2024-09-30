import json
import numpy as np
import backend.core.variables as v

class ForwardKinematics:
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
    
    def ForwardKinematics(self, Joint_angle):
        
        dh_params = v.DH_PARAM
        dh_params = [[float(value) for value in sublist] for sublist in dh_params]

        Joints = ["J1", "J2", "J3", "J4", "J5", "J6", "TOOL"]
        PositionsJoints = {}
        T =np.eye(4)

        for i in range(len(dh_params)):
            dh_param = dh_params[i]

            dh_param[0] = dh_param[0] + Joint_angle[i]

            T_i = self.dh_transform(dh_param)
            T = np.dot(T, T_i)
            
            PositionsJoints[Joints[i]] = T
            

        Tool_matrix = self.ToolMatrix(v.TOOL_FRAME)      
        T = np.dot(T, Tool_matrix)  
        
        PositionsJoints[Joints[6]] = T
        
        return PositionsJoints