import unittest
import tempfile
import os
import shutil
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__File_System         import LLM_Request__Cache__File_System
from osbot_utils.helpers.llms.cache.Virtual_Storage__Sqlite                 import Virtual_Storage__Sqlite
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                   import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Data             import Schema__LLM_Request__Data
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Content import Schema__LLM_Request__Message__Content
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role    import Schema__LLM_Request__Message__Role
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                  import Schema__LLM_Response
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Files                   import Sqlite__DB__Files


class test_LLM_Request__Cache__Sqlite(unittest.TestCase):        # Test cache integration with SQLite storage
    cache    : LLM_Request__Cache__File_System
    temp_dir : str

    @classmethod
    def setUpClass(cls):                                                                                      # Set up a cache with SQLite virtual storage
        cls.temp_dir                   = tempfile.mkdtemp()                                                   # Create temporary directory for the database
        cls.db_path                    = os.path.join(cls.temp_dir, "llm_cache_test.sqlite")
        cls.virtual_storage            = Virtual_Storage__Sqlite()                                            # Create the SQLite virtual storage
        cls.virtual_storage.db.db_path = cls.db_path                                                          # Set database path
        cls.cache                      = LLM_Request__Cache__File_System(virtual_storage=cls.virtual_storage) # Create cache system
        cls.cache.setup()                                                                                     # Initialize cache

    @classmethod
    def tearDownClass(cls):                                           # Clean up after tests
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def create_test_request(self, message_text: str) -> Schema__LLM_Request:   # Helper to create a test request
        message = Schema__LLM_Request__Message__Content(role    = Schema__LLM_Request__Message__Role.USER ,
                                                        content = message_text                            )

        request_data = Schema__LLM_Request__Data(model       = "test-model"    ,
                                                 platform    = "test-platform" ,
                                                 provider    = "test-provider" ,
                                                 temperature = 0.7             ,
                                                 max_tokens  = 100             )
        request_data.messages.append(message)
        return Schema__LLM_Request(request_data=request_data)

    def create_test_response(self, content="This is a test response") -> Schema__LLM_Response:                    # Helper to create a test response
        return Schema__LLM_Response(response_data = {"content": content})

    def test_add_and_get(self):                                                     # Test adding and retrieving from cache
        request_text       = "Hello, SQLite world!"
        response_text      = "This is a test response"
        request            = self.create_test_request         (request_text     )   # create a test request with a custom message
        response           = self.create_test_response        (response_text    )   # and a test response
        cache_id           = self.cache.add                   (request, response)   # Add to cache


        hash_request       = self.cache.compute_request_hash           (request          ).__to_primitive__()   # Compute request hash
        cache_path         = self.cache.path_file__cache_entry         (cache_id         ).__to_primitive__()   # Get cache entry path
        cached_response    = self.cache.get                            (request          )                      # Get from cache
        cache_entry        = self.cache.get__cache_entry__from__cache_id(cache_id)
        cache_id_str       = cache_id.__to_primitive__()
        response_id        = response.response_id .__to_primitive__()                                           # we need to use the primitive value for for the comparison below to work
        response_timestamp = response.timestamp   .__to_primitive__()
        cached_timestamp   = cache_entry.timestamp.__to_primitive__()
        db_name            = self.virtual_storage.db.db_name
        cache_entry_data   = { 'cache_id'     : cache_id,
                               'llm__request'  : { 'request_data': { 'function_call': None,
                                                                    'max_tokens'   : 100,
                                                                    'messages'     : [ { 'content': request_text,
                                                                                         'role'   : 'user'      }],
                                                                    'model'        : 'test-model'     ,
                                                                    'platform'     : 'test-platform'  ,
                                                                    'provider'     : 'test-provider'  ,
                                                                    'temperature'  : 0.7              ,
                                                                    'top_p'        : None             }},
                               'llm__response' : { 'response_data': { 'content': response_text}  ,
                                                  'response_id'  : response_id                  ,
                                                  'timestamp'    : response_timestamp           },
                               'llm__payload'  : {}                                              ,
                               'request__duration': 0.0,
                               'request__hash'    : hash_request,
                               'timestamp': cached_timestamp }
        cache_index_data  = { 'cache_id__from__hash__request': { hash_request  : cache_id       },
                              'cache_id__to__file_path'       : { cache_id_str : cache_path     }}

        assert cache_id                                             is not None         # Verify it worked
        assert hash_request                                         == "acfed094a5"     # Given the same import this value should always be the same
        assert self.cache.storage().exists__cache_entry(cache_path) is True             # Verify through storage API
        assert cached_response                                      is not None
        assert cached_response.response_id                          == response.response_id


        assert self.cache.json() == { 'cache_entries'   : { cache_id_str: cache_entry_data},
                                      'cache_index'     : cache_index_data             ,
                                      'path_generator'  : {},
                                      'shared_areas'    : [],
                                      'shared_domains'  : [],
                                      'virtual_storage' : { 'db': { 'auto_schema_row': False        ,
                                                                    'closed'         : False        ,
                                                                    'connected'      : True         ,
                                                                    'db_name'        : db_name      ,
                                                                    'db_path'        : self.db_path ,
                                                                    'deleted'        : False        ,
                                                                    'in_memory'      : False        },
                                                             'root_folder': 'llm-cache/'}}

        with self.virtual_storage.db  as _:
            file__cache_index = 'llm-cache/cache_index.json'
            file__cache_file  = f'llm-cache/{cache_path}'
            assert type(_)        is Sqlite__DB__Files
            assert _.file_names() == [file__cache_index, file__cache_file]
            #assert _.file_contents__json(file__cache_index) == cache_index_data            # todo: this started to fail when we added Type_Safe__Primitive to the primitive classes (the prob is that we are using a dict that has classes that use those primitives)
            assert _.file_contents__json(file__cache_file ) == cache_entry_data

    def test_cache_persistence(self):                                          # Test that cache data persists
        request  = self.create_test_request("Persistence test")
        response = self.create_test_response()

        self.cache.add(request, response)                                      # Add to cache

        new_virtual_storage            = Virtual_Storage__Sqlite()             # Create new storage
        new_virtual_storage.db.db_path = self.db_path
        new_cache                      = LLM_Request__Cache__File_System(virtual_storage=new_virtual_storage)
        new_cache.setup()

        cached_response = new_cache.get(request)

        assert new_cache.exists(request)    is True                            # Check data persistence
        assert cached_response              is not None
        assert cached_response.response_id  == response.response_id

    def test_delete(self):                                                     # Test deleting from cache
        request  = self.create_test_request("Delete me from SQLite")
        response = self.create_test_response()
        self.cache.add(request, response)                                      # Add to cache
        assert self.cache.exists(request) is True                              # Verify it exists
        assert self.cache.delete(request) is True                              # Delete it
        assert self.cache.exists(request) is False                             # Verify it's gone

    def test_clear(self):                                                      # Test clearing the cache
        self.cache.clear()
        for i in range(3):
            request  = self.create_test_request(f"SQLite clear test {i}")
            response = self.create_test_response()
            self.cache.add(request, response)                                  # Add multiple entries

        assert len(self.cache.get_all_cache_ids()) == 3                        # Verify entries exist
        assert self.cache.clear() is True                                      # Clear cache
        assert len(self.cache.get_all_cache_ids()) == 0                        # Verify all entries are gone

    def test_rebuild_index(self):                                              # Test rebuilding the index
        request1  = self.create_test_request("SQLite rebuild test 1")
        request2  = self.create_test_request("SQLite rebuild test 2")
        response  = self.create_test_response()
        self.cache.add(request1, response)
        self.cache.add(request2, response)

        self.cache.cache_index.cache_id__from__hash__request = {}                   # Clear index but keep data
        assert self.cache.rebuild_index()                                is True    # Rebuild index
        assert len(self.cache.cache_index.cache_id__from__hash__request) == 2       # Verify index rebuilt
        assert self.cache.exists(request1)                               is True    # Verify requests accessible
        assert self.cache.exists(request2)                               is True
