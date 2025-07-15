from meshes.mesh import Mesh
from geometry.simple3D.sphere import Sphere
from material.basic.basic import BasicMaterial
from material.lighted.flat import FlatMaterial
from geometry.geometry import Geometry

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


class SphereFactory:
    @staticmethod
    def create(radius: int = 1, segments: int = 16, rings: int = 16, 
               material: BasicMaterial = None, num_of_light: int = 1, position: list = [0, 0, 0]) -> SphereMesh:
        """
        Factory method to create a SphereMesh object.
        :param radius: The radius of the sphere.
        :param segments: The number of segments around the sphere.
        :param rings: The number of rings from top to bottom.
        :param material: Optional material to use for the sphere.
        :param num_of_light: Number of lights affecting the material (if applicable).
        :param position: Initial position of the sphere.
        :return: A SphereMesh object.
        """
        
        geometry = Sphere(radius=radius, seg_radius=segments, seg_height=rings)

        return SphereMesh(material=material, geometry=geometry, 
                          num_of_light=num_of_light, position=position)

#################################: Function for spawning Sphere Meshes :#################################:

def generate_sphere_mesh(radius: int = 1, segments: int = 16, rings: int = 16, 
                         material: BasicMaterial = None, num_of_light: int = 1,
                           position: list = [0, 0, 0]) ->SphereMesh:
    """
    Generates a SphereMesh object with the given radius, segments, and rings.
    :param radius: The radius of the sphere.
    :param segments: The number of segments around the sphere.
    :param rings: The number of rings from top to bottom.
    :param material: Optional material to use for the sphere.
    :param num_of_light: Number of lights affecting the material (if applicable).
    :param position: Initial position of the sphere.
    :return: A SphereMesh object.
    """
    return SphereMesh(material=material, radius=radius, segments=segments, rings=rings, 
                      num_of_light=num_of_light, position=position)