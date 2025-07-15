from core.geometry.simple3D.cylindrical import Cylindrical

class Cone(Cylindrical):
    def __init__(self,radius: float = 1.0, height: float = 1.0, seg_radius: float = 32.0,
                 seg_heights: float = 4, closed: bool = True) -> None:
        
        super().__init__(0, radius, height, seg_radius, seg_heights, False, closed)