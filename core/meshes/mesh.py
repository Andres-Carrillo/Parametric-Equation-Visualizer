from core.objects.object3D import Object3D
from core.material.basic.basic import BasicMaterial
from core.material.lighted.flat import FlatMaterial
from core.geometry.geometry import Geometry
import OpenGL.GL as gl

class Mesh(Object3D):

    def __init__(self,geometry,material) -> None:
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        
        self._init_buffers()


    def _init_buffers(self):
        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)
        
        for var_name,attrib_obj in self.geometry.attributes.items():
            attrib_obj.associate_variable(self.material.program,var_name)

        gl.glBindVertexArray(0)



""" SphereMesh class
This class creates a sphere mesh with a specified radius, number of segments, and rings.
It also allows for the use of a custom material and the number of lights affecting the material.
The class inherits from the Mesh class and initializes the geometry and material for the sphere.
As well as the shader program for the material and geometry."""
class SphereMesh(Mesh):
    def __init__(self,material:BasicMaterial = None,
                 geometry:Geometry = None,num_of_light:int=1,position:list = [0,0,0]):
        
        
        if material is None:
            material = FlatMaterial(properties={"base_color": [1.0, 1.0, 1.0]}, number_of_lights=num_of_light)


        super().__init__(geometry=geometry, material=material)
        self.set_position(position)
