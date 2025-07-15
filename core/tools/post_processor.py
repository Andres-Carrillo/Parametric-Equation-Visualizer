from core.rendering.renderer import Renderer
from core.rendering.scene import Scene
from core.rendering.camera import Camera
from meshes.mesh import Mesh
from core.rendering.render_target import RenderTarget
from geometry.geometry import Geometry


class Postprocessor(object):

    def __init__(self,renderer:Renderer,scene:Scene,camera:Camera,render_target:RenderTarget = None) -> None:
        self.renderer = renderer
        self.scene_list = [scene]
        self.camera_list = [camera]
        self.render_target_list = [render_target]
        self.parent_render_target = render_target

        self.ortho_camera = Camera()
        self.ortho_camera.set_orthographic()

        self.rectangle_geo = Geometry()
        P0 = [-1,-1]
        P1 = [1,-1]
        P2 = [-1,1]
        P3 = [1,1]

        T0 = [0, 0]
        T1 = [1, 0]
        T2 = [0,1]
        T3 = [1,1]
        
        pos_data = [ P0,P1,P3, P0,P3,P2 ]

        uv_data = [ T0,T1,T3, T0,T3,T2 ]

        self.rectangle_geo.add_attribute("vertex_position",pos_data,"vec2")
        self.rectangle_geo.add_attribute("vertex_uv",uv_data,"vec2")


    def add_effect(self,effect:object) -> None:
        # create dummpy scene to store the scene after the effect
        post_scene = Scene()

        resolution = self.renderer.window_size
        
        # create a new render target with the same resolution as the previous one
        target = RenderTarget(resolution=resolution)
        #chande the previous render target to the new one
        self.render_target_list[-1] = target

        effect.uniforms["texture_sampler"].data[0] = target.texture.texture_reference


        mesh = Mesh(self.rectangle_geo,effect)

        post_scene.add(mesh)

        self.scene_list.append(post_scene)
        self.camera_list.append(self.ortho_camera)
        self.render_target_list.append(self.parent_render_target)


    def render(self) -> None:
        passes = len(self.scene_list)
        for i in range(passes):
            scene = self.scene_list[i]
            camera = self.camera_list[i]
            target = self.render_target_list[i]

            self.renderer.render(scene,camera,render_target=target)