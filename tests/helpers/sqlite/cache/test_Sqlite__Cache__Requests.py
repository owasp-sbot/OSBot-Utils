from unittest                                                           import TestCase
from osbot_utils.base_classes.Kwargs_To_Self                            import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database                        import Sqlite__Database
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests           import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.TestCase__Sqlite__Cache__Requests import TestCase__Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local               import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests            import Sqlite__DB__Requests, SQLITE_TABLE__REQUESTS
from osbot_utils.helpers.sqlite.domains.schemas.Schema__Table__Requests import Schema__Table__Requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files                                            import temp_file, current_temp_folder, parent_folder, file_exists, file_not_exists
from osbot_utils.utils.Json                                             import from_json_str, json_dump, to_json_str, json_loads, json_dumps
from osbot_utils.utils.Misc                                             import random_text, list_set, random_string, str_sha256
from osbot_utils.utils.Objects                                          import base_types, pickle_load_from_bytes, pickle_save_to_bytes, pickle_from_bytes


class test_Sqlite__Cache__Requests(TestCase__Sqlite__Cache__Requests):

    def test___init__(self):
        with self.sqlite_cache_requests as _:
            assert type      (_)                  is Sqlite__Cache__Requests
            assert base_types(_)                  == [Kwargs_To_Self, object]
            assert type      (_.sqlite_requests)  is Sqlite__DB__Requests
            assert base_types(_.sqlite_requests)  == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert _.sqlite_requests.db_name.startswith('db_local_')
            assert _.sqlite_requests.table_name   == SQLITE_TABLE__REQUESTS


    def test_setup(self):
        with self.sqlite_cache_requests.sqlite_requests as _:
            assert type(_)   is Sqlite__DB__Requests
            assert _.db_path != Sqlite__DB__Requests().path_local_db()
            assert _.db_path is None

        with self.sqlite_cache_requests.cache_table() as _:

            _._table_create().add_fields_from_class(Schema__Table__Requests).sql_for__create_table()

            assert _.exists()   is True
            assert _.row_schema is Schema__Table__Requests
            assert _.schema__by_name_type() == { 'comments'      : 'TEXT'    ,
                                                 'id'            : 'INTEGER' ,
                                                 'metadata'      : 'TEXT'    ,
                                                 'request_data'  : 'TEXT'    ,
                                                 'request_hash'  : 'TEXT'    ,
                                                 'request_type'  : 'TEXT'    ,
                                                 'response_bytes': 'BLOB'    ,
                                                 'response_data' : 'TEXT'    ,
                                                 'response_hash' : 'TEXT'    ,
                                                 'response_type' : 'TEXT'    ,
                                                 'source'        : 'TEXT'    ,
                                                 'timestamp'     : 'INTEGER' }
            assert _.indexes() == ['idx__requests__request_hash']




