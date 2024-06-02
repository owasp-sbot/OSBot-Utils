from unittest                                                            import TestCase

from osbot_utils.helpers.cache_requests.Cache__Requests__Config          import Cache__Requests__Config
from osbot_utils.helpers.cache_requests.Cache__Requests__Row import Cache__Requests__Row
from osbot_utils.helpers.sqlite.cache.db.Sqlite__Cache__Requests__Table  import Sqlite__Cache__Requests__Table
from osbot_utils.helpers.sqlite.cache.db.Sqlite__Cache__Requests__Sqlite import Sqlite__Cache__Requests__Sqlite
from osbot_utils.utils.Json                                              import json_dumps


class test_Sqlite__Cache__Requests__Row(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_config      = Cache__Requests__Config()
        cls.cache_sqlite      = Sqlite__Cache__Requests__Sqlite(config=cls.cache_config)
        cls.cache_table       = Sqlite__Cache__Requests__Table (cache_table=cls.cache_sqlite.cache_table())
        cls.cache_request_row = Cache__Requests__Row           (config=cls.cache_config, cache_table=cls.cache_table)

        cls.cache_config.set__add_timestamp(False)  # disabling timestamp since it complicates the test data verification below

    def test__init__(self):
        assert self.cache_request_row.config        == self.cache_config
        assert self.cache_request_row.cache_table   == self.cache_table
        assert self.cache_table.database.in_memory  is True
        assert self.cache_table.database.db_path    is None

    def test_create_new_cache_row_data(self):
        model_id                 = 'aaaa'
        body                     = {'the': 'request data'}
        response_data            = {'the': 'return value'}
        request_data             = self.cache_request_row.cache_request_data(model_id=model_id, body=body)
        new_cache_entry          = self.cache_request_row.create_new_cache_row_data(request_data, response_data)
        expected_new_cache_entry = { 'request_data'  : json_dumps(request_data)                                           ,
                                     'request_hash'  : 'f917e6f5658f5b761a77416d487c5d9a70253abce68b348bc360a6f39657753a' ,
                                     'response_bytes': b''                                                                ,
                                     'response_data' : json_dumps(response_data)                                          ,
                                     'response_hash' : '69e330ec7bf6334aa41ecaf56797fa86345d3cf85da4c622821aa42d4bee1799' ,
                                     'response_type' : 'dict'                                                             ,
'timestamp'     :  0                                                                 }
        expected_new_cache_obj   = { **expected_new_cache_entry ,
                                     'comments'     : ''        ,
                                     'metadata'     : ''        ,
                                     'request_type' : ''        ,
                                     'source'       : ''        ,
                                     'timestamp'    : 0         }
        assert new_cache_entry == expected_new_cache_entry
        new_cache_obj = self.cache_request_row.cache_table.new_row_obj(new_cache_entry)
        assert new_cache_obj.__locals__() == expected_new_cache_obj
        assert self.cache_request_row.cache_table.rows() ==[]

        self.cache_config.set__add_timestamp(True)

        new_cache_entry = self.cache_request_row.create_new_cache_row_data(request_data, response_data)
        assert new_cache_entry.get('timestamp') != 0
        assert new_cache_entry.get('timestamp') > 0
        self.cache_config.set__add_timestamp(False)