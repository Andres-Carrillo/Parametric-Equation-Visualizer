from core.material.lighted.light import LightMaterial
from core.textures.texture import Texture
from core.shaders.shaders import Shader
from core.glsl.utils import generate_light_sum,generate_light_uniform_list
import OpenGL.GL as gl

class PhongMaterial(LightMaterial):
    def __init__(self,texture:Texture=None,noise:Texture = None,bump_texture:Texture = None,
                  properties:dict={},number_of_lights:int = 0,use_shadow=False) -> None:
        vertex_shader_code =  Shader.shadow_struct() + Shader.shadow_enabled_vertex_shader() 
        
        
        # the lamber model calculates the lighting effect inside the fragment shader
        fragment_shader_code = Shader.moving_distortion_shader() + Shader.shadow_struct() + Shader.shadow_functions() + """
                                // variables used for the phong model:
                                uniform vec3 view_position;
                                uniform float specular_strength;
                                uniform float shininess; """ + Shader.light_struct() + """

                                vec3 calculate_light(Light light, vec3 point_pos,vec3 point_normal)
                                {
                                    float ambient = 0.0;
                                    float diffuse = 0.0;
                                    float specular = 0.0;
                                    float attenuation = 1.0;
                                    vec3 light_dir = vec3(0.0,0.0,0.0);

                                    // ========= setup variables based on type of light =========:
                                        // ambient light:
                                    if (light.light_type == 0){ 
                                        ambient = 1.0;
                                    }   // directional light:
                                    else if (light.light_type == 1){ 
                                        light_dir = normalize(light.direction);
                                    }   // point light:
                                    else if (light.light_type == 2){ 
                                        light_dir = normalize(point_pos - light.position);
                                        float distance = length(light.position - point_pos);
                                        attenuation = 1.0 / (light.attenuation[0] + 
                                                                light.attenuation[1] * distance +
                                                                    light.attenuation[2] * distance * distance);
                                    }

                                    // ========= calculate the diffuse  values for directional and point lights =========:
                                    if (light.light_type > 0){
                                        point_normal = normalize(point_normal);
                                        diffuse = max(dot(point_normal, -light_dir), 0.0);
                                        diffuse = diffuse * attenuation;
                                    }

                                    // ========= calculate the specular values for directional and point lights =========:
                                    if (diffuse > 0.0){
                                        vec3 view_dir = normalize(view_position - point_pos);
                                        vec3 reflect_dir = reflect(light_dir, point_normal);
                                        specular = max(dot(view_dir,reflect_dir), 0.0);
                                        specular = specular_strength * pow(specular, shininess);
                                    }

                                    return light.color * (ambient + diffuse + specular);
                                }
                             """ + generate_light_uniform_list(number_of_lights) + """ \n """ + """
                                uniform vec3 base_color;
                                uniform bool use_texture;
                                uniform bool use_bump_texture;
                                uniform bool use_shadow;
                                uniform bool using_lights;
                                uniform sampler2D texture_sampler;
                                uniform sampler2D bump_texture;
                                uniform float bump_strength;
                                uniform Shadow shadow_obj;
                                in vec2 uv;
                                in vec3 normal;
                                in vec3 position;
                                in vec3 shadow_pos;
                                out vec4 frag_color;
                                
                                void main()
                                {
                                    // set the color to the base color with full alpha
                                    vec4 color = vec4(base_color,1.0);

                                    // normal used for lighting calculations
                                    vec3 calculated_normal = normal;
                                    
                                  // if texture is used, use the texture color
                                    if (apply_moving_distortion)
                                    {
                                        color *= time_distort(uv,uv_offset,distortion_strength, time, noise, texture_sampler);
                                    }
                                    else if (use_texture)
                                    {
                                        color *= texture(texture_sampler,uv);
                                    }

                                    // if bump texture is used, use the bump texture color
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
                                    
                                    if (use_shadow)
                                    {
                                       
                                        // determine if surface is facing towards light direction
                                        float cosAngle = dot(normalize(normal), -normalize(shadow_obj.light_dir));
                                        bool facingLight = (cosAngle > 0.01);
                                        // convert range [-1, 1] to range [0, 1]
                                        // for UV coordinate and depth information
                                        vec3 shadowCoord = (shadow_pos.xyz + 1.0) / 2.0;
                                        float closestDistanceToLight = texture(shadow_obj.depth_map, shadowCoord.xy).r;
                                        float fragmentDistanceToLight = clamp(shadowCoord.z, 0, 1);
                                        // determine if fragment lies in shadow of another object
                                        bool inShadow = (fragmentDistanceToLight > closestDistanceToLight + shadow_obj.bias);
                                        if (facingLight && inShadow)
                                        {
                                            float s = 1.0 - shadow_obj.strength;
                                            color *= vec4(s, s, s, 1);
                                        }
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

        if noise is not None:
            self.add_uniform("apply_moving_distortion", True, "bool")
            self.add_uniform("noise", [noise.texture_reference, texture_counter], "sampler2D")
            self.add_uniform("time", 0.0, "float")
            self.add_uniform("uv_offset", [0.3,0.07], "vec2")
            self.add_uniform("distortion_strength", 0.02, "float")
            texture_counter += 1
        else:
            self.add_uniform("apply_moving_distortion", False, "bool")

        if bump_texture is not None:
            self.add_uniform("use_bump_texture", True, "bool")
            self.add_uniform("bump_texture", [bump_texture.texture_reference, texture_counter], "sampler2D")
            self.add_uniform("bump_strength", 1.0, "float")
            texture_counter += 1
    

        # check for shadow
        if use_shadow:
            self.add_uniform("use_shadow", True, "bool")
            self.add_uniform("shadow_obj", None, "Shadow")
            # self.add_uniform("shadow_pos", [0.0,0.0,0.0], "vec3")
        else:
            self.add_uniform("use_shadow", False, "bool")

            
        self.add_uniform("view_position", [0.0, 0.0, 0.0], "vec3")
        self.add_uniform("specular_strength", 1.0, "float")
        self.add_uniform("shininess", 32.0, "float")

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