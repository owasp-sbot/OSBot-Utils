from typing                                                                 import List
from unittest                                                               import TestCase
from osbot_utils.helpers.llms.builders.LLM_Request__Factory                 import LLM_Request__Factory
from osbot_utils.helpers.llms.builders.LLM_Request__Builder                 import LLM_Request__Builder
from osbot_utils.helpers.llms.schemas.Safe_Str__LLM__Model_Name             import Safe_Str__LLM__Model_Name
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data             import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role    import Schema__LLM_Request__Message__Role
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Text                            import Safe_Str__Text
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.validators.Validator__Min                        import Min
from osbot_utils.type_safe.validators.Validator__Max                        import Max
from osbot_utils.helpers.python_compatibility.python_3_8                    import Annotated
from osbot_utils.utils.Objects                                              import __


class test_LLM__Request_Builder(TestCase):                               # Tests for the LLM request building functionality.

    def setUp(self):                                                     # Set up test resources.
        #pytest.skip("fix after refactoring of LLM_Request_Builder")
        self.builder = LLM_Request__Builder()
        self.factory = LLM_Request__Factory()

    def test_add_message(self):                                      # Test creating a message object.
        role    = Schema__LLM_Request__Message__Role.USER
        content = "an message"

        with self.builder  as _:
            assert _.llm_request_data.messages == []
            assert _.add_message(role=role, content=content) == _
            assert _.llm_request_data.messages[0].json() == Schema__LLM_Request__Message__Content(role=role, content=content).json()

    def test_add_message__assistant(self):
        role    = Schema__LLM_Request__Message__Role.ASSISTANT
        content = "an assistant message"
        with self.builder as _:
            assert _.add_message__assistant(content=content) == _
            assert _.llm_request_data.messages[0].json() == Schema__LLM_Request__Message__Content(role=role, content=content).json()

    def test_add_message__system(self):
        role    = Schema__LLM_Request__Message__Role.SYSTEM
        content = "an system message"
        with self.builder as _:
            assert _.add_message__system(content=content) == _
            assert _.llm_request_data.messages[0].json() == Schema__LLM_Request__Message__Content(role=role, content=content).json()

    def test_add_message__user(self):
        role    = Schema__LLM_Request__Message__Role.USER
        content = "an user message"
        with self.builder as _:
            assert _.add_message__user(content=content) == _
            assert _.llm_request_data.messages[0].json() == Schema__LLM_Request__Message__Content(role=role, content=content).json()


    def test_create_function_calling_request(self):                                         # Test creating a request with function calling.

        class TestEntity(Type_Safe):                                                        # Define an entity schema for testing
            name : str
            score: Annotated[float, Min(0), Max(1)]
            tags : List[str]

        model         = Safe_Str__LLM__Model_Name("gpt-4" )
        provider      = Safe_Str__Text("openai")
        platform      = Safe_Str__Text("oai"   )
        parameters    = TestEntity
        function_name = "extract_test_entity"
        function_desc = "Extract test entity from text"
        user_message  = "Extract from: John has a score of 0.85 and tags: python, testing."

        self.factory.create_function_calling_request(model         = model        ,
                                                    provider      = provider     ,
                                                    platform      = platform     ,
                                                    parameters    = parameters   ,
                                                    function_name = function_name,
                                                    function_desc = function_desc,
                                                    user_message  = user_message )
        with self.factory.request_data() as _:
            assert _.function_call               is not None
            assert _.function_call.function_name == function_name
            assert _.function_call.parameters    == parameters
            assert _.obj() == __(function_call = __(parameters    = 'test_LLM__Request__Builder.TestEntity',
                                                    function_name = 'extract_test_entity'                  ,
                                                    description   = 'Extract test entity from text'        ),
                                 temperature   = None    ,
                                 top_p         = None    ,
                                 max_tokens    = None    ,
                                 model         = 'gpt-4' ,
                                 platform      = 'oai'   ,
                                 provider      = 'openai',
                                 messages      =[ __( role    = 'USER'                                                              ,
                                                      content = 'Extract from: John has a score of 0.85 and tags: python, testing.')])


        return
        payload = self.builder.build_request_payload(request)            # Build and check payload

        assert "tools"                                               in payload
        assert payload["tools"][0]["function"]["name"]                == function_name
        assert "parameters"                                           in payload["tools"][0]["function"]
        assert "properties"                                           in payload["tools"][0]["function"]["parameters"]
        assert "name"                                                 in payload["tools"][0]["function"]["parameters"]["properties"]
        assert "score"                                                in payload["tools"][0]["function"]["parameters"]["properties"]
        assert "tags"                                                 in payload["tools"][0]["function"]["parameters"]["properties"]

        assert "tool_choice"                                          in payload
        assert payload["tool_choice"]["function"]["name"]             == function_name

        assert type(request) is Schema__LLM_Request__Data
        assert type(payload) is dict
        assert request.obj() == __(function_call    =__(parameters    = 'test_LLM_Request__Builder.TestEntity',
                                                        function_name = 'extract_test_entity'                 ,
                                                        description   = 'Extract test entity from text'       ),
                                   temperature  =None       ,
                                   top_p        =None       ,
                                   max_tokens   =None       ,
                                   model        ='gpt-4'    ,
                                   platform=    'oai'       ,
                                   provider     ='openai'   ,
                                   messages     =[ __(role='user', content='Extract from: John has a score of 0.85 and tags: python, testing.')])
        assert payload == {'messages'       : [{'content' : 'Extract from: John has a score of 0.85 and tags: python, testing.',
                                                'role'    : 'user'                          }],
                           'model'          : 'gpt-4'                                       ,
                           'response_format': { 'type'    : 'json_object'                   },
                           'tool_choice'    : { 'function': {'name' : 'extract_test_entity' },
                                                'type'    : 'function'                      },
                           'tools'          : [{'function': {'description': 'Extract test entity from text',
                                                             'name'       : 'extract_test_entity',
                                                             'parameters' : {'properties': {'name' : { 'type'   : 'string'          },
                                                                                            'score': { 'maximum': 1                 ,
                                                                                                       'minimum': 0                 ,
                                                                                                       'type'   : 'number'          },
                                                                                            'tags' : { 'items'  : {'type': 'string' },
                                                                                                       'type'   : 'array'           }},
                                                                             'required'  : ['name', 'score', 'tags']                ,
                                                                             'type'      : 'object'                                 }},
                                                'type'    : 'function'}]}