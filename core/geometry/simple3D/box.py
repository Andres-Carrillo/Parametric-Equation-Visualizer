from core.geometry.geometry import Geometry

def generate_box_vertices(width=1, height=1, depth=1):
        p0 = [-width / 2, -height / 2, -depth / 2]
        p1 = [width / 2, -height / 2, -depth / 2]
        p2 = [-width / 2, height / 2, -depth / 2]
        p3 = [width / 2, height / 2, -depth / 2]
        p4 = [-width / 2, -height / 2, depth / 2]
        p5 = [width / 2, -height / 2, depth / 2]
        p6 = [-width / 2, height / 2, depth / 2]
        p7 = [width / 2, height / 2, depth / 2]


        position_data = [p5, p1, p3, p5, p3, p7,
                         p0, p4, p6, p0, p6, p2,
                         p6, p7, p3, p6, p3, p2,
                         p0, p1, p5, p0, p5, p4,
                         p4, p5, p7, p4, p7, p6,
                         p1, p0, p2, p1, p2, p3]
        

        return position_data

class BoxGeometry(Geometry):
    def __init__(self, width=2, height=2, depth=1):
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth

        # colors for faces in order:
        c1, c2 = [1, 0.5, 0.5], [0.5, 0, 0]
        c3, c4 = [0.5, 1, 0.5], [0, 0.5, 0]
        c5, c6 = [0.5, 0.5, 1], [0, 0, 0.5]

        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        # aligning the texture coordinates to the faces
        uv_data = [t0,t1,t3  , t0,t3,t2] * 6 #

        position_data = generate_box_vertices(width,height,depth)

        # colors for each vertex
        # each face has 6 vertices, so we need to repeat the colors
        color_data = [c1] * 6 + [c2] * 6 + [c3] * 6 + [c4] * 6 + [c5] * 6 + [c6] * 6

        #normals facing each direction
        # each face has 6 vertices, so we need to repeat the normals
        n1 = [1,0,0]
        n2 = [-1,0,0]
        n3 = [0,1,0]
        n4 = [0,-1,0]
        n5 = [0,0,1]
        n6 = [0,0,-1]

        normal_data = [n1] * 6 + [n2] * 6 + [n3] * 6 + [n4] * 6 + [n5] * 6 + [n6] * 6
        
        self.add_attribute( "vertex_position", position_data,"vec3")
        self.add_attribute( "vertex_color", color_data,"vec3")
        self.add_attribute( "vertex_uv", uv_data,"vec2")
        self.add_attribute( "vertex_normal", normal_data,"vec3")
        self.add_attribute( "face_normal", normal_data,"vec3")

        self.count_vertices()
