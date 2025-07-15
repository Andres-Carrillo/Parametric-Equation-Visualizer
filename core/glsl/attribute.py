import OpenGL.GL  as gl
import numpy as np
import PyQt5

"""
This class is used to create and manage OpenGL vertex buffer objects (VBOs) for
storing vertex attributes. It handles the creation of the buffer, uploading data
to the GPU, and associating the buffer with a shader program."""

class Attribute:
    def __init__(self,datatype:str,data:object):
        self._data_type = datatype
        self._data = data

        self._bufferRef = gl.glGenBuffers(1)

        self.upload_data()

    """
        This method is used to upload the data to the GPU. It creates a buffer object
        and uploads the data to the GPU. The data is converted to a numpy array of
        the appropriate data type before being uploaded. The buffer is created with
        the GL_STATIC_DRAW usage hint, which indicates that the data will not be changed
        frequently. 
            Raises:
                RuntimeError: If there is an error uploading the data to the GPU.
    """
    def upload_data(self):
        data = np.array(self._data,dtype=np.float32)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,self._bufferRef)

        # allocate memory for the buffer
        gl.glBufferData(gl.GL_ARRAY_BUFFER,data.nbytes,data,gl.GL_STATIC_DRAW)
        # check for errors
        error = gl.glGetError()
        if error != gl.GL_NO_ERROR:
            raise RuntimeError(f"Error uploading data to GPU: {error}")
        
    """
        This method is used to associate the buffer with a shader program. It creates
        a reference to a variable with the given name in the shader program and binds
        the buffer to the program. The method checks that the variable is valid and
        not -1 before associating it with the buffer. It also sets the appropriate
        pointer for the variable based on its data type. The method raises an exception
        if the data type is unknown.
            Args:
                program_ref (int): The reference to the shader program.
                variable_name (str): The name of the variable in the shader program.
            Raises:
             RuntimeError: If the variable is not valid or if the data type is unknown.
    """
    def associate_variable(self,program_ref:int,variable_name:str) -> None:
        
        # check if the program_ref is a shader program or a program id
        if isinstance(program_ref,PyQt5.QtGui.QOpenGLShaderProgram):
            program_ref = program_ref.programId()

        # create a reference to a variable with the given name
        self._variable_ref = gl.glGetAttribLocation(program_ref,variable_name)

        # check that the variable is valid is not skip associating
        if self._variable_ref == -1:
            return
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,self._bufferRef)

        if self._data_type == "int":
            gl.glVertexAttribIPointer(self._variable_ref,1,gl.GL_INT,False,0,None)
        elif self._data_type == "float":
            gl.glVertexAttribPointer(self._variable_ref,1,gl.GL_FLOAT,False,0,None)
        elif self._data_type == "vec2":
            gl.glVertexAttribPointer(self._variable_ref,2,gl.GL_FLOAT,False,0,None)
        elif self._data_type == "vec3":
            gl.glVertexAttribPointer(self._variable_ref,3,gl.GL_FLOAT,False,0,None)
        elif self._data_type == "vec4":
            gl.glVertexAttribPointer(self._variable_ref,4,gl.GL_FLOAT,False,0,None)
        else:
            raise RuntimeError(f"Unknown data type {self._data_type}")
        
        # enable the variable
        gl.glEnableVertexAttribArray(self._variable_ref)