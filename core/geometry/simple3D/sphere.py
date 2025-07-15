from core.geometry.simple3D.ellipsoid import Ellipsoid

class Sphere(Ellipsoid):

    def __init__(self,radius:float = 1.0,seg_radius:float=32.0,seg_height:float=16) -> None:
        self.radius = radius

        super().__init__(2*radius,2*radius,2*radius,seg_radius,seg_height)