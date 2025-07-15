from core.textures.texture import Texture
import OpenGL.GL as gl
import pygame as pg

class RenderTarget(object):
    def __init__(self,resolution: list =[512,512],texture:Texture=None,properties:dict={})-> None:
        self.width, self.height = resolution

        # Set texture or a default texture
        if texture is not None:
            self.texture = texture
        else:
            self.texture = Texture(None,{
                "magnify_filter":gl.GL_LINEAR,
                "minify_filter":gl.GL_LINEAR,
                "wrap":gl.GL_CLAMP_TO_EDGE,
            })

        # Set default properties
        self.texture.set_properties(properties)

        # Set the texture surface to a new surface
        self.texture._surface = pg.Surface(resolution)

        # upload the texture to GPU
        self.texture.upload_texture()

        # create framebuffer for storing image data
        self.frame_buffer = gl.glGenFramebuffers(1)
        
        # Bind the framebuffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,self.frame_buffer)

        # configure color buffer to use the texture
        gl.glFramebufferTexture(gl.GL_FRAMEBUFFER,gl.GL_COLOR_ATTACHMENT0,self.texture.texture_reference,0)

        # create depth buffer to store depth information
        depth_buffer = gl.glGenRenderbuffers(1)
        # Bind the depth buffer
        
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER,depth_buffer)
        # Allocate storage for the depth buffer
        
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER,gl.GL_DEPTH_COMPONENT24,self.width,self.height)
        
        # Attach the depth buffer to the framebuffer
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER,gl.GL_DEPTH_ATTACHMENT,gl.GL_RENDERBUFFER,depth_buffer)

        # Check if the framebuffer is complete
        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Error: Framebuffer is not complete.")



class QtRenderTarget(object):
    def __init__(self, resolution: list = [512, 512], texture: Texture = None, properties: dict = {}, parent_widget=None) -> None:
        """
        Initialize a RenderTarget for offscreen rendering.
        :param resolution: The resolution of the framebuffer.
        :param texture: Optional texture to use as the color attachment.
        :param properties: Additional properties for the texture.
        :param parent_widget: The parent QOpenGLWidget (TestWidget) to ensure context compatibility.
        """
        self.width, self.height = resolution
        self.parent_widget = parent_widget  # Reference to the parent widget

        # Ensure the OpenGL context is current
        if self.parent_widget:
            self.parent_widget.makeCurrent()

        # Set texture or create a default texture
        if texture is not None:
            self.texture = texture
        else:
            self.texture = Texture(None, {
                "magnify_filter": gl.GL_LINEAR,
                "minify_filter": gl.GL_LINEAR,
                "wrap": gl.GL_CLAMP_TO_EDGE,
            })

        # Set default properties
        self.texture.set_properties(properties)

        # Set the texture surface to a new surface
        self.texture._surface = pg.Surface(resolution)

        # Upload the texture to the GPU
        self.texture.upload_texture()

        # Create framebuffer for storing image data
        self.frame_buffer = gl.glGenFramebuffers(1)

        # Bind the framebuffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.frame_buffer)

        # Configure color buffer to use the texture
        gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, self.texture.texture_reference, 0)

        # Create depth buffer to store depth information
        self.depth_buffer = gl.glGenRenderbuffers(1)

        # Bind the depth buffer
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self.depth_buffer)

        # Allocate storage for the depth buffer
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT24, self.width, self.height)

        # Attach the depth buffer to the framebuffer
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, self.depth_buffer)

        # Check if the framebuffer is complete
        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Error: Framebuffer is not complete.")

        # Unbind the framebuffer to avoid accidental rendering
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.parent_widget.defaultFramebufferObject() if self.parent_widget else 0)

    def bind(self):
        """
        Bind the custom framebuffer for rendering.
        """
        if self.parent_widget:
            self.parent_widget.makeCurrent()  # Ensure the context is current
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.frame_buffer)

    def unbind(self):
        """
        Unbind the custom framebuffer and bind the default framebuffer.
        """
        if self.parent_widget:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.parent_widget.defaultFramebufferObject())
        else:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)