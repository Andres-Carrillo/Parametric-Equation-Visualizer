from core.material.basic.basic import BasicMaterial
import OpenGL.GL as gl

class LineMaterial(BasicMaterial):
    def __init__(self,properties: dict = {}) -> None:
        super().__init__()

        self.settings["draw_mode"] = gl.GL_LINE_STRIP

        self.settings["line_width"] = 1.0

        self.settings["line_type"] = "connected"

        self.set_properties(properties)


    def update_render_settings(self) -> None:
        gl.glLineWidth(self.settings["line_width"])

        if self.settings["line_type"] == "connected":
            self.settings["draw_mode"] = gl.GL_LINE_STRIP

        elif self.settings["line_type"] == "loop":
            self.settings["draw_mode"] = gl.GL_LINE_LOOP

        elif self.settings["line_type"] == "segments":
            self.settings["draw_mode"] = gl.GL_LINES
        else:
            raise RuntimeError(f"Line type {self.settings['line_type']} not supported")
