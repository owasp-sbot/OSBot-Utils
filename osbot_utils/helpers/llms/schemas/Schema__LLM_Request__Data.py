from typing                                                                 import List, Optional
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Function_Call    import Schema__LLM_Request__Function_Call
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.safe_str.Safe_Str__Text                            import Safe_Str__Text
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe

class Schema__LLM_Request__Data(Type_Safe):                                         # Schema for LLM API request data
    model         : Safe_Str__Text                                                  # LLM model identifier
    platform      : Safe_Str__Text
    provider      : Safe_Str__Text
    messages      : List    [Schema__LLM_Request__Message__Content]                 # Message content entries
    function_call : Optional[Schema__LLM_Request__Function_Call  ] = None           # Details of function call
    temperature   : Optional[float                               ] = None           # Model temperature (0-1)
    top_p         : Optional[float                               ] = None           # Nucleus sampling parameter
    max_tokens    : Optional[int                                 ] = None           # Maximum tokens to generate