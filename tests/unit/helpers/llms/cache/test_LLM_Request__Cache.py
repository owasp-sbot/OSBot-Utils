import unittest
from osbot_utils.testing.__                                                        import __
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Id import Safe_Str__LLM__Model_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                   import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now   import Timestamp_Now
from osbot_utils.helpers.llms.cache.LLM_Request__Cache                             import LLM_Request__Cache
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                          import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data                    import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role           import Schema__LLM_Request__Message__Role
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                         import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content        import Schema__LLM_Request__Message__Content


class test_LLM_Request__Cache(unittest.TestCase):
    cache : LLM_Request__Cache

    def setUp(self):
        self.cache = LLM_Request__Cache()

    def create_test_request(self, message_text: str) -> Schema__LLM_Request:                   # Helper to create a test request
        message = Schema__LLM_Request__Message__Content(role    = Schema__LLM_Request__Message__Role.USER,
                                                        content = message_text                           )

        request_data = Schema__LLM_Request__Data(model       = "test-model"   ,
                                                 platform    = "test-platform",
                                                 provider    = "test-provider",
                                                 temperature = 0.7            ,
                                                 max_tokens  = 100            )
        request_data.messages.append(message)

        return Schema__LLM_Request(request_data  = request_data )

    def create_test_response(self) -> Schema__LLM_Response:                                    # Helper to create a test response
        return Schema__LLM_Response(response_id   = Obj_Id()                              ,
                                    timestamp     = Timestamp_Now()                       ,
                                    response_data = {"content": "This is a test response"})

    def test_compute_request_hash(self):
        request = self.create_test_request("Test message")
        hash_1   = self.cache.compute_request_hash(request)
        hash_2   = self.cache.compute_request_hash(request)

        assert hash_1      == hash_2                                                           # Same request should produce same hash
        assert len(hash_1) == 10                                                               # Hash should be of correct length


        request_2 = self.create_test_request("Different message")                              # Different requests should have different hashes
        hash_3    = self.cache.compute_request_hash(request_2)
        assert hash_1 != hash_3

    def test_add_and_get(self):
        request  = self.create_test_request("Hello, world!")
        response = self.create_test_response()
        assert request.obj() == __(request_data=__(function_call=None,
                                                   temperature  =0.7,
                                                   top_p        =None,
                                                   max_tokens   =100,
                                                   model        ='test-model',
                                                   platform     ='test-platform',
                                                   provider     ='test-provider',
                                                   messages     =[__(role='user', content='Hello, world!')]))

        assert response.obj() == __(response_id   = response.response_id,
                                    timestamp     = response.timestamp  ,
                                    response_data = __(content='This is a test response'))

        cache_id = self.cache.add(request, response,{})            # Add to cache
        assert type(cache_id) is Obj_Id                         # Add should succeed

        # Check if it exists
        assert self.cache.exists(request) is True                                              # Item should exist in cache

        # Retrieve it
        cached_response                 = self.cache.get(request)
        cache_entry                     = self.cache.get__cache_entry__from__cache_id(cache_id)
        assert cached_response          is not None                                                # Should retrieve cached response
        assert response.response_id     == cached_response.response_id                             # Response IDs should match
        assert cache_entry.llm__response == response

    def test_delete(self):
        request = self.create_test_request("Delete me")
        response = self.create_test_response()

        # Add and then delete
        self.cache.add(request, response)
        assert self.cache.exists(request) == True                                              # Item should exist before deletion

        delete_result = self.cache.delete(request)
        assert delete_result == True                                                           # Delete should return True
        assert self.cache.exists(request) == False                                             # Item should not exist after deletion

    def test_get_by_id(self):
        request  = self.create_test_request("Get by ID test")
        response = self.create_test_response()

        self.cache.add(request, response)

        # Get the cache_id
        request_hash = self.cache.compute_request_hash(request)
        cache_id     = self.cache.cache_index.cache_id__from__hash__request[request_hash]

        # Get by ID
        cached_response = self.cache.get_by_id(cache_id)
        assert cached_response is not None
        assert response.response_id == cached_response.response_id

        # Try with non-existent ID
        non_existent_id = Obj_Id()
        assert self.cache.get_by_id(non_existent_id) is None

    def test_clear(self):
        # Add several items
        for i in range(3):
            request = self.create_test_request(f"Clear test {i}")
            response = self.create_test_response()
            self.cache.add(request, response)

        # Verify we have entries
        assert len(self.cache.cache_index.cache_id__from__hash__request) == 3

        # Clear
        clear_result = self.cache.clear()
        assert clear_result == True

        # Check everything is cleared
        assert len(self.cache.cache_index.cache_id__from__hash__request) == 0
        assert len(self.cache.cache_entries) == 0

    def test_stats(self):
        # Add items with different models
        request1 = self.create_test_request("Stats test 1")
        request1.request_data.model = "model-A"
        response1 = self.create_test_response()

        request2 = self.create_test_request("Stats test 2")
        request2.request_data.model = "model-B"
        response2 = self.create_test_response()

        request3 = self.create_test_request("Stats test 3")
        request3.request_data.model = "model-A"                                                # Second entry for model-A
        response3 = self.create_test_response()

        self.cache.add(request1, response1, {})
        self.cache.add(request2, response2, {})
        self.cache.add(request3, response3, {})

        # Get stats
        stats = self.cache.stats()

        assert stats["total_entries"] == 3
        assert Safe_Str__LLM__Model_Id("model-A")                  in stats["models"]
        assert stats["models"][Safe_Str__LLM__Model_Id("model-A")] == 2
        assert Safe_Str__LLM__Model_Id("model-B")                  in stats["models"]
        assert stats["models"][Safe_Str__LLM__Model_Id("model-B")] == 1
        assert stats["oldest_entry"]                                 is not None
        assert stats["newest_entry"]                                 is not None