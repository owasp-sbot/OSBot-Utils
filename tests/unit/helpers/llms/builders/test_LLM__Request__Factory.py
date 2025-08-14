from unittest                                                           import TestCase
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI    import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.builders.LLM_Request__Factory             import LLM_Request__Factory
from osbot_utils.helpers.llms.schemas.Safe_Str__LLM__Model_Name         import Safe_Str__LLM__Model_Name
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data         import Schema__LLM_Request__Data
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Text                        import Safe_Str__Text
from osbot_utils.utils.Objects                                          import __


class test_LLM__Request_Builder(TestCase):                               # Tests for the LLM request building functionality.

    def setUp(self):                                                     # Set up test resources.
        self.factory = LLM_Request__Factory()

    def test_create_simple_request(self):                               # Test creating a simple request without function calling.
        model         = Safe_Str__LLM__Model_Name("gpt-4" )
        provider      = Safe_Str__Text          ("openai")
        platform      = Safe_Str__Text          ("openai")
        system_prompt = "You are a helpful assistant."
        user_message  = "Tell me about Python."
        self.factory.create_simple_chat_request(model         = model        ,
                                                provider      = provider     ,
                                                platform      = platform     ,
                                                system_prompt = system_prompt,
                                                user_message  = user_message )
        with self.factory.request_data() as _:
            assert type(_) is Schema__LLM_Request__Data
            assert _.obj() == __(function_call = None     ,
                                       temperature   = None     ,
                                       top_p         = None     ,
                                       max_tokens    = None     ,
                                       model         = model    ,
                                       platform      = platform ,
                                       provider      = provider ,
                                       messages      =[ __(role='SYSTEM', content=system_prompt),
                                                        __(role='USER'  , content=user_message )])

    def test_build_openai_payload(self):                                # Test building an OpenAI-specific payload.
        self.factory.request_builder = LLM_Request__Builder__Open_AI()
        model        = "gpt-4"
        provider     = "openai"
        platform     = "oai"
        user_message = "Tell me about Python."
        self.factory.create_simple_chat_request(model        = model       ,
                                                provider     = provider    ,
                                                platform     = platform    ,
                                                user_message = user_message)

        payload = self.factory.build_request_payload()

        assert payload["model"]                    == model
        assert len(payload["messages"])            == 1
        assert payload["messages"][0]["role"]      == "user"
        assert payload["messages"][0]["content"]   == user_message