from meshes.mesh import Mesh
from geometry.geometry import Geometry
from material.basic.line import LineMaterial

class AxesAid(Mesh):
    def __init__(self,axis_len:int =1,line_width =4,axix_colors=[[1,0,0],[0,1,0],[0,0,1]]):
        geo = Geometry()

        position_data = [[0,0,0],[axis_len,0,0],
                         [0,0,0],[0,axis_len,0],
                         [0,0,0],[0,0,axis_len]]
        
        color_data = [axix_colors[0],axix_colors[0],
                        axix_colors[1],axix_colors[1],
                        axix_colors[2],axix_colors[2]]
        
        geo.add_attribute("vertex_position",position_data,"vec3")
        geo.add_attribute("vertex_color",color_data,"vec3")

        geo.count_vertices()

        mat = LineMaterial({
            "use_vertex_colors":True,
            "line_width":line_width,
            "line_type":"segments"
        })

        super().__init__(geo,mat)