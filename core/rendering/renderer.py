from core.meshes.mesh import Mesh
from core.light.light import Light
from core.rendering.render_target import RenderTarget
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.light.shadow import Shadow
from core.tools.bbox import BBoxMesh
from core.tools.grid import GridTool
from core.material.basic.point import PointMaterial
from core.material.basic.line import LineMaterial
from core.geometry.simple3D.box import BoxGeometry
from core.geometry.simple3D.sphere import Sphere
from core.meshes.terrain import InfiniteTerrainManager
import OpenGL.GL as gl

class Renderer(object):
    def __init__(self,clear_color:list = [0.0, 0.0, 0.],window_width:int=SCREEN_WIDTH,window_height:int = SCREEN_HEIGHT) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)
        # enables anti-aliasing
        gl.glEnable(gl.GL_MULTISAMPLE)

        # enables blending
        gl.glEnable(gl.GL_BLEND)
        # set the blending function
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # set the clear color
        gl.glClearColor(clear_color[0], clear_color[1], clear_color[2], 1.0)

        self.window_size = (window_width,window_height)

        self.shadows_enabled = False
        self.bound_box_enabled = False
        self._use_lights = False


    def render(self,scene:object,camera:object,clear_color:bool = True,clear_depth:bool = True,
               render_target:RenderTarget=None,terrain_manager:InfiniteTerrainManager=None) -> None:
        
        # filter out only the visible meshes in the scene
        obj_list = scene.descendant_list

        viewable_meshes = scene.get_visible_objects()

        # filter out only the lights in the scene
        light_filter = lambda x: isinstance(x,Light)
        light_list = list(filter(light_filter,obj_list))

        self._update_viewport(render_target,clear_color,clear_depth)

        # handle shadows
        self._shadow_pass(viewable_meshes)

        # handle rendering viewable meshes
        self._render_meshes(camera,viewable_meshes,light_list,terrain_manager=terrain_manager)

        # handle rendering the bounding boxes
        if self.bound_box_enabled:
            self._render_bboxes(viewable_meshes,camera)

    def update_window_size(self,window_width, window_height):
            self.window_size = (window_width, window_height)
    
    @property
    def shadow_object(self):
        return self._shadow_object
    
    @property
    def enable_lights(self):
        return self._use_lights

    @enable_lights.setter
    def enable_lights(self,enable:bool):
        self._use_lights = enable


    def enable_shadows(self,shadow_light:Light,strenth:float = 0.5,resolution:list = [512,512]):
        self.shadows_enabled = True
        self._shadow_object = Shadow(light_source=shadow_light,resolution=resolution,strength=strenth)

    def enable_bound_box(self):
        self.bbox_dict = {}
        self.bound_box_enabled = True

    def disable_bound_box(self):
        self.bound_box_enabled = False

    def _update_bound_box(self,mesh:Mesh):
        if not self.bound_box_enabled:
            return
        
        if type(mesh) == GridTool:
            return

        mesh_id = str(mesh)
                
        if mesh_id not in self.bbox_dict.keys():
            bbox = BBoxMesh(mesh)
            self.bbox_dict[mesh_id] = bbox
        else:
            bbox = self.bbox_dict[mesh_id]
            bbox._update()
            


    def _shadow_pass(self,mesh_list):
        if not self.shadows_enabled:
            return

        # Set render target properties
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._shadow_object.render_target.frame_buffer)
        gl.glViewport(0, 0, self._shadow_object.render_target.width, self._shadow_object.render_target.height)

        # # Set default color to black, used when no objects present to cast shadows
        gl.glClearColor(0, 0, 0, 1)

        # Clear color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        
        # Everything in the scene gets rendered with depthMaterial so
        # only need to call glUseProgram & set matrices once
        gl.glUseProgram(self._shadow_object.material.program)
        self._shadow_object.update_internal()
        
        for mesh in mesh_list:
            # Skip invisible meshes
            if not mesh.visible:
                continue
            # Only triangle-based meshes cast shadows
            if mesh.material.settings["draw_mode"] != gl.GL_TRIANGLES:
                continue
            # Bind VAO
            gl.glBindVertexArray(mesh.vao_ref)
            # Update transform data
            self._shadow_object.material.uniforms["model_matrix"].data = mesh.global_matrix
            # Update uniforms (matrix data) stored in shadow material
            for var_name, uniform_obj in self._shadow_object.material.uniforms.items():
                uniform_obj.upload_data()
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh.geometry.vertex_count)

            # Unbind VAO
            gl.glBindVertexArray(0)



    def _render_meshes(self,camera,viewable_meshes,light_list,terrain_manager:InfiniteTerrainManager=None):
        # print("terrain manager:", terrain_manager)
        # if terrain manager is provided, update the terrain chunks
        if terrain_manager is not None:
            terrain_manager.update(camera.global_position)

        # if the terrain manager is provided, get the terrain meshes
        if terrain_manager is not None:
            terrain_chunks = terrain_manager.chunks.values()
            # iterate through the chunks and render them before the other meshes
            for chunk in terrain_chunks:
                self._render_mesh(chunk,camera,light_list)

        # update camera
        camera.update_view_matrix()

        for mesh in viewable_meshes:
            self._render_mesh(mesh,camera,light_list)



    def _render_mesh(self,mesh:Mesh,camera,light_list):
            # install the program for the mesh
            gl.glUseProgram(mesh.material.program)
            # bind vertex array object for the mesh
            gl.glBindVertexArray(mesh.vao_ref)

            # ================== update the uniforms for the mesh not stored in the material ==================
            #update the model matrix based on the mesh's world matrix
            mesh.material.uniforms["model_matrix"].data = mesh.global_matrix

            # update the view matrix to match the camera
            mesh.material.uniforms["view_matrix"].data = camera.view_matrix

            # update the projection matrix to match the camera
            mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix

            # =========== Handle lights if any exist ==============
            if self._use_lights:
                # if the current mesh has a light material, update the light uniforms
                if "light_0" in mesh.material.uniforms.keys():
                
                    number_of_lights = len(light_list) # number of lights in the scene
                  
                    for light_n in range(number_of_lights):
                        # check if the light exists in the material
                        light_name = "light_" + str(light_n) # figure out the name of the light
                        light_inst = light_list[light_n] # get the light instance from the list
                
                        #update the light uniforms in the material incase the light has changed
                        mesh.material.uniforms[light_name].data = light_inst

            # check if the mesh uses specular lighting
            if "view_position" in mesh.material.uniforms.keys():
                # update the view position to match the camera
                mesh.material.uniforms["view_position"].data = camera.global_position

            # check if the mesh uses shadows
            if self.shadows_enabled and "shadow_obj" in mesh.material.uniforms.keys():   
                mesh.material.uniforms["shadow_obj"].data = self.shadow_object  

            # ================== update the uniforms for the mesh stored in the material ==================
            for var_name,uniform_obj in mesh.material.uniforms.items():
                if uniform_obj.data is not None:
                    uniform_obj.upload_data()


            #update the render settings for the material
            mesh.material.update_render_settings()

            # draw the mesh
            gl.glDrawArrays(mesh.material.settings["draw_mode"],0,mesh.geometry.get_vertex_count())

            # unbind the vertex array object
            gl.glBindVertexArray(0)
            # unbind the program
            gl.glUseProgram(0)

    def _update_viewport(self,render_target:RenderTarget,clear_color:bool = True,clear_depth:bool = True):
        # set the viewport to the size of the window
        if (render_target  == None):
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,0)
            gl.glViewport(0, 0, self.window_size[0], self.window_size[1])
        else: # set the viewport to the size of the render target
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,render_target.frame_buffer)
            gl.glViewport(0, 0, render_target.width, render_target.height)

        if clear_color:
            # clear the color buffer
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if clear_depth:
            # clear the depth buffer
            gl.glClear(gl.GL_DEPTH_BUFFER_BIT)


    def _render_bboxes(self,viewable_meshes,camera,draw_wireframe:bool = True,draw_corners:bool = True):
        gl.glDisable(gl.GL_DEPTH_TEST)
        
        for obj in viewable_meshes:
            if type(obj) == GridTool:
                continue

            bounding_box = obj.geometry.AA_bounding_box()

            center = [(bounding_box[0][0] + bounding_box[1][0]) / 2,
                      (bounding_box[0][1] + bounding_box[1][1]) / 2,
                      (bounding_box[0][2] + bounding_box[1][2]) / 2]
            
            
            width = max(bounding_box[1][0] - bounding_box[0][0],1)
            height = max(bounding_box[1][1] - bounding_box[0][1],1)
            depth = max(bounding_box[1][2] - bounding_box[0][2],1)

            if type(obj) == Sphere:
                width = 2 #obj.radius * 2
                height = 2 #obj.radius * 2
                depth = 2 #obj.radius * 2
                center = obj.global_position

            ############################## render BBOx CORNERS ##############################
            if draw_corners:
                point_material = PointMaterial(properties={"base_color": [1.0, 0.0, 0.0]})

                point_geo = BoxGeometry(width, height, depth)

                point_mesh = Mesh(point_geo,point_material)
                point_mesh.set_position(obj.global_position + center)
                # install the program for the mesh
                gl.glUseProgram(point_mesh.material.program)
                
                # bind vertex array object for the mesh
                gl.glBindVertexArray(point_mesh.vao_ref)

                # ================== update the uniforms for the mesh not stored in the material ==================
                #update the model matrix based on the mesh's world matrix
                point_mesh.material.uniforms["model_matrix"].data = point_mesh.global_matrix

                # update the view matrix to match the camera
                point_mesh.material.uniforms["view_matrix"].data = camera.view_matrix

                # update the projection matrix to match the camera
                point_mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix

                # ================== update the uniforms for the mesh stored in the material ==================
                for var_name,uniform_obj in point_mesh.material.uniforms.items():
                    if uniform_obj.data is not None:
                        uniform_obj.upload_data()


                #update the render settings for the material
                point_mesh.material.update_render_settings()

                # draw the mesh
                gl.glDrawArrays(point_mesh.material.settings["draw_mode"],0,point_mesh.geometry.get_vertex_count())


                # unbind the vertex array object
                gl.glBindVertexArray(0)
                # unbind the program
                gl.glUseProgram(0)

            # ############################### render the bbox edges ##############################
            if draw_wireframe:
                edge_material = LineMaterial(properties={"base_color": [1.0, 0.0, 0.0]})
                edge_material.settings['use_vertex_colors'] = False
                edge_material.settings['line_type'] = "segments"

                edge_geo = BoxGeometry(width, height, depth)

                edge_mesh = Mesh(edge_geo,edge_material)
                edge_mesh.set_position(obj.global_position + center)
                
                # install the program for the mesh
                gl.glUseProgram(edge_mesh.material.program)
                
                # bind vertex array object for the mesh
                gl.glBindVertexArray(edge_mesh.vao_ref)

                # ================== update the uniforms for the mesh not stored in the material ==================
                #update the model matrix based on the mesh's world matrix
                edge_mesh.material.uniforms["model_matrix"].data = edge_mesh.global_matrix

                # update the view matrix to match the camera
                edge_mesh.material.uniforms["view_matrix"].data = camera.view_matrix

                # update the projection matrix to match the camera
                edge_mesh.material.uniforms["projection_matrix"].data = camera.projection_matrix


                # ================== update the uniforms for the mesh stored in the material ==================
                for var_name,uniform_obj in edge_mesh.material.uniforms.items():
                    if uniform_obj.data is not None:
                        uniform_obj.upload_data()


                #update the render settings for the material
                edge_mesh.material.update_render_settings()

                # draw the mesh
                gl.glDrawArrays(edge_mesh.material.settings["draw_mode"],0,edge_mesh.geometry.get_vertex_count())
                # unbind the vertex array object
                gl.glBindVertexArray(0)
                # unbind the program
                gl.glUseProgram(0)
    
        # enable depth testing again
        gl.glEnable(gl.GL_DEPTH_TEST)
