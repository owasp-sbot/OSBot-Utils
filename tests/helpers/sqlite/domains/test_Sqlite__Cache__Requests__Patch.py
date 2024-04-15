from unittest                                                           import TestCase
from osbot_utils.utils.Http                                             import GET
from osbot_utils.utils                                                  import Http
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests__Patch  import Sqlite__Cache__Requests__Patch
from osbot_utils.utils.Files                                            import parent_folder, current_temp_folder, file_name
from osbot_utils.utils.Json                                             import to_json_str
from osbot_utils.utils.Misc                                             import str_sha256
from osbot_utils.utils.Objects                                          import pickle_save_to_bytes, pickle_load_from_bytes


class test_Sqlite__Cache__Requests__Patch(TestCase):
    requests_cache : Sqlite__Cache__Requests__Patch

    def setUp(self):
        self.requests_cache = Sqlite__Cache__Requests__Patch()

    def tearDown(self):
        self.requests_cache.sqlite_requests.delete()
        assert self.requests_cache.sqlite_requests.exists() is False

    def test__init__(self):
        _ = self.requests_cache                 # we can't use the with context here since it auto applies the patch

        assert _.__attr_names__() == ['add_timestamp', 'cache_only_mode', 'capture_exceptions', 'db_name','enabled','on_invoke_target',
                                      'pickle_response', 'sqlite_requests','table_name','target_class','target_function',
                                      'target_function_name','update_mode']
        assert type(_.target_class)     is object               # default value for object
        assert _.target_function        is None                 # default value for types.FunctionType
        assert _.target_function_name   is ''                   # default value for str
        assert _.db_name   .startswith('requests_cache_')
        assert _.table_name.startswith('requests_table_')
        assert _.sqlite_requests.exists() is True
        assert _.cache_entries() == []
        assert _.cache_table().new_row_obj().__locals__() == {'cache_hits'      : 0     ,
                                                              'comments'        : ''    ,
                                                              'latest'          : False ,
                                                              'request_data'    : ''    ,
                                                              'request_hash'    : ''    ,
                                                              'response_bytes'  : b''   ,
                                                              'response_data'   : ''    ,
                                                              'response_hash'   : ''    ,
                                                              'timestamp'       : 0     }
        assert parent_folder(_.sqlite_requests.db_path) == current_temp_folder()
        assert file_name    (_.sqlite_requests.db_path).startswith('requests_cache_')

    def test_patch_apply(self):
        expected_message = 'target_function, target_object and target_function_name must be set'
        def assert_expected_message():
            with self.assertRaises(ValueError) as context:
                self.requests_cache.patch_apply()
            assert context.exception.args[0] == expected_message

        assert_expected_message()                                                                           # expect to fail
        self.requests_cache.target_class         = Http
        assert_expected_message()                                                                           # expect to fail
        self.requests_cache.target_function      = GET
        assert_expected_message()                                                                           # expect to fail
        self.requests_cache.target_function_name = 'GET'

        assert Http.GET.__qualname__ == 'GET'                                                               # original
        with self.requests_cache as _:                                                                      # patch will work now
            assert Http.GET.__qualname__ ==  'Sqlite__Cache__Requests__Patch.patch_apply.<locals>.proxy'    # patched
        assert Http.GET.__qualname__ == 'GET'                                                               # back to original

    def test__attr__capture_exceptions(self):

        def on_invoke_target(target, args, kwargs):
            return f'GET call with args = {args} and kwargs = {kwargs}'

        self.requests_cache.target_class         = Http
        self.requests_cache.target_function      = GET
        self.requests_cache.target_function_name = 'GET'
        self.requests_cache.on_invoke_target     =   on_invoke_target
        self.requests_cache.add_timestamp        = False

        target_url                = 'https://www.google.com'
        expected_response         =  f"GET call with args = ('{target_url}',) and kwargs = {{}}"
        expected_request_data_obj = {'args': ['https://www.google.com'], 'kwargs': {}}
        expected_request_data     = to_json_str(expected_request_data_obj)
        expected_request_hash     = str_sha256(expected_request_data)
        expected_response_bytes   = pickle_save_to_bytes(expected_response)

        expected_cache_entry   = {'cache_hits'     : 0                      ,
                                   'comments'      : ''                     ,
                                   'id'            : 1                      ,
                                   'latest'        : 0                      ,
                                   'request_data'  : expected_request_data  ,
                                   'request_hash'  : expected_request_hash  ,
                                   'response_bytes': expected_response_bytes,
                                   'response_data' : ''                     ,
                                   'response_hash' : ''                     ,
                                   'timestamp'     : 0                      }

        with self.requests_cache as _:
            assert _.cache_entries() == []
            for i in range(0,5):
                response = Http.GET(target_url)
                assert response == expected_response
            assert len(_.cache_entries()) == 1
            cache_entry = _.cache_entries()[0]
            assert cache_entry.get('response_bytes') == expected_response_bytes
            assert cache_entry == expected_cache_entry

    def test_bug__exceptions_are_not_cached(self):

        exception_message = 'exception raise inside on_invoke_target'

        def on_invoke_target(target, args, kwargs):
            exception = Exception(exception_message)
            raise exception

        self.requests_cache.target_class         = Http
        self.requests_cache.target_function      = GET
        self.requests_cache.target_function_name = 'GET'
        self.requests_cache.on_invoke_target     = on_invoke_target

        # with capture_exceptions set to False (default behaviour)
        with self.requests_cache as _:
            assert _.cache_entries() == []
            with self.assertRaises(Exception) as context:
                Http.GET('')
            assert context.exception.args[0] == exception_message
            assert _.cache_entries() == []

        # with capture_exceptions set to True
        with self.requests_cache as _:
            _.capture_exceptions = True
            assert _.cache_entries() == []
            with self.assertRaises(Exception) as context:
                Http.GET('')
            assert context.exception.args[0] == exception_message

            assert len(_.cache_entries()) == 1
            cache_entry    = _.cache_entries()[0]
            response_bytes = cache_entry.get('response_bytes')
            response_obj   = pickle_load_from_bytes(response_bytes)
            assert type(response_obj) is Exception
            assert response_obj.args == (exception_message,)

    # def test_regression__confirm_exceptions_are_handled(self):
    #     self.requests_cache.target_class         = Http
    #     self.requests_cache.target_function      = GET
    #     self.requests_cache.target_function_name = 'GET'
    #
    #     with self.requests_cache as _:
    #         # assert len(_.cache_entries()) == 0
    #         # assert _.capture_exceptions is False                        # default setting
    #         #
    #         # with self.assertRaises(Exception) as context:
    #         #     Http.GET('https://www.google.com/404')
    #         #
    #         # assert context.exception.filename == 'https://www.google.com/404'
    #         # assert context.exception.status   == 404
    #         # assert context.exception.msg      == 'Not Found'
    #         # assert len(_.cache_entries()) == 0                          # without capture_exceptions there is not data cached
    #
    #         _.capture_exceptions = True
    #
    #         with self.assertRaises(Exception) as context:
    #             Http.GET('https://www.google.com/404')
    #
    #         assert len(_.cache_entries()) == 0
