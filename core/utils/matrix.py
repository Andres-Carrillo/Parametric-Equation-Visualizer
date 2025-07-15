import numpy as np
import pyglm as glm
from math import sin,cos,tan,pi
# from pyglm import glm ## want to use glm but not necessarily right now as performance is currently not an issue
class Matrix(object):

    # Construct a 2D matrix of dimension size x size
    @staticmethod
    def identity(size:int)->np.ndarray:
        return np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        ).astype(float)
    
    # Construct 4x4 identity matrix for basis of 3D Transformations
    @staticmethod
    def mat4_identity()->np.ndarray:
        return Matrix.identity(4)
    
    # Construct 4x4 translation matrix for 3D Transformations
    @staticmethod
    def mat4_translation(x,y,z)->np.ndarray:
        return np.array(
                    [[1, 0, 0, x],
                    [0, 1, 0, y],
                    [0, 0, 1, z],
                    [0, 0, 0, 1]]
                ).astype(float)
    
    # Construct 4x4 rotation matrix for 3D rotations about the x axis
    @staticmethod
    def mat4_rotate_x(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[1,  0,  0,  0],
             [0,  c, -s,  0],
             [0,  s,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    
    @staticmethod
    def mat4_rotate_y(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[c,  0,  s,  0],
             [0,  1,  0,  0],
             [-s, 0,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    

    @staticmethod
    def mat4_rotate_z(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[c, -s,  0,  0],
             [s,  c,  0,  0],
             [0,  0,  1,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    
    # construct 4x4 scaling matrix for 3D scaling
    @staticmethod
    def mat4_scale_uniform(scale_val:float)->np.ndarray:
        return np.array(
            [[scale_val, 0, 0, 0],
             [0, scale_val, 0, 0],
             [0, 0, scale_val, 0],
             [0, 0, 0, 1]]
        ).astype(float)
        
    @staticmethod
    def mat4_scale(x:float,y:float,z:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        mat[0][0] = x
        mat[1][1] = y
        mat[2][2] = z

        return mat
    

    
    # construct 4x4 perspective projection matrix
    @staticmethod
    def mat4_perspective(angle_of_view:float = 60.0, aspect_ratio:float=1.0, near:float = 0.1, far:float =1000)->np.ndarray:
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a / 2)
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)
        return np.array(
            [[d / aspect_ratio, 0, 0, 0],
             [0, d, 0, 0],
             [0, 0, b, c],
             [0, 0, -1, 0]]
        ).astype(np.float32)
    
    @staticmethod
    def make_orthographic(left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        return np.array(
            [[2 / (right - left), 0, 0, -(right + left) / (right - left)],
             [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
             [0, 0, -2 / (far - near), -(far + near) / (far - near)],
             [0, 0, 0, 1]]
        ).astype(float)

    @staticmethod
    def make_look_at(position, target):
        world_up = [0, 1, 0]
        forward = np.subtract(target, position)
        right = np.cross(forward, world_up)
        # If forward and world_up vectors are parallel,
        # the right vector is zero.
        # Fix this by perturbing the world_up vector a bit
        if np.linalg.norm(right) < 1e-6:
            offset = np.array([0, 0, -1e-3])
            right = np.cross(forward, world_up + offset)
        up = np.cross(right, forward)
        # All vectors should have length 1
        forward = np.divide(forward, np.linalg.norm(forward))
        right = np.divide(right, np.linalg.norm(right))
        
        #need check to avoid division by zero
        if np.linalg.norm(up) > 0:
            up = np.divide(up, np.linalg.norm(up))
        else:
            up = np.array([0, 1, 0])
        # up = np.divide(up, np.linalg.norm(up))
        return np.array(
            [[right[0], up[0], -forward[0], position[0]],
             [right[1], up[1], -forward[1], position[1]],
             [right[2], up[2], -forward[2], position[2]],
             [0, 0, 0, 1]]
        ).astype(float)
    

    
    



# class GLMMatrix(object):
#     """ A wrapper around pyglm to provide a more Pythonic interface.
#         Rotations should be quaternions, not Euler angles. But should take Euler angles for compatibility.
#     """
#     @staticmethod
#     def mat4_identity():
#         return glm.mat4(1.0)

#     @staticmethod
#     def mat4_translation(x, y, z):
#         return glm.translate(glm.mat4(1.0), glm.vec3(x, y, z))

#     @staticmethod
#     def mat4_rotate_x(angle):
#         return glm.rotate(glm.mat4(1.0), angle, glm.vec3(1, 0, 0))

#     @staticmethod
#     def mat4_rotate_y(angle):
#         return glm.rotate(glm.mat4(1.0), angle, glm.vec3(0, 1, 0))

#     @staticmethod
#     def mat4_rotate_z(angle):
#         return glm.rotate(glm.mat4(1.0), angle, glm.vec3(0, 0, 1))

#     @staticmethod
#     def mat4_scale(scale_val):
#         return glm.scale(glm.mat4(1.0), glm.vec3(scale_val, scale_val, scale_val))
#     @staticmethod
#     def mat4_scale(x, y, z):
#         return glm.scale(glm.mat4(1.0), glm.vec3(x, y, z))
#     @staticmethod
#     def mat4_perspective(angle_of_view=60.0, aspect_ratio=1.0, near=0.1, far=1000):
#         return glm.perspective(glm.radians(angle_of_view), aspect_ratio, near, far)
#     @staticmethod
#     def make_orthographic(left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
#         return glm.ortho(left, right, bottom, top, near, far)
   
#     @staticmethod
#     def mat4_to_np(mat):
#         """ Convert a glm.mat4 to a numpy array. """
#         return np.array(mat).astype(float)
#     @staticmethod
#     def np_to_mat4(np_array):
#         """ Convert a numpy array to a glm.mat4. """
#         return glm.mat4(*np_array.flatten().tolist())
#     @staticmethod
#     def mat4_multiply(mat_a, mat_b):
#         """ Multiply two glm.mat4 matrices. """
#         return glm.mat4(mat_a) * glm.mat4(mat_b)
#     @staticmethod
#     def mat4_inverse(mat):
#         """ Inverse of a glm.mat4 matrix. """
#         return glm.inverse(mat)
#     @staticmethod
#     def mat4_transpose(mat):
#         """ Transpose of a glm.mat4 matrix. """
#         return glm.transpose(mat)
#     @staticmethod
#     def mat4_determinant(mat):
#         """ Determinant of a glm.mat4 matrix. """
#         return glm.determinant(mat)
    
#     @staticmethod
#     def mat4_decompose(mat):
#         """ Decompose a glm.mat4 matrix into translation, rotation, and scale. """
#         translation, rotation, scale = glm.decompose(mat)
#         return translation, rotation, scale
    
#     @staticmethod
#     def mat4_look_at(position, target, up=glm.vec3(0, 1, 0)):
#         """ Create a look-at matrix using glm. """
#         return glm.lookAt(glm.vec3(position), glm.vec3(target), glm.vec3(up))
    
     
#     @staticmethod
#     def make_look_at(position, target):
#         world_up = glm.vec3(0, 1, 0)

#         forward = glm.normalize(glm.vec3(target) - glm.vec3(position))
#         right = glm.normalize(glm.cross(forward, world_up))
#         up = glm.normalize(glm.cross(right, forward))
        
#         return glm.mat4(
#             right.x, up.x, -forward.x, position[0],
#             right.y, up.y, -forward.y, position[1],
#             right.z, up.z, -forward.z, position[2],
#             0, 0, 0, 1
#         )
    
#     @staticmethod
#     def mat4_frustum(left, right, bottom, top, near, far):
#         """ Create a frustum matrix using glm. """
#         return glm.frustum(left, right, bottom, top, near, far)
#     @staticmethod
#     def mat4_perspective_fov(fov, aspect, near, far):
#         """ Create a perspective projection matrix using glm. """
#         return glm.perspective(glm.radians(fov), aspect, near, far)
