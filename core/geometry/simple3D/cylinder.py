from core.geometry.simple3D.cylindrical import Cylindrical


class Cylinder(Cylindrical):

    def __init__(self, radius: float = 1.0, height: float = 1.0,seg_raduis:float = 32.0, 
                 seg_heights: float = 4 ,closed: bool = True) -> None:
        
        super().__init__(radius, radius, height, seg_raduis, seg_heights, closed, closed)
        