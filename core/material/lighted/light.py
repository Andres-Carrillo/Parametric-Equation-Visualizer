from core.material.basic.material import Material

class LightMaterial(Material):
    def __init__(self,number_of_lights:int = 0,vertex_shader_code:str = "",fragment_shader_code:str = "") -> None:   

        super().__init__(vertex_shader_code,fragment_shader_code)

        self.add_light_souces(number_of_lights)

    def add_light_souces(self,number_of_lights:int) -> None:
        """
        Given a number of lights, add the light sources to the shader
        :return: None
        """
        # need to find the number of lights already in the uniforms
        if number_of_lights < 1:
            self.add_uniform("using_lights", False, "bool")
            return
        
        cur_lights = 0
        for key in self.uniforms.keys():
            if "light_" in key:
                cur_lights += 1

        # if this is the first time we are adding lights set the using_lights uniform to True
        if cur_lights == 0 and number_of_lights > 0:
            self.add_uniform("using_lights", True, "bool")

        # if the number of lights is greater than the current number of lights
        # then we need to add the new lights
        if number_of_lights > cur_lights:
            # add the new lights
            for i in range(cur_lights,number_of_lights):
                self.add_uniform(f"light_{i}",None,"Light")
        




