import numpy as np

def XYZToMatrix(XYZ_pos):
    translation_vector = [
        XYZ_pos[0],
        XYZ_pos[1], 
        XYZ_pos[2]
        ]
    
    rotation_angles_degrees = [
        XYZ_pos[3],
        XYZ_pos[4], 
        XYZ_pos[5]
    ]
    
    # Convert degrees to radians for the rotations
    rotation_angles_radians = np.radians(rotation_angles_degrees)

    # Create translation matrix
    translation_matrix = np.eye(4)
    translation_matrix[0:3, 3] = translation_vector

    # Create rotation matrices for x, y, and z axes
    rotation_matrices = []
    for axis, angle in enumerate(rotation_angles_radians):
        rotation_matrix = np.eye(4)
        if axis == 0:
            rotation_matrix[1:3, 1:3] = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        elif axis == 1:
            rotation_matrix[0, 0] = np.cos(angle)
            rotation_matrix[0, 2] = np.sin(angle)
            rotation_matrix[2, 0] = -np.sin(angle)
            rotation_matrix[2, 2] = np.cos(angle)
        elif axis == 2:
            rotation_matrix[0:2, 0:2] = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        rotation_matrices.append(rotation_matrix)

    # Multiply all rotation matrices together
    combined_rotation_matrix = np.eye(4)
    for matrix in rotation_matrices:
        combined_rotation_matrix = np.matmul(combined_rotation_matrix, matrix)

    # Combine translation and rotation into a single matrix
    combined_matrix = np.matmul(combined_rotation_matrix, translation_matrix)

    return combined_matrix

def MatrixToXYZ(matrix):    
    rotation_matrix = matrix[:3, :3]
    euler_radians = np.array([
        np.arctan2(rotation_matrix[2,1], rotation_matrix[2,2]), # Roll
        np.arctan2(-rotation_matrix[2,0], np.sqrt(rotation_matrix[2,1]**2 + rotation_matrix[2,2]**2)), # Pitch
        np.arctan2(rotation_matrix[1,0], rotation_matrix[0,0])  # Yaw
    ])
    euler_degrees = np.degrees(euler_radians)
    
    POSXYZ = [0] * 6
    
    POSXYZ[0] = matrix[0][3]
    POSXYZ[1] = matrix[1][3]
    POSXYZ[2] = matrix[2][3]
    POSXYZ[3] = euler_degrees[0]
    POSXYZ[4] = euler_degrees[1]
    POSXYZ[5] = euler_degrees[2]
    
    return POSXYZ