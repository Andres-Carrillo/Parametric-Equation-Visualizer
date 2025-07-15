import numpy as np

class Math:
 
        @staticmethod
        def clamp(value, min_value, max_value):
            """Clamp a value between a minimum and maximum value."""
            return max(min(value, max_value), min_value)
    
        @staticmethod
        def lerp(start, end, t):
            """Linearly interpolate between two values."""
            return start + (end - start) * t
        

        @staticmethod
        def calclulate_normal(p0, p1, p2):
            """
            Calculate the normal vector of a triangle defined by three points.
            The normal vector is calculated using the cross product of two edges of the triangle.
            """
            v1 = np.array(p1) - np.array(p0)
            v2 = np.array(p2) - np.array(p0)
            orthogonal_vector = np.cross(v1, v2)
            norm = np.linalg.norm(orthogonal_vector)

            # protect against division by zero
            # if the normal vector is too small, return a default value
            normal_vector = orthogonal_vector / norm if norm > 1e-6 else np.array(p0) / np.linalg.norm(p0)

            return normal_vector
        

        @staticmethod
        def ray_cast(mouse_position, camera, width, height):
        
            x_normalized = (2.0*mouse_position[0]) / width - 1.0
            y_normalized = 1.0 - (2.0*mouse_position[1]) / height
            z = 1.0
            
            # Create a ray in normalized device coordinates
            ray_nds = [x_normalized, y_normalized, z]
            
            # Convert to world coordinates
            ray_clip = [ray_nds[0], ray_nds[1], -1.0, 1.0]
            ray_eye = np.linalg.inv(camera.projection_matrix)  @ ray_clip
            ray_eye = [ray_eye[0], ray_eye[1], -1.0, 0.0]
            ray_wor = np.linalg.inv(camera.view_matrix) @ ray_eye
            normalized_ray = [ray_wor[0], ray_wor[1], ray_wor[2]]
            
            # Normalize the ray
            length = (normalized_ray[0]**2 + normalized_ray[1]**2 + normalized_ray[2]**2)**0.5
            normalized_ray = [normalized_ray[0]/length, normalized_ray[1]/length, normalized_ray[2]/length]
            
            return normalized_ray
        

        @staticmethod
        def point_in_rectangle(point:list, rect:list)-> bool:
            """
            Check if a point is inside a rectangle defined by its top-left and bottom-right corners.
            :param point: Tuple (x, y) representing the point.
            :param rect: List [x1, y1, x2, y2] representing the rectangle (top-left and bottom-right corners).
            :return: True if the point is inside the rectangle, False otherwise.
            """
            x1, y1, x2, y2 = rect
            return x1 <= point[0] <= x2 and y1 <= point[1] <= y2

        @staticmethod
        def point_in_regions(point, deadzones):
            """
            Check if a point is inside any of the deadzones.
            :param point: Tuple (x, y) representing the point.
            :param deadzones: List of deadzones, where each deadzone is defined by [x1, y1, x2, y2].
            :return: True if the point is inside any deadzone, False otherwise.
            """

    
            if Math.point_in_rectangle(point, deadzones):
                    return True
                
            return False




