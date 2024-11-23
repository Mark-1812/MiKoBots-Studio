########### FIle with all the calculation for a six axis robot arm


import numpy as np
import backend.core.variables as v
import math

class ForwardKinematics_6:
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

        for i in range(v.NUMBER_OF_JOINTS):
            try:
                dh_param = dh_params[i]
            except:
                dh_param = [0,0,0,0]

            dh_param[0] = dh_param[0] + Joint_angle[i]

            T_i = self.dh_transform(dh_param)
            T = np.dot(T, T_i)
            
            PositionsJoints[Joints[i]] = T
            
        Tool_matrix = self.ToolMatrix(v.TOOL_FRAME)      
        T = np.dot(T, Tool_matrix)  
        
        PositionsJoints[Joints[6]] = T
        
        return PositionsJoints
    
class InverseKinmatics_6:
    def __init__(self):
        pass

    def ToolMatrix(self, Xval, Yval, Zval, RZval, RYval, RXval):
        # Initialize the toolFrame matrix as a 4x4 identity matrix
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

        # The last row is already initialized as an identity matrix

        return toolFrame
    
    def ToolRevMatrix(self, Xval, Yval, Zval, RZval, RYval, RXval):
        # Initialize the toolFrame matrix as a 4x4 identity matrix
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
        toolFrame[0][3] = -Xval

        toolFrame[1][0] = sinRZ * cosRY
        toolFrame[1][1] = sinRZ * sinRY * sinRX + cosRZ * cosRX
        toolFrame[1][2] = sinRZ * sinRY * cosRX - cosRZ * sinRX
        toolFrame[1][3] = -Yval

        toolFrame[2][0] = -sinRY
        toolFrame[2][1] = cosRY * sinRX
        toolFrame[2][2] = cosRY * cosRX
        toolFrame[2][3] = -Zval

        return toolFrame
    
    def R0T_rev_matrix(self,X, Y, Z, y, p, r):
        # Initialize R0T_rev_matrix as a 4x4 identity matrix
        R0T_rev_matrix = np.eye(4)

        # Calculate trigonometric functions
        cos3 = np.cos(np.radians(y))
        sin3 = np.sin(np.radians(y))
        cos4 = np.cos(np.radians(p))
        sin4 = np.sin(np.radians(p))
        cos5 = np.cos(np.radians(r))
        sin5 = np.sin(np.radians(r))

        # Assign values to R0T_rev_matrix
        R0T_rev_matrix[0][0] = cos3 * cos4
        R0T_rev_matrix[0][1] = cos3 * sin4 * sin5 - sin3 * cos5
        R0T_rev_matrix[0][2] = cos3 * sin4 * cos5 + sin3 * sin5
        R0T_rev_matrix[0][3] = X

        R0T_rev_matrix[1][0] = sin3 * cos4
        R0T_rev_matrix[1][1] = sin3 * sin4 * sin5 + cos3 * cos5
        R0T_rev_matrix[1][2] = sin3 * sin4 * cos5 - cos3 * sin5
        R0T_rev_matrix[1][3] = Y

        R0T_rev_matrix[2][0] = -sin4
        R0T_rev_matrix[2][1] = cos4 * sin5
        R0T_rev_matrix[2][2] = cos4 * cos5
        R0T_rev_matrix[2][3] = Z 

        return R0T_rev_matrix 

    def J1matrixRev(self, DHparams, J1, J2, J3):
        J1matrix_rev = np.eye(4)

        # Calculate trigonometric functions
        cos1 = np.cos(np.radians(J1 + DHparams[0][0]))
        sin1 = np.sin(np.radians(J1 + DHparams[0][0]))
        cos2 = np.cos(np.radians(DHparams[0][1]))
        sin2 = np.sin(np.radians(DHparams[0][1]))

        # Assign values to J1matrix_rev
        J1matrix_rev[0][0] = cos1
        J1matrix_rev[0][1] = -sin1 * cos2
        J1matrix_rev[0][2] = sin1 * sin2
        J1matrix_rev[0][3] = DHparams[0][3] * cos1

        J1matrix_rev[1][0] = sin1
        J1matrix_rev[1][1] = cos1 * cos2
        J1matrix_rev[1][2] = -cos1 * sin2
        J1matrix_rev[1][3] = DHparams[0][3] * sin1

        J1matrix_rev[2][0] = 0
        J1matrix_rev[2][1] = sin2
        J1matrix_rev[2][2] = cos2
        J1matrix_rev[2][3] = DHparams[0][2]

        return J1matrix_rev

    def J2matrixRev(self, DHparams, J1, J2, J3):
        J2matrix_rev = np.eye(4)

        # Calculate trigonometric functions
        cos1 = np.cos(np.radians(J2 + DHparams[1][0]))
        sin1 = np.sin(np.radians(J2 + DHparams[1][0]))
        cos2 = np.cos(np.radians(DHparams[1][1]))
        sin2 = np.sin(np.radians(DHparams[1][1]))

        # Assign values to J2matrix_rev
        J2matrix_rev[0][0] = cos1
        J2matrix_rev[0][1] = -sin1 * cos2
        J2matrix_rev[0][2] = sin1 * sin2
        J2matrix_rev[0][3] = DHparams[1][3] * cos1

        J2matrix_rev[1][0] = sin1
        J2matrix_rev[1][1] = cos1 * cos2
        J2matrix_rev[1][2] = -cos1 * sin2
        J2matrix_rev[1][3] = DHparams[1][3] * sin1

        J2matrix_rev[2][0] = 0
        J2matrix_rev[2][1] = sin2
        J2matrix_rev[2][2] = cos2
        J2matrix_rev[2][3] = DHparams[1][2]

        return J2matrix_rev

    def J3matrixRev(self, DHparams, J1, J2, J3):
        J3matrix_rev = np.eye(4)

        # Calculate trigonometric functions
        cos1 = np.cos(np.radians(J3 + DHparams[2][0]))
        sin1 = np.sin(np.radians(J3 + DHparams[2][0]))
        cos2 = np.cos(np.radians(DHparams[2][1]))
        sin2 = np.sin(np.radians(DHparams[2][1]))

        # Assign values to J3matrix_rev
        J3matrix_rev[0][0] = cos1
        J3matrix_rev[0][1] = -sin1 * cos2
        J3matrix_rev[0][2] = sin1 * sin2
        J3matrix_rev[0][3] = DHparams[2][3] * cos1

        J3matrix_rev[1][0] = sin1
        J3matrix_rev[1][1] = cos1 * cos2
        J3matrix_rev[1][2] = -cos1 * sin2
        J3matrix_rev[1][3] = DHparams[2][3] * sin1

        J3matrix_rev[2][0] = 0
        J3matrix_rev[2][1] = sin2
        J3matrix_rev[2][2] = cos2
        J3matrix_rev[2][3] = DHparams[2][2]

        return J3matrix_rev

    def R06_neg_matrix(self, DHparams):
        R06_neg_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -DHparams[5][2]],
            [0, 0, 0, 1]
        ])
        return R06_neg_matrix 

    def InverseKinematics(self, POS_XYZ, POS_J123):     
        X = POS_XYZ[0]
        Y = POS_XYZ[1]
        Z = POS_XYZ[2]
        y = POS_XYZ[3]
        p = POS_XYZ[4]
        r = POS_XYZ[5]

        J5_start = POS_J123[4]

        
        TX = v.TOOL_FRAME[0]
        TY = v.TOOL_FRAME[1]
        TZ = v.TOOL_FRAME[2]
        Ty = v.TOOL_FRAME[3]
        Tp = v.TOOL_FRAME[4]
        Tr = v.TOOL_FRAME[5]
        
        if J5_start >= 0:
            WristCon = "F"
        else:
            WristCon = "N"
        
        DHparams = v.DH_PARAM
        DHparams = [[float(value) for value in sublist] for sublist in DHparams]

        ToolFrame = self.ToolMatrix(TX, TY, TZ, Ty, Tp, Tr)
        InvToolFrame = self.ToolRevMatrix(TX, TY, TZ, Ty, Tp, Tr)

        R0T_rev_matrix = self.R0T_rev_matrix(X, Y, Z, y, p, r)

        R06_neg_matrix = self.R06_neg_matrix(DHparams)

        InvR03matrix_rev = np.zeros((4, 4))
        
        R03matrix_rev = np.zeros((4, 4))
        R02matrix_rev = np.zeros((4, 4))
        R03_6matrix = np.zeros((4, 4))
        R06_rev_matrix = np.zeros((4, 4))
        R05_rev_matrix = np.zeros((4, 4))

        for k in range(4):
            for i in range(4):
                for j in range(4):
                    R06_rev_matrix[k, i] += R0T_rev_matrix[k, j] * InvToolFrame[j, i]

        for k in range(4):
            for i in range(4):
                for j in range(4):
                    R05_rev_matrix[k][i] += R06_rev_matrix[k][j] * R06_neg_matrix[j][i]

        # Calculate robot[0].PosJEnd based on conditions
        if R05_rev_matrix[0][3] == 0:
            R05_rev_matrix[0][3] = 0.001
        if R05_rev_matrix[1][3] == 0:
            R05_rev_matrix[1][3] = 0.001

        if R05_rev_matrix[0][3] >= 0 and R05_rev_matrix[1][3] > 0:
            J1 = math.degrees(math.atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]))
        elif R05_rev_matrix[0][3] >= 0 and R05_rev_matrix[1][3] <= 0:
            J1 = math.degrees(math.atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]))
        elif R05_rev_matrix[0][3] < 0 and R05_rev_matrix[1][3] <= 0:
            J1 = -180 + math.degrees(math.atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]))
        elif R05_rev_matrix[0][3] <= 0 and R05_rev_matrix[1][3] > 0:
            J1 = 180 + math.degrees(math.atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]))

        # Calculate XatJ1zero and YatJ1zero
        XatJ1zero = (R05_rev_matrix[0][3] * math.cos(math.radians(-J1))) - (R05_rev_matrix[1][3] * math.sin(math.radians(-J1)))
        #print(f"XatJ1zero {XatJ1zero}")
        YatJ1zero = 0
        
        Length_1 = abs(XatJ1zero - DHparams[0][3])
        #print(f"length 1 {Length_1}")
        Length_2 = math.sqrt((XatJ1zero - DHparams[0][3])**2 + (YatJ1zero - YatJ1zero)**2 + (R05_rev_matrix[2][3] - DHparams[0][2])**2)
        #print(f"length 2 {Length_2}")
        Length_3 = math.sqrt(DHparams[3][2]**2 + DHparams[2][3]**2)
        #print(f"length 3 {Length_3}")
        Length_4 = R05_rev_matrix[2][3] - DHparams[0][2]
        #print(f"length 4 {Length_4}")
        
        Theta_B = math.degrees(math.atan(Length_1 / Length_4))
        #print(f"Theta_B {Theta_B}")
        Theta_C = math.degrees(math.acos((DHparams[1][3]**2 + Length_2**2 - Length_3**2) / (2 * DHparams[1][3] * Length_2)))
        
        #print(f"Theta_C {Theta_C}")
        Theta_D = math.degrees(math.acos((Length_3**2 + DHparams[1][3]**2 - Length_2**2) / (2 * Length_3 * DHparams[1][3])))
        #print(f"Theta_D {Theta_D}")
        Theta_E = math.degrees(math.atan(DHparams[2][3] / DHparams[3][2]))
        #print(f"Theta_E {Theta_E}")

        # Calculate robot[1].PosJEnd
        if XatJ1zero > DHparams[0][3]:
            if Length_4 > 0:
                J2 = Theta_B - Theta_C
            else:
                J2 = Theta_B - Theta_C + 180
        else:
            J2 = -(Theta_B + Theta_C)

        # Calculate robot[2].PosJEnd
        J3 = -(Theta_D + Theta_E) + 90

        J1matrix_rev = self.J1matrixRev(DHparams, J1, J2, J3)
        J2matrix_rev = self.J2matrixRev(DHparams, J1, J2, J3)
        J3matrix_rev = self.J3matrixRev(DHparams, J1, J2, J3)

        for k in range(4):
            for i in range(4):
                for j in range(4):
                    R02matrix_rev[k][i] += J1matrix_rev[k][j] * J2matrix_rev[j][i]

        for k in range(4):
            for i in range(4):
                for j in range(4):
                    R03matrix_rev[k][i] += R02matrix_rev[k][j] * J3matrix_rev[j][i]          

        #print(f"R03matrix_rev \n {R03matrix_rev}")
        InvR03matrix_rev[0][0] = R03matrix_rev[0][0]
        InvR03matrix_rev[0][1] = R03matrix_rev[1][0]
        InvR03matrix_rev[0][2] = R03matrix_rev[2][0]
        InvR03matrix_rev[1][0] = R03matrix_rev[0][1]
        InvR03matrix_rev[1][1] = R03matrix_rev[1][1]
        InvR03matrix_rev[1][2] = R03matrix_rev[2][1]
        InvR03matrix_rev[2][0] = R03matrix_rev[0][2]
        InvR03matrix_rev[2][1] = R03matrix_rev[1][2]
        InvR03matrix_rev[2][2] = R03matrix_rev[2][2]

        for k in range(4):
            for i in range(4):
                for j in range(4):
                    R03_6matrix[k][i] += InvR03matrix_rev[k][j] * R06_rev_matrix[j][i]
        
        try:
            if WristCon == "F":
                J5 = math.degrees(math.atan2(math.sqrt(1 - R03_6matrix[2][2]**2), R03_6matrix[2][2]))
            else:
                J5 = math.degrees(math.atan2(-math.sqrt(1 - R03_6matrix[2][2]**2), R03_6matrix[2][2]))
        except:
            if 1-R03_6matrix[2][2]**2 < 0:
                J5 = 0

        if J5 < 0:
            test = math.degrees(math.atan2(R03_6matrix[1][2], R03_6matrix[0][2]))
            J4 = -test
        else:
            test = math.degrees(math.atan2(-R03_6matrix[1][2], R03_6matrix[0][2]))
            J4 = -test



        if J5 < 0:
            test = math.degrees(math.atan2(R03_6matrix[2][1], R03_6matrix[2][0]))
            J6 = -test
        else:
            test = math.degrees(math.atan2(-R03_6matrix[2][1], -R03_6matrix[2][0]))
            J6 = -test
            

        Joint_angles = [J1, J2, J3, J4, J5, J6]
        return Joint_angles
    