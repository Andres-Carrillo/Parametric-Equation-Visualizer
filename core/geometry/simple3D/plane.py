from core.geometry.parametric import Parametric

class Plane(Parametric):

    def __init__(self,width:float = 1.0,height:float = 1.0,seg_width:int = 8, seg_height:int = 8) -> None:
        
        def parametric_equation(u:float,v:float) -> tuple[float,float,float]:
            x = u 
            y = v 
            z = 0.0
            return [x,y,z]
        

        super().__init__(-width/2,width/2,seg_width,
                         -height/2,height/2,seg_height,parametric_equation)