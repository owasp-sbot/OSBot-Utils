from osbot_utils.helpers.Obj_Id         import Obj_Id
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__LLM_Response(Type_Safe):
    response_id   : Obj_Id
    timestamp     : Timestamp_Now
    response_data : dict