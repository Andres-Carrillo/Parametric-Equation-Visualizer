import imgui
import math
from core.utils.openGLUtils import GlUtils
from core.glsl.uniform import UNIFORM_TYPE
from core.meshes.mesh import Mesh
from core.tools.bbox import BBoxMesh
from core.meshes.terrain import InfiniteTerrainManager

# Geometry imports
from core.geometry.geometry import GEOMETRY_TYPE
from core.geometry.simple3D.box import BoxGeometry
from core.geometry.simple3D.sphere import Sphere
from core.geometry.simple3D.cylinder import Cylinder
from core.geometry.simple3D.plane import Plane
from core.geometry.simple2D.rectangle import Rectangle
from core.geometry.simple2D.circle import Circle
from core.geometry.simple2D.triangle import Triangle
from core.geometry.simple2D.polygon import Polygon
from core.geometry.simple2D.pentagon import Pentagon
from core.geometry.simple2D.hexagon import Hexagon
from core.geometry.simple2D.octagon import Octagon
from core.geometry.simple2D.heptagon import Heptagon
from core.geometry.simple2D.quad import Quad
from core.geometry.simple3D.cone import Cone
from core.geometry.simple3D.prism import Prism
from core.geometry.simple3D.pyramid import Pyramid

# Material imports
from core.material.basic.material import MATERIAL_TYPE
from core.material.basic.surface import SurfaceMaterial
from core.material.lighted.lambert import LambertMaterial
from core.material.lighted.phong import PhongMaterial
from core.material.lighted.flat import FlatMaterial
from core.material.basic.line import LineMaterial
from core.material.basic.point import PointMaterial
from core.material.basic.sprite import Sprite
from core.material.basic.texture import TextureMaterial

# Light imports
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from core.light.ambient import AmbientLight
from core.light.light import LIGHT_TYPE
from core.tools.point_light_tool import PointLightTool
from core.tools.directional_light_tool import DirectionalLightTool

# import shadows
from core.light.shadow import Shadow

import random

def draw_mesh_uniform_editor(mesh):
    # display the mesh's current uniforms and allow the user to edit them
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Uniforms")
    if open_header:
        for key, value in mesh.material.uniforms.items():
            if key in ("model_matrix", "view_matrix", "projection_matrix"):
                continue
            if key == "use_vertex_colors":
                changed, new_value = imgui.checkbox("Use Vertex Color", value.data)
                imgui.same_line()
                if changed:
                    mesh.material.uniforms[key].data = new_value
            if key == "wire_frame":
                changed, new_value = imgui.checkbox("Wire Frame", value.data)
                imgui.same_line()
                if changed:
                    mesh.material.uniforms[key].data = new_value
            if key == "base_color":
                changed, new_color = imgui.color_edit4("Base Color", value.data[0], value.data[1], value.data[2], 1.0)
                if changed:
                    mesh.material.set_properties({"base_color": new_color})

def draw_material_settings(mesh):
    # display the mesh's current material settings and allow the user to edit them
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Settings")
    if open_header:
        for key, value in mesh.material.settings.items():
                if key == "wire_frame":
                    changed, new_value = imgui.checkbox("Wire Frame", value)
                    imgui.same_line()
                    if changed:
                        mesh.material.settings[key] = new_value
                if mesh.material.settings.get('wire_frame', False) and key == "line_width":
                    changed, new_value = imgui.slider_float("Line Width", value, 0.1, 10.0)
                    if changed:
                        mesh.material.settings[key] = new_value
                if key == "double_sided":
                    changed, new_value = imgui.checkbox("Double Sided", value)
                    imgui.same_line()
                    if changed:
                        mesh.material.settings[key] = new_value

def draw_position_editor(mesh):
     # Display the mesh's current position and allow the user to edit it
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Position transform")
    if open_header:
        changed_x, new_x_pos = imgui.input_int("X Position##pos", mesh.global_position[0])
        changed_y, new_y_pos = imgui.input_int("Y Position##pos", mesh.global_position[1])
        changed_z, new_z_pos = imgui.input_int("Z Position##pos", mesh.global_position[2])
        if changed_x or changed_y or changed_z:
            mesh.set_position([new_x_pos, new_y_pos, new_z_pos])

