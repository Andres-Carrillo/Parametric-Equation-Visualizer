from core.glsl.attribute import Attribute
from enum import Enum
import numpy as np

class GEOMETRY_TYPE(Enum):
    CIRCLE = 0
    RECTANGLE = 1
    TRIANGLE = 2
    QUAD = 3
    PENTAGON = 4
    HEXAGON = 5
    HEPTAGON = 6
    OCTAGON = 7
    BOX = 8
    PLANE = 9
    SPHERE = 10
    CYLINDER = 11
    CONE = 12
    PRISM = 13
    PYRAMID = 14

    def __str__(self):
        if self == GEOMETRY_TYPE.CIRCLE:
            return "circle"
        elif self == GEOMETRY_TYPE.RECTANGLE:
            return "rectangle"
        elif self == GEOMETRY_TYPE.TRIANGLE:
            return "triangle"
        elif self == GEOMETRY_TYPE.QUAD:
            return "quad"
        elif self == GEOMETRY_TYPE.PENTAGON:
            return "pentagon"
        elif self == GEOMETRY_TYPE.HEXAGON:
            return "hexagon"
        elif self == GEOMETRY_TYPE.HEPTAGON:
            return "heptagon"
        elif self == GEOMETRY_TYPE.OCTAGON:
            return "octagon"
        elif self == GEOMETRY_TYPE.BOX:
            return "box"
        elif self == GEOMETRY_TYPE.PLANE:
            return "plane"
        elif self == GEOMETRY_TYPE.SPHERE:
            return "sphere"
        elif self == GEOMETRY_TYPE.CYLINDER:
            return "cylinder"
        elif self == GEOMETRY_TYPE.CONE:
            return "cone"
        elif self == GEOMETRY_TYPE.PRISM:
            return "prism"
        elif self == GEOMETRY_TYPE.PYRAMID:
            return "pyramid"


