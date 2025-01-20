from unittest import TestCase
from osbot_utils.base_classes.Kwargs_To_Self                            import Kwargs_To_Self
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests           import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Patch    import Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.ssh.SSH__Cache__Requests                       import SSH__Cache__Requests, SQLITE_DB_NAME__SSH_REQUESTS_CACHE, SQLITE_TABLE_NAME__SSH_REQUESTS
from osbot_utils.helpers.ssh.SSH__Execute                               import ENV_VAR__SSH__HOST, SSH__Execute
from osbot_utils.utils.Env                                              import get_env
from osbot_utils.utils.Files                                            import temp_file, current_temp_folder, parent_folder, file_extension, file_name
from osbot_utils.utils.Json                                             import to_json_str
from osbot_utils.utils.Misc                                             import bytes_to_str, str_sha256, sha_256, bytes_sha256
from osbot_utils.utils.Objects                                          import base_types, pickle_load_from_bytes, pickle_from_bytes, pickle_to_bytes
from osbot_utils.utils.Toml                                             import dict_to_toml

class test_SSH__Cache__Requests(TestCase):
    cache_ssh_requests : SSH__Cache__Requests
    temp_db_path         : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path = temp_file(extension='sqlite')
        cls.cache_ssh_requests = SSH__Cache__Requests(db_path=cls.temp_db_path)
        cls.cache_ssh_requests.add_caller_signature_to_cache_key = False                # disable for these tests

    @classmethod
    def tearDownClass(cls):
        cls.cache_ssh_requests.delete()
        assert cls.cache_ssh_requests.sqlite_requests.exists() is False
        assert SSH__Execute.execute_command.__qualname__ == 'SSH__Execute.execute_command'

    def test__init__(self):
        with self.cache_ssh_requests as _:

            # assert _.__attr_names__()                         == [ 'add_source_location', 'add_timestamp', 'cache_actions', 'cache_data', 'cache_only_mode', 'capture_exceptions', 'db_name','enabled',
            #                                                        'exception_classes', 'on_invoke_target', 'pickle_response', 'print_requests','sqlite_requests',
            #                                                        'table_name','target_class', 'target_function', 'target_function_name','update_mode']
            assert _.db_name                                  == SQLITE_DB_NAME__SSH_REQUESTS_CACHE
            assert _.table_name                               == SQLITE_TABLE_NAME__SSH_REQUESTS
            assert _.sqlite_requests.exists()                 is True
            assert _.cache_entries()                          == []
            assert _.cache_table.new_row_obj().__locals__() == {'comments'        : '' ,
                                                                'metadata'        : '' ,
                                                                'request_data'    : '' ,
                                                                'request_hash'    : '' ,
                                                                'request_type'    : '' ,
                                                                'response_bytes'  : b'',
                                                                'response_data'   : '' ,
                                                                'response_hash'   : '' ,
                                                                'response_type'   : '' ,
                                                                'source'          : '' ,
                                                                'timestamp'       : 0  }
            assert parent_folder (_.sqlite_requests.db_path)  == current_temp_folder()
            assert file_extension(_.sqlite_requests.db_path)  == '.sqlite'
            assert _.sqlite_requests.in_memory                is False
            assert base_types(_)                              == [Sqlite__Cache__Requests__Patch ,
                                                                  Sqlite__Cache__Requests        ,
                                                                  Kwargs_To_Self                 ,
                                                                  object                         ]
            assert _.target_class                             == SSH__Execute
            assert _.target_function                          != SSH__Execute.execute_command
            assert _.target_function_name                     == "execute_command"

            assert _.table_name == _.database().table_name
            assert _.db_name    == _.database().db_name



    def test___enter____exit__(self):
        assert SSH__Execute.execute_command == SSH__Execute.execute_command
        assert SSH__Execute.execute_command == self.cache_ssh_requests.target_function
        assert SSH__Execute.execute_command.__qualname__ == 'SSH__Execute.execute_command'
        with self.cache_ssh_requests  as _:
            assert SSH__Execute.execute_command              != self.cache_ssh_requests.target_function
            assert SSH__Execute.execute_command.__qualname__ == 'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'
        assert SSH__Execute.execute_command == self.cache_ssh_requests.target_function
        assert SSH__Execute.execute_command.__qualname__ == 'SSH__Execute.execute_command'

    def test_invoke_target(self):
        mock_ssh_host          = get_env(ENV_VAR__SSH__HOST, '')
        mock_path              = '/aaa'
        mock_files             = ['/ccc', '/ddd']
        expected_request_data  = to_json_str(dict_to_toml({'args': ('/aaa',), 'kwargs': {}, 'ssh_host': mock_ssh_host}))
        expected_response_data = {'files': mock_files, 'path': mock_path}
        expected_response_bytes = pickle_to_bytes(expected_response_data)
        expected_request_hash   = sha_256(expected_request_data)
        expected_response_hash  = bytes_sha256(expected_response_bytes)

        def on_invoke_target(*args):
            return {'files': mock_files,
                    'path'  : args[1][1]  }

        with self.cache_ssh_requests as _:
            _.set__add_timestamp(False)
            _.set_on_invoke_target(on_invoke_target)

            assert _.cache_entries() == []

            ssh = SSH__Execute(ssh_host= mock_ssh_host).setup()
            ssh.execute_command__return_stdout(mock_path)

            cache_entry = _.cache_entries()[0]
            assert len(_.cache_entries()) == 1

            response_data          = pickle_from_bytes(cache_entry.get('response_bytes'))
            assert response_data == expected_response_data

            assert cache_entry == { 'comments'       : ''                     ,
                                    'id'             : 1                      ,
                                    'metadata'       : ''                     ,
                                    'request_data'   : expected_request_data  ,
                                    'request_hash'   : expected_request_hash  ,
                                    'request_type'   : ''                     ,
                                    'response_bytes' : expected_response_bytes,
                                    'response_data'  : ''                     ,
                                    'response_hash'  : expected_response_hash ,
                                    'response_type'  : 'pickle'               ,
                                    'source'         : ''                     ,
                                    'timestamp'      : 0                      }



    def test__bug__db_name_does_not_match_db_path(self):
        with self.cache_ssh_requests as _:
            assert _.database().db_name    == _.db_name                                 # FIXED     # BUG, these should be the same
            assert _.database().table_name == _.table_name
            assert _.database().db_name    != file_name(_.database().db_path)           # FIXED     # BUG, these should be the same

            assert _.db_name               == 'ssh_requests_cache.sqlite' == SQLITE_DB_NAME__SSH_REQUESTS_CACHE
            assert _.table_name            == 'ssh_requests'              == SQLITE_TABLE_NAME__SSH_REQUESTS
            assert _.database().table_name != 'requests'                                # FIXED     # BUG, these should be the same


        ssh__cache__requests = SSH__Cache__Requests()
        assert ssh__cache__requests.db_name    == SQLITE_DB_NAME__SSH_REQUESTS_CACHE
        assert ssh__cache__requests.table_name == SQLITE_TABLE_NAME__SSH_REQUESTS
        assert ssh__cache__requests.database().db_path   is not None                    # FIXED     # BUG, this should be set
        assert ssh__cache__requests.database().in_memory is False                       # FIXED     # BUG, this should be False
        assert ssh__cache__requests.db_name == ssh__cache__requests.database().db_name  # FIXED     # BUG, these should be the same

        sqlite__cache__requests__patch = Sqlite__Cache__Requests__Patch()
        assert sqlite__cache__requests__patch.db_name    == ''
        assert sqlite__cache__requests__patch.table_name == ''
        assert sqlite__cache__requests__patch.database().db_path   is None
        assert sqlite__cache__requests__patch.database().in_memory is True
        assert sqlite__cache__requests__patch.database().db_name.startswith('db_local_')