def draw_rotation_editor(mesh,range =(-math.pi, math.pi)):
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Rotation transform")
    if open_header:
        x_rot_changed, new_x_rot = imgui.slider_float("X Rotation", mesh.ueler_angles[0], range[0], range[1])
        y_rot_changed, new_y_rot = imgui.slider_float("Y Rotation", mesh.ueler_angles[1], range[0], range[1])
        z_rot_changed, new_z_rot = imgui.slider_float("Z Rotation", mesh.ueler_angles[2], range[0], range[1])
        if x_rot_changed or y_rot_changed or z_rot_changed:
            mesh.set_euler_rotation([new_x_rot*360, new_y_rot*360, new_z_rot*360])

def draw_uniform_maker(uniform_name:str = "", uniform_type:int = 0, uniform_data:str = ""):
    # draw a window to create a new uniform
    make = False
    imgui.text("Create a new uniform:")
    imgui.separator()

    _,new_uniform_data = imgui.input_text("Uniform Data", uniform_data)
    _,new_uniform_name = imgui.input_text("Uniform Name", uniform_name)
    _, new_uniform_type = imgui.combo("Uniform Type", uniform_type, [str(type) for type in UNIFORM_TYPE])

    if imgui.button("Create"):
        make = True

    imgui.separator()

    return new_uniform_name, new_uniform_type, new_uniform_data, make


class ShaderEditor:
    def __init__(self, mesh: Mesh = None,window_width:int = 1000, window_height:int = 300,embedded:bool = False):
        self.embedded = embedded
        self.window_width = window_width
        self.window_height = window_height
        self.show_editor = False
        self.compile_error = False
        self.edit_uniforms = False
        self.creating_uniform = False
        self.temp_uniform_type = 0
        self.temp_uniform_name = ""
        self.temp_uniform_data = ""
        self.mesh = mesh
        self.menu_bbox = [0, 0, 0, 0]
        self.error_message = ""

        if mesh:
            self.vertex_shader = self.mesh.materia.vertex_shader
            self.fragment_shader = self.mesh.material.fragment_shader
        else:
            self.vertex_shader = """"""
            self.fragment_shader = """"""

    # for setting a new mesh without having to recompile the shaders or create a new editor
    def change_mesh(self, mesh: Mesh = None):
        self.mesh = mesh
        if mesh:
            self.vertex_shader = self.mesh.material.vertex_shader
            self.fragment_shader = self.mesh.material.fragment_shader
        else:
            self.vertex_shader = """"""
            self.fragment_shader = """"""

    def show(self):
        open_header, _ = imgui.collapsing_header("Shader Editor")
        if open_header: 
            imgui.separator()
            if self.edit_uniforms:
                imgui.text("Edit Uniforms:")
                imgui.separator()
                draw_mesh_uniform_editor(self.mesh)
                imgui.separator()

                
                # handle adding a new uniform to the mesh material
                if imgui.button("Add a new Uniform"):
                    self.creating_uniform = True

                if self.creating_uniform:
                    self.temp_uniform_name,self.temp_uniform_type, self.temp_uniform_data,add_uniform = draw_uniform_maker(uniform_name=self.temp_uniform_name, uniform_type=self.temp_uniform_type, uniform_data=self.temp_uniform_data)
                
                    if add_uniform:
                        uniform_data =  GlUtils.make_uniform_data( UNIFORM_TYPE(self.temp_uniform_type), self.temp_uniform_data)
                        self.mesh.material.add_uniform(self.temp_uniform_name,  uniform_data,str(UNIFORM_TYPE(self.temp_uniform_type)))
                        self.mesh.material.locate_uniforms()    
                        
                        # reset the buffers
                        self.creating_uniform = False
                        self.temp_uniform_name = ""
                        self.temp_uniform_data = ""
                        self.temp_uniform_type = 0

                imgui.separator()
               
                if imgui.button("Done"):
                    self.edit_uniforms = False


            open_vertex_shader, _ = imgui.collapsing_header("Vertex Shader")
            if open_vertex_shader:
                imgui.text("Vertex Shader Editor:")
                imgui.separator()
                _, self.vertex_shader = imgui.input_text_multiline("##vertex shader", self.vertex_shader, 1024 * 16, self.window_width, self.window_height)
                
            imgui.separator()

            open_fragment_shader, _ = imgui.collapsing_header("Fragment Shader")
            if open_fragment_shader:
                imgui.text("Fragment Shader Editor:")
                imgui.separator()
                _, self.fragment_shader = imgui.input_text_multiline("##fragment shader", self.fragment_shader, 1024 * 16, self.window_width, self.window_height)

            imgui.separator()
            
            if self.compile_error:
                imgui.separator()
                imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
                imgui.text("Error compiling shaders:")
                imgui.text(self.error_message)
                imgui.pop_style_color()
                imgui.separator()
                imgui.text("Please check the shader code and try again.")

            imgui.separator() 
            if(imgui.button("Compile")):
                self.compile_shaders()

            imgui.same_line()   
            if(imgui.button("Edit Uniforms")):
                self.edit_uniforms = not self.edit_uniforms
               
    def compile_shaders(self):
        try:
            self.mesh.material.compile_shaders(self.vertex_shader, self.fragment_shader)
            self.compile_error = False
            self.error_message = ""
        except Exception as e:
            self.error_message = str(e)
            self.compile_error = True


    def get_menu_deadzones(self):
        return self.menu_bbox

