from core.light.light import Light
from core.light.light import LIGHT_TYPE

class PointLight(Light):
    def __init__(self,color:list=[1.0, 1.0, 1.0], position:list=[0.0, 0.0, 0.0], attenuation:list=[1.0, 0.0, 0.1],max_distance:float = 325) -> None:
        super().__init__(LightType=LIGHT_TYPE.POINT, color=color, attenuation=attenuation)
        self.set_position(position)

    # need to implement look up table for attenuation values
    # attenuation = [constant, linear, quadratic]
    # constant = 1.0
    # linear = 0.7 -> 0.0014
    # quadratic = 1.8 -> 0.0000075
    def __scale_attenuation(self,attenuation:list):
        self.attenuation = attenuation
        self.attenuation[2] = 1.0 / (self.max_distance * self.max_distance)