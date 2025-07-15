from core.rendering.camera import Camera
from core.light.light import Light
from core.rendering.render_target import RenderTarget
from core.material.lighted.depth import DepthMaterial
import OpenGL.GL as gl

class Shadow(object):
    def __init__(self,light_source:Light,strength:float=0.5,resolution:list=[512,512],
                    camera_bounds=[-5,5, -5,5, 0,20],bias:float=0.01) -> None:
        
        super().__init__()

        self.light_source = light_source

        # camera used to render scene to generate shadow map
        self.camera = Camera()

        #setting camera to orthographic projection
        left, right, bottom, top, near, far = camera_bounds
        self.camera.set_orthographic(left, right, bottom, top, near, far)

        # bind the camera to the light source by making the camera a child of the light source
        self.light_source.add(self.camera)

        #target used to render the shadow map
        self.render_target = RenderTarget(resolution=resolution,properties={"wrap":gl.GL_CLAMP_TO_BORDER})

        # material for rendering the shadow map
        self.material = DepthMaterial()

        # control the strength of the shadow
        self.strength = strength

        # bias used to avoid artifacts in the shadow map
        self.bias = bias



    def update_internal(self):
        self.camera.update_view_matrix()

        self.material.uniforms["view_matrix"].data = self.camera.view_matrix

        self.material.uniforms["projection_matrix"].data = self.camera.projection_matrix