class MeshEditor:
    def __init__(self, mesh: Mesh = None):
        self.mesh = mesh
        self.shader_editor = ShaderEditor(mesh,embedded=True)
        self.menu_bbox = [0, 0, 0, 0]
        self.editing_shader = False

    def change_mesh(self, mesh: Mesh = None):
        self.mesh = mesh
        self.shader_editor.change_mesh(mesh)

    def show(self):
        imgui.text("{}".format(self.mesh.geometry.object_type))

        # Display the mesh's current position and allow the user to edit it
        draw_position_editor(self.mesh)

        # Display the mesh's current rotation and allow the user to edit it
        draw_rotation_editor(self.mesh)

        draw_mesh_uniform_editor(self.mesh)

        draw_material_settings(self.mesh)

        imgui.separator()

        if imgui.button("Edit Shaders"):
            self.shader_editor.show_editor = not self.shader_editor.show_editor

        if self.shader_editor.show_editor:
            # Open the shader editor window
            self.editing_shader = True
            self.shader_editor.show()


    def get_menu_deadzones(self):
        # return the menu bounding box for the mesh editor and shader editor
        return [self.menu_bbox, self.shader_editor.menu_bbox]   



class ObjectSpawner: 
    def __init__(self) -> None:
        self._range = None 
        self._location = None
        self._material_type = MATERIAL_TYPE.SURFACE.value
        self._geometry_type = GEOMETRY_TYPE.BOX.value
        self.show_bbox = False
        self.lights_in_scene = 0

    def set_range(self, range:list = [-2,2]):
        self._range = range

    def set_location(self, location:list = [0,0,0]):
        self._location = location

    def get_object(self):
        return self._obj
    
    def get_bbox(self):
        if self._obj is not None:
            bbox = BBoxMesh(self._obj)
            return bbox.get_bbox()
        else:
            return None

    def spawn_object(self):
        return {
            "object": self._obj,
            "bbox": self.get_bbox()
        }


    def show(self):
        imgui.text("Geometry Type:")
        imgui.same_line()
        imgui.text(" Material Type:")
        imgui.set_next_item_width(100)
        _,self._geometry_type = imgui.combo("##Geometry Type", self._geometry_type, [str(geo_type) for geo_type in GEOMETRY_TYPE])
        imgui.same_line()
        imgui.set_next_item_width(100)

        _,self._material_type = imgui.combo("##Material Type", self._material_type, ["Point", "Line", "Surface", "Flat", "Lambert", "Phong"])

        if imgui.button("Generate Mesh"):
            geo = self.get_geometry(self._geometry_type)
            surface_material = self.get_material(self._material_type)
            self._obj = Mesh(geometry=geo, material=surface_material)

            if self._location is not None:
                self._obj.set_position(self._location)
            else:
                x_pos = random.uniform(-2, 2)
                y_pos = random.uniform(-2, 2)
                z_pos = random.uniform(-2, 2)
                self._obj.set_position([x_pos, y_pos, z_pos])
        else:
            self._obj = None

        imgui.same_line()
        _,self.show_bbox = imgui.checkbox("show BBox", self.show_bbox)


    def get_geometry(self,geometry_type):
        if geometry_type == GEOMETRY_TYPE.BOX.value:
            return BoxGeometry()
        elif geometry_type == GEOMETRY_TYPE.SPHERE.value:
            return Sphere()
        elif geometry_type == GEOMETRY_TYPE.CYLINDER.value:
            return Cylinder()
        elif geometry_type == GEOMETRY_TYPE.PLANE.value:
            return Plane()
        elif geometry_type == GEOMETRY_TYPE.CIRCLE.value:
            return Circle()
        elif geometry_type == GEOMETRY_TYPE.RECTANGLE.value:
            return Rectangle()
        elif geometry_type == GEOMETRY_TYPE.TRIANGLE.value:
            return Triangle()
        elif geometry_type == GEOMETRY_TYPE.CONE.value:
            return Cone()
        elif geometry_type == GEOMETRY_TYPE.PRISM.value:
            return Prism()
        elif geometry_type == GEOMETRY_TYPE.PYRAMID.value:
            return Pyramid()
        elif geometry_type == GEOMETRY_TYPE.PENTAGON.value:
            return Pentagon()
        elif geometry_type == GEOMETRY_TYPE.HEXAGON.value:
            return Hexagon()
        elif geometry_type == GEOMETRY_TYPE.OCTAGON.value:
            return Octagon()
        elif geometry_type == GEOMETRY_TYPE.HEPTAGON.value:
            return Heptagon()
        elif geometry_type == GEOMETRY_TYPE.QUAD.value:
            return Quad()
        elif geometry_type == GEOMETRY_TYPE.TRIANGLE.value:
            return Triangle()
        
    def get_material(self,material_type):
        if material_type == 0:
            return PointMaterial()
        elif material_type == 1:
            return LineMaterial()
        elif material_type == 2:
            return SurfaceMaterial()
        elif material_type == 3:
            return FlatMaterial(number_of_lights=self.lights_in_scene)
        elif material_type == 4:
            return LambertMaterial(number_of_lights=self.lights_in_scene)
        elif material_type == 5:
            return PhongMaterial(number_of_lights=self.lights_in_scene)
        else:
            raise ValueError(f"Unknown material type: {material_type}")
        
