import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from PyQt5.QtGui import QOpenGLShaderProgram,QOpenGLShader
from core.glsl.uniform import UNIFORM_TYPE
import numpy as np


def str_to_matrix(data:str,size:int=4) -> np.ndarray:
    """
    This function takes a string and converts it to a matrix
    """
    #remove the brackets
    data = data.replace("[","").replace("]","").replace(" ","")
    print("normalized data: ",data)
    #split the string by commas
    # and convert it to a list of floats
    data = data.split(",")
    print("split data: ",data)
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(float(data[i*size+j]))
        matrix.append(row)
    
    return np.array(matrix, dtype=np.float32)

class GlUtils(object):
    
    IS_QT = False
    
    @staticmethod
    def InitializeShader(code:str, shader_type:int) -> int:
        # add header to shader code
        shader_code = '#version 420 core' + code

        # if shader_type is QOpenGLShader.ShaderTypeBit:
        if isinstance(shader_type, QOpenGLShader.ShaderTypeBit):
                    # create dummy shader
            shader = QOpenGLShader(shader_type)
            
            # store shader code in shader & check for compile errors
            if not shader.compileSourceCode(shader_code):
                raise RuntimeError(f"Shader compilation failed: {shader.log()}")
            
            return shader
        
        else:
            # create dummy shader
            shader = gl.glCreateShader(shader_type)

            # store shader code in shader
            gl.glShaderSource(shader, shader_code)
            # compile shader
            gl.glCompileShader(shader)

            # check for compile errors
            compile_status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
            if compile_status != gl.GL_TRUE:
                info_log = gl.glGetShaderInfoLog(shader)
                gl.glDeleteShader(shader)
                raise RuntimeError(f"Shader compilation failed: {info_log.decode()}")
            
            return shader
    

    @staticmethod
    def InitializeProgram(vertex_shader_code:str, fragment_shader_code:str) -> int:
       
        # handle the case where the shader is a QOpenGLShader
        if GlUtils.IS_QT:
            print("Using QOpenGLShader")
            vertex_shader_ref = GlUtils.InitializeShader(vertex_shader_code, QOpenGLShader.Vertex)
            fragment_shader_ref = GlUtils.InitializeShader(fragment_shader_code, QOpenGLShader.Fragment)
            # create program
            program = QOpenGLShaderProgram()
            
            # attach shaders to program
            if not program.addShader(vertex_shader_ref):
                raise RuntimeError(f"Vertex shader compilation failed: {program.log()}")
            
            if not program.addShader(fragment_shader_ref):
                raise RuntimeError(f"Fragment shader compilation failed: {program.log()}")
            
            # link program
            if not program.link():
                raise RuntimeError(f"Program linking failed: {program.log()}")
            
            # bind program
            program.bind()
            
            return program.programId()
        else:
            vertex_shader_ref = GlUtils.InitializeShader(vertex_shader_code, gl.GL_VERTEX_SHADER)
            fragment_shader_ref = GlUtils.InitializeShader(fragment_shader_code, gl.GL_FRAGMENT_SHADER)

            # check for shader compilation errors
            GlUtils.check_shader_compilation(vertex_shader_ref)
            GlUtils.check_shader_compilation(fragment_shader_ref)
            
            # create program
            program = gl.glCreateProgram()

            #attach shaders to program
            gl.glAttachShader(program,vertex_shader_ref)
            gl.glAttachShader(program,fragment_shader_ref)

            # link program
            gl.glLinkProgram(program)

            # check for link errors
            GlUtils.check_program_linking(program)
            
            return program
        
    @staticmethod
    def create_shader_module(filepath:str,module_type: int) -> int:
        source_code = ""

        with open(filepath, 'r') as file:
            source_code = file.readlines()

        return compileShader(source_code, module_type)

    @staticmethod
    def create_shader_program(vertex_filepath:str,fragment_filepath:str) ->int:
        vertex_module = GlUtils.create_shader_module(vertex_filepath,gl.GL_VERTEX_SHADER)
        fragment_module = GlUtils.create_shader_module(fragment_filepath,gl.GL_FRAGMENT_SHADER)
        
        shader_program = compileProgram(vertex_module, fragment_module)
        
        gl.glDeleteShader(vertex_module)
        gl.glDeleteShader(fragment_module)

        return shader_program
   
    @staticmethod
    def printSystemInfo():
        print("OpenGL Version:", gl.glGetString(gl.GL_VERSION).decode())
        print("GLSL Version:", gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode())
        print("Vendor:", gl.glGetString(gl.GL_VENDOR).decode())
        print("Renderer:", gl.glGetString(gl.GL_RENDERER).decode())
        print("Extensions:", gl.glGetString(gl.GL_EXTENSIONS).decode())

    @staticmethod
    def check_shader_compilation(shader_ref):
        status = gl.glGetShaderiv(shader_ref, gl.GL_COMPILE_STATUS)
        if status != gl.GL_TRUE:
            info_log = gl.glGetShaderInfoLog(shader_ref)
            raise RuntimeError(f"Shader compilation failed: {info_log.decode()}")
        

    @staticmethod
    def check_program_linking(program_ref):
        status = gl.glGetProgramiv(program_ref, gl.GL_LINK_STATUS)
        if status != gl.GL_TRUE:
            info_log = gl.glGetProgramInfoLog(program_ref)
            print("log: ",info_log)
            raise RuntimeError(f"Program linking failed: {info_log}")
        
    @staticmethod
    def make_uniform_data(data_type:UNIFORM_TYPE, data:str):
        """
        This function takes data_type and data both strings and converts the data to the appropriate type
        """

        print(f"data_type: {data_type}, data: {data}")

        if data_type == UNIFORM_TYPE.INT:
            return int(data)
        elif data_type == UNIFORM_TYPE.BOOL:
            if data.lower() == "true":
                return True
            elif data.lower() == "false":
                return False
            else:
                raise RuntimeError(f"Invalid boolean value {data}")
        elif data_type == UNIFORM_TYPE.FLOAT:
            return float(data)
        elif data_type == UNIFORM_TYPE.VEC2:
            return [float(data[0]), float(data[1])]
        elif data_type == UNIFORM_TYPE.VEC3:
            return [float(data[0]), float(data[1]), float(data[2])]
        elif data_type == UNIFORM_TYPE.VEC4:
            return [float(data[0]), float(data[1]), float(data[2]), float(data[3])]
        elif data_type == UNIFORM_TYPE.MAT4:
            return str_to_matrix(data)
        elif data_type == UNIFORM_TYPE.SAMPLER2D:
            texture_obj_ref, texture_unit_ref = data
            gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit_ref)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_obj_ref)
            return gl.glUniform1i(data, texture_unit_ref)
        else:
            raise RuntimeError(f"Unsupported data type {data_type}")
