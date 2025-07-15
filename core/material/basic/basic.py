from core.material.basic.material import Material

class BasicMaterial(Material):

    def __init__(self,vertex_shader_code = None, fragment_shader_code = None,
                 use_vertex_colors = True) -> None:
        

        if vertex_shader_code is None:
            vertex_shader_code = """
    uniform mat4 projection_matrix;
    uniform mat4 view_matrix;
    uniform mat4 model_matrix;
    in vec3 vertex_position;
    in vec3 vertex_color;
    out vec3 color;

    void main(){
        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
        color = vertex_color;
    }
                                """
        if fragment_shader_code is None:
            fragment_shader_code = """
    uniform vec3 base_color;
    uniform bool use_vertex_colors;
    in vec3 color;
    out vec4 frag_color;
                                
    void main(){
        frag_color = vec4(base_color,1.0);
                                    
        if (use_vertex_colors)
        {
            frag_color = vec4(color,1.0);
        }

                          
    }
                """

        super().__init__(vertex_shader_code, fragment_shader_code)
        
        self.add_uniform("base_color", (1.0, 1.0, 1.0), "vec3")
        
       
        self.add_uniform("use_vertex_colors", use_vertex_colors, "bool")

        self.locate_uniforms()
