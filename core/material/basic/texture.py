from core.material.basic.material import Material
from core.textures.texture import Texture
import OpenGL.GL as gl

class TextureMaterial(Material):

    def __init__(self,texture:Texture,properties:dict={}) -> None:
        vertex_shader_code = """
                                uniform mat4 projection_matrix;
                                uniform mat4 view_matrix;
                                uniform mat4 model_matrix;
                                in vec3 vertex_position;
                                in vec2 vertex_uv;
                                uniform vec2 repeat_uv;
                                uniform vec2 offset_uv;
                                out vec2 uv;
                                
                                void main(){
                                    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                                    uv = vertex_uv * repeat_uv + offset_uv;
                                }
                             """
        
        fragment_shader_code = """
                                uniform vec3 base_color;
                                uniform sampler2D texture;
                                in vec2 uv;
                                out vec4 frag_color;

                                void main(){
                                    vec4 color = vec4(base_color,1.0) * texture2D(texture, uv);

                                    if (color.a < 0.10)
                                        discard;

                                    frag_color = color;
                                }
                               """
        
        super().__init__(vertex_shader_code, fragment_shader_code)
        
        # add uniform variables
        self.add_uniform("base_color",[1.0,1.0,1.0],"vec3")
        self.add_uniform("texture",[texture.texture_reference,1],"sampler2D")
        self.add_uniform("repeat_uv",[1.0,1.0],"vec2")
        self.add_uniform("offset_uv",[0.0,0.0],"vec2")
    
        self.locate_uniforms()

        # initialize the settings
        self.settings["double_sided"] = True
        self.settings["wire_frame"] = False
        self.settings["line_width"] = 1.0

        # set the properties
        self.set_properties(properties)


    def update_render_settings(self):
        if self.settings["double_sided"]:
            gl.glDisable(gl.GL_CULL_FACE)
        else:
            gl.glEnable(gl.GL_CULL_FACE)

        if self.settings["wire_frame"]:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        gl.glLineWidth(self.settings["line_width"])