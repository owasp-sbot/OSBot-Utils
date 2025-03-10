import pytest
import re
from unittest                                                               import TestCase
from osbot_utils.helpers.Obj_Id                                             import Obj_Id
from osbot_utils.helpers.Timestamp_Now                                      import Timestamp_Now
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                   import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data             import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role    import Schema__LLM_Request__Message__Role
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache           import Schema__LLM_Response__Cache
from osbot_utils.utils.Objects                                              import __

class test_Schema__LLM_Request(TestCase):

    def test_json_roundtrip(self):
        role         = Schema__LLM_Request__Message__Role.USER
        message      = Schema__LLM_Request__Message__Content(role         = role        , content='an_question')
        request_data = Schema__LLM_Request__Data            (messages     = [message]   )
        llm_request  = Schema__LLM_Request                  (request_data = request_data)

        assert llm_request.obj() == __(request_id   = llm_request.request_id,
                                       request_data = request_data.obj()   )

        assert Schema__LLM_Request                   .from_json(llm_request .json()).json() == llm_request .json()
        assert Schema__LLM_Request__Data             .from_json(request_data.json()).json() == request_data.json()
        assert Schema__LLM_Request__Message__Content.from_json(message      .json()).json() == message     .json()


    def test_json_roundtrip_from_json(self):
        json_llm_request  = { 'request_id'  : Obj_Id()                                                                ,
                              'request_data': { 'function_call': None                                                 ,
                                                                'max_tokens'   : 100                                  ,
                                                                'messages'     : [ { 'content': 'Test disk retrieval' ,
                                                                                     'role'   : 'USER'}]              ,
                                                                'model'        : 'test-model'                         ,
                                                                'platform'     : 'test-platform'                      ,
                                                                'provider'     : 'test-provider'                      ,
                                                                'temperature'  : 0.7                                  ,
                                                                'top_p'        : None                                 }}
        json_response_cache = { 'cache_id'               : Obj_Id()         ,
                                'hash__request'          : None             ,
                                'hash__request__messages': None             ,
                                'llm_request'            : json_llm_request ,
                                'llm_response'           : None             ,
                                'timestamp'               : Timestamp_Now() }
        Schema__LLM_Response__Cache.from_json(json_response_cache)

        assert Schema__LLM_Request.from_json        (json_llm_request   ).json() == json_llm_request
        assert Schema__LLM_Response__Cache.from_json(json_response_cache).json() == json_response_cache
