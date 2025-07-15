from core.material.basic.material import Material
from core.textures.texture import Texture
import OpenGL.GL as gl

class Sprite(Material):
    def __init__(self,texture:Texture,properties = {}) -> None:
        vertex_shader_code = """
                            uniform mat4 projection_matrix;
                            uniform mat4 view_matrix;
                            uniform mat4 model_matrix;
                            uniform bool billboard;
                            uniform float tile_number;
                            uniform vec2 tile_count;
                            in vec3 vertex_position;
                            in vec2 vertex_uv;
                            out vec2 uv;
                            
                            void main(){
                                mat4 mv_matrix = view_matrix * model_matrix;
                                if (billboard){
                                    mv_matrix[0][0] = 1.0;
                                    mv_matrix[0][1] = 0.0;
                                    mv_matrix[0][2] = 0.0;
                                    mv_matrix[1][0] = 0.0;
                                    mv_matrix[1][1] = 1.0;
                                    mv_matrix[1][2] = 0.0;
                                    mv_matrix[2][0] = 0.0;
                                    mv_matrix[2][1] = 0.0;
                                    mv_matrix[2][2] = 1.0;
                                }

                                gl_Position = projection_matrix * mv_matrix * vec4(vertex_position,1.0);
                                uv = vertex_uv;

                                if (tile_number > -1.0){
                                    vec2 tile_size = 1.0 / tile_count;
                                    float column_index = mod(tile_number,tile_count[0]);
                                    float row_index = floor(tile_number/tile_count[0]);

                                    vec2 tile_offset = vec2(column_index/tile_count[0], 1.0 - (row_index + 1.0)/tile_count[1]);
                                    
                                    uv = uv * tile_size + tile_offset;
                                }                        
                            }
                            """
        fragment_shader_code = """
                             uniform vec3 base_color;
                             uniform sampler2D texture;
                             in vec2 uv;
                             out vec4 frag_color;

                             void main(){
                                vec4 color = vec4(base_color,1.0) * texture2D(texture, uv);

                                if (color.a < 0.1)
                                    discard;

                                frag_color = color;
                             }            

                            """
        

        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("base_color",[1.0,1.0,1.0],"vec3")
        self.add_uniform("texture",[texture.texture_reference,1],"sampler2D")
        self.add_uniform("billboard",True,"bool")
        self.add_uniform("tile_number",-1.0,"float")
        self.add_uniform("tile_count",[1.0,1.0],"vec2")
        self.locate_uniforms()

        # rendering properties
        self.settings['double_sided'] = True
        self.set_properties(properties)



    def update_render_settings(self):

        if self.settings['double_sided']:
            gl.glDisable(gl.GL_CULL_FACE)
        else:
            gl.glEnable(gl.GL_CULL_FACE)
            gl.glCullFace(gl.GL_BACK)





