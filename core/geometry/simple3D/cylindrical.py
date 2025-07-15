from core.geometry.parametric import Parametric
from core.geometry.simple2D.polygon import Polygon
from core.utils.matrix import Matrix
from math import pi, sin, cos

class Cylindrical(Parametric):
    def __init__(self,top_radius:float = 1.0,bot_radius:float = 1.0,height:float = 1.0,
                 seg_radius:float=32.0,seg_height:float=4,top_closed=True,bot_closed=True) -> None:
        
        def parametric_equation(u:float,v:float):
            x = (v*top_radius + (1-v)*bot_radius) * sin(u)
            y = height*(v-0.5)
            z = (v*top_radius + (1-v)*bot_radius) * cos(u)
            return [x,y,z]
        
        super().__init__(0,2*pi,seg_radius,0,1,seg_height,parametric_equation)

        if top_closed:
            #create a polygon for the top that matches the shape of the cylinder
            top_geometry = Polygon(radius=top_radius, sides=seg_radius)

            #transformation to position the polygon at the top of the cylindrical
            transform = Matrix.mat4_translation(0, height/2, 0) @ Matrix.mat4_rotate_y(-pi/2) @ Matrix.mat4_rotate_x(-pi/2)
            top_geometry.apply_transform(transform)

            self.merge(top_geometry)

        if bot_closed:
            bot_geometry = Polygon(radius=bot_radius, sides=seg_radius)

            transform = Matrix.mat4_translation(0, -height/2, 0) @ Matrix.mat4_rotate_y(-pi/2) @ Matrix.mat4_rotate_x(-pi/2)
            bot_geometry.apply_transform(transform)

            self.merge(bot_geometry)

            
        
