from typing                             import Dict
from osbot_utils.helpers.Obj_Id         import Obj_Id
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__LLM_Cache__Index(Type_Safe):
    hash__request  : Dict[int, Obj_Id]               # map hash of the full request to an Schema__LLM_Response__Cache Obj_Id
    hash__messages : Dict[int, set[Obj_Id]]          # map hash of the messages to an Schema__LLM_Response__Cache Obj_Id