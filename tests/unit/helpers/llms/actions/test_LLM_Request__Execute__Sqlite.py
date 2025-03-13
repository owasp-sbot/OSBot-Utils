import pytest
from unittest                                                           import TestCase
from osbot_utils.helpers.llms.actions.LLM_Request__Execute              import LLM_Request__Execute
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI    import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__File_System     import LLM_Request__Cache__File_System
from osbot_utils.helpers.llms.cache.Virtual_Storage__Sqlite             import Virtual_Storage__Sqlite
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI       import ENV_NAME_OPEN_AI__API_KEY, API__LLM__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request               import Schema__LLM_Request
from osbot_utils.utils.Env                                              import get_env, load_dotenv

TEST__TEMP__SQLITE_DB = '/tmp/_osbot_utils/test_LLM_Request__Execute__Sqlite.sqlite'

class test_LLM_Request__Execute__Sqlite(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip("Test needs OpenAI key")
        cls.virtual_storage = Virtual_Storage__Sqlite()
        cls.virtual_storage.db.db_path = TEST__TEMP__SQLITE_DB                      # todo: find a better way to do this
        cls.llm_cache                  = LLM_Request__Cache__File_System(virtual_storage=cls.virtual_storage).setup()  # Create cache system
        cls.llm_api                    = API__LLM__Open_AI()
        cls.request_builder            = LLM_Request__Builder__Open_AI()
        cls.llm_execute                = LLM_Request__Execute(llm_cache       = cls.llm_cache      ,
                                                              llm_api         = cls.llm_api        ,
                                                              request_builder = cls.request_builder)

    def test_execute(self):
        with self.request_builder as _:
            _.llm_request_data.model = 'gpt-4o-mini'
            _.add_message__user("What is 1+1")
            llm_request  = Schema__LLM_Request(request_data=_.llm_request_data)
            llm_response = self.llm_execute.execute(llm_request)

        with self.llm_cache as _:
            request_hash   = _.compute_request_hash(llm_request)
            cache_response = _.get(llm_request)
            assert cache_response == llm_response

        with self.virtual_storage as _:
            cache_index  = _.db.file_contents__json('llm-cache/cache_index.json')
            cache_id     = cache_index.get('cache_id__from__hash__request').get(request_hash)
            file_path    = cache_index.get('cache_id__to__file_path'      ).get(cache_id)
            cache_entry  = _.db.file_contents__json('llm-cache/' + file_path)


            assert type(cache_entry) is dict

            assert cache_entry == { 'cache_id'      : cache_id,
                                    'hash__request' : request_hash,
                                     'llm_payload': {'messages': [{'content': 'What is 1+1', 'role': 'user'}],
                                                                   'model'  : 'gpt-4o-mini'                },
                                    'llm_request'   : llm_request.json(),
                                    'llm_response'  : llm_response.json(),
                                    'timestamp'     : cache_entry.get('timestamp')}

