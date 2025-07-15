from core.meshes.mesh import Mesh
from core.geometry.geometry import Geometry
from core.material.basic.line import LineMaterial

class GridTool(Mesh):
    def __init__(self,size:int =10, division:int = 10,grid_color:list = [0,0,0],center_color = [0.5,0.5,0.5],line_width=1):
        geo = Geometry()

        position_data = []
        color_data = []

        delta_size = size/division
        values = []
        # calculate the values for the grid lines
        for n in range(division+1):
            values.append(-size/2 + n*delta_size)


        # add the vertical and colors for the grid lines
        for x in values:
            position_data.append([x,-size/2,0])
            position_data.append([x,size/2,0])

            if x == 0:
                color_data.append(center_color)
                color_data.append(center_color)

            else:
                color_data.append(grid_color)
                color_data.append(grid_color)


        # add the horizontal lines and colors for the grid lines
        for y in values:
            position_data.append([-size/2,y,0])
            position_data.append([size/2,y,0])

            if y == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)


        geo.add_attribute("vertex_position",position_data,"vec3")
        geo.add_attribute("vertex_color",color_data,"vec3")
        geo.count_vertices()

        mat = LineMaterial({
            "use_vertex_colors":True,
            "line_width":line_width,
            "line_type":"segments"
        })


        super().__init__(geo,mat)   





        

