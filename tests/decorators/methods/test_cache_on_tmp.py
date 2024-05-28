import sys
from unittest import TestCase

import pytest

from osbot_utils.utils.Misc import str_md5, random_string
from osbot_utils.utils.Files import file_name
from osbot_utils.testing.Profiler import Profiler
from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp


class An_Class:
    @cache_on_tmp()
    def an_function(self):
        return 42

    @cache_on_tmp()
    def an_function_with_params(self, an_param):
        return an_param

class test_cache_on_tmp(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

    def test_cache_on_tmp(self):

        an_class = An_Class()
        with Profiler() as profiler:
            assert an_class.an_function() == 42

        cache_on_tmp_self: cache_on_tmp

        cache_on_tmp_self = profiler.get_f_locals_variable('self')
        last_cache_path   = cache_on_tmp_self.last_cache_path
        assert profiler.get_last_event()['event'] == 'return'
        assert cache_on_tmp_self.get_cache_in_tmp_data(last_cache_path) == 42
        assert an_class.an_function() == 42

        cache_on_tmp_self.save_cache_in_tmp_data(last_cache_path, "abc")
        assert an_class.an_function() == "abc"

        cache_on_tmp_self.reload_data = True
        assert an_class.an_function() == 42

        cache_on_tmp_self.return_cache_key = True

        assert 'osbot_cache_on_tmp/An_Class_an_function.gz' in an_class.an_function()

    def test_cache_on_tmp__with_params(self):
        param = 'aaaaa'
        with Profiler() as profiler:
            assert An_Class().an_function_with_params(param) == param

        cache_on_tmp_self = profiler.get_f_locals_variable('self')

        temp_file_name= f'An_Class_an_function_with_params_{str_md5(param)}.gz'
        assert file_name(cache_on_tmp_self.last_cache_path) == temp_file_name

    def test_test_cache_on_tmp__on_static_method(self):
        @cache_on_tmp()
        def an_method():
            return random_string(prefix='an_method')

        assert an_method() == an_method()