class LightSpawner:
    def __init__(self):
        self._location = None
        self.display_light_tools = True
        self.use_lights_in_scene = False
        self._light = None
        self._light_type = 0
        self._light_color = [1, 1, 1, 1] # default white light
        self._light_counter = 0

    @property
    def light(self):
        return self._light
    
    @property
    def color(self):
        return self._light_color
    
    @property
    def count(self):
        return self._light_counter

    def show(self):
        imgui.text("Light Type:")
        imgui.set_next_item_width(100)
        _,self._light_type = imgui.combo("##Light Type", self._light_type, ["Point", "Directional", "Ambient"])

        # add color picker for light color
        imgui.text("Light Color:")
        imgui.same_line()

        _,self._light_color = imgui.color_edit4("Light Color", *self._light_color)

        # if the generate light button is pressed, create a new light of the selected type otherwise set the light to None
        self._light = self._make_light(self._light_type) if imgui.button("Generate Light") else None

        if self._light is not None:
            self._light_counter += 1

        # Create checkboxes for light options
        imgui.same_line()
        _,self.display_light_tools = imgui.checkbox("show Light Tools", self.display_light_tools)
        imgui.same_line()
        _,self.use_lights_in_scene = imgui.checkbox("Use Lights in Scene", self.use_lights_in_scene)
        
    def _make_light(self,light_type):
        # current no tool for ambient light so always simply return the light
        if light_type == 2:
            return AmbientLight(color=self._light_color[:3])

        # if not showing light tools, return the light without the tool
        if not self.display_light_tools:
            if light_type == 0:
                return PointLight(color=self._light_color[:3])
            elif light_type == 1:
                return DirectionalLight(color=self._light_color[:3])
        else: # if showing light tools, return the light with the tool
            if light_type == 0:
                light = PointLight(color=self._light_color[:3])
                light_tool = PointLightTool(light)
                light.add(light_tool)
                return light

            elif light_type == 1:
                light = DirectionalLight(color=self._light_color[:3])
                light_tool = DirectionalLightTool(light)
                light_tool.set_position([3, 4, 0])
                light.add(light_tool)
                return light

        # if the light type is not recognized, return None
        return None



