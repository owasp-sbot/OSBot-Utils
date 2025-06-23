from unittest                                        import TestCase
from osbot_utils.decorators.methods.cache_on_self    import cache_on_self
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

        cache_key_1 = cache_a.key_generator.generate_key(function=obj.method_a, args=(obj, 42), kwargs={})
        cache_key_2 = cache_a.key_generator.generate_key(function=obj.method_b, args=(obj, 42), kwargs={})

        # Both have cached values but in separate storage

        assert cache_a.cache_storage.has_cached_value(obj, cache_key_1) is True
        assert cache_b.cache_storage.has_cached_value(obj, cache_key_2) is True
        assert cache_key_1 != cache_key_2
        assert cache_key_1 == "__cache_on_self___method_a_ad5d62e7fc98fba2d0bd5069a26b55ab_"
        assert cache_key_2 == "__cache_on_self___method_b_ad5d62e7fc98fba2d0bd5069a26b55ab_"

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

    def test__regression__cache_on_self__complete_cache_collision__after__non_supported_values(self):
        class Test_Class:
            @cache_on_self
            def process(self, data):
                return f"processing: {repr(data)}"

        obj_a = Test_Class()

        result_a_1 = obj_a.process(obj_a )      # using an object
        result_a_2 = obj_a.process(self)        # using another object

        assert result_a_1 == f"processing: {repr(obj_a)}"                   # ok
        assert result_a_2 == f"processing: {repr(obj_a)}"                   # Fixed: BUG
        assert result_a_2 != f"processing: {repr(self)}"                    # Fixed: BUG

        obj_b = Test_Class()

        result_b_1 = obj_b.process(None)  # starting with None
        result_b_2 = obj_b.process(self)  # using an obj

        assert result_b_1 == f"processing: None"                            # ok
        assert result_b_2 == f"processing: {repr(self)}"                    # Fixed:  BUG

        obj_c = Test_Class()

        result_c_1 = obj_b.process(None)    # starting with None
        result_c_2 = obj_b.process(123)     # using a supported value
        result_c_3 = obj_b.process(self)    # using an obj

        assert result_c_1 == f"processing: None"            # ok
        assert result_c_2 == f"processing: 123"             # ok
        assert result_c_3 == f"processing: {repr(self)}"    # Fixed: BUG      (picks up the 'non-supported' value)

        assert obj_a.__dict__ == {}
        assert obj_b.__dict__ == {}
        assert obj_c.__dict__ == {}


    def test__regression__cache_on_self__complete_cache_collision(self):
        class Test_Class:
            @cache_on_self
            def process(self, data):
                return f"processing: {repr(data)}"

        obj = Test_Class()

        # All these different calls will share the SAME cache entry!
        result_1 = obj.process({'a': 1})
        result_2 = obj.process({'b': 2, 'c': 3})
        result_3 = obj.process([1, 2, 3])
        result_4 = obj.process(set([4, 5, 6]))
        result_5 = obj.process(None)
        result_6 = obj.process(obj)  # Even passing self!

        # They all return the FIRST cached value
        #assert result_1 == "processing: {'a': 1}"
        # assert result_2 == "processing: {'a': 1}"  # BUG!
        # assert result_3 == "processing: {'a': 1}"  # BUG!
        # assert result_4 == "processing: {'a': 1}"  # BUG!
        # assert result_5 == "processing: {'a': 1}"  # BUG!
        # assert result_6 == "processing: {'a': 1}"  # BUG!

        assert result_2 == "processing: {'b': 2, 'c': 3}"   # Fixed
        assert result_3 == "processing: [1, 2, 3]"          # Fixed
        assert result_4 == "processing: {4, 5, 6}"          # Fixed
        assert result_5 == "processing: None"               # Fixed
        assert result_6 == f"processing: {repr(obj)}"       # Fixed

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test__regression__cache_on_self__caching__mutable_arguments(self):
        class Test_Class:
            @cache_on_self
            def process_dict(self, data):
                # Return a value that includes the dict's content
                return f"processed: {data.get('key', 'no-key')}"

            @cache_on_self
            def process_list(self, items):
                return f"count: {len(items)}"

        obj = Test_Class()

        # Test with dict
        data    = {'key': 'value_1'}
        result_1 = obj.process_dict(data)
        assert result_1 == "processed: value_1"

        # Mutate the dict
        data['key'] = 'value_2'
        result_2 = obj.process_dict(data)
        assert result_2 == "processed: value_2"             # FIXED: BUG: should be "processed: value_2"

        # Test with list
        items = [1, 2, 3]
        list_result_1 = obj.process_list(items)
        assert list_result_1 == "count: 3"

        items.append(4)
        list_result_2 = obj.process_list(items)
        assert list_result_2 == "count: 4"                  # FIXED: BUG: should be "count: 4"

        # Verify instance remains clean
        assert obj.__dict__ == {}


    def test__regression__cache_on_self__string_concatenation_collision(self):
        """Test the string concatenation collision bug"""
        class Collision_Class:
            call_count = 0

            @cache_on_self
            def concat_numbers(self, *args):
                self.call_count += 1
                return f"call {self.call_count}: {args}"

        obj = Collision_Class()

        # These should all have different cache entries but they collide
        result1 = obj.concat_numbers(1, 23    )   # "123"
        result2 = obj.concat_numbers(12, 3    )   # "123"
        result3 = obj.concat_numbers(123            )   # "123"
        result4 = obj.concat_numbers("12", "3")   # "123"


        assert result1 == "call 1: (1, 23)"             # Fixed: BUG: All return the same cached value despite different args
        assert result2 == "call 2: (12, 3)"             # Fixed: BUG: Should be "call 2: (12, 3)"
        assert result3 == "call 3: (123,)"              # Fixed: BUG: Should be "call 3: (123,)"
        assert result4 == "call 4: ('12', '3')"         # Fixed: BUG: Should be "call 4: ('12', '3')"

        assert obj.call_count == 4                      # FIXED : BUG: Only called once due to collision

    def test__regression__cache_on_self__mixed_type_arguments(self):
        """Test bug with mixed supported and unsupported types"""
        class Mixed_Types_Class:
            @cache_on_self
            def process_mixed(self, name, data, count):
                return f"{name}: {len(data)} items, count={count}"

        obj = Mixed_Types_Class()

        # First call with list
        result1 = obj.process_mixed("test1", [1, 2, 3], 100)
        assert result1 == "test1: 3 items, count=100"

        # Different list but same name and count - should be different but isn't
        result2 = obj.process_mixed("test1", [1, 2, 3, 4, 5], 100)
        assert result2 == "test1: 5 items, count=100"           # FIXED: BUG: Should be "test1: 5 items, count=100"

        # Different name - creates new entry
        result3 = obj.process_mixed("test2", [1, 2], 100)
        assert result3 == "test2: 2 items, count=100"

    def test__regression__cache_on_self__recursive_calls(self):                          # Test caching with recursive method calls
        class Recursive_Class:

            def fibonacci__no_cache(self, n):
                if n <= 1:
                    return n
                return self.fibonacci__no_cache(n - 1) + self.fibonacci__no_cache(n - 2)        # Recursive calls will also use cache

            @cache_on_self
            def fibonacci(self, n):
                if n <= 1:
                    return n
                return self.fibonacci(n - 1) + self.fibonacci(n - 2)        # Recursive calls will also use cache

        obj = Recursive_Class()

        assert obj.fibonacci(1) == 1
        assert obj.fibonacci(2) == 1
        assert obj.fibonacci(3) == 2        # Fixed: BUG should be 2
        assert obj.fibonacci(4) == 3        # Fixed: BUG should be 3
        assert obj.fibonacci(5) == 5        # Fixed:BUG should be 5

        obj_1 = Recursive_Class()

        assert obj_1.fibonacci(1) == 1      # ok
        assert obj_1.fibonacci(1) == 1      # here there are no side effect of multiple class
        assert obj_1.fibonacci(2) == 1      # ok
        assert obj_1.fibonacci(2) == 1      # Fixed:BUG: should still be 1


        # Calculate fibonacci(5) without cache
        assert obj.fibonacci__no_cache(5) == 5                              # OK should be 5 (no cache response)
        assert obj.fibonacci__no_cache(5) == 5                              # OK multiple calls return same value
        assert obj.fibonacci__no_cache(5) == 5                              # OK multiple calls return same value
        assert obj.fibonacci__no_cache(4) == 3                              # OK, confirm other values
        assert obj.fibonacci__no_cache(3) == 2
        assert obj.fibonacci__no_cache(2) == 1
        assert obj.fibonacci__no_cache(1) == 1
        # Calculate fibonacci(5) with cache

        assert obj.fibonacci(5) == 5                                       # BUG should be 5 (not 14)
        assert obj.fibonacci(5) == 5                                      # BUG should be 5 (not 252)
        cache = obj.fibonacci(__return__='cache_on_self')
        cache.disabled = True                                               # BUG: Disable should had kicked in
        assert obj.fibonacci(5) == 5                                        # FIXED: BUG should be 5
        # Verify instance remains clean
        assert obj.__dict__ == {}