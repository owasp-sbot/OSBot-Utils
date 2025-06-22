from unittest                                      import TestCase
from osbot_utils.decorators.methods.cache_on_self  import cache_on_self
from osbot_utils.helpers.cache_on_self.Cache_On_Self import Cache_On_Self


class test__regression__cache_on_self(TestCase):

    def test__regression__cache_on_self__none_values_ignored(self):
        """Test that None values are completely ignored in cache key generation"""
        class None_Values_Class:
            call_count = 0

            @cache_on_self
            def process_with_none(self, a, b, c):
                self.call_count += 1
                return f"call {self.call_count}: a={a}, b={b}, c={c}"

        obj = None_Values_Class()

        # These should have different cache keys but don't
        result1 = obj.process_with_none("x", None, "y")
        result2 = obj.process_with_none("x", "ignored", "y")  # 'ignored' is where None was

        # BUG: Both calls produce the same cache key "xy"
        assert result1 == "call 1: a=x, b=None, c=y"
        assert result2 == "call 2: a=x, b=ignored, c=y"  # FIXED: Now creates different cache entry
        assert obj.call_count == 2  # Called twice as expected

    def test__regression__no_instance_pollution(self):
        """Verify that cache storage doesn't pollute instance attributes"""
        class Clean_Class:
            def __init__(self):
                self.my_attribute = "original"

            @cache_on_self
            def cached_method(self, value):
                return value * 2

        obj = Clean_Class()

        # Initial state
        assert obj.__dict__ == {'my_attribute': 'original'}

        # Make several cached calls
        assert obj.cached_method(5) == 10
        assert obj.cached_method(5) == 10  # Cache hit
        assert obj.cached_method(10) == 20

        # Instance should remain clean
        assert obj.__dict__ == {'my_attribute': 'original'}

        # Verify cache exists internally
        cache_manager = obj.cached_method(__return__='cache_on_self')
        assert len(cache_manager.cache_storage.cache_data[obj]) == 2  # Two different cache entries

    def test__regression__cache_isolation_between_methods(self):
        """Ensure cache is properly isolated between different methods"""
        class Multi_Method_Class:
            @cache_on_self
            def method_a(self, value):
                return f"A: {value}"

            @cache_on_self
            def method_b(self, value):
                return f"B: {value}"

        obj = Multi_Method_Class()

        # Call both methods with same argument
        assert obj.method_a(42) == "A: 42"
        assert obj.method_b(42) == "B: 42"

        # Each should have its own cache
        cache_a : Cache_On_Self
        cache_b : Cache_On_Self
        cache_a = obj.method_a(__return__='cache_on_self')
        cache_b = obj.method_b(__return__='cache_on_self')

        # Different cache managers
        assert cache_a is not cache_b

        cache_key_1 = cache_a.key_generator.generate_key(function=obj.method_a, args=[42], kwargs={})
        cache_key_2 = cache_a.key_generator.generate_key(function=obj.method_b, args=[42], kwargs={})

        # Both have cached values but in separate storage
        assert cache_a.cache_storage.has_cached_value(obj, cache_key_1) is True
        assert cache_b.cache_storage.has_cached_value(obj, cache_key_2) is True
        assert cache_key_1 == "__cache_on_self___method_a_a1d0c6e83f027327d8461063f4ac58a6_"
        assert cache_key_2 == "__cache_on_self___method_b_a1d0c6e83f027327d8461063f4ac58a6_"

    def test__regression__cache_with_inheritance(self):
        """Verify cache works correctly with inheritance"""
        class Base:
            @cache_on_self
            def method(self):
                return "base"

        class Child(Base):
            @cache_on_self
            def method(self):
                return "child"

        base_obj = Base()
        child_obj = Child()

        # Each should have its own behavior
        assert base_obj.method() == "base"
        assert child_obj.method() == "child"

        # Verify separate cache managers
        base_cache = base_obj.method(__return__='cache_on_self')
        child_cache = child_obj.method(__return__='cache_on_self')

        assert base_cache is not child_cache
        assert base_cache.function.__name__ == 'method'
        assert child_cache.function.__name__ == 'method'

        # But they're different functions
        assert base_cache.function is not child_cache.function

    def test__regression__cache_metrics_shared(self):
        """Test that metrics are incorrectly shared between instances"""
        class Metrics_Class:
            @cache_on_self
            def method(self, value):
                return value * 2

        obj1 = Metrics_Class()
        obj2 = Metrics_Class()

        # Get cache managers
        cache1 = obj1.method(__return__='cache_on_self')
        cache2 = obj2.method(__return__='cache_on_self')

        # Reset metrics to start fresh
        cache1.metrics.reset()

        # obj1 makes some calls
        obj1.method(5)   # miss
        obj1.method(5)   # hit
        obj1.method(10)  # miss

        # Check metrics from obj1's perspective
        assert cache1.metrics.hits == 1
        assert cache1.metrics.misses == 2

        # Check metrics from obj2's perspective - they're the same!
        assert cache2.metrics.hits   == 0      # FIXED: BUG: Should be 0 (was 1)
        assert cache2.metrics.misses == 0      # FIXED: BUG: Should be 0 (was 2)

        # obj2's calls affect obj1's metrics!
        obj2.method(15)  # miss
        assert cache1.metrics.misses == 2     # FIXED: BUG: obj2's miss counted in obj1's metrics! (was 3)

    def test__regression__shared_cache_storage_across_instances(self):
        """Test that cache storage is incorrectly shared between instances"""
        class Shared_Storage_Class:
            def __init__(self, name):
                self.name = name

            @cache_on_self
            def get_data(self, key):
                return f"{self.name}: {key}"

        obj1 = Shared_Storage_Class("obj1")
        obj2 = Shared_Storage_Class("obj2")

        # Cache some data
        assert obj1.get_data("test") == "obj1: test"
        assert obj2.get_data("test") == "obj2: test"

        # Get the cache managers
        cache_mgr = obj1.get_data(__return__='cache_on_self')

        # The SAME cache storage contains data for BOTH instances!

        # for instance, cache_dict in cache_mgr.cache_storage.cache_data.items():
        #     print(f"  Instance {instance.name}: {list(cache_dict.keys())}")

        # Both instances are in the same cache storage
        assert obj1 in cache_mgr.cache_storage.cache_data
        assert obj2 not in cache_mgr.cache_storage.cache_data           # FIXED: BUG obj2 was in  cache_data

        # This means any instance can potentially access any other instance's cache!