class TerrainHandler:
    noise_functions = ["Perlin", "Simplex", "Value"]

    def __init__(self,chunk_size:int = 100, view_distance:int = 3, u_resolution:int = 100, v_resolution:int = 100):
        self.chunk_size = chunk_size
        self.view_distance = view_distance
        self.u_resolution = u_resolution
        self.v_resolution = v_resolution
        self._terrain_manager = InfiniteTerrainManager(chunk_size=chunk_size, view_distance=view_distance, u_resolution=u_resolution, v_resolution=v_resolution)
        self.update_terrain = False
        self.noise_function_type = 0  # Default to Perlin noise

    @property
    def terrain_manager(self):
        return self._terrain_manager
    
    @terrain_manager.setter
    def terrain_manager(self, terrain_manager: InfiniteTerrainManager):
        self._terrain_manager = terrain_manager
    
    def show(self):
        imgui.text("Terrain Manager:")
        imgui.separator()
        imgui.text("Chunk Size:")
        imgui.set_next_item_width(100)
        changed, chunk_size = imgui.input_int("##Chunk Size", self.chunk_size)
        if changed:
            self.chunk_size = chunk_size
   
        imgui.text("View Distance:")
        imgui.set_next_item_width(100)
        changed, view_distance = imgui.input_int("##View Distance", self.view_distance)
        if changed:
            self.view_distance = view_distance


        imgui.text("U Resolution:")
        imgui.set_next_item_width(100)
        changed, u_resolution = imgui.input_int("##U Resolution", self.u_resolution)
        if changed:
            self.u_resolution = u_resolution

        imgui.text("V Resolution:")
        imgui.set_next_item_width(100)
        changed, v_resolution = imgui.input_int("##V Resolution", self.v_resolution)
        if changed:
            self.v_resolution = v_resolution

        imgui.separator()
        imgui.text("Terrain Geometry:")
        imgui.separator()
        imgui.text("Noise function type:")
       
        imgui.set_next_item_width(100)
        changed, noise_function_type = imgui.combo("##Noise Function Type", self.noise_function_type, ["Perlin", "Simplex", "Value"])
        if changed:
            print("Noise function type changed to: ", noise_function_type)
            # self.noise_function_type = noise_function_type
            # if self.noise_function_type == 0:

        imgui.text("Surface Function (u,v):")
        imgui.set_next_item_width(300)
        imgui.text("X(u,v) = ")
        imgui.same_line()
        changed, x_function = imgui.input_text("##xfunction", "u + noise([u,v]) * 0.3")
        if changed:
            print("X function changed to: ", x_function)

        imgui.set_next_item_width(300)
        imgui.text("Y(u,v) = ")
        imgui.same_line()
        changed, y_function = imgui.input_text("##yfunction", "sin(u*v)")
        if changed:
            print("Y function changed to: ", y_function)
        
        imgui.set_next_item_width(300)
        imgui.text("Z(u,v) = ")
        imgui.same_line()
        changed, z_function = imgui.input_text("##Z(u,v) = ", "v + noise([u,v]) * 0.1")
        if changed:
            print("Z function changed to: ", z_function)

        imgui.separator()

        if imgui.button("Update Terrain"):
            self.terrain_manager = InfiniteTerrainManager(chunk_size=self.chunk_size, view_distance=self.view_distance, u_resolution=self.u_resolution, v_resolution=self.v_resolution)
            self.update_terrain = True
        else:
            self.update_terrain = False