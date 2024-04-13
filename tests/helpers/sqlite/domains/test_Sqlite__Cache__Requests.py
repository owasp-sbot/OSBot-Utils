from unittest import TestCase
from unittest.mock import Mock

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests import Sqlite__DB__Requests, SQLITE_TABLE__REQUESTS
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file, current_temp_folder, parent_folder, file_exists, file_not_exists
from osbot_utils.utils.Json import from_json_str
from osbot_utils.utils.Misc import random_text, list_set
from osbot_utils.utils.Objects import base_types


class test_Sqlite__Cache__Requests(TestCase):
    sqlite_cache_requests : Sqlite__Cache__Requests
    temp_db_path          : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path                        = temp_file(extension='sqlite')
        cls.sqlite_cache_requests               = Sqlite__Cache__Requests(db_path = cls.temp_db_path)       # the db_path to the tmp file path
        cls.sqlite_cache_requests.add_timestamp = False                                                     # disabling timestamp since it complicates the test data verification below
        assert parent_folder(cls.sqlite_cache_requests.sqlite_bedrock.db_path) == current_temp_folder()
        assert file_exists  (cls.temp_db_path)                                 is True

    @classmethod
    def tearDownClass(cls):    #file_delete(cls.temp_db_path)
        cls.sqlite_cache_requests.sqlite_bedrock.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def tearDown(self):
        self.sqlite_cache_requests.cache_table().clear()

    def test___init__(self):
        with self.sqlite_cache_requests as _:
            assert type      (_)                is Sqlite__Cache__Requests
            assert base_types(_)                == [Kwargs_To_Self, object]
            assert type      (_.sqlite_bedrock) is Sqlite__DB__Requests
            assert base_types(_.sqlite_bedrock) == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert _.sqlite_bedrock.db_name     == ''
            assert _.sqlite_bedrock.table_name  == SQLITE_TABLE__REQUESTS

    def add_test_requests(self, count=10):
        def invoke_target(**target_kwargs):
            return {'target_kwargs': target_kwargs}

        for i in range(count):
            an_key        = random_text('an_key')
            an_dict       = {'the': random_text('random_request')}
            target        = invoke_target
            target_kwargs = {'an_key': an_key, 'an_dict': an_dict}
            self.sqlite_cache_requests.invoke(target, target_kwargs)
            #self.sqlite_cache_requests.model_invoke(**kwargs)

    def test__add_test_requests(self):
        with self.sqlite_cache_requests as _:
            assert _.cache_entries() == []
            self.add_test_requests()
            assert len(_.cache_entries()) == 10
            for entry in _.cache_entries():
                request_data = from_json_str(entry.get('request_data'))
                response_data = from_json_str(entry.get('response_data'))
                assert list_set(request_data )            == ['an_dict', 'an_key']
                assert list_set(response_data)            == ['target_kwargs']
                assert response_data.get('target_kwargs') == request_data
                assert list_set(entry)                    == ['cache_hits', 'comments', 'id', 'latest', 'request_data',
                                                              'request_hash', 'response_data', 'response_hash', 'timestamp']

            self.add_test_requests(3)
            assert len(_.cache_entries()) == 13

