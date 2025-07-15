import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import ctypes
from core.utils.openGLUtils import GlUtils
# from core.base import .


from core.base import SceneEditor
        
# Run the application
if __name__ == "__main__":

    app = SceneEditor( width=1280, height=720,display_grid=False,static_camera=False)
    app.run()
