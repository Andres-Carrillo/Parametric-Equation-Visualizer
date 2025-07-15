import enum

class ShaderType(enum.Enum):
    VERTEX = 0
    FRAGMENT = 1
    GEOMETRY = 2
    COMPUTE = 3
    TESSELLATION_CONTROL = 4
    TESSELLATION_EVALUATION = 5

    def __str__(self):
        return self.name.lower()

def edit_light_list(material:object,number_of_lights:int,shader:ShaderType = ShaderType.FRAGMENT) -> None:
        """
        Given a material and a number of lights,
        find the ##LIGHT_LIST##  tag in the shader code 
        and replace it with the light uniforms
        :return: str
        """
        code = material.vertex_shader if shader == ShaderType.VERTEX else material.fragment_shader
        
        # start after the begin tag
        start = code.find("<LIGHT_LIST_BEGIN>") #+ len("<LIGHT_LIST_BEGIN>")

        # end before the end tag
        end = code.find("<LIGHT_LIST_END>",start) + len("<LIGHT_LIST_END>")
    
        #if the tag is not found, return False for debugging
        if start == -1 or end == -1:
            return False
        
        light_list = generate_light_uniform_list(number_of_lights)

        # replace the tag and the code after it with the light uniforms
        code = code[:start] + light_list  + "\n" + code[end:]

        # update the shader code
        if shader == ShaderType.VERTEX:
            material.vertex_shader = code
        else:
            material.fragment_shader = code

        # if the shader code is valid, return True
        return True




def edit_light_summation(material:object,number_of_lights:int,shader:ShaderType = ShaderType.FRAGMENT) -> None:
        """
        Given a material and a number of lights,
        find the ##LIGHT_SUMMATION##  tag in the shader code 
        and replace it with the light uniforms
        :return: str
        """
        code = material.vertex_shader if shader == ShaderType.VERTEX else material.fragment_shader

        # start after the begin tag
        start = code.find("//<LIGHT_SUMMATION_START>") 

        # end before the end tag
        end = code.find("//<LIGHT_SUMMATION_END>",start)
    
        #if the tag is not found, return False for debugging
        if start == -1 or end == -1:
            return False
        
        light_calculation = generate_light_sum(number_of_lights)

        # replace the tag and the code after it with the light uniforms
        code = code[:start] + light_calculation  + "\n" + code[end:]

        # update the shader code
        if shader == ShaderType.VERTEX:
            material.vertex_shader = code
        else:
            material.fragment_shader = code

        # if the shader code is valid, return True
        return True


def find_tag(shader_code:str,start_tag:str,end_tag:str) -> str:
    """
    Given a shader code and a tag,
    find the tag in the shader code 
    and return the code before and after the tag
    :return: str
    """
    # find the tag in the shader code
    start = shader_code.find(start_tag)
    end = shader_code.find(end_tag,start) + 1

    # if the tag is not found, return None
    if start == -1 or end == -1:
        return None

    # return the code before and after the tag
    return start, end


    #  method to generate the glsl code for the light uniforms

def generate_light_uniform_list(number_of_lights:int = 1) -> str:
        """
        Generates the light uniforms for the shader
        :return: str
        """
        code = "\n   \t\t\t\t// <LIGHT_LIST_BEGIN> \n \n"

        for i in range(number_of_lights):
            code += f"   \t\t\t\tuniform Light light_{i};\n"

        code += "\n   \t\t\t\t// <LIGHT_LIST_END> \n"
        
        return code
    
    # method to generate the glsl code for summing the effect of all the lights
    # in the scene
def generate_light_sum(number_of_lights:int = 1) -> str:
        """"
            For calculating the effect of all the lights in the scene.
            This allows the user to add as many lights as they want
            and the shader will handle the calculations.
            :return: str
        """

        code = "\n\t\t\t\t\t//<LIGHT_SUMMATION_START>\n"
        for i in range(number_of_lights):
            code += f"\t\t\t\t\tlight += calculate_light(light_{i}, position, calculated_normal);\n"


        code += "\n \t\t\t\t\t//<LIGHT_SUMMATION_END>\n"
        return code
    