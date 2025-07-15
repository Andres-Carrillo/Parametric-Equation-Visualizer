from core.objects.object3D import Object3D
from core.utils.matrix import Matrix
from numpy.linalg import inv


class Camera(Object3D):
    def __init__(self,angle_of_view:float = 60.0, aspect_ratio:float=1.0, near:float = 0.1, far:float =1000):
        super().__init__()
        self.angle_of_view = angle_of_view
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        self.projection_matrix = Matrix.mat4_perspective(angle_of_view,aspect_ratio,near,far)
        self.view_matrix = Matrix.mat4_identity()

    def update_view_matrix(self):
        """Update the view matrix based on the camera's position and orientation"""
        self.view_matrix = inv(self.global_matrix)


    def set_perspective(self,angle_of_view:float = 50.0,aspect_ratio:float=1.0, near:float = 0.1, far:float =1000):
        """Set the perspective projection matrix"""
        self.projection_matrix = Matrix.mat4_perspective(angle_of_view,aspect_ratio,near,far)
        self.angle_of_view = angle_of_view
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far


    def set_orthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self.projection_matrix = Matrix.make_orthographic(left, right, bottom, top, near, far)

    def update_aspect_ratio(self, aspect_ratio:float):
        """Update the aspect ratio of the camera"""
        self.aspect_ratio = aspect_ratio
        self.projection_matrix = Matrix.mat4_perspective(self.angle_of_view,aspect_ratio,self.near,self.far)