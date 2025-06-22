from unittest                                             import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Controller  import Cache_Controller
from osbot_utils.testing.Catch                           import Catch


class test_Cache_Controller(TestCase):

    def setUp(self):
        self.controller = Cache_Controller()

    def test__init__(self):
        assert type(self.controller) is Cache_Controller

    def test_extract_clean_kwargs(self):
        # Test with no special parameters
        kwargs = {'a': 1, 'b': 2, 'c': 3}
        clean = self.controller.extract_clean_kwargs(kwargs)
        assert clean == kwargs

        # Test with reload_cache
        kwargs = {'a': 1, 'reload_cache': True, 'b': 2}
        clean = self.controller.extract_clean_kwargs(kwargs)
        assert clean == {'a': 1, 'b': 2}
        assert 'reload_cache' not in clean

        # Test with __return__
        kwargs = {'a': 1, '__return__': 'cache_on_self', 'b': 2}
        clean = self.controller.extract_clean_kwargs(kwargs)
        assert clean == {'a': 1, 'b': 2}
        assert '__return__' not in clean

        # Test with both special parameters
        kwargs = {'a': 1, 'reload_cache': False, '__return__': 'metrics', 'b': 2}
        clean = self.controller.extract_clean_kwargs(kwargs)
        assert clean == {'a': 1, 'b': 2}

        # Test with empty kwargs
        assert self.controller.extract_clean_kwargs({}) == {}

    def test_should_reload(self):
        # Test with no reload indicators
        assert self.controller.should_reload({}, False) is False
        assert self.controller.should_reload({'a': 1}, False) is False

        # Test with reload_cache in kwargs
        assert self.controller.should_reload({'reload_cache': True}, False) is True
        assert self.controller.should_reload({'reload_cache': False}, False) is False
        assert self.controller.should_reload({'reload_cache': None}, False) is False
        assert self.controller.should_reload({'reload_cache': 'yes'}, False) is False  # Only True matters

        # Test with reload_next_flag
        assert self.controller.should_reload({}, True) is True
        assert self.controller.should_reload({'a': 1}, True) is True
        assert self.controller.should_reload({'reload_cache': False}, True) is True  # Flag takes precedence

    def test_should_return_cache_manager(self):
        # Test when should return cache manager
        assert self.controller.should_return_cache_manager({'__return__': 'cache_on_self'}) is True

        # Test when should not return cache manager
        assert self.controller.should_return_cache_manager({}) is False
        assert self.controller.should_return_cache_manager({'__return__': 'metrics'}) is False
        assert self.controller.should_return_cache_manager({'__return__': None}) is False
        assert self.controller.should_return_cache_manager({'__return__': ''}) is False
        assert self.controller.should_return_cache_manager({'other': 'value'}) is False

    def test_extract_self_from_args__valid(self):
        class TestClass:
            pass

        test_obj = TestClass()
        args = (test_obj, 'arg1', 'arg2')

        result = self.controller.extract_self_from_args(args)
        assert result is test_obj

        # Test with just self
        args = (test_obj,)
        result = self.controller.extract_self_from_args(args)
        assert result is test_obj

    def test_extract_self_from_args__errors(self):
        # Test with empty args
        with Catch(expect_exception=True) as catch:
            self.controller.extract_self_from_args(())
        assert catch.exception_value.args[0] == "cache_on_self could not find self - no arguments provided"

        # Test with non-instance first argument (though this is a bit contrived since classes have types)
        # In practice, this error might not trigger as easily since most objects have a class type
        # But we can test the logic is there
        args = (None, 'arg1')  # None still has a type (NoneType)
        result = self.controller.extract_self_from_args(args)
        assert result is None  # This actually passes the check

    def test__integration__complex_kwargs_handling(self):
        kwargs = {
            'param1': 'value1',
            'param2': 42,
            'reload_cache': True,
            '__return__': 'cache_on_self',
            'param3': [1, 2, 3],
            'param4': {'nested': 'dict'}
        }

        # Extract clean kwargs
        clean = self.controller.extract_clean_kwargs(kwargs)
        assert clean == {
            'param1': 'value1',
            'param2': 42,
            'param3': [1, 2, 3],
            'param4': {'nested': 'dict'}
        }

        # Check reload
        assert self.controller.should_reload(kwargs, False) is True

        # Check return cache manager
        assert self.controller.should_return_cache_manager(kwargs) is True