from core.geometry.parametric import Parametric
from core.utils.matrix import Matrix
from math import pi, sin, cos

class Ellipsoid(Parametric):
    def __init__(self, width=1, height=1, depth=1, theta_segments=16, phi_segments=32):
        def surface_function(u, v):

            phi = 2 * pi * u
            theta = (1 - v) * pi
            return [width / 2 * sin(theta) * cos(phi),\
                    height / 2 * sin(theta) * sin(phi),\
                    depth / 2 * cos(theta)]

        super().__init__(0,
                         1,
                         phi_segments,
                         0,
                         1,
                         theta_segments,
                         surface_function)
        # Rotate the ellipsoid around the x-axis on -90 degrees.
        # The vertices and normals will be recalculated.
        self.apply_transform(Matrix.mat4_rotate_x(-pi/2))