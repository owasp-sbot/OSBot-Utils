from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request   import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response  import Schema__LLM_Response
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class Schema__LLM_Response__Cache(Type_Safe):
    cache_id          : Obj_Id
    llm__payload      : dict
    llm__request      : Schema__LLM_Request  = None
    llm__response     : Schema__LLM_Response = None
    request__duration : float
    request__hash     : Safe_Str__Hash       = None
    timestamp         : Timestamp_Now

