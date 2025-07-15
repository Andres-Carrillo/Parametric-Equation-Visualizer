import glfw
import glfw.GLFW as GLFW_CONSTANTS

class Input(object):
    def __init__(self) -> None:
        self.quit = False
        self.key_queue = set()
        # self.key_down_list = []
        self.key_pressed_list = set()
        self.key_held_list = set()
        self.key_released_list = set()
        self.mouse_buttons = set()
        self._mouse_position = (0, 0)
        self.mouse_wheel = (0, 0)
        self.mouse_wheel_delta = (0, 0)
        self.mouse_held = False
        self.imgui_renderer = None

    @property
    def mouse_position(self):
        return self._mouse_position


    def set_callbacks(self,window,imgui_renderer=None)->None:
        self.imgui_renderer = imgui_renderer    
        def key_callback(window, key, scancode, action, mods):
            self.key_callback(window, key, scancode, action, mods)
            if self.imgui_renderer is not None:
                self.imgui_renderer.keyboard_callback(window, key, scancode, action, mods)
        glfw.set_key_callback(window, key_callback)

        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(window, self.cursor_position_callback)


    def key_callback(self, window, key, scancode, action, mods):
        if self.imgui_renderer is not None:
            self.imgui_renderer.keyboard_callback(window, key, scancode, action, mods)
        if key == GLFW_CONSTANTS.GLFW_KEY_BACKSPACE:
            print("Backspace pressed")
        
        if action == GLFW_CONSTANTS.GLFW_PRESS: 
            self.key_pressed_list.add(key)
            self.key_queue.add(key)

        elif action == GLFW_CONSTANTS.GLFW_RELEASE:
            self.key_pressed_list.remove(key)   

        if key == GLFW_CONSTANTS.GLFW_KEY_ESCAPE and action == GLFW_CONSTANTS.GLFW_PRESS:
            self.quit = True

    def mouse_button_callback(self, window, button, action, mods):
        if action == GLFW_CONSTANTS.GLFW_PRESS:
            self.mouse_buttons.add(button)
            self.mouse_held = True
        elif action == GLFW_CONSTANTS.GLFW_RELEASE:
            self.mouse_buttons.remove(button)
            self.mouse_held = False

    def right_click(self):
        return GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_RIGHT in self.mouse_buttons
    
    def left_click(self):
        return GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_LEFT in self.mouse_buttons
    
    def middle_click(self):
        return GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_MIDDLE in self.mouse_buttons
    

    def mouse_wheel_callback(self, window, xoffset, yoffset):
        self.mouse_wheel = (xoffset, yoffset)
        self.mouse_wheel_delta = (xoffset, yoffset)


    def cursor_position_callback(self, window, xpos, ypos):
        self._mouse_position = (xpos, ypos)


    def is_key_pressed(self, key) -> bool:
        return key in self.key_pressed_list
    
    def is_key_held(self, key) -> bool:
        pass

    def is_key_released(self, key) -> bool:
        return key in self.key_released_list

    def update(self) -> None:
        glfw.poll_events()

        