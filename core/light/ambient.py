from core.light.light import Light
from core.light.light import LIGHT_TYPE

class AmbientLight(Light):
    def __init__(self, color:list=[1.0, 1.0, 1.0], attenuation:list=[1.0,0.0,0.0]) -> None:
        super().__init__(LIGHT_TYPE.AMBIENT, color, attenuation)