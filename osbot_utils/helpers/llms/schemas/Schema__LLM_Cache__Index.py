from typing                                             import Dict
from osbot_utils.helpers.Obj_Id                         import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash        import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Schema__LLM_Cache__Index(Type_Safe):
    cache_id__from__hash__request            : Dict[Safe_Str__Hash, Obj_Id]                 # map hash of the full request to a Schema__LLM_Response__Cache Obj_Id
    cache_ids__from__hash__request__messages : Dict[Safe_Str__Hash, set[Obj_Id]]            # map hash of the messages to a Schema__LLM_Response__Cache Obj_Id
    cache_id__to__file_path                  : Dict[Obj_Id        , Safe_Str__File__Path]