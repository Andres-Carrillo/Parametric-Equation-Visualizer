from core.utils.math import Math as RenderMath
from core.tools.point_light_tool import PointLightTool
from core.tools.directional_light_tool import DirectionalLightTool
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np

def rodrigues_rotation_matrix(axis, theta):
    """
    Returns the rotation matrix using Rodrigues' rotation formula.
    axis: 3-element array-like, should be normalized
    theta: rotation angle in radians
    """
    axis = np.asarray(axis, dtype=np.float64)
    axis = axis / np.linalg.norm(axis)
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    I = np.eye(3)
    R = I + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    # Convert to 4x4 matrix
    R4 = np.eye(4)
    R4[:3, :3] = R
    return R4


def ray_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal):
    """
    Find the intersection point of a ray and a plane.
    ray_origin: np.array([x, y, z]) - origin of the ray (camera position)
    ray_direction: np.array([dx, dy, dz]) - normalized direction of the ray
    plane_point: np.array([x, y, z]) - a point on the plane (e.g., object's original position)
    plane_normal: np.array([nx, ny, nz]) - normal vector of the plane (e.g., [0, 1, 0] for y=constant)
    Returns: intersection point as np.array([x, y, z]) or None if no intersection
    """
    ray_direction = ray_direction / np.linalg.norm(ray_direction)
    denom = np.dot(plane_normal, ray_direction)
    if abs(denom) < 1e-6:
        return None  # Ray is parallel to the plane
    t = np.dot(plane_point - ray_origin, plane_normal) / denom
    if t < 0:
        return None  # Intersection is behind the ray origin
    intersection = ray_origin + t * ray_direction
    return intersection

def choose_drag_plane(ray_direction, mesh_position):
    # Find the axis least aligned with the ray direction
    abs_dir = np.abs(ray_direction)
    # The axis with the smallest component is the best normal
    axis = np.argmin(abs_dir)
    if axis == 0:
        # X is the best normal, so use the YZ plane (normal [1,0,0])
        plane_normal = np.array([1, 0, 0])
        plane_point = np.array(mesh_position)
    elif axis == 1:
        # Y is the best normal, so use the XZ plane (normal [0,1,0])
        plane_normal = np.array([0, 1, 0])
        plane_point = np.array(mesh_position)
    else:
        # Z is the best normal, so use the XY plane (normal [0,0,1])
        plane_normal = np.array([0, 0, 1])
        plane_point = np.array(mesh_position)
    return plane_point, plane_normal


def drag_object(mouse_position, mesh, camera,width,height,input_handler):
  # Get ray origin and direction from your camera and mouse
    ray_origin = np.array(camera.global_position)  # or self.camera.global_position
    ray_direction = RenderMath.ray_cast(mouse_position, camera, width, height)

    if input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_1):
        plane_point = np.array([0, mesh.global_position[1], mesh.global_position[2]])
        plane_normal = np.array([1, 0, 0])
    else:
        plane_point = np.array([mesh.global_position[0], mesh.global_position[1], 0])
        plane_normal = np.array([0, 0, 1])
    
    new_pos = ray_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal)
    
    if new_pos is not None:
            if isinstance(mesh,PointLightTool) or isinstance(mesh,DirectionalLightTool):
                mesh.light_reference.set_position(new_pos)
            else:
                mesh.set_position(new_pos)