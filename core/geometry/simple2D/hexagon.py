from core.geometry.simple2D.polygon import Polygon

class Hexagon(Polygon):
    def __init__(self,raduis:float = 1) -> None:
        super().__init__(raduis, 6)
    