from core.material.basic.basic import BasicMaterial
import OpenGL.GL as gl

class PointMaterial(BasicMaterial):
    def __init__(self,properties:dict = {}) ->None:
        super().__init__()

        self.settings["draw_mode"] = gl.GL_POINTS
        self.settings["point_size"] = 8.0
        # self.settings["rounded_points"] = False 


        self.set_properties(properties)


    def update_render_settings(self)->None:
        gl.glPointSize(self.settings["point_size"])

             