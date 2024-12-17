from .kinematics_3_axis import InverseKinematics_3, ForwardKinematics_3
from .kinematics_5_axis import InverseKinematics_5, ForwardKinematics_5
from .kinematics_6_axis import InverseKinematics_6, ForwardKinematics_6
from .convert_matrix import MatrixToXYZ_5, MatrixToXYZ

inverse_kinematics_3 = InverseKinematics_3()
forward_kinematics_3 = ForwardKinematics_3()

inverse_kinematics_5 = InverseKinematics_5()
forward_kinematics_5 = ForwardKinematics_5()

inverse_kinematics_6 = InverseKinematics_6()
forward_kinematics_6 = ForwardKinematics_6()

def inverseKinematics(number_of_joints, pos, old_pos = None):
    pos_joint_end = None
    if number_of_joints == 3:
        pos_joint_end = inverse_kinematics_3.run(pos)
    if number_of_joints == 5:
        pos_joint_end = inverse_kinematics_5.run(pos)
    if number_of_joints == 6:
        pos_joint_end = inverse_kinematics_6.run(pos, old_pos)
        
    return pos_joint_end
        
def forwardKinematics(number_of_joints, pos, dh_param):
    matrix = None
    if number_of_joints == 3:
        matrix = forward_kinematics_3.run(pos, dh_param)
    if number_of_joints == 5:
        matrix = forward_kinematics_5.run(pos, dh_param)
    if number_of_joints == 6:
        matrix = forward_kinematics_6.run(pos, dh_param)
        
    return matrix

def matrix_to_xyz(number_of_joints, matrix):
    pos_xyz = None
    if number_of_joints == 3:
        pos_xyz = MatrixToXYZ(matrix)
    if number_of_joints == 5:
        pos_xyz = MatrixToXYZ_5(matrix)
    if number_of_joints == 6:
        pos_xyz = MatrixToXYZ(matrix)
        
    return pos_xyz
        
    
        