from core.objects.object3D import Object3D
import enum

class LIGHT_TYPE(enum.Enum):
    AMBIENT = 0
    DIRECTIONAL = 1
    POINT = 2
    SPOT = 3
    AREA = 4
    IMAGE_BASED = 5


class Light(Object3D):
    def __init__(self, LightType:LIGHT_TYPE = LIGHT_TYPE.AMBIENT, color:list=[1.0, 1.0, 1.0], attenuation:list=[1.0,0.0,0.0])-> None:
        super().__init__()
        self.light_type = LightType
        self.color = color
        self.attenuation = attenuation
