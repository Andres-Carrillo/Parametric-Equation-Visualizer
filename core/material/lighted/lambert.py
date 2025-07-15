from core.material.lighted.light import LightMaterial
from core.textures.texture import Texture
from core.shaders.shaders import Shader
from core.glsl.utils import generate_light_uniform_list,generate_light_sum
import OpenGL.GL as gl

class LambertMaterial(LightMaterial):
    def __init__(self,texture:Texture=None,noise:Texture= None,bump_texture:Texture=None,
                  properties:dict={},number_of_lights:int = 0,use_shadow:bool = False) -> None:
        vertex_shader_code =   """
            uniform mat4 projection_matrix;
            uniform mat4 view_matrix;
            uniform mat4 model_matrix;
            in vec3 vertex_position;
            in vec2 vertex_uv;
            in vec3 vertex_normal;
            out vec3 position;
            out vec2 uv;
            out vec3 normal;
            
            struct Shadow
            {
                // direction of light that casts shadow
                vec3 light_dir;
                // data from camera that produces depth texture
                mat4 projection_matrix;
                mat4 view_matrix;
                // texture that stores depth values from shadow camera
                sampler2D depth_map;
                // regions in shadow multiplied by (1-strength)
                float strength;
                // reduces unwanted visual artifacts
                float bias;
            };
            
            uniform bool use_shadow;
            uniform Shadow shadow_obj;
            out vec3 shadow_pos;

            void main()
            {
                gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position, 1);
                position = vec3(model_matrix * vec4(vertex_position, 1));
                uv = vertex_uv;
                normal = normalize(mat3(model_matrix) * vertex_normal);
                
                if (use_shadow)
                {
                    vec4 temp0 = shadow_obj.projection_matrix * shadow_obj.view_matrix * model_matrix * vec4(vertex_position, 1);
                    shadow_pos = vec3(temp0);
                }            
            }
        """

        fragment_shader_code =  Shader.moving_distortion_shader()  + Shader.shadow_struct()  + Shader.shadow_functions()+ Shader.light_struct() + """
                                           vec3 calculate_light(Light light, vec3 pointPosition, vec3 pointNormal)
                                            {
                                                float ambient = 0;
                                                float diffuse = 0;
                                                float specular = 0;
                                                float attenuation = 1;
                                                vec3 lightDirection = vec3(0, 0, 0);

                                                if (light.light_type == 0)  // ambient light
                                                {
                                                    ambient = 1;
                                                }                
                                                else if (light.light_type == 1)  // directional light
                                                {
                                                    lightDirection = normalize(light.direction);
                                                }
                                                else if (light.light_type == 2)  // point light 
                                                {
                                                    lightDirection = normalize(pointPosition - light.position);
                                                    float distance = length(light.position - pointPosition);
                                                    attenuation = 1.0 / (light.attenuation[0] 
                                                                       + light.attenuation[1] * distance 
                                                                       + light.attenuation[2] * distance * distance);
                                                }

                                                if (light.light_type > 0)  // directional or point light
                                                {
                                                    pointNormal = normalize(pointNormal);
                                                    diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                                                    diffuse *= attenuation;
                                                }
                                                return light.color * (ambient + diffuse + specular);
                                            }

                             """ + generate_light_uniform_list(number_of_lights)  + """
                                uniform bool use_shadow;
                                uniform Shadow shadow_obj;
                                uniform vec3 base_color;
                                uniform bool use_texture;
                                uniform bool using_lights;
                                uniform sampler2D texture_sampler;
                                uniform bool use_bump_texture;
                                uniform sampler2D bump_texture;
                                uniform float bump_strength;
                                in vec2 uv;
                                in vec3 normal;
                                in vec3 position;
                                in vec3 shadow_pos;
                                out vec4 frag_color;

                                void main()
                                {
                                    // set the color to the base color with full alpha
                                    vec4 color = vec4(base_color,1.0);

                                    // normal to be used for lighting calculations
                                    vec3 calculated_normal = normal;
                                    
                                    // if texture is used, use the texture color
                                    if (apply_moving_distortion)
                                    {
                                        color *= time_distort(uv,uv_offset,distortion_strength, time, noise, texture_sampler);
                                    }
                                    
                                    if (use_texture)
                                    {
                                        color *= texture(texture_sampler,uv);
                                    }

                                    if (use_bump_texture)
                                    {
                                        calculated_normal += bump_strength * vec3(texture2D(bump_texture,uv));
                                    }

                                    
                                    
                                    if (using_lights)
                                    {
                                        // calculate the lighting effect
                                        vec3 light = vec3(0.0,0.0,0.0);
                                        """ + generate_light_sum(number_of_lights) + """ \n """ + """

                                    
                                        // apply lighting to color
                                        color *= vec4(light,1.0);
                                    }

                                    // shadow calculations
                                    if (use_shadow)
                                    {
                                        color = shadow_calculation(color,normal,shadow_obj,shadow_pos);
                                        
                                    }

                                    // set the fragment color
                                    frag_color = color;
                                }
                                """
        
        # handles creating the shader program and linking the shaders to the program
        # also handles setting up light uniforms based on the number of lights
        super().__init__(number_of_lights,vertex_shader_code,fragment_shader_code)

        # counter to keep track of the number of textures used
        texture_counter = 1

        self.add_uniform("base_color", [1.0, 1.0, 1.0], "vec3")
        if texture is None:
            self.add_uniform("use_texture", False, "bool")
        else:
            self.add_uniform("use_texture", True, "bool")
            self.add_uniform("texture_sampler", [texture.texture_reference,texture_counter], "sampler2D")
            texture_counter += 1

         # check for noise texture
        if noise is not None:
            self.add_uniform("apply_moving_distortion", True, "bool")
            self.add_uniform("noise", [noise.texture_reference, texture_counter], "sampler2D")
            self.add_uniform("time", 0.0, "float")
            self.add_uniform("uv_offset", [0.3,0.07], "vec2")
            self.add_uniform("distortion_strength", 0.02, "float")
            texture_counter += 1
        else:
            self.add_uniform("apply_moving_distortion", False, "bool")


        if bump_texture is None:
            self.add_uniform("use_bump_texture", False, "bool")
        else:
            self.add_uniform("use_bump_texture", True, "bool")
            self.add_uniform("bump_texture", [bump_texture.texture_reference,texture_counter], "sampler2D")
            self.add_uniform("bump_strength", 1.0, "float")
            


        # check for shadow
        if use_shadow:
            self.add_uniform("use_shadow", True, "bool")
            self.add_uniform("shadow_obj", None, "Shadow")
        else:
            self.add_uniform("use_shadow", False, "bool")


        self.locate_uniforms()

        self.settings['double_sided'] = True
        self.settings['wire_frame'] = False
        self.settings['line_width'] = 1.0

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