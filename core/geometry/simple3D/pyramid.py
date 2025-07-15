from core.geometry.simple3D.cylindrical import Cylindrical

class Pyramid(Cylindrical):

    def __init__(self, radius: float = 1.0, height: float = 1.0, sides: int = 4,
                 seg_height: float = 4, closed: bool = True) -> None:
        
        super().__init__(0, radius, height, sides, seg_height, False, closed)