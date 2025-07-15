from core.material.basic.basic import BasicMaterial
import OpenGL.GL as gl

class SurfaceMaterial(BasicMaterial):
    def __init__(self,vertex_shader:str = None,fragment_shader:str = None,properties:dict = {}) -> None:
        super().__init__(vertex_shader, fragment_shader)

        self.settings["draw_mode"] = gl.GL_TRIANGLES
        self.settings["double_sided"] = False
        self.settings["wire_frame"] = False
        self.settings['line_width'] = 1.0
        
        self.set_properties(properties)


    def update_render_settings(self) -> None:
        if self.settings["double_sided"]:
            gl.glDisable(gl.GL_CULL_FACE)
        else:
            gl.glEnable(gl.GL_CULL_FACE)

        if self.settings["wire_frame"]:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        gl.glLineWidth(self.settings["line_width"])