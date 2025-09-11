from typing                                                                         import List, Optional
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Function_Call            import Schema__LLM_Request__Function_Call
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content         import Schema__LLM_Request__Message__Content
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.safe_float.llm.Safe_Float__LLM__Temperature   import Safe_Float__LLM__Temperature
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Model_Name        import Safe_Str__LLM__Model_Name
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text                  import Safe_Str__Text


class Schema__LLM_Request__Data(Type_Safe):                                         # Schema for LLM API request data
    model         : Safe_Str__LLM__Model_Name                                       # LLM model identifier
    platform      : Safe_Str__Text
    provider      : Safe_Str__Text
    messages      : List    [Schema__LLM_Request__Message__Content]                 # Message content entries
    function_call : Optional[Schema__LLM_Request__Function_Call  ] = None           # Details of function call
    temperature   : Optional[Safe_Float__LLM__Temperature        ] = None           # Model temperature (0-1)
    top_p         : Optional[float                               ] = None           # Nucleus sampling parameter
    max_tokens    : Optional[int                                 ] = None           # Maximum tokens to generate