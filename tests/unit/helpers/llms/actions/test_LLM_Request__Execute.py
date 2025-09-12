from unittest                                                                      import TestCase
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Id         import Safe_Str__LLM__Model_Id
from osbot_utils.helpers.llms.cache.LLM_Request__Cache                             import LLM_Request__Cache
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__File_System                import LLM_Request__Cache__File_System
from osbot_utils.helpers.llms.actions.LLM_Request__Execute                         import LLM_Request__Execute
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI               import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.cache.Virtual_Storage__Local__Folder                 import Virtual_Storage__Local__Folder
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                  import API__LLM__Open_AI, ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                          import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data                    import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content        import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role           import Schema__LLM_Request__Message__Role
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                         import Schema__LLM_Response
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                 import Safe_Str__Text
from osbot_utils.utils.Env                                                         import get_env, load_dotenv
from osbot_utils.utils.Files                                                       import folder_create

TEST__TEMP__ROOT_FOLDER = '/tmp/_osbot_utils/cache__test_LLM_Request__Execute'

class test_LLM_Request__Execute(TestCase):
    llm_execute       : LLM_Request__Execute
    llm_cache         : LLM_Request__Cache
    llm_api           : API__LLM__Open_AI
    api_key_available : bool

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.cache_root_folder = Safe_Str__File__Path(folder_create(TEST__TEMP__ROOT_FOLDER))
        cls.virtual_storage   = Virtual_Storage__Local__Folder (root_folder     = cls.cache_root_folder)
        cls.llm_cache         = LLM_Request__Cache__File_System(virtual_storage = cls.virtual_storage  ).setup()
        cls.llm_api           = API__LLM__Open_AI()
        cls.request_builder   = LLM_Request__Builder__Open_AI()
        cls.llm_execute       = LLM_Request__Execute(llm_cache       = cls.llm_cache      ,
                                                     llm_api         = cls.llm_api        ,
                                                     request_builder = cls.request_builder)
        cls.api_key_available = get_env(ENV_NAME_OPEN_AI__API_KEY) is not None

    def create_test_request(self, message_text: str = "Test message") -> Schema__LLM_Request:
        message = Schema__LLM_Request__Message__Content(role    = Schema__LLM_Request__Message__Role.USER,
                                                        content = message_text                           )

        request_data = Schema__LLM_Request__Data(model       = Safe_Str__LLM__Model_Id("gpt-4o-mini"),
                                                 platform    = Safe_Str__Text         ("OpenAI"     ),
                                                 provider    = Safe_Str__Text         ("OpenAI-API" ),
                                                 temperature = 0.7          ,
                                                 max_tokens  = 50           )      # Limit tokens to reduce costs

        request_data.messages.append(message)

        return Schema__LLM_Request(request_data=request_data)

    def create_test_response(self, content: str = "This is a test response") -> Schema__LLM_Response:
        return Schema__LLM_Response(response_data={"content": content})

    def test_cache_functionality(self):
        if not self.api_key_available:
            self.skipTest("OpenAI API key not available")

        # First request
        request        = self.create_test_request("Tell me a short joke about programming")
        first_response = self.llm_execute.execute(request)

        assert "response_data" in first_response.json()                         # Verify we got a response
        assert first_response.response_data is not None


        cached_response = self.llm_execute.execute(request)                     # Second request with same content should hit cache

        assert first_response.response_id == cached_response.response_id        # Verify we get the same response object
        assert first_response.timestamp   == cached_response.timestamp



    # def test_cache_disabled(self):
    #     if not self.api_key_available:
    #         self.skipTest("OpenAI API key not available")
    #
    #     # First request with cache enabled
    #     request = self.create_test_request("What is Python?")
    #     first_response = self.llm_execute.execute(request)
    #
    #     # Disable cache for second request
    #     self.llm_execute.use_cache = False
    #     second_response = self.llm_execute.execute(request)
    #
    #     # Verify we got a different response object
    #     assert first_response.response_id != second_response.response_id
    #     assert first_response.timestamp != second_response.timestamp

    def test_cache_with_different_parameters(self):
        if not self.api_key_available:
            self.skipTest("OpenAI API key not available")

        # Create first request
        request1 = self.create_test_request("What is artificial intelligence?")
        response1 = self.llm_execute.execute(request1)

        # Create second request with same message but different temperature
        request2 = self.create_test_request("What is artificial intelligence?")
        request2.request_data.temperature = 0.9  # Different temperature

        # Execute second request
        response2 = self.llm_execute.execute(request2)

        # Should be a different response (cache miss due to different params)
        assert response1.response_id != response2.response_id

        # But we should get a hit if we use the same request again
        response1_again = self.llm_execute.execute(request1)
        assert response1.response_id == response1_again.response_id

    # def test_api_errors(self):
    #     if not self.api_key_available:
    #         self.skipTest("OpenAI API key not available")
    #
    #     # Try with an invalid model to trigger an API error
    #     request = self.create_test_request("This should fail")
    #     request.request_data.model = "non-existent-model"
    #
    #     # Execute should handle errors gracefully
    #     response = self.llm_execute.execute(request)
    #
    #     pprint(response)
    #     # Response should contain error info
    #     assert "error" in response.response_data
