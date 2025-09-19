import unittest
import tempfile
import shutil
import os
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id, is_obj_id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now    import Timestamp_Now
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__File_System                 import LLM_Request__Cache__File_System
from osbot_utils.helpers.llms.cache.Virtual_Storage__Local__Folder                  import Virtual_Storage__Local__Folder
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data                     import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role            import Schema__LLM_Request__Message__Role
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                          import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content         import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache                   import Schema__LLM_Response__Cache
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.utils.Files                                                        import file_exists, folder_exists, files_names_in_folder
from osbot_utils.utils.Json                                                         import json_file_load
from osbot_utils.utils.Misc                                                         import list_set


class test_LLM_Request__Cache__Local_Folder(unittest.TestCase):
    cache    : LLM_Request__Cache__File_System
    temp_dir : str

    @classmethod
    def setUpClass(cls):
        cls.temp_dir          = Safe_Str__File__Path(tempfile.mkdtemp())                                # Create a temporary directory for testing
        cls.virtual_storage   = Virtual_Storage__Local__Folder (root_folder     = cls.temp_dir       )  # use it on the virtual storage
        cls.cache             = LLM_Request__Cache__File_System(virtual_storage = cls.virtual_storage)  # Initialize the cache
        cls.cache.setup()                                                                               # Setup Cache

    @classmethod
    def tearDownClass(cls):
        if cls.temp_dir and os.path.exists(cls.temp_dir):                                 # Clean up the temporary directory
            shutil.rmtree(cls.temp_dir)

    def create_test_request(self, message_text: str) -> Schema__LLM_Request:     # Helper to create a test request
        message = Schema__LLM_Request__Message__Content(role    = Schema__LLM_Request__Message__Role.USER,
                                                        content = message_text                           )

        request_data = Schema__LLM_Request__Data(model       = "test-model"   ,
                                                 platform    = "test-platform",
                                                 provider    = "test-provider",
                                                 temperature = 0.7            ,
                                                 max_tokens  = 100            )
        request_data.messages.append(message)

        return Schema__LLM_Request(request_data  = request_data )

    def create_test_response(self) -> Schema__LLM_Response:                      # Helper to create a test response
        return Schema__LLM_Response(response_id   = Obj_Id()                        ,
                                    timestamp     = Timestamp_Now()                 ,
                                    response_data = {"content": "This is a test response"})

    def test_initialization(self):
        assert folder_exists(self.cache.virtual_storage.path_folder__root_cache())                  # Folder should be created on initialization
        assert file_exists  (self.cache.storage().path_file__cache_index())                   # Index file should exist after setup
        cache_index_content = json_file_load(self.cache.storage().path_file__cache_index())
        assert isinstance(cache_index_content, dict)                                # Index file should contain a valid JSON object
        assert list_set(cache_index_content) == ['cache_id__from__hash__request',
                                                 'cache_id__to__file_path'      ]

    def test_add_and_get(self):
        request         = self.create_test_request("Hello, world!")
        response        = self.create_test_response()
        cache_id        = self.cache.add(request, response)                                 # Add to cache
        hash_request    = self.cache.compute_request_hash(request)
        cache_path      = self.cache.path_file__cache_entry(cache_id)
        full_cache_path = self.cache.storage().path_file__cache_entry(cache_path)
        cached_response = self.cache.get(request)                                           # Retrieve it

        assert is_obj_id(cache_id)          is True
        assert cache_id                     == self.cache.cache_index.cache_id__from__hash__request[hash_request]
        assert file_exists(full_cache_path) is True                                       # Cache file should exist on disk
        assert self.cache.exists(request)   is True                                       # Item should exist in cache
        assert cached_response              is not None                                   # Should retrieve cached response
        assert response.response_id         == cached_response.response_id                # Response IDs should match

    def test_get_cache_entry_from_disk(self):
        request  = self.create_test_request("Test disk retrieval")
        response = self.create_test_response()

        self.cache.add(request, response)                                        # Add to cache
        hash_request         = self.cache.compute_request_hash(request)
        cache_id             = self.cache.cache_index.cache_id__from__hash__request[hash_request]
        cache_entry_1        = self.cache.get__cache_entry__from__cache_id(cache_id)
        path_cache_file      = self.cache.path_file__cache_entry(cache_id)
        full_path_cache_file = self.cache.storage().path_file__cache_entry(path_cache_file)

        assert type(cache_entry_1)               is Schema__LLM_Response__Cache
        assert cache_entry_1.json()              == Schema__LLM_Response__Cache.from_json(cache_entry_1.json()).json()   # confirm json roundtrip
        assert type(cache_id     )               is Obj_Id
        assert type(hash_request )               is Safe_Str__Hash
        assert type(cache_entry_1)               is Schema__LLM_Response__Cache
        assert cache_entry_1.request__hash == hash_request
        assert cache_entry_1.cache_id            == cache_id
        assert file_exists(full_path_cache_file) is True
        assert cache_id                          == self.cache.get__cache_id__from__request     (request     )
        assert cache_id                          == self.cache.get__cache_id__from__request_hash(hash_request)
        assert cache_entry_1                     == self.cache.get__cache_entry__from__cache_id (cache_id    )
        assert cache_entry_1                     == self.cache.get__cache_entry__from__request  (request     )

        self.cache.cache_entries = {}                                               # Clear the in-memory cache

        cache_entry_2 = self.cache.get__cache_entry__from__cache_id(cache_id)                        # will load from disk

        assert cache_entry_2                          is not None                   # confirm it was loaded
        assert cache_entry_2.json()                   == cache_entry_1.json()       # confirm match memory version
        assert cache_entry_2.llm__response.response_id == response.response_id       # double check request id

    def test_get_all_cache_ids(self):
        self.cache.clear()
        request1 = self.create_test_request("First request" )
        request2 = self.create_test_request("Second request")
        response = self.create_test_response()

        self.cache.add(request1, response)
        self.cache.add(request2, response)

        cache_ids = self.cache.get_all_cache_ids()
        assert len(cache_ids) == 2                                               # Should find both cache files

        previous_cache = self.cache.cache_index.cache_id__to__file_path.copy()      # todo: move this rebuild_cache_id_to_file_path check into a new folder
        self.cache.rebuild_cache_id_to_file_path()
        assert self.cache.cache_index.cache_id__to__file_path == previous_cache

        #assert self.cache.get_all_cache_ids__from__disk() == cache_ids

    def test_delete(self):
        request  = self.create_test_request("Delete me")
        response = self.create_test_response()

        self.cache.add(request, response)
        hash_request    = self.cache.compute_request_hash(request)
        cache_id        = self.cache.cache_index.cache_id__from__hash__request[hash_request]
        cache_path      = self.cache.path_file__cache_entry(cache_id)
        full_cache_path = self.cache.storage().path_file__cache_entry(cache_path)

        assert file_exists(full_cache_path)                                      # File should exist before deletion
        assert self.cache.exists(request)                                        # Entry should exist in cache

        delete_result = self.cache.delete(request)
        assert delete_result == True                                             # Delete should return True
        assert not file_exists(full_cache_path)                                  # File should be deleted
        assert not self.cache.exists(request)                                    # Entry should not exist in cache

    def test_delete_nonexistent(self):
        request  = self.create_test_request("Nonexistent")                       # Request not in cache
        result   = self.cache.delete(request)
        assert result == False                                                   # Delete should return False for nonexistent

    def test_clear(self):
        for i in range(3):                                                      # Add several items
            request  = self.create_test_request(f"Clear test {i}")
            response = self.create_test_response()
            self.cache.add(request, response)

        assert len(files_names_in_folder(self.temp_dir)) > 0                    # Should have files before clearing
        assert len(self.cache.cache_index.cache_id__from__hash__request) > 0                    # Should have entries before clearing

        clear_result = self.cache.clear()
        assert clear_result == True                                             # Clear should return True

        files_remaining = files_names_in_folder(self.temp_dir)                  # get all files in folder
        all_ids         = self.cache.get_all_cache_ids()                        # get all ids in cache (from disk)
        assert files_remaining == ['cache_index']                               # Only the index file should remain after clearing
        assert len(all_ids        ) == 0                                        # All files should be deleted
        assert len(files_remaining) == 1                                        # only one left should be the index
        assert len(self.cache.cache_index.cache_id__from__hash__request) == 0                   # Cache index should be cleared
        assert len(self.cache.cache_entries) == 0                               # Cache entries should be cleared

    def test_rebuild_index(self):
        self.cache.clear()
        request1 = self.create_test_request("Rebuild test 1")
        request2 = self.create_test_request("Rebuild test 2")
        response = self.create_test_response()

        self.cache.add(request1, response)
        self.cache.add(request2, response)

        # Create a new empty cache, but using the same folder
        self.cache                                     = LLM_Request__Cache__File_System(virtual_storage=self.virtual_storage)
        self.cache.root_folder                         = self.temp_dir
        self.cache.cache_index.cache_id__from__hash__request           = {}                               # Clear the index

        # Rebuild index
        result = self.cache.rebuild_index()

        assert result == True                                                  # Rebuild should return True

        # After rebuild, we should have the same entries
        assert len(self.cache.cache_index.cache_id__from__hash__request) == 2                  # Should have 2 entries after rebuild

        # The requests should be accessible again
        request_hash1 = self.cache.compute_request_hash(request1)
        request_hash2 = self.cache.compute_request_hash(request2)

        assert request_hash1 in self.cache.cache_index.cache_id__from__hash__request           # Hash should be in the rebuilt index
        assert request_hash2 in self.cache.cache_index.cache_id__from__hash__request           # Hash should be in the rebuilt index

    # def test_stats(self):
    #     self.cache.clear()
    #     request1 = self.create_test_request("Stats test 1")
    #     request2 = self.create_test_request("Stats test 2")
    #     request1.request_data.model = "model-A"
    #     request2.request_data.model = "model-B"
    #     response = self.create_test_response()
    #
    #     self.cache.add(request1, response)
    #     self.cache.add(request2, response)
    #
    #     stats = self.cache.stats()
    #     assert stats["total_entries"    ] == 2                                      # Should have 2 cache entries
    #     assert stats["models"]["model-A"] == 1                                      # Should have 1 entry for model-A
    #     assert stats["models"]["model-B"] == 1                                      # Should have 1 entry for model-B
    #     assert stats["root_folder"      ] == self.temp_dir                          # Should show the correct root folder
    #     assert stats["cache_files"      ] == 2                                      # Should show the correct number of cache files
    #     assert "total_size_bytes" in stats                                          # Should include total size information
    #     assert stats["total_size_bytes" ] > 0                                       # Size should be greater than 0

    def test_persistent_after_restart(self):
        request  = self.create_test_request("Persistent test")
        response = self.create_test_response()

        self.cache.add(request, response)                                       # Add to cache

        # Create a new cache with the same root folder (simulating a restart)
        virtual_storage = Virtual_Storage__Local__Folder (root_folder     = self.temp_dir  )
        new_cache       = LLM_Request__Cache__File_System(virtual_storage = virtual_storage).setup()

        assert new_cache.exists(request) is True                                # Item should still exist in cache after restart

        cached_response = new_cache.get(request)       # Should be able to retrieve it

        assert cached_response is not None
        assert cached_response.response_id == response.response_id              # Should get the same response back