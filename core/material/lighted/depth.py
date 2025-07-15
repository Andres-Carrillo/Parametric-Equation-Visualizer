from core.material.basic.material import Material

class DepthMaterial(Material):

    def __init__(self):
        vertex_shader_code = """
                               
                                uniform mat4 projection_matrix;
                                uniform mat4 view_matrix;
                                uniform mat4 model_matrix;
                                in vec3 vertex_position;

                                void main(){
                                    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1);
                                }
                                """
        
        
        fragment_shader_code = """
                                out vec4 frag_color;

                                void main(){
                                    float depth = gl_FragCoord.z;
                                    frag_color = vec4(depth,depth,depth,1.0);
                                }



                """

        super().__init__(vertex_shader_code,fragment_shader_code)

        self.locate_uniforms()