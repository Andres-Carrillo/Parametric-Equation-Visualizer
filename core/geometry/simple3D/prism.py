from core.geometry.simple3D.cylindrical import Cylindrical

class Prism(Cylindrical):
    def __init__(self,radius:float = 1.0,height:float = 1.0,sides = 6,seg_height = 4,closed = True) -> None:
        
        super().__init__(0.0,radius,height,sides,seg_height,closed,closed)

