from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests__Patch import Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.helpers.ssh.SSH__Cache__Requests import SSH__Cache__Requests, SQLITE_DB_NAME__SSH_REQUESTS_CACHE, \
    SQLITE_TABLE_NAME__SSH_REQUESTS
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_file, current_temp_folder, parent_folder, file_extension
from osbot_utils.utils.Json import to_json_str
from osbot_utils.utils.Misc import bytes_to_str, str_sha256, sha_256
from osbot_utils.utils.Objects import base_types, pickle_load_from_bytes, pickle_from_bytes, pickle_to_bytes
from osbot_utils.utils.Toml import dict_to_toml

class test_SSH__Cache__Requests(TestCase):
    cache_ssh_requests : SSH__Cache__Requests
    temp_db_path         : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path = temp_file(extension='sqlite')
        cls.cache_ssh_requests = SSH__Cache__Requests(db_path=cls.temp_db_path)

    @classmethod
    def tearDownClass(cls):
        cls.cache_ssh_requests.delete()
        assert cls.cache_ssh_requests.sqlite_requests.exists() is False
        assert SSH.execute_command.__qualname__ == 'SSH.execute_command'

    def test__init__(self):
        with self.cache_ssh_requests as _:

            assert _.__attr_names__()                         == ['add_timestamp', 'cache_only_mode', 'capture_exceptions', 'db_name','enabled',
                                                                  'exception_classes', 'on_invoke_target', 'pickle_response', 'print_requests','sqlite_requests',
                                                                  'table_name','target_class', 'target_function', 'target_function_name','update_mode']
            assert _.db_name                                  == SQLITE_DB_NAME__SSH_REQUESTS_CACHE
            assert _.table_name                               == SQLITE_TABLE_NAME__SSH_REQUESTS
            assert _.sqlite_requests.exists()                 is True
            assert _.cache_entries()                          == []
            assert _.cache_table().new_row_obj().__locals__() == {'cache_hits'      : 0     ,
                                                                  'comments'        : ''    ,
                                                                  'latest'          : False ,
                                                                  'request_data'    : ''    ,
                                                                  'request_hash'    : ''    ,
                                                                  'response_bytes'  : b''   ,
                                                                  'response_data'   : ''    ,
                                                                  'response_hash'   : ''    ,
                                                                  'timestamp'       : 0     }
            assert parent_folder (_.sqlite_requests.db_path)  == current_temp_folder()
            assert file_extension(_.sqlite_requests.db_path)  == '.sqlite'
            assert base_types(_)                              == [Sqlite__Cache__Requests__Patch ,
                                                                  Sqlite__Cache__Requests        ,
                                                                  Kwargs_To_Self                 ,
                                                                  object                         ]
            assert _.target_class                             == SSH
            assert _.target_function                          != SSH.execute_command
            assert _.target_function_name                     == "execute_command"

    def test___enter____exit__(self):
        assert SSH.execute_command == SSH.execute_command
        assert SSH.execute_command == self.cache_ssh_requests.target_function
        assert SSH.execute_command.__qualname__ == 'SSH.execute_command'
        with self.cache_ssh_requests  as _:
            assert SSH.execute_command              != self.cache_ssh_requests.target_function
            assert SSH.execute_command.__qualname__ == 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'
        assert SSH.execute_command == self.cache_ssh_requests.target_function
        assert SSH.execute_command.__qualname__ == 'SSH.execute_command'

    def test_invoke_target(self):
        mock_ssh_host          = '127.0.0.1'
        mock_path              = '/aaa'
        mock_files             = ['/ccc', '/ddd']
        expected_request_data  = to_json_str(dict_to_toml({'args': ('/aaa',), 'kwargs': {}, 'ssh_host': '127.0.0.1'}))
        expected_response_data = {'files': mock_files, 'path': mock_path}
        expected_response_bytes = pickle_to_bytes(expected_response_data)
        expected_request_hash   = sha_256(expected_request_data)

        def on_invoke_target(*args):
            return {'files': mock_files,
                    'path'  : args[1][1]  }

        with self.cache_ssh_requests as _:
            _.add_timestamp     = False
            _.on_invoke_target = on_invoke_target

            assert _.cache_entries() == []

            ssh = SSH(ssh_host= mock_ssh_host).setup()
            ssh.execute_command__return_stdout(mock_path)

            cache_entry = _.cache_entries()[0]
            assert len(_.cache_entries()) == 1

            response_data          = pickle_from_bytes(cache_entry.get('response_bytes'))
            assert response_data == expected_response_data

            assert cache_entry == { 'cache_hits'    : 0                      ,
                                    'comments'      : ''                     ,
                                    'id'            : 1                      ,
                                    'latest'        : 0                      ,
                                    'request_data'  : expected_request_data  ,
                                    'request_hash'  : expected_request_hash  ,
                                    'response_bytes': expected_response_bytes,
                                    'response_data' : ''                     ,
                                    'response_hash' : ''                     ,
                                    'timestamp'     : 0                      }
