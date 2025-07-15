from core.objects.object3D import Object3D
from math import pi
import glfw.GLFW as GLFW_CONSTANTS

class MovementRig(Object3D):
    def __init__(self, units_per_second:int = 16,degrees_per_second:int = 45):
        super().__init__()

        # child for handling looking up and down
        self.look_attachment = Object3D()

        self.children = [self.look_attachment]

        self.look_attachment.parent = self


        # controls rate of movement
        self.units_per_second = units_per_second
        self.degrees_per_second = degrees_per_second


    def add(self, obj):
        super().add(obj)
        self.look_attachment.add(obj)


    def remove(self, obj):
        self.look_attachment.remove(obj)


    def update(self,input:object,delta_time:float) -> None:
        move_amount = self.units_per_second * delta_time
        rotate_amount = self.degrees_per_second * (pi/180) * delta_time

        ### =========== MOVEMENT =================
            ### =========== Linear Movement =================
        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_W):
            self.translate(0,0,-move_amount)

        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_S):
            self.translate(0,0,move_amount)
        
        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_A):
            self.translate(-move_amount,0,0)

        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_D):
            self.translate(move_amount,0,0)

        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_R):
            self.translate(0,move_amount,0)

        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_F):
            self.translate(0,-move_amount,0)
            ### =========== ROTATION =================
        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_Q):
            self.rotate_y(rotate_amount)
        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_E):
            self.rotate_y(-rotate_amount)


        ### =========== LOOKING UP AND DOWN =================
        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_T):
            self.look_attachment.rotate_x(rotate_amount)

        if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_G):
            self.look_attachment.rotate_x(-rotate_amount)

        # ### =========== LOOKING LEFT AND RIGHT =================
        # if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_Y):
        #     self.look_attachment.rotate_y(rotate_amount)
        # if input.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_H):
        #     self.look_attachment.rotate_y(-rotate_amount)





                