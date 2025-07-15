from core.geometry.geometry import Geometry

class Rectangle(Geometry):
    def __init__(self, width: float = 1.0, height: float = 1.0,position:list = [0,0],alignment:list = [0.5,0.5]) -> None:
        super().__init__()
        self.width = width
        self.height = height

        self._create_rectangle(position=position,alignment=alignment,width=width,height=height)


    def _create_rectangle(self,position,alignment,width,height) -> None:
        # position and alignment are 2D vectors
        # position is the center of the rectangle
        # alignment is the point of the rectangle that is aligned to the position
        # alignment is a 2D vector that ranges from 0 to 1
        x, y = position
        a, b = alignment
        
        # vertices
        p0 = [x + (-a) * width, y + (-b) * height, 0]
        p1 = [x + (1 - a) * width, y + (-b) * height, 0]
        p2 = [x + (-a) * width, y + (1 - b) * height, 0]
        p3 = [x + (1 - a) * width, y + (1 - b) * height, 0]

        # vertex colors
        c0  = [1, 1, 1]
        c1 = [1, 0, 0]
        c2 = [0, 1, 0]
        c3 = [0, 0, 1]
        
        # texture coordinates
        t0 = [0, 0] 
        t1 = [1, 0] 
        t2 = [0, 1] 
        t3 = [1, 1]
        
        normal_vector = [0, 0, 1]

        # define the vertices of the rectangle in counter clockwise order:
        # drawing using triangles so we need to define 2 triangles. 
        # Grouped in 3s for 6 total points, two of which are shared
        # so in total we have 4 points 
        position_data = [p0, p1, p3, p0, p3, p2]

        # colors for each vertex
        color_data = [c0, c1, c3, c0, c3, c2]
        # texture coordinates for each vertex
        uv_data = [t0, t1, t3, t0, t3, t2]
        # normals for each vertex
        normal_data = [normal_vector] * 6 


        self.add_attribute("vertex_position", position_data, "vec3")
        self.add_attribute("vertex_color", color_data, "vec3")
        self.add_attribute("vertex_uv", uv_data, "vec2")
        self.add_attribute("vertex_normal", normal_data, "vec3")
        self.add_attribute("face_normal", normal_data, "vec3")
        self.count_vertices()


