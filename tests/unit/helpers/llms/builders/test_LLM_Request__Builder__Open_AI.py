from typing                                                                  import List
from unittest                                                                import TestCase
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI         import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.builders.LLM_Request__Factory                  import LLM_Request__Factory
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Model_Name import Safe_Str__LLM__Model_Name
from osbot_utils.type_safe.Type_Safe                                         import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text           import Safe_Str__Text


class test_LLM_Request__Builder__Open_AI(TestCase):

    def setUp(self):
        self.request_builder = LLM_Request__Builder__Open_AI()
        self.request_factory = LLM_Request__Factory(request_builder=self.request_builder)

    def test_create_function_calling_request(self):                                         # Test creating a request with function calling.
        class TestEntity(Type_Safe):                                                        # Define an entity schema for testing
            name : str
            score: float
            tags : List[str]

        # score: Annotated[float, Min(0), Max(1)] # these annotations didn't work in open-ai structured outputs

        model         = Safe_Str__LLM__Model_Name("gpt-4o-mini")
        provider      = Safe_Str__Text("openai"     )
        platform      = Safe_Str__Text("oai"        )
        parameters    = TestEntity
        function_name = "extract_test_entity"
        function_desc = "Extract test entity from text"
        user_message  = "Extract from: John has a score of 0.85 and tags: python, testing."

        self.request_factory.create_function_calling_request(model         = model        ,
                                                             provider      = provider     ,
                                                             platform      = platform     ,
                                                             parameters    = parameters   ,
                                                             function_name = function_name,
                                                             function_desc = function_desc,
                                                             user_message  = user_message )
        with self.request_factory.request_data() as _:
            assert _.function_call               is not None
            assert _.function_call.function_name == function_name
            assert _.function_call.parameters    == parameters



        payload = self.request_builder.build_request_payload()            # Build and check payload
        assert payload == { 'messages': [ { 'content': 'Extract from: John has a score of 0.85 and tags: python, testing.',
                                            'role'   : 'user'                                                            }],
                            'model'   : 'gpt-4o-mini',
                            'response_format': { 'json_schema': { 'name'  : 'extract_test_entity',
                                                                  'schema': { 'additionalProperties': False,
                                                                              'properties'          : { 'name' : { 'type': 'string'           },
                                                                                                        'score': { 'type': 'number'           },
                                                                                                        'tags' : { 'items': { 'type': 'string'},
                                                                                                                   'type' : 'array'           }},
                                                                              'required'             : [ 'name', 'score','tags'                 ],
                                                                              'type'                 : 'object'                                 },
                                                                  'strict': True},
                                                 'type': 'json_schema'}}