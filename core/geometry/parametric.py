from core.geometry.geometry import Geometry
from core.utils.math import Math

class Parametric(Geometry):
    """
    The Parametric class is a base class for creating parametric shapes.
    It inherits from the Geometry class and provides a method to generate
    vertices based on a parametric equation.
    """
    def __init__(self,u_start:float,u_end:float,u_resolution:float,
                 v_start:float,v_end:float,v_resolution:float,surface_functions:object) -> None:
        
        super().__init__()
        # the step values for u and v
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        # array to store the vertices
        positions = []
        # array to store the texture coordinates
        texture_uvs = []
        # array to store the vertex normals
        vertex_normals = []

        # arrays to store the data for the geometry
        texture_uv_data = []
        position_data = []
        color_data = []
        vertex_normal_data = []
        vertex_face_normal_data = []

        # color data
        c1 = [1,0,0]
        c2 = [0,1,1]
        c3 = [0,0,1]
        c4 = [0,1,1]
        c5 = [1,0,1]
        c6 = [1,1,0]

        # generate the vertices of the surface
        # loop through the u and v values to generate the vertices
        for u_index in range(int(u_resolution + 1)):
            # temp arrays to store the vertices, texture coordinates and normals of the surface
            v_array = []
            texture__uv_array = []
            normal_array = []
            for v_index in range(int(v_resolution + 1)):
                # get step values for u and v
                u = u_start + u_index * delta_u
                v = v_start +  v_index * delta_v
                # step size for normal vector calculation
                h = 0.0001 

                # generate the position of the vertex along the surface
                position = surface_functions(u, v)

                # generate positions just above and below the vertex for calculating the normal vector
                p2 = surface_functions(u + h, v)
                p3 = surface_functions(u, v + h)
                # calculate the normal vector using the cross product
                normal_vector = Math.calclulate_normal(position, p2, p3)

                 # generate the texture coordinates
                texture_u = u_index/u_resolution
                texture_v = v_index/v_resolution
               
                #append the normal vector for each vertex all facing the camera
                normal_array.append(normal_vector)

                # add the normal vector for each vertex all facing the camera
                v_array.append(position)

                # add the texture coordinates for each vertex
                texture__uv_array.append([texture_u, texture_v])

            positions.append(v_array)
            texture_uvs.append(texture__uv_array)
            vertex_normals.append(normal_array)
        
        # groups vertices into triangles to draw the surface
        # each square is made of 2 triangles, so we need to group the vertices in 3s
        for i_index in range(int(u_resolution)):
            for j_index in range(int(v_resolution)):
                # The vertices in groups of each square
                p_a = positions[i_index + 0][j_index + 0]
                p_b = positions[i_index + 1][j_index + 0]
                p_c = positions[i_index + 1][j_index + 1]
                p_d = positions[i_index + 0][j_index + 1]
             
                # color data also in groups of each triangle
                color_data += [c1, c2, c3,
                               c4, c5, c6]
                
                # texture coordinates
                t_a = texture_uvs[i_index + 0][j_index + 0]
                t_b = texture_uvs[i_index + 1][j_index + 0]
                t_c = texture_uvs[i_index + 1][j_index + 1]
                t_d = texture_uvs[i_index + 0][j_index + 1]

                # vertex normals vectors
                n_a = vertex_normals[i_index + 0][j_index + 0]
                n_b = vertex_normals[i_index + 1][j_index + 0]
                n_c = vertex_normals[i_index + 1][j_index + 1]
                n_d = vertex_normals[i_index + 0][j_index + 1]

                # calculate the face normal vectors for each triangle
                face_norm_1 = Math.calclulate_normal(p_a, p_b, p_c)
                face_norm_2 = Math.calclulate_normal(p_a, p_c, p_d)

                
                # group the vertices in triangles to draw the square
                position_data += [p_a.copy(), p_b.copy(), p_c.copy(), # first triangle
                                  p_a.copy(), p_c.copy(), p_d.copy()] # second triangle

                # group the texture coordinates in triangles for the square
                texture_uv_data += [t_a.copy(), t_b.copy(), t_c.copy(),
                                    t_a.copy(), t_c.copy(), t_d.copy()]
                
                 # normals for each square in triangles
                vertex_normal_data += [n_a.copy(), n_b.copy(), n_c.copy(),
                                       n_a.copy(), n_c.copy(), n_d.copy()]
                
                # face normals for each square in triangles
                vertex_face_normal_data += [face_norm_1.copy(), face_norm_1.copy(), face_norm_1.copy(),
                                            face_norm_2.copy(), face_norm_2.copy(), face_norm_2.copy()]


        self.add_attribute("vertex_position", position_data, "vec3")
        self.add_attribute("vertex_color", color_data, "vec3")
        self.add_attribute("vertex_uv", texture_uv_data, "vec2")
        self.add_attribute("vertex_normal", vertex_normal_data, "vec3")
        self.add_attribute("face_normal", vertex_face_normal_data, "vec3")
        self.count_vertices()

