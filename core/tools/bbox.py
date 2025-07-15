from core.material.basic.point import PointMaterial
from core.geometry.simple3D.box import BoxGeometry
from core.material.basic.line import LineMaterial
from core.meshes.mesh import Mesh
import numpy as np

class BBoxMesh:
    def __init__(self, object_ref:Mesh,line_width:float=2.0,double_sided:bool=True,point_size:float=10.0) -> None:
        """
        BBoxMesh class
        This class creates a bounding box mesh for visualizating a specified axis-aligned bounding box (AABB).
        It also allows for the use of a custom line width and point size.
        The class initializes the geometry and materials for the bounding box.
        """
        self.object = object_ref
        self._update()
        
        self.double_sided = double_sided
        self.line_width = line_width
        self.point_size = point_size

    def _update(self):
        self.bbox = self.object.geometry.AA_bounding_box()

        min_corner,max_corner = self.bbox[0],self.bbox[1]
        self.width = max_corner[0] - min_corner[0]
        self.height = max_corner[1] - min_corner[1]
        self.depth = max_corner[2] - min_corner[2]

        self.center = np.array([(max_corner[0] + min_corner[0]) / 2,
                               (max_corner[1] + min_corner[1]) / 2,
                               (max_corner[2] + min_corner[2]) / 2])
        
        self.wire_geometry = BoxGeometry(self.width, self.height, self.depth)
        self.point_geometry = BoxGeometry(self.width, self.height, self.depth)
        
    """ creates and returns a mesh based on the bounding box geometry and the line material """
    def get_wireframe(self, update: bool = False):
        # prevent double update when calling get_bbox
        if update:
            self._update()

        edge_material = LineMaterial(properties={"base_color": [1.0, 0.0, 0.0]})
        # edge_material.settings['wire_frame'] = True
        edge_material.settings['use_vertex_colors'] = False
        edge_material.settings['double_sided'] = self.double_sided
        # edge_material.settings["draw_mode"] = gl.GL_LINES
        edge_material.settings['line_width'] = 5 
        # edge_material.settings['double_sided'] = self.double_sided

        wire_frame_mesh = Mesh(self.wire_geometry, edge_material)
        wire_frame_mesh.set_position(self.object.global_position + self.center)
        
        return wire_frame_mesh
    
    """creates and returns a mesh based on the bounding box geometry and the point material """
    def get_corners(self, update: bool = False):
        # prevent double update when calling get_bbox
        if update:
            self._update()

        corner_material = PointMaterial(properties={"base_color": [1.0, 0.0, 0.0]})
        corner_material.settings['point_size'] = self.point_size
        corner_material.settings['double_sided'] = self.double_sided

        corner_points_mesh = Mesh(self.point_geometry, corner_material)
        corner_points_mesh.set_position(self.object.global_position + self.center)

        return corner_points_mesh

    """returns the bounding box mesh and the wireframe mesh"""
    def get_bbox(self): 
        self._update()
        return  {"corners": self.get_corners(),
                    "wireframe": self.get_wireframe()
                }