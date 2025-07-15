from core.geometry.simple3D.sphere import Sphere
from core.material.basic.surface import SurfaceMaterial
from core.meshes.mesh import Mesh
from core.light.point import PointLight

class PointLightTool(Mesh):
    def __init__(self,point_light:PointLight,size:float=0.1,line_width:int=1):
        self.light_reference = point_light
        color = point_light.color
        geometry = Sphere(radius=size,seg_radius=2,seg_height=4)

        material = SurfaceMaterial(properties={
            "base_color":color,
            "wire_frame":True,
            "double_sided":True,
            "line_width":line_width,
            "use_vertex_colors":False,
        })

        super().__init__(geometry,material)




