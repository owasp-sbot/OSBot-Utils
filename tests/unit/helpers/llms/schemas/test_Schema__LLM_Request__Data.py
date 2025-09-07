from typing                                                                 import List
from unittest                                                               import TestCase
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data             import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role    import Schema__LLM_Request__Message__Role
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                                  import Type_Safe__List
from osbot_utils.utils.Objects                                              import __


class test_Schema__LLM_Request__Data(TestCase):

    def test__init__(self):
        with Schema__LLM_Request__Data() as _:
            assert type(_) is Schema__LLM_Request__Data
            assert _.obj()  == __( function_call = None ,
                                   temperature   = None ,
                                   top_p         = None ,
                                   max_tokens    = None ,
                                   model         = ''   ,
                                   platform      = ''   ,
                                   provider      = ''   ,
                                   messages      = []   )
            assert type(_.messages) is Type_Safe__List
            assert _.messages.expected_type == Schema__LLM_Request__Message__Content

    def test_json_roundtrip_from_json(self):
        json_data  =  { 'function_call': None                                 ,
                        'max_tokens'   : 100                                  ,
                        'messages'     : [ { 'content': 'Test disk retrieval' ,
                                             'role'   : 'user'}]              ,
                        'model'        : 'test-model'                         ,
                        'platform'     : 'test-platform'                      ,
                        'provider'     : 'test-provider'                      ,
                        'temperature'  : 0.7                                  ,
                        'top_p'        : None                                 }
        # expected_error = "Invalid type for attribute 'role'. Expected '<enum 'Schema__LLM_Request__Message__Role'>' but got '<class 'str'>'"
        # with pytest.raises(ValueError, match=expected_error):
        assert Schema__LLM_Request__Data.from_json(json_data).json() == json_data

    def test__regression__messages__json_roundtrip(self):
        class An_Class(Type_Safe):
            messages: List[Schema__LLM_Request__Message__Content]

        json_data = {'messages': [ { 'content': 'Test disk retrieval' ,
                                     'role'   : 'user'                }]}

        # expected_error = "Invalid type for attribute 'role'. Expected '<enum 'Schema__LLM_Request__Message__Role'>' but got '<class 'str'>'"
        # with pytest.raises(ValueError, match=expected_error):
        #     An_Class.from_json(json_data)                         # FIXED: BUG

        an_class = An_Class.from_json(json_data)
        assert an_class.json() == json_data
        assert type(an_class.messages           ) is Type_Safe__List
        assert type(an_class.messages[0]        ) is Schema__LLM_Request__Message__Content
        assert type(an_class.messages[0].role   ) is Schema__LLM_Request__Message__Role
        assert type(an_class.messages[0].content) is str

        json_messages =  [ { 'content': 'Test disk retrieval' ,'role'   : 'user' }]
        messages      = Type_Safe__List(Schema__LLM_Request__Message__Content, json_messages)
        assert messages.json() == json_messages