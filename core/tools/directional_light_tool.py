from core.tools.grid import GridTool
from core.light.directional import DirectionalLight

class DirectionalLightTool(GridTool):

    def __init__(self,directional_light:DirectionalLight) -> None:
        color = directional_light.color
        super().__init__(size=1,division=1,grid_color=color,center_color=[1,1,1])

        # add a vector pointing in the direction of the light
        self.geometry.attributes["vertex_position"]._data += [[0,0,0],[0,0,-self.direction[2]]]
        self.geometry.attributes["vertex_position"]._data += [[0,0,0],[0,0,self.direction[2]]]
        self.geometry.attributes["vertex_color"]._data += [color,color]

        self.geometry.attributes["vertex_position"].upload_data()
        self.geometry.attributes["vertex_color"].upload_data()
        self.geometry.count_vertices()
