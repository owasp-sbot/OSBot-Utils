from unittest                                               import TestCase

from osbot_utils.utils.Http                                 import GET
from osbot_utils.utils                                      import Http
from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests__Patch import Sqlite__Cache__Requests__Patch
from osbot_utils.utils.Files                                import parent_folder, current_temp_folder, file_name
from osbot_utils.utils.Misc                                 import in_github_action


class test_Sqlite__Cache__Requests__Patch(TestCase):
    requests_cache : Sqlite__Cache__Requests__Patch

    @classmethod
    def setUpClass(cls):
        cls.requests_cache = Sqlite__Cache__Requests__Patch()

    @classmethod
    def tearDownClass(cls):
        cls.requests_cache.sqlite_requests.delete()
        assert cls.requests_cache.sqlite_requests.exists() is False

    def test__init__(self):
        _ = self.requests_cache                 # we can't use the with context here since it auto applies the patch

        assert _.__attr_names__() == ['add_timestamp', 'cache_only_mode', 'db_name','enabled','on_invoke_target',
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

    def test_patch_apply__on_Http_GET(self):
        if in_github_action():
            # _.target_class

            self.requests_cache.target_class         = Http
            self.requests_cache.target_function      = GET
            self.requests_cache.target_function_name = 'GET'

            with self.requests_cache as _:
                assert _.cache_entries() == []
                for i in range(0,5):
                    response = Http.GET('https://www.google.com')
                    assert '<title>Google</title>' in response


