from core.light.light import Light
from core.light.light import LIGHT_TYPE

class DirectionalLight(Light):
    def __init__(self,color:list=[1.0, 1.0, 1.0], direction:list=[0.0, -1.0, 0.0]) -> None:
        super().__init__(LightType=LIGHT_TYPE.DIRECTIONAL, color=color)
        self.set_direction(direction)