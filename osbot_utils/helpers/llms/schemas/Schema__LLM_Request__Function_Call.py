from typing                          import Type
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__LLM_Request__Function_Call(Type_Safe):
    parameters    : Type[Type_Safe]                     # Class to generate schema from for function calling
    function_name : str                                 # Name of the function to call
    description   : str                                 # Description of the function
