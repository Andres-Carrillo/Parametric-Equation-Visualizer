import OpenGL.GL as gl
import numpy as np
import enum

class UNIFORM_TYPE(enum.Enum):
    INT = 0
    BOOL = 1
    FLOAT = 2
    VEC2 = 3
    VEC3 = 4
    VEC4 = 5
    MAT4 = 6
    SAMPLER2D = 7
    LIGHT = 8
    SHADOW = 9

    def __str__(self):
        if self == UNIFORM_TYPE.INT:
            return "int"
        elif self == UNIFORM_TYPE.BOOL:
            return "bool"
        elif self == UNIFORM_TYPE.FLOAT:
            return "float"
        elif self == UNIFORM_TYPE.VEC2:
            return "vec2"
        elif self == UNIFORM_TYPE.VEC3:
            return "vec3"
        elif self == UNIFORM_TYPE.VEC4:
            return "vec4"
        elif self == UNIFORM_TYPE.MAT4:
            return "mat4"
        elif self == UNIFORM_TYPE.SAMPLER2D:
            return "sampler2D"
        elif self == UNIFORM_TYPE.LIGHT:
            return "Light"
        elif self == UNIFORM_TYPE.SHADOW:
            return "Shadow"

class Uniform(object):

    def __init__(self,data_type,data):
        self.data_type = data_type
        self.data = data

        self.var_ref = None

    
    def locate_variable(self,program_ref,var_name):

        if self.data_type =="Light":
            # create a dictionary to hold the light type based on struct within the shader
            self.var_ref = {}
            # get the light type
            self.var_ref['light_type'] = gl.glGetUniformLocation(program_ref,var_name + ".light_type")
            # get the light color
            self.var_ref['color'] = gl.glGetUniformLocation(program_ref,var_name + ".color")
            # get the light direction
            self.var_ref['direction'] = gl.glGetUniformLocation(program_ref,var_name + ".direction")
            # get the light position
            self.var_ref['position'] = gl.glGetUniformLocation(program_ref,var_name + ".position")
            # get the light attenuation
            self.var_ref['attenuation'] = gl.glGetUniformLocation(program_ref,var_name + ".attenuation")
        elif self.data_type == "Shadow":
            self.var_ref = {}
            self.var_ref['light_dir'] = gl.glGetUniformLocation(program_ref,var_name + ".light_dir")
            self.var_ref['projection_matrix'] = gl.glGetUniformLocation(program_ref,var_name + ".projection_matrix")
            self.var_ref['view_matrix'] = gl.glGetUniformLocation(program_ref,var_name + ".view_matrix")
            self.var_ref['depth_map'] = gl.glGetUniformLocation(program_ref,var_name + ".depth_map")
            self.var_ref['shadow_strength'] = gl.glGetUniformLocation(program_ref,var_name + ".strength")
            self.var_ref['shadow_bias'] = gl.glGetUniformLocation(program_ref,var_name + ".bias")
        else:
            self.var_ref = gl.glGetUniformLocation(program_ref,var_name)

        # check if the variable was found if not return -1 for debugging and error handling
        if self.var_ref == -1:
            return -1
        
        
    def upload_data(self):
        
        if self.var_ref !=-1:
            if self.data_type == "int":
                    gl.glUniform1i(self.var_ref,self.data)
            elif self.data_type == "bool":
                gl.glUniform1i(self.var_ref,self.data)
            elif self.data_type == "float":
                gl.glUniform1f(self.var_ref,self.data)
            elif self.data_type == "vec2":
                gl.glUniform2f(self.var_ref,self.data[0],self.data[1])
            elif self.data_type == "vec3":
                gl.glUniform3f(self.var_ref,self.data[0],self.data[1],self.data[2])
            elif self.data_type == "vec4":
                gl.glUniform4f(self.var_ref,self.data[0],self.data[1],self.data[2],self.data[3])
            elif self.data_type == "mat4":
                gl.glUniformMatrix4fv(self.var_ref, 1, gl.GL_TRUE, np.array(self.data, dtype=np.float32))
            elif self.data_type == "sampler2D":
                # split the data into 2 parts the texture object and the texture unit reference
                texture_obj_ref,texture_unit_ref = self.data

                # activate the texture unit
                gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit_ref)   

                #associate the texture object with the texture unit
                gl.glBindTexture(gl.GL_TEXTURE_2D,texture_obj_ref)

                # upload texture  unit number 0-15 to the uniform variable in the shader
                gl.glUniform1i(self.var_ref,texture_unit_ref)

            elif self.data_type == "Light":
                pos = self.data.local_position
                direction = self.data.direction
                # upload the light type 
                gl.glUniform1i(self.var_ref['light_type'],self.data.light_type.value)
                # upload the light color
                gl.glUniform3f(self.var_ref['color'],self.data.color[0],self.data.color[1],self.data.color[2])
                 # upload the light direction
                gl.glUniform3f(self.var_ref['direction'],direction[0],direction[1],direction[2])
                # upload the light position
                gl.glUniform3f(self.var_ref['position'],pos[0],pos[1],pos[2])
                # upload the light attenuation
                gl.glUniform3f(self.var_ref['attenuation'],self.data.attenuation[0],self.data.attenuation[1],self.data.attenuation[2])

            elif self.data_type == "Shadow":
                direction = self.data.light_source.direction
                # upload the light direction
                gl.glUniform3f(self.var_ref["light_dir"],direction[0],direction[1],direction[2])

                # upload the projection matrix
                gl.glUniformMatrix4fv(self.var_ref["projection_matrix"], 1, gl.GL_TRUE, np.array(self.data.camera.projection_matrix, dtype=np.float32))

                # upload the view matrix
                gl.glUniformMatrix4fv(self.var_ref["view_matrix"], 1, gl.GL_TRUE, np.array(self.data.camera.view_matrix, dtype=np.float32))

                # upload the depth map
                texture_obj_ref = self.data.render_target.texture.texture_reference

                # texture unit reference set arbitrarily to 15 for now to keep things simple
                # in the future need to create a texture unit manager to handle this and avoid conflicts
                # this texture manager will be responsible for keeping track of the texture units and their references for the 
                # different textures and their references in the scene
                texture_unit_ref = 3

                gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit_ref)
                gl.glBindTexture(gl.GL_TEXTURE_2D,texture_obj_ref)

                # upload the texture unit reference to the shader
                gl.glUniform1i(self.var_ref["depth_map"],texture_unit_ref)

                # upload the shadow strength
                gl.glUniform1f(self.var_ref["shadow_strength"],self.data.strength)

                # upload the shadow bias
                gl.glUniform1f(self.var_ref["shadow_bias"],self.data.bias)
               
            else:
                    raise RuntimeError(f"Unsupported data type {self.data_type}")
