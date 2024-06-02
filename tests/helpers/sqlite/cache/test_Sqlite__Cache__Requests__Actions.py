from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Actions import Sqlite__Cache__Requests__Actions
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row import Sqlite__Cache__Requests__Row
from osbot_utils.helpers.sqlite.cache.TestCase__Sqlite__Cache__Requests import TestCase__Sqlite__Cache__Requests
from osbot_utils.utils.Files import temp_file, file_not_exists
from osbot_utils.utils.Json import json_dumps, json_dump, to_json_str
from osbot_utils.utils.Misc import random_string, str_sha256


class test_Sqlite__Cache__Requests__Actions(TestCase__Sqlite__Cache__Requests):

    def setUp(self):
        self.cache_request_actions = Sqlite__Cache__Requests__Actions()                     # todo: refactor tests below to use this one, instead of the one from self.sqlite_cache_requests

    def test_cache_add(self):
        self.sqlite_cache_requests.sqlite_requests.table_requests__reset()                  # todo: do we still need this?
        request_data         = {'the':'request_data', 'random_value' : random_string()}
        request_data_json    = json_dump(request_data)
        request_data_sha256  = str_sha256(request_data_json)
        response_data        = {'the':'response_data'}
        response_data_json   = json_dump(response_data)
        response_data_sha256 = str_sha256(response_data_json)
        expected_new_row     = { 'comments'       : ''                   ,
                                 'metadata'       : ''                   ,
                                 'request_data'   : request_data_json    ,
                                 'request_hash'   : request_data_sha256  ,
                                 'request_type'   : ''                   ,
                                 'response_bytes' : b''                  ,
                                 'response_data'  : response_data_json   ,
                                 'response_hash'  : response_data_sha256 ,
                                 'response_type'  : 'dict'               ,
                                 'source'         : ''                   ,
                                 'timestamp'      : 0                    }
        expected_row_entry   = { **expected_new_row                      ,
                                 'id'            : 1                     }

        new_row = self.sqlite_cache_requests.cache_add(request_data, response_data)
        assert new_row.json() == expected_new_row

        with self.sqlite_cache_requests.cache_table as _:
            rows = _.select_rows_where(request_hash=request_data_sha256)
            assert len(rows) == 1
            row = rows [0]
            assert row == expected_row_entry

            assert self.sqlite_cache_requests.cache_entry(request_data) == expected_row_entry   # confirm we can get the row via it's row_data
            _.rows_delete_where(request_hash=request_data_sha256)                               # delete added row
            assert _.rows() == []                                                               # confirm we are back to having an empty table
            assert self.sqlite_cache_requests.cache_entry(request_data) == {}                   # confirm entry is not available anymore


    def test_cache_delete(self):
        request_data  = {'an': 'request' }
        response_data = {'an': 'response'}
        with self.sqlite_cache_requests as _:
            row = _.cache_add(request_data, response_data)
            assert row.request_data         == to_json_str(request_data )
            assert row.response_data        == to_json_str(response_data)
            assert len (_.cache_entries())  == 1
            assert _.cache_delete(request_data).get('status') == 'ok'
            assert len(_.cache_entries())   == 0
