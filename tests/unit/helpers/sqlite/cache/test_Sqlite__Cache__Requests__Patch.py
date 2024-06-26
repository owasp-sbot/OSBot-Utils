from unittest                                                           import TestCase
from osbot_utils.utils.Http                                             import GET
from osbot_utils.utils                                                  import Http
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Patch    import Sqlite__Cache__Requests__Patch
from osbot_utils.utils.Json                                             import to_json_str
from osbot_utils.utils.Misc                                             import str_sha256, bytes_sha256
from osbot_utils.utils.Objects                                          import pickle_save_to_bytes, pickle_load_from_bytes


class test_Sqlite__Cache__Requests__Patch(TestCase):
    requests_cache : Sqlite__Cache__Requests__Patch

    def setUp(self):
        self.requests_cache = Sqlite__Cache__Requests__Patch()
        assert self.requests_cache.cache_table.database.in_memory is True

    def test__init__(self):
        _ = self.requests_cache                 # we can't use the with context here since it auto applies the patch

        # assert _.__attr_names__() == ['add_source_location', 'add_timestamp', 'cache_actions', 'cache_data', 'cache_only_mode', 'capture_exceptions', 'db_name','enabled',
        #                               'exception_classes', 'on_invoke_target', 'pickle_response', 'sqlite_requests',
        #                               'table_name','target_class','target_function', 'target_function_name','update_mode']
        assert type(_.target_class)     is object               # default value for object
        assert _.target_function        is None                 # default value for types.FunctionType
        assert _.target_function_name   is ''                   # default value for str
        assert _.db_name                == ''
        assert _.table_name             == ''
        assert _.sqlite_requests.exists() is True
        assert _.cache_entries() == []
        assert _.cache_table.new_row_obj().__locals__() == {'comments'        : ''    ,
                                                            'metadata'        : ''    ,
                                                            'request_data'    : ''    ,
                                                            'request_hash'    : ''    ,
                                                            'request_type'    : ''    ,
                                                            'response_bytes'  : b''   ,
                                                            'response_data'   : ''    ,
                                                            'response_hash'   : ''    ,
                                                            'response_type'   : ''    ,
                                                            'source'          : ''    ,
                                                            'timestamp'       : 0     }
        assert _.sqlite_requests.db_path is None


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
        self.requests_cache.set_on_invoke_target(on_invoke_target)

        self.requests_cache.set__add_timestamp(False)

        target_url                = 'https://www.google.com'
        expected_response         =  f"GET call with args = ('{target_url}',) and kwargs = {{}}"
        expected_request_data_obj = {'args': ['https://www.google.com'], 'kwargs': {}}
        expected_request_data     = to_json_str(expected_request_data_obj)
        expected_request_hash     = str_sha256(expected_request_data)
        expected_response_bytes   = pickle_save_to_bytes(expected_response)
        expected_response_hash    = bytes_sha256(expected_response_bytes)

        expected_cache_entry   = { 'comments'      : ''                     ,
                                   'id'            : 1                      ,
                                   'metadata'      : ''                     ,
                                   'request_data'  : expected_request_data  ,
                                   'request_hash'  : expected_request_hash  ,
                                   'request_type'  : ''                     ,
                                   'response_bytes': expected_response_bytes,
                                   'response_data' : ''                     ,
                                   'response_hash' : expected_response_hash ,
                                   'response_type' :  'pickle'              ,   # todo: BUG we should not be using pikle in this '__Patch' class,
                                   'source'        : ''                     ,
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
        self.requests_cache.set_on_invoke_target(on_invoke_target)

        # with capture_exceptions set to False (default behaviour)
        with self.requests_cache as _:
            assert _.cache_entries() == []
            with self.assertRaises(Exception) as context:
                Http.GET('')
            assert context.exception.args[0] == exception_message
            assert _.cache_entries() == []

        # with capture_exceptions set to True
        with self.requests_cache as _:
            _.config.capture_exceptions = True

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


    def test__bug__capture_exceptions__not_propagated_to_all_configs(self):
        def check_value_in_config(target, attribute_name, expected_value):
            current_value = getattr(target, attribute_name)
            assert current_value == expected_value , f'expected value for {attribute_name} to be {expected_value} but got {current_value}'
            return

        def check_all_values_in_config(attribute_name, expected_value):
            targets = [ self.requests_cache             .config ,
                        self.requests_cache.cache_invoke.config ,
                        self.requests_cache.cache_row   .config ,
                        self.requests_cache.cache_sqlite.config ]
            for target in targets:
                check_value_in_config(target, attribute_name, expected_value)

        check_all_values_in_config('capture_exceptions', False)

        self.requests_cache.config.capture_exceptions = True

        check_all_values_in_config('capture_exceptions', True)

        self.requests_cache.config.capture_exceptions = False

        check_all_values_in_config('capture_exceptions', False)