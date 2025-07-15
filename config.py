import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

vertex_3d = np.dtype([
    ('x', np.float32),    # 4 bytes for x
    ('y', np.float32),    # 4 bytes for y
    ('z', np.float32),    # 4 bytes for z
    ('color', np.uint32),  # 4 bytes for color
])

def create_shader_program(vertex_filepath:str,fragment_filepath:str) ->int:
    vertex_module = create_shader_module(vertex_filepath,gl.GL_VERTEX_SHADER)
    fragment_module = create_shader_module(fragment_filepath,gl.GL_FRAGMENT_SHADER)
    
    shader_program = compileProgram(vertex_module, fragment_module)
    
    gl.glDeleteShader(vertex_module)
    gl.glDeleteShader(fragment_module)

    return shader_program

def create_shader_module(filepath:str,module_type: int) -> int:
    source_code = ""

    with open(filepath, 'r') as file:
        source_code = file.readlines()

    return compileShader(source_code, module_type)