class Geometry(object):
    def __init__(self):
        self.attributes = {}
        self.vertex_count = None


    @property
    def object_type(self):
        type_name = type(self).__name__
        return type_name

    
    def add_attribute(self, name:str, data:object,datatype:str):
        attribute = Attribute(datatype,data)
        self.attributes[name] = attribute
        
        if name == "vertex_position":
            self.vertex_count = len(data)

    def count_vertices(self):
        attribute = list(self.attributes.values())[0]
        self.vertex_count = len(attribute._data)

    def get_vertex_count(self):
        if self.vertex_count is None:
            self.count_vertices()
            
        return self.vertex_count


    def apply_transform(self,matrix):
        rotational_matrix = np.array([matrix[0][0:3],
                                      matrix[1][0:3],
                                      matrix[2][0:3]])
        
        old_position = self.attributes["vertex_position"]._data
        old_vertex_normal_data = self.attributes["vertex_normal"]._data
        old_face_normal_data = self.attributes["face_normal"]._data
        new_position = []
        new_vertex_normal = []
        new_face_normal = []

        #apply the transformation to all the old positions
        for prev_pos in old_position:
            # get the position of the vertex
            new_pos = prev_pos.copy()
            # transform to vec4 for matrix multiplication
            new_pos.append(1)
            # apply the transformation
            new_pos = matrix @ new_pos
            # remove the last element to get back to vec3
            new_pos = list(new_pos[:3])
            # add the new position to the list
            new_position.append(new_pos)


        # apply transformation to the vertex normals
        for old_normal in old_vertex_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotational_matrix @ new_normal
            new_vertex_normal.append(new_normal)
        

        # apply transformation to the face normals
        for old_normal in old_face_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotational_matrix @ new_normal
            new_face_normal.append(new_normal)

        # update data and upload it
        self.attributes["vertex_position"]._data = new_position
        self.attributes["vertex_normal"]._data = new_vertex_normal
        self.attributes["face_normal"]._data = new_face_normal


        # upload the data to the GPU
        self.attributes["vertex_position"].upload_data()
        self.attributes["vertex_normal"].upload_data()
        self.attributes["face_normal"].upload_data()

        # update the vertex count
        self.vertex_count = len(new_position)

    def merge(self,other_geometry):
        for var_name, attrib_obj in self.attributes.items():
            attrib_obj._data += other_geometry.attributes[var_name]._data
            attrib_obj.upload_data()
        
        self.count_vertices()


    def AA_bounding_box(self):
        # get the min and max values of the vertex positions
        vertex_positions = self.attributes["vertex_position"]._data
        min_x = min(vertex_positions, key=lambda x: x[0])[0]
        max_x = max(vertex_positions, key=lambda x: x[0])[0]
        min_y = min(vertex_positions, key=lambda x: x[1])[1]
        max_y = max(vertex_positions, key=lambda x: x[1])[1]
        min_z = min(vertex_positions, key=lambda x: x[2])[2]
        max_z = max(vertex_positions, key=lambda x: x[2])[2]

        return np.array([[min_x, min_y, min_z], [min_x, min_y, max_z],[min_x,max_y,min_z],\
                [min_x,max_y,max_z],[max_x,min_y,min_z],[max_x,min_y,max_z],\
                [max_x,max_y,min_z],[max_x,max_y,max_z]]).astype(float)
    

    def intersection_test(self, ray, origin, world_matrix):
        """
        Test if the ray intersects with the object
        """
        aa_bbox = self.AA_bounding_box()
   
        # convert aabb to homogeneous coordinates
        aabb = np.array([[aa_bbox[0][0], aa_bbox[0][1], aa_bbox[0][2], 1],
                            [aa_bbox[1][0], aa_bbox[1][1], aa_bbox[1][2], 1],
                            [aa_bbox[2][0], aa_bbox[2][1], aa_bbox[2][2], 1],
                            [aa_bbox[3][0], aa_bbox[3][1], aa_bbox[3][2], 1],
                            [aa_bbox[4][0], aa_bbox[4][1], aa_bbox[4][2], 1],
                            [aa_bbox[5][0], aa_bbox[5][1], aa_bbox[5][2], 1],
                            [aa_bbox[6][0], aa_bbox[6][1], aa_bbox[6][2], 1],
                            [aa_bbox[7][0], aa_bbox[7][1], aa_bbox[7][2], 1]])

        aabb = world_matrix @ aabb.T
        aabb = aabb.T

        bbox_min_x = min(aabb[:,0])
        bbox_max_x = max(aabb[:,0])
        bbox_min_y = min(aabb[:,1])
        bbox_max_y = max(aabb[:,1])
        bbox_min_z = min(aabb[:,2])
        bbox_max_z = max(aabb[:,2])
 
        bbox_min = np.array([bbox_min_x, bbox_min_y, bbox_min_z])
        bbox_max = np.array([bbox_max_x, bbox_max_y, bbox_max_z])
        t_min = []
        t_max = []
        inverse_ray = []

        # Calculate the inverse of the ray
        # used to calculate the t values for each axis without the use of division.
        # reduces the number of divisions by half,
        # and avoids division by zero.
        for i in range(3):
            if abs(ray[i]) < 1e-8:
                inverse_ray.append(float('inf'))
            else:
                inverse_ray.append(1.0 / ray[i])

        for i in range(3):
            if abs(ray[i]) < 1e-8:
                # Ray is parallel to slab. No hit if origin not within slab
                if origin[i] < bbox_min[i] or origin[i] > bbox_max[i]:
                    return None
                else:
                    # Ray is parallel and inside slab, so it always "intersects" this slab
                    t1 = float('-inf')
                    t2 = float('inf')
            else:
                t1 = (bbox_min[i] - origin[i]) * inverse_ray[i]
                t2 = (bbox_max[i] - origin[i]) *  inverse_ray[i]

            t_axis_min = min(t1, t2)
            t_axis_max = max(t1, t2)
            t_min.append(t_axis_min)
            t_max.append(t_axis_max)

        t_enter = max(t_min)
        t_exit = min(t_max)
        
        if t_exit >= max(t_enter, 0):
            return True
    
        return False
    

