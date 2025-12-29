import pytest
from unittest                                                   import TestCase
from osbot_utils.utils.Env                                      import in_github_action
from osbot_utils.helpers.cache_on_self.Cache_On_Self            import Cache_On_Self
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self


class test__performance__cache_on_self(TestCase):

    def test__performance__confirm__cache_on_self__current_invocation_overhead(self):
        if in_github_action():
            pytest.skip("disable in GH actions since the durations are much slower there")
        class Performance_Host:
            def an_function(self):
                return 42

            @cache_on_self
            def an_function_with_cache(self):
                return 42

        host = Performance_Host()
        host.an_function()                       # warm up both functions
        host.an_function_with_cache()            # especially the one with the cache

        invocation_count = 1000
        with capture_duration(precision=5) as duration__an_function:
            for i in range(invocation_count):
                assert host.an_function() is 42

        cache = host.an_function_with_cache(__return__='cache_on_self')
        assert type(cache) is Cache_On_Self
        assert cache.disabled is False

        with capture_duration(precision=5) as duration__an_function_with_cache:
            for i in range(invocation_count):
                assert host.an_function_with_cache() is 42

        assert 0.0001 < duration__an_function_with_cache.seconds < 0.003

        overhead_ratio = duration__an_function_with_cache.seconds / duration__an_function.seconds
        assert overhead_ratio < 20                           # confirm that the cache overhead is less than 15x

    def test__performance__cache_overhead_with_arguments(self):
        """Test performance overhead with various argument patterns"""
        class Performance_Test_Class:
            def no_cache_method(self, a, b, c):
                return a + b + c

            @cache_on_self
            def cached_method(self, a, b, c):
                return a + b + c

        obj = Performance_Test_Class()
        if in_github_action():
            iterations = 10000                      # in GH actions try with 10000x (which should take about 190ms
        else:
            iterations = 100                        # locally do 100x (which taks about 1.9 ms)

        # Warm up
        obj.no_cache_method(1, 2, 3)
        obj.cached_method(1, 2, 3)

        # Test no cache
        with capture_duration(precision=5) as duration_no_cache:
            for _ in range(iterations):
                obj.no_cache_method(1, 2, 3)

        # Test with cache (cache hit scenario)
        with capture_duration(precision=5) as duration_cached:
            for _ in range(iterations):
                obj.cached_method(1, 2, 3)

        overhead_ratio = duration_cached.seconds / duration_no_cache.seconds
        assert overhead_ratio < 500  # Higher overhead due to hash calculation

    def test__performance__cache_miss_overhead(self):
        """Test performance overhead for cache misses"""
        class Cache_Miss_Class:
            @cache_on_self
            def process(self, value):
                return value * 2

        obj = Cache_Miss_Class()
        iterations = 100

        # Each call will be a cache miss (different arguments)
        with capture_duration(precision=5) as duration_misses:
            for i in range(iterations):
                obj.process(i)

        # Verify all were cache misses by checking internal cache
        cache_manager = obj.process(__return__='cache_on_self')
        assert len(cache_manager.cache_storage.cache_data[obj]) == iterations

    def test__performance__memory_usage(self):
        """Test memory usage with large cache"""
        class Memory_Test_Class:
            @cache_on_self
            def create_large_data(self, size):
                return [0] * size

        obj = Memory_Test_Class()

        # Create multiple large cached values
        for i in range(10):
            obj.create_large_data(i * 1000)

        # Get cache manager to verify internal storage
        cache_manager = obj.create_large_data(__return__='cache_on_self')
        assert len(cache_manager.cache_storage.cache_data[obj]) == 10

        # Each entry holds a reference to a large list
        # In production, this could lead to memory issues

    def test__performance__fast_path_optimization(self):
        """Test that fast path (no args) is significantly faster"""
        class Fast_Path_Class:
            @cache_on_self
            def no_args_method(self):
                return 42

            @cache_on_self
            def with_args_method(self, x):
                return x * 2

        obj = Fast_Path_Class()
        iterations = 100                    # 10000 produce the same result (but takes 190ms vs 1.9ms)

        # Warm up
        obj.no_args_method()
        obj.with_args_method(21)

        # Test fast path (no args)
        with capture_duration(precision=5) as duration_fast_path:
            for _ in range(iterations):
                obj.no_args_method()

        # Test slow path (with args)
        with capture_duration(precision=5) as duration_slow_path:
            for _ in range(iterations):
                obj.with_args_method(21)

        # Fast path should be significantly faster
        speedup = duration_slow_path.seconds / duration_fast_path.seconds
        assert speedup > 8  # Fast path should be at least 8x faster

    def test__performance__cache_size_impact(self):
        """Test performance impact of large cache sizes"""
        class Large_Cache_Class:
            @cache_on_self
            def method(self, n):
                return n * n

        obj = Large_Cache_Class()

        if in_github_action():
            iterations = 1000                   # takes about 30ms
        else:
            iterations = 100                    # takes about 3 ms
        # Fill cache with many entries
        for i in range(iterations):
            obj.method(i)

        # Measure lookup time with large cache
        with capture_duration(precision=5) as duration_lookup:
            for _ in range(iterations):
                obj.method(iterations/2)  # Hit in middle of cache

        # Even with large cache, lookups should be fast
        avg_lookup_time = duration_lookup.seconds / iterations
        assert avg_lookup_time < 0.00015     # Less than 0.15 milliseconds per lookup