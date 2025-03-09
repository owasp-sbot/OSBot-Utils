from typing                                                      import List, Optional
from unittest                                                    import TestCase

import pytest

from osbot_utils.helpers.llms.actions.LLM_Request_Factory        import LLM_Request_Factory
from osbot_utils.helpers.llms.builders.LLM_Request_Builder import LLM_Request_Builder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data  import Schema__LLM_Request__Data
from osbot_utils.type_safe.Type_Safe                             import Type_Safe
from osbot_utils.type_safe.validators.Validator__Min             import Min
from osbot_utils.type_safe.validators.Validator__Max             import Max
from osbot_utils.helpers.python_compatibility.python_3_8         import Annotated
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects                                  import __


class test_LLM_Request_Builder(TestCase):                               # Tests for the LLM request building functionality.

    @classmethod
    def setUpClass(cls):                                                # Set up test resources.
        pytest.skip("fix after refactoring of LLM_Request_Builder")
        cls.builder = LLM_Request_Builder()
        cls.factory = LLM_Request_Factory()

    def test_create_message(self):                                      # Test creating a message object.
        message = self.builder.create_message(role="user", content="Hello")
        assert message.role    ==  "user"
        assert message.content == "Hello"

    def test_create_simple_request(self):                               # Test creating a simple request without function calling.
        model         = "gpt-4"
        provider      = "openai"
        platform      = "openai"
        system_prompt = "You are a helpful assistant."
        user_message  = "Tell me about Python."
        request = self.factory.create_simple_chat_request(model         = model        ,
                                                          provider      = provider     ,
                                                          platform      = platform     ,
                                                          system_prompt = system_prompt,
                                                          user_message  = user_message )

        assert type(request) is Schema__LLM_Request__Data
        assert request.obj() == __(function_call = None     ,
                                   temperature   = None     ,
                                   top_p         = None     ,
                                   max_tokens    = None     ,
                                   model         = model    ,
                                   platform      = platform ,
                                   provider      = provider ,
                                   messages      =[ __(role='system', content=system_prompt),
                                                    __(role='user'  , content=user_message )])

    def test_build_openai_payload(self):                                # Test building an OpenAI-specific payload.
        model        = "gpt-4"
        provider     = "openai"
        platform     = "oai"
        user_message = "Tell me about Python."
        request = self.factory.create_simple_chat_request(model        = model       ,
                                                          provider     = provider    ,
                                                          platform     = platform    ,
                                                          user_message = user_message)

        payload = self.builder.build_request_payload(request)

        assert payload["model"]                    == model
        assert len(payload["messages"])            == 1
        assert payload["messages"][0]["role"]      == "user"
        assert payload["messages"][0]["content"]   == user_message

    def test_build_anthropic_payload(self):                              # Test building an Anthropic-specific payload.
        model        = "claude-3-opus-20240229"
        provider     = "anthropic"
        platform     = "claude"
        user_message = "Tell me about Python."
        request = self.factory.create_simple_chat_request(model        = model       ,
                                                          provider     = provider    ,
                                                          platform     = platform    ,
                                                          user_message = user_message)

        payload = self.builder.build_request_payload(request)

        assert payload["model"]                    == model
        assert len(payload["messages"])            == 1
        assert payload["messages"][0]["role"]      == "user"
        assert payload["messages"][0]["content"]   == user_message

    def test_function_calling(self):                                     # Test creating a request with function calling.

        class TestEntity(Type_Safe):                                     # Define an entity schema for testing
            name : str
            score: Annotated[float, Min(0), Max(1)]
            tags : List[str]

        model         = "gpt-4"
        provider      = "openai"
        platform      = "oai"
        parameters    = TestEntity
        function_name = "extract_test_entity"
        function_desc = "Extract test entity from text"
        user_message  = "Extract from: John has a score of 0.85 and tags: python, testing."

        request = self.factory.create_function_calling_request(model         = model        ,
                                                               provider      = provider     ,
                                                               platform      = platform     ,
                                                               parameters    = parameters   ,
                                                               function_name = function_name,
                                                               function_desc = function_desc,
                                                               user_message  = user_message )

        assert request.function_call               is not None
        assert request.function_call.function_name == function_name
        assert request.function_call.parameters    == parameters

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
        assert request.obj() == __(function_call    =__(parameters    = 'test_LLM_Request_Builder.TestEntity',
                                                        function_name = 'extract_test_entity'                ,
                                                        description   = 'Extract test entity from text'      ),
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

    def test_entity_extraction_request(self):                            # Test creating a specialized entity extraction request.

        class PersonEntity(Type_Safe):                                    # Define an entity schema for extraction
            name       : str
            age        : Optional[int]  = None
            occupation : Optional[str]  = None

        model           = "gpt-4"
        provider        = "openai"
        platform        = "oai"
        entity_class    = PersonEntity
        function_name   = "extract_entities"
        text_to_analyze = "John Smith is a 35-year-old software engineer."

        request = self.factory.create_entity_extraction_request(model           = model          ,
                                                                provider        = provider       ,
                                                                platform        = platform       ,
                                                                entity_class    = entity_class   ,
                                                                text_to_analyze = text_to_analyze)

        assert request.function_call.function_name == function_name
        assert request.function_call.parameters    == entity_class

        payload = self.builder.build_request_payload(request)              # Build and check the payload

        system_message_found = False                                       # Verify the system message contains extraction instructions
        for msg in payload["messages"]:
            if msg["role"] == "system" and "expert at analyzing text" in msg["content"]:
                system_message_found = True
                break
        assert system_message_found is True

        user_message_found = False                                         # Verify the user message contains the text to analyze
        for msg in payload["messages"]:
            if msg["role"] == "user" and text_to_analyze in msg["content"]:
                user_message_found = True
                break
        assert user_message_found is True

        schema = payload["tools"][0]["function"]["parameters"]             # Verify the schema properties
        assert "name"       in schema["properties"]
        assert "age"        in schema["properties"]
        assert "occupation" in schema["properties"]