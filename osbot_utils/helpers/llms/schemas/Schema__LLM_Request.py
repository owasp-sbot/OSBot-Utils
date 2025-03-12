from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data  import Schema__LLM_Request__Data
from osbot_utils.type_safe.Type_Safe                             import Type_Safe


class Schema__LLM_Request(Type_Safe):
    #request_id   : Obj_Id                      # can't put this id here or we won't be able to cache this data
    request_data : Schema__LLM_Request__Data