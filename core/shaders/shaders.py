class Shader(object):

    @staticmethod
    def basic_vertex_shader() -> str:
        return """
                    uniform mat4 projection_matrix;
                    uniform mat4 view_matrix;
                    uniform mat4 model_matrix;
                    in vec3 vertex_position;
                    in vec3 vertex_normal;
                    in vec2 vertex_uv;
                    out vec2 uv;
                    out vec3 normal;
                    out vec3 position;

                    void main(){
                        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                        uv  = vertex_uv;
                            position = vec3(model_matrix * vec4(vertex_position, 1));
                        normal = normalize(mat3(model_matrix) * vertex_normal);
                    }\n
                """
    

    @staticmethod
    def basic_fragment_shader() -> str:
        return """
                                uniform vec3 base_color;
                                uniform bool use_texture;
                                uniform sampler2D texture_sampler;
                                in vec2 uv;
                                out vec4 frag_color;
                                void main(){
                                    // set the color to the base color with full alpha
                                    vec4 color = vec4(base_color,1.0);
                                    
                                    // if texture is used, use the texture color
                                    if (use_texture){
                                        color *= texture(texture_sampler,uv);
                                    }
                                    // set the fragment color
                                    frag_color = color;
                                }\n
                """
    

    @staticmethod
    def random_number_generator() -> str:
        return """
                                float random(vec2 uv){
                                    return fract(235711.0 * sin(14.337 *uv.x + 42.428 * uv.y));
                                }


                                float box_random(vec2 uv, float scale){
                                    vec2 uv_scaled = floor(uv * scale);
                                    return random(uv_scaled);
                                }

                                float smooth_random(vec2 uv, float scale){
                                    vec2 integer_part = floor(uv * scale);
                                    vec2 fractional_part = fract(uv * scale);

                                    float a = random(integer_part);
                                    float b = random(integer_part + vec2(1.0, 0.0));
                                    float c = random(integer_part + vec2(0.0, 1.0));
                                    float d = random(integer_part + vec2(1.0, 1.0));

                                    return mix(
                                                mix(a, b, fractional_part.x),
                                                mix(c, d, fractional_part.x),
                                                fractional_part.y);
                                }


                                float fractal_random(vec2 uv, float scale){
                                    float val = 0.0;
                                    float amp = 0.5;

                                    for (int i = 0; i < 6; i++){
                                        val += amp * smooth_random(uv, scale);
                                        scale *= 2.0;
                                        amp *= 0.5;
                                    }

                                    return val;
                                
                                }\n
                """

    @staticmethod
    def procedural_shaders() -> str:
        return    Shader.random_number_generator() + \
                    """
                        // cloud generator
                        vec4 cloud_gen(vec2 uv, float scale){
                            float r = fractal_random(uv, scale);
                            vec4 color1 = vec4(0.5,0.7,1.0,1.0);
                            vec4 color2 = vec4(1.0,1.0,1.0,1.0);
                            
                            return mix(color1, color2, r);
                        }

                        // lava generator
                        vec4 lava_gen(vec2 uv, float scale){
                            float r = fractal_random(uv, scale);
                            vec4 color1 = vec4(1.0,0.8,0.0,1.0);
                            vec4 color2 = vec4(0.8,0.0,0.0,1.0);

                            return mix(color1, color2, r);  
                        }

                        // marble generator
                        vec4 marble_gen(vec2 uv, float scale){
                            float t = fractal_random(uv, scale);
                            float r = abs(sin(20*t));
                            
                            vec4 color1 = vec4(0.0,0.2,0.0,1.0);
                            vec4 color2 = vec4(1.0,1.0,1.0,1.0);

                            return mix(color1,color2,r);
                        }

                        //wood grain generator
                        vec4 grain_gen(vec2 uv, float scale){
                            float t = 80 * uv.y + 20 * fractal_random(uv, scale);
                            float r = clamp(2 * abs(sin(t)),0,1);
                            vec4 color1 = vec4(0.3,0.2,0.0,1.0);
                            vec4 color2 = vec4(0.6,0.4,0.2,1.0);

                            return mix(color1,color2,r);
                        }\n
                """


    @staticmethod
    def moving_distortion_shader() -> str:
         
         return """
                                // ======= TIME BASED DISTORTION SHADER  =======
                                //      Samples noise from a texture and applies distoration to the image texture  
                                //      The distortion is time based. This results in a moving distortion effect
                                // variables:
                                //      uv: the texture coordinates of the fragment
                                //      time: the time value to distort the image
                                //      noise: the noise texture to sample from
                                //      image: the image texture to distort
                                // required uniforms:
                                //      noise: the noise texture to sample from
                                //      time: the delta_time value to distort the image
                                
                                uniform sampler2D noise;
                                uniform float time;
                                uniform vec2 uv_offset;
                                uniform float distortion_strength;
                                uniform  bool apply_moving_distortion; // bool is used in main to check if distortion is applied

                                vec4 time_distort(vec2 uv,vec2 uv_offset,float distortion_strength, 
                                                            float time,sampler2D noise, sampler2D texture_sampler)
                                {
                                    vec2 uv_shift = uv + uv_offset * time;
                                    vec4 noise_vals = texture2D(noise, uv_shift);
                                    vec2 uv_noise = uv + distortion_strength * noise_vals.rg;
                                    return texture2D(texture_sampler, uv_noise);
                                };\n
        """
    
    @staticmethod
    def light_struct()->str:
        return """
                                // ========= Base Light Struct =========:
                                struct Light
                                {
                                    int light_type;
                                    vec3 color;
                                    vec3 direction;
                                    vec3 position;
                                    vec3 attenuation;
                                };\n
        """
    
    @staticmethod
    def shadow_struct()->str:
        return """
                                // ========= Base Shadow Struct =========:
                                struct Shadow
                                {
                                    //direction of light casting shadow
                                    vec3 light_dir;

                                    //camera data that produces the depth map
                                    mat4 projection_matrix;
                                    
                                    mat4 view_matrix;

                                    //texture that store depth values of the shadow map from the light's perspective
                                    sampler2D depth_map;

                                    // strength of the shadow
                                    float strength;

                                    // reduces artifacts in the shadow
                                    float bias;
                                };
                                
                                \n
        """
    

    @staticmethod
    def shadow_functions()->str:
        return """
                                // ========= Shadow Functions =========:
                                // apply shadow to the color if the fragment is in shadow and facing the light
                                // color: the original color of the fragment
                                // normal: the normal vector of the fragment
                                // shadow_obj: the shadow object containing the light direction, 
                                //             projection matrix, view matrix, depth map, shadow 
                                //             strength and bias.
                                // shadow_pos: the position of the fragment in world space
                                // returns: the color of the fragment with shadow applied

                                vec4 shadow_calculation(vec4 color,vec3 normal,Shadow shadow_obj,vec3 shadow_pos)
                                {
                                    // get the angle between the normal and the light direction
                                    float cos_angle = dot(normalize(normal),-normalize(shadow_obj.light_dir));

                                    // determine if the normal is facing the light
                                    bool is_facing_light = (cos_angle > 0.01);

                                    // convert range from [-1,1] to [0,1]
                                    // for uv and depth map
                                    vec3 shadow_coord = (shadow_pos.xyz + 1.0) / 2.0;

                                    // get the closest depth value from the shadow map
                                    float closest_depth = texture(shadow_obj.depth_map,shadow_coord.xy).r;

                                    // get the current depth value
                                    float fragment_depth = clamp(shadow_coord.z,0.0,1.0);

                                    // is fragment in shadow of another object
                                    bool is_in_shadow = (fragment_depth > closest_depth + shadow_obj.bias); 

                                    // calculate the shadow factor
                                    if (is_facing_light && is_in_shadow)
                                    {
                                        float s = 1 - shadow_obj.strength;
                                        return color * vec4(s,s,s,1.0);
                                    }

                                    return color;

                                };\n

            """
    

    @staticmethod
    def shadow_enabled_vertex_shader() -> str:
        return """
                    uniform mat4 projection_matrix;
                    uniform mat4 view_matrix;
                    uniform mat4 model_matrix;
                    uniform bool use_shadow;
                    uniform Shadow shadow_obj;
                    in vec3 vertex_position;
                    in vec3 vertex_normal;
                    in vec2 vertex_uv;
                    out vec2 uv;
                    out vec3 normal;
                    out vec3 position;
                    out vec3 shadow_pos;

                    void main()
                    {
                        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                        uv  = vertex_uv;
                        position = vec3(model_matrix * vec4(vertex_position, 1));
                        normal = normalize(mat3(model_matrix) * vertex_normal);

                        // calculate the shadow position
                        if (use_shadow)
                        {
                            vec4 temp0 = shadow_obj.projection_matrix * shadow_obj.view_matrix * model_matrix * vec4(vertex_position,1.0);
                            shadow_pos = vec3(temp0);
                            
                        }
                    }\n
                """