from unittest                                           import TestCase
from osbot_utils.helpers.cache_on_self.Cache_On_Self    import Cache_On_Self
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class test_Cache_On_Self(TestCase):

    def setUp(self):
        self.sample_function = lambda self: 42
        self.cache_on_self = Cache_On_Self(function=self.sample_function)

    def test__init__(self):
        assert type(self.cache_on_self)                is Cache_On_Self
        assert self.cache_on_self.function             == self.sample_function
        assert self.cache_on_self.function_name        == '<lambda>'
        assert self.cache_on_self.no_args_key          == '__cache_on_self___<lambda>__'
        assert self.cache_on_self.target_self          is None
        assert self.cache_on_self.current_cache_key    == ''
        assert self.cache_on_self.current_cache_value  is None
        assert self.cache_on_self.reload_next          is False

        # Verify Type_Safe inheritance
        assert isinstance(self.cache_on_self, Type_Safe)
        assert self.cache_on_self.__locals__() == { 'cache_storage'      : self.cache_on_self.cache_storage        ,
                                                    'controller'          : self.cache_on_self.controller          ,
                                                    'current_cache_key'   : ''                                     ,
                                                    'current_cache_value' : None                                   ,
                                                    'disabled'            : False                                  ,
                                                    'function'            : self.sample_function                   ,
                                                    'function_name'       : '<lambda>'                             ,
                                                    'key_generator'       : self.cache_on_self.key_generator       ,
                                                    'metrics'             : self.cache_on_self.metrics             ,
                                                    'no_args_key'         : '__cache_on_self___<lambda>__'         ,
                                                    'reload_next'         : False                                  ,
                                                    'target_self'         : None                                   }

    def test__init__with_custom_function(self):
        def custom_function(self, x, y):
            return x + y

        cache = Cache_On_Self(function=custom_function)
        assert cache.function_name == 'custom_function'
        assert cache.no_args_key   == '__cache_on_self___custom_function__'

    def test__init__with_custom_supported_types(self):
        custom_types = [str, int]  # Only support strings and ints
        cache = Cache_On_Self(function=self.sample_function, supported_types=custom_types)
        assert cache.key_generator.supported_types == custom_types

    def test_handle_call__fast_path_no_args(self):
        class TestClass:
            pass

        test_obj = TestClass()
        args = (test_obj,)
        kwargs = {}

        # First call - cache miss
        result = self.cache_on_self.handle_call(args, kwargs)
        assert result == 42
        assert self.cache_on_self.metrics.hits   == 0
        assert self.cache_on_self.metrics.misses == 1
        assert hasattr(test_obj, '__cache_on_self___<lambda>__')

        # Second call - cache hit
        result = self.cache_on_self.handle_call(args, kwargs)
        assert result == 42
        assert self.cache_on_self.metrics.hits   == 1
        assert self.cache_on_self.metrics.misses == 1

    def test_handle_call__slow_path_with_args(self):
        def func_with_args(self, x):
            return x * 2

        cache = Cache_On_Self(function=func_with_args)

        class TestClass:
            pass

        test_obj = TestClass()
        args = (test_obj, 21)
        kwargs = {}

        # First call
        result = cache.handle_call(args, kwargs)
        assert result == 42
        assert cache.target_self       == test_obj
        assert cache.current_cache_key != cache.no_args_key  # Should use computed key
        assert cache.metrics.misses    == 1

        # Second call with same args
        result = cache.handle_call(args, kwargs)
        assert result == 42
        assert cache.metrics.hits == 1

    def test_handle_call__with_kwargs(self):
        def func_with_kwargs(self, x=10, y=20):
            return x + y

        cache = Cache_On_Self(function=func_with_kwargs)

        class TestClass:
            pass

        test_obj = TestClass()
        args = (test_obj,)
        kwargs = {'x': 15, 'y': 25}

        result = cache.handle_call(args, kwargs)
        assert result == 40
        assert cache.current_cache_key.startswith('__cache_on_self___func_with_kwargs__')  # Should have kwargs hash

    def test_handle_call__reload_cache(self):
        counter = {'value': 0}

        def counting_function(self):
            counter['value'] += 1
            return counter['value']

        cache = Cache_On_Self(function=counting_function)

        class TestClass:
            pass

        test_obj = TestClass()
        args     = (test_obj,)

        # First call
        assert cache.handle_call(args, {})  == 1
        assert counter                      == {'value': 1}
        assert cache.handle_call(args, {})  == 1  # Cached
        assert counter                      == {'value': 1}

        # Force reload via parameter
        assert cache.handle_call(args, {'reload_cache': True}) == 2
        assert cache.metrics.reloads == 1
        assert counter               == {'value': 2}
        assert cache.reload_next     is False           # Flag should be False

        # Force reload via flag
        cache.reload_next = True
        assert cache.handle_call_full(args, {}) == 3                                # we need to call the handle_call_full since that is path that handles extra params
        assert counter                     == {'value': 3}
        assert cache.reload_next is False  # Flag should be reset

    def test_execute_and_cache(self):
        def func(self, x):
            return x * 3

        cache = Cache_On_Self(function=func)

        class TestClass:
            pass

        test_obj = TestClass()
        cache.target_self = test_obj
        cache.current_cache_key = 'test_key'

        args = (test_obj, 14)
        clean_kwargs = {}

        cache.execute_and_cache(args, clean_kwargs, should_reload=False)

        assert hasattr(test_obj, 'test_key')
        assert getattr(test_obj, 'test_key') == 42
        assert cache.metrics.misses == 1

        # Test with reload
        cache.execute_and_cache(args, clean_kwargs, should_reload=True)
        assert cache.metrics.reloads == 1

    def test_clear(self):
        class TestClass:
            pass

        test_obj = TestClass()
        self.cache_on_self.target_self = test_obj
        self.cache_on_self.current_cache_key = 'test_key'

        # Set a cached value
        setattr(test_obj, 'test_key', 'cached_value')
        assert hasattr(test_obj, 'test_key')

        # Clear it
        self.cache_on_self.clear()
        assert not hasattr(test_obj, 'test_key')

    def test_clear_all(self):
        class TestClass:
            pass

        test_obj = TestClass()
        self.cache_on_self.target_self = test_obj

        # Set multiple cached values
        setattr(test_obj, '__cache_on_self___method1__', 'value1')
        setattr(test_obj, '__cache_on_self___method2_hash_', 'value2')
        setattr(test_obj, 'regular_attribute', 'not_cached')

        # Clear all cache
        self.cache_on_self.clear_all()

        assert not hasattr(test_obj, '__cache_on_self___method1__')
        assert not hasattr(test_obj, '__cache_on_self___method2_hash_')
        assert hasattr(test_obj, 'regular_attribute')  # Should not be cleared

    def test_get_all_keys(self):
        class TestClass:
            pass

        test_obj = TestClass()
        self.cache_on_self.target_self = test_obj

        # No cache initially
        assert self.cache_on_self.get_all_keys() == []

        # Add some cache entries
        setattr(test_obj, '__cache_on_self___method1__', 'value1')
        setattr(test_obj, '__cache_on_self___method2_hash_', 'value2')

        keys = self.cache_on_self.get_all_keys()
        assert len(keys) == 2
        assert '__cache_on_self___method1__' in keys
        assert '__cache_on_self___method2_hash_' in keys

    def test_stats(self):
        self.cache_on_self.metrics.hits = 10
        self.cache_on_self.metrics.misses = 5
        self.cache_on_self.metrics.reloads = 2
        self.cache_on_self.current_cache_key = 'test_key'

        stats = self.cache_on_self.stats()
        assert stats == { 'hits'      : 10                                       ,
                         'misses'    : 5                                        ,
                         'reloads'   : 2                                        ,
                         'hit_rate'  : 10 / (10 + 5)                           ,
                         'cache_key' : 'test_key'                               }

    def test__integration__full_workflow(self):
        def expensive_computation(self, n):
            # Simulate expensive operation
            return sum(range(n))

        cache = Cache_On_Self(function=expensive_computation)

        class ComputeClass:
            pass

        compute_obj = ComputeClass()

        # First computation
        result1 = cache.handle_call((compute_obj, 100), {})
        assert result1 == sum(range(100))
        assert cache.metrics.misses == 1

        # Cached result
        result2 = cache.handle_call((compute_obj, 100), {})
        assert result2 == result1
        assert cache.metrics.hits == 1

        # Different argument
        result3 = cache.handle_call((compute_obj, 50), {})
        assert result3 == sum(range(50))
        assert cache.metrics.misses == 2

        # Check stats
        stats = cache.stats()
        assert stats['hits']     == 1
        assert stats['misses']   == 2
        assert stats['hit_rate'] == 1/3