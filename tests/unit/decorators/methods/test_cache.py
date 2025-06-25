import sys
from unittest import TestCase

import pytest

from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.testing.Catch import Catch
from osbot_utils.testing.Profiler import Profiler


class test_cache(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

    def test_cache(self):

        class An_Class:
            @cache
            def an_function(self):
                return 42

        with Profiler() as profiler:
            assert An_Class().an_function() == 42

        assert len(profiler.events) == 10
        event    = profiler.events.pop()
        f_locals = event['f_locals']
        assert event['event'] == 'return'
        cache_id = f_locals['cache_id']
        function = f_locals['function']

        assert cache_id == 'osbot_cache_return_value__an_function'

        assert getattr(function, cache_id) == 42

        setattr(function, cache_id, 123)
        assert An_Class().an_function() == 123

    def test_cache_on_self__outside_an_class(self):

        @cache_on_self
        def an_function():
            pass

        with Catch(log_exception=False) as catch:
            an_function()

        assert catch.exception_value.args[0] == "cache_on_self could not find self - no arguments provided"