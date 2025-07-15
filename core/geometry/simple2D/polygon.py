from core.geometry.geometry import Geometry
from math import sin,cos,pi

class Polygon(Geometry):
    def __init__(self, radius: float = 1, sides: int = 3) -> None:
        super().__init__()
        self.radius = radius
        self.sides = int(sides)
        self._create_polygon()

    def _create_polygon(self):
        area = 2*pi/self.sides
        positions = []
        colors = []
        uv_data = []
        normal_data = []
        normal_vector = [0,0,1]
        uv_center = [0.5,0.5]

        for i in range(self.sides):
            # generate 3 points for each triangle of the polygon
            # the first point is always the center of the polygon
            positions.append([0,0,0])
            positions.append([self.radius*cos(i*area),self.radius*sin(i*area),0])
            positions.append([self.radius*cos((i+1)*area),self.radius*sin((i+1)*area),0])

            # generate colors for each vertex
            colors.append([1,1,1])
            colors.append([1,0,0])
            colors.append([0,0,1])

            # generate uv coordinates for each vertex
            uv_data.append(uv_center)
            uv_data.append([cos(i*area)*0.5 + 0.5, sin(i*area)*0.5 + 0.5])
            uv_data.append([cos((i+1)*area)*0.5 + 0.5, sin((i+1)*area)*0.5 + 0.5])

            # add the normal vector for each vertex all facing the camera
            # since the polygon is flat, we can use the same normal vector for all vertices
            # but we need to repeat it for each vertex
            normal_data.append(normal_vector)
            normal_data.append(normal_vector)
            normal_data.append(normal_vector)

        # add the attributes to the geometry
        self.add_attribute("vertex_position", positions, "vec3")
        self.add_attribute("vertex_color", colors, "vec3")
        self.add_attribute("vertex_uv", uv_data, "vec2")
        self.add_attribute("vertex_normal", normal_data, "vec3")
        self.add_attribute("face_normal", normal_data, "vec3")
        
        # count the vertices
        self.count_vertices()