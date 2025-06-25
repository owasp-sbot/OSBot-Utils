# from unittest                                                   import TestCase
# from osbot_utils.helpers.cache_on_self.Cache_Key_Generator      import CACHE_ON_SELF_KEY_PREFIX
# from osbot_utils.helpers.cache_on_self.Cache_On_Self            import Cache_On_Self
# from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
# from osbot_utils.type_safe.Type_Safe                            import Type_Safe
# from osbot_utils.decorators.methods.cache_on_self               import cache_on_self, cache_on_self__get_cache_in_key, cache_on_self__args_to_str, cache_on_self__kwargs_to_str
# from osbot_utils.testing.Catch                                  import Catch
# from osbot_utils.utils.Objects                                  import obj_data
#
#
# class An_Class:
#     @cache_on_self
#     def an_function(self):
#         return 42
#
#     @cache_on_self
#     def echo(self, value):
#         return value
#
#     @cache_on_self
#     def echo_args(self, *args):
#         return args
#
#
# class test_cache_on_self(TestCase):
#
#     # ===== ORIGINAL TESTS =====
#
#     def test_cache_on_self(self):
#         an_class_1                = An_Class()                                              # create 1st instance
#         cache_key                 = cache_on_self__get_cache_in_key(an_class_1.an_function)  # get key from self
#         assert cache_key          == f'{CACHE_ON_SELF_KEY_PREFIX}_an_function__'            # confirm cache key value
#         assert obj_data(an_class_1) == {}                                                   # confirm cache key has not been added to self
#
#         # testing function that returns static value
#         assert an_class_1.an_function() == 42                                               # invoke method, set cache and confirm return value
#         assert obj_data(an_class_1, show_internals=True).get(cache_key) == 42                # confirm attribute has been set in class
#
#         assert an_class_1.__cache_on_self___an_function__               == 42               # which can be accessed directly
#         an_class_1.__cache_on_self___an_function__                      = 12                # if we change the attribute directly
#         assert obj_data(an_class_1, show_internals=True).get(cache_key) == 12               # confirm value changes (via obj data)
#         assert an_class_1.__cache_on_self___an_function__               == 12               # confirm value change (directly)
#
#         an_class_2 = An_Class()                                                             # create 2nd instance
#         assert an_class_2.an_function() == 42                                               # confirm previous version was not affected
#
#         an_class_3 = An_Class()                                                             # create 3rd instance
#         assert an_class_3.an_function() == 42                                               # confirm previous version was not affected
#
#         # testing function that returns dynamic value (with args)
#         assert an_class_1.echo(111) == 111                                                  # confirm returns echo value
#         assert an_class_1.echo(111) == 111
#         assert an_class_1.echo(222) == 222                                                  # config, new value has been set
#         assert an_class_1.echo(111) == 111
#
#         assert an_class_2.echo(333) == 333                                                  # confirm returns echo value
#         assert an_class_2.echo(333) == 333
#         assert an_class_2.echo(444) == 444                                                  # config, new value has been set
#
#         assert an_class_3.echo(555) == 555                                                  # confirm returns echo value
#         assert an_class_3.echo(555) == 555
#         assert an_class_3.echo(666) == 666                                                  # config, new value has been set
#
#         obj_data__class_1 = obj_data(an_class_1, show_internals=True)
#         obj_data__class_2 = obj_data(an_class_2, show_internals=True)
#         obj_data__class_3 = obj_data(an_class_3, show_internals=True)
#         cache_items__class_1 = {k: v for k, v in obj_data__class_1.items() if k.startswith('__cache_on_self__')}
#         cache_items__class_2 = {k: v for k, v in obj_data__class_2.items() if k.startswith('__cache_on_self__')}
#         cache_items__class_3 = {k: v for k, v in obj_data__class_3.items() if k.startswith('__cache_on_self__')}
#
#         assert cache_items__class_1 == {'__cache_on_self___an_function__'                         : 12  ,
#                                         '__cache_on_self___echo_698d51a19d8a121ce581499d7b701668_': 111 ,
#                                         '__cache_on_self___echo_bcbe3365e6ac95ea2c0343a2395834dd_': 222 }
#
#         assert cache_items__class_2 == {'__cache_on_self___an_function__'                         : 42  ,
#                                         '__cache_on_self___echo_310dcbbf4cce62f762a2aaa148d556bd_': 333 ,
#                                         '__cache_on_self___echo_550a141f12de6341fba65b0ad0433500_': 444 }
#
#         assert cache_items__class_3 == {'__cache_on_self___an_function__'                         : 42  ,
#                                         '__cache_on_self___echo_15de21c670ae7c3f6f3f1f37029303c9_': 555 ,
#                                         '__cache_on_self___echo_fae0b27c451c728867a567e8c1bb4e53_': 666 }
#
#         # testing function that returns dynamic value (with kargs)
#         assert an_class_1.echo(value=111) == 111                                                    # confirm returns echo value
#         assert an_class_1.echo(value=222) == 222                                                    # confirms new value
#
#         assert an_class_2.echo(value=333) == 333                                                    # confirm returns echo value
#         assert an_class_2.echo(value=444) == 444                                                    # confirms new value
#
#         assert an_class_3.echo(value=555) == 555                                                    # confirm returns echo value
#         assert an_class_3.echo(value=666) == 666                                                    # confirms new value
#
#     def test_cache_on_self__multiple_types_in_arg_cache(self):
#         args      = ('a', 1, 1.0)
#         an_class = An_Class()
#         assert an_class.echo_args(*args) == args
#         assert cache_on_self__args_to_str(args) == "a11.0"
#
#         args = ('a', None, 'bbb', [], {})
#         assert an_class.echo_args(*args) == args
#         assert cache_on_self__args_to_str(args) == "abbb"
#
#         args = ('a', -1, ['a'], {'b':None})
#         assert an_class.echo_args(*args) == args
#         assert cache_on_self__args_to_str(args) == "a-1"
#
#         args = (1, int(1), float(1), bytearray(b'1'), bytes(b'1'), bool(True), complex(1), str('1'))
#         assert an_class.echo_args(*args)        == args
#         assert an_class.echo_args(*args)        == (1, 1, 1.0, bytearray(b'1'), b'1', True, (1 + 0j), '1')
#         assert cache_on_self__args_to_str(args) == "111.0bytearray(b'1')b'1'True(1+0j)1"
#
#     def test_cache_on_self__kwargs_to_str(self):
#         assert cache_on_self__kwargs_to_str({"an":"value"    }) == 'an:value|'
#         assert cache_on_self__kwargs_to_str({"a": "b","c":"d"}) == 'a:b|c:d|'
#         assert cache_on_self__kwargs_to_str({"an": None      }) == ''
#         assert cache_on_self__kwargs_to_str({"an": 1         }) == 'an:1|'
#
#     def test_cache_on_self__outside_an_class(self):
#         @cache_on_self
#         def an_function():
#             pass
#
#         with Catch(log_exception=False) as catch:
#             an_function()
#
#         assert catch.exception_value.args[0] == "cache_on_self could not find self - no arguments provided"
#
#     def test_cache_on_self__reload_cache(self):
#         class An_Class_2(Type_Safe):
#             an_value : int = 41
#
#             @cache_on_self
#             def an_function(self):
#                 self.an_value += 1
#                 return self.an_value
#
#         an_class = An_Class_2()
#
#         assert an_class.an_function(                  ) == 42
#         assert an_class.an_function(                  ) == 42
#
#         assert an_class.an_function(reload_cache=True ) == 43
#         assert an_class.an_function(reload_cache=False) == 43
#         assert an_class.an_function(                  ) == 43
#
#         assert an_class.an_function(reload_cache=True ) == 44
#         assert an_class.an_function(reload_cache=False) == 44
#         assert an_class.an_function(                  ) == 44
#
#     def test__performance__confirm__cache_on_self__current_invocation_overhead(self):
#         class Performance_Host:
#             def an_function(self):
#                 return 42
#
#             @cache_on_self
#             def an_function_with_cache(self):
#                 return 42
#
#         host = Performance_Host()
#         host.an_function()                                                                          # warm up both functions
#         host.an_function_with_cache()                                                               # especially the one with the cache, since we are not measuring here the overhead of the cache creation (the focus is on the overhead of the cache check)
#
#         invocation_count = 1000
#         with capture_duration(precision=5) as duration__an_function:
#             for i in range(invocation_count):
#                 assert host.an_function() is 42
#         #assert duration__an_function.seconds < 0.0001                                               # confirm that 1000 invocations happen in less than 0.1 ms
#
#         cache = host.an_function_with_cache(__return__='cache_on_self')
#         assert type(cache) is Cache_On_Self
#         assert cache.disabled is False
#         #cache.disabled = False
#         with capture_duration(precision=5) as duration__an_function_with_cache:
#             for i in range(invocation_count):
#                 assert host.an_function_with_cache() is 42
#
#         # todo: remove this from the final version since we are better doing the comparison with the
#         assert 0.0001 < duration__an_function_with_cache.seconds < 0.0005                   # confirm that 1000 invocations now happen in between 0.1 and 0.5 ms
#
#         overhead_ratio = duration__an_function_with_cache.seconds / duration__an_function.seconds   # Calculate the overhead ratio instead
#
#         # print()
#         # print(f'duration__an_function           : {duration__an_function.seconds}')
#         # print(f'duration__an_function_with_cache: {duration__an_function_with_cache.seconds}')
#         # print(f'overhead_ratio                  : {overhead_ratio}')
#
#         #assert overhead_ratio > 20          # confirm that the cached version is significantly slower
#         assert overhead_ratio < 5          # confirm that the cache overhead is less than 5
#
#     # ===== EXTENDED TESTS =====
#
#     # ----- Basic Functionality Tests -----
#
#     def test_cache_on_self__with_multiple_arguments(self):
#         """Test caching with multiple arguments of supported types"""
#         class Multi_Args_Class:
#             @cache_on_self
#             def calculate(self, a, b, c):
#                 return a + b + c
#
#         obj = Multi_Args_Class()
#
#         # First call - should cache
#         assert obj.calculate(10, 20, 30) == 60
#
#         # Second call with same args - should use cache
#         assert obj.calculate(10, 20, 30) == 60
#
#         # Different args - should create new cache entry
#         assert obj.calculate(1, 2, 3) == 6
#
#         # Verify both entries exist
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 2
#
#     def test_cache_on_self__with_default_arguments(self):
#         """Test caching with default arguments"""
#         class Default_Args_Class:
#             @cache_on_self
#             def method_with_defaults(self, a=10, b=20):
#                 return a * b
#
#         obj = Default_Args_Class()
#
#         # Call without args
#         assert obj.method_with_defaults() == 200
#
#         # Call with partial args
#         assert obj.method_with_defaults(5) == 100
#
#         # Call with all args
#         assert obj.method_with_defaults(3, 4) == 12
#
#         # Verify separate cache entries
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 3
#
#     def test_cache_on_self__with_kwargs_order(self):
#         """Test that kwargs order doesn't affect caching"""
#         class Kwargs_Order_Class:
#             @cache_on_self
#             def method_with_kwargs(self, **kwargs):
#                 return sum(kwargs.values())
#
#         obj = Kwargs_Order_Class()
#
#         # Call with kwargs in different order
#         result1 = obj.method_with_kwargs(a=1, b=2, c=3)
#         result2 = obj.method_with_kwargs(c=3, a=1, b=2)
#         result3 = obj.method_with_kwargs(b=2, c=3, a=1)
#
#         assert result1 == result2 == result3 == 6
#
#         # Should have multiple cache entries (kwargs order matters in current implementation)
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) >= 1
#
#     def test_cache_on_self__return_value_types(self):
#         """Test caching with various return value types"""
#         class Various_Returns_Class:
#             @cache_on_self
#             def return_dict(self):
#                 return {'key': 'value', 'nested': {'data': 123}}
#
#             @cache_on_self
#             def return_list(self):
#                 return [1, 2, 3, [4, 5]]
#
#             @cache_on_self
#             def return_none(self):
#                 return None
#
#             @cache_on_self
#             def return_object(self):
#                 return self
#
#         obj = Various_Returns_Class()
#
#         # Test dict return
#         dict_result = obj.return_dict()
#         assert dict_result == {'key': 'value', 'nested': {'data': 123}}
#         assert obj.return_dict() is dict_result  # Same object reference
#
#         # Test list return
#         list_result = obj.return_list()
#         assert list_result == [1, 2, 3, [4, 5]]
#         assert obj.return_list() is list_result  # Same object reference
#
#         # Test None return
#         assert obj.return_none() is None
#
#         # Test object return
#         assert obj.return_object() is obj
#
#     # ----- Edge Case Tests -----
#
#     def test_cache_on_self__empty_string_arguments(self):
#         """Test caching with empty strings"""
#         class Empty_String_Class:
#             @cache_on_self
#             def process_string(self, s):
#                 return f"processed: '{s}'"
#
#         obj = Empty_String_Class()
#
#         assert obj.process_string('') == "processed: ''"
#         assert obj.process_string('') == "processed: ''"  # Should use cache
#         assert obj.process_string('a') == "processed: 'a'"
#
#         # Empty string and 'a' should have different cache entries
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 2
#
#     def test_cache_on_self__numeric_edge_cases(self):
#         """Test caching with numeric edge cases"""
#         class Numeric_Edge_Class:
#             @cache_on_self
#             def process_number(self, n):
#                 return n * 2
#
#         obj = Numeric_Edge_Class()
#
#         # Test various numeric edge cases
#         assert obj.process_number(0) == 0
#         assert obj.process_number(-0) == -0
#         assert obj.process_number(float('inf')) == float('inf')
#         assert obj.process_number(float('-inf')) == float('-inf')
#
#         # NaN is special - it's not equal to itself
#         nan_result = obj.process_number(float('nan'))
#         assert str(nan_result) == 'nan'
#
#     def test_cache_on_self__boolean_arguments(self):
#         """Test caching with boolean arguments"""
#         class Boolean_Class:
#             @cache_on_self
#             def process_bool(self, flag):
#                 return f"flag is {flag}"
#
#         obj = Boolean_Class()
#
#         assert obj.process_bool(True) == "flag is True"
#         assert obj.process_bool(False) == "flag is False"
#         assert obj.process_bool(True) == "flag is True"  # From cache
#
#         # True and False should have separate cache entries
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 2
#
#     # ----- Bug Tests (Extended) -----
#
#     def test__bug__cache_on_self__string_concatenation_collision(self):
#         """Test the string concatenation collision bug"""
#         class Collision_Class:
#             call_count = 0
#
#             @cache_on_self
#             def concat_numbers(self, *args):
#                 self.call_count += 1
#                 return f"call {self.call_count}: {args}"
#
#         obj = Collision_Class()
#
#         # These should all have different cache entries but they collide
#         result1 = obj.concat_numbers(1, 23)      # "123"
#         result2 = obj.concat_numbers(12, 3)      # "123"
#         result3 = obj.concat_numbers(123)        # "123"
#         result4 = obj.concat_numbers("12", "3")  # "123"
#
#         # BUG: All return the same cached value despite different args
#         assert result1 == "call 1: (1, 23)"
#         assert result2 == "call 1: (1, 23)"    # BUG: Should be "call 2: (12, 3)"
#         assert result3 == "call 1: (1, 23)"    # BUG: Should be "call 3: (123,)"
#         assert result4 == "call 1: (1, 23)"    # BUG: Should be "call 4: ('12', '3')"
#
#         # Only called once due to collision
#         assert obj.call_count == 1
#
#     def test__bug__cache_on_self__mixed_type_arguments(self):
#         """Test bug with mixed supported and unsupported types"""
#         class Mixed_Types_Class:
#             @cache_on_self
#             def process_mixed(self, name, data, count):
#                 return f"{name}: {len(data)} items, count={count}"
#
#         obj = Mixed_Types_Class()
#
#         # First call with list
#         result1 = obj.process_mixed("test1", [1, 2, 3], 100)
#         assert result1 == "test1: 3 items, count=100"
#
#         # Different list but same name and count - should be different but isn't
#         result2 = obj.process_mixed("test1", [1, 2, 3, 4, 5], 100)
#         assert result2 == "test1: 3 items, count=100"  # BUG: Should be "test1: 5 items, count=100"
#
#         # Different name - creates new entry
#         result3 = obj.process_mixed("test2", [1, 2], 100)
#         assert result3 == "test2: 2 items, count=100"
#
#     def test__regression__cache_on_self__none_values_ignored(self):     # Test that None values are completely ignored in cache key generation
#         class None_Values_Class:
#             call_count = 0
#
#             @cache_on_self
#             def process_with_none(self, a, b, c):
#                 self.call_count += 1
#                 return f"call {self.call_count}: a={a}, b={b}, c={c}"
#
#         obj = None_Values_Class()
#
#         # These should have different cache keys but don't
#         result1 = obj.process_with_none("x", None, "y")
#         result2 = obj.process_with_none("x", "ignored", "y")  # 'ignored' is where None was
#
#         # BUG: Both calls produce the same cache key "xy"
#         assert result1 == "call 1: a=x, b=None, c=y"
#         assert result2 == "call 2: a=x, b=ignored, c=y"                 # FIXED:  BUG: Returns wrong cached value
#         assert obj.call_count == 2  # Only called once
#
#     # ----- Security Tests -----
#
#     def test__security__cache_poisoning(self):
#         """Test cache poisoning vulnerability"""
#         class Secure_Class:
#             @cache_on_self
#             def get_user_data(self, user_id):
#                 # Simulate fetching sensitive user data
#                 return f"private data for user {user_id}"
#
#         obj = Secure_Class()
#
#         # Normal usage
#         user1_data = obj.get_user_data("user1")
#         assert user1_data == "private data for user user1"
#
#         # Direct cache manipulation (security vulnerability)
#         cache_key = '__cache_on_self___get_user_data_' + cache_on_self__args_to_str(('user1',)) + '_'
#         setattr(obj, cache_key, "HACKED DATA")
#
#         # Now returns poisoned data
#         assert obj.get_user_data("user1") == "HACKED DATA"
#
#     def test__security__cache_key_collision_exploit(self):
#         """Test how cache key collisions could be exploited"""
#         class Auth_Class:
#             @cache_on_self
#             def check_permission(self, user_id, resource_id):
#                 # Simulate permission check
#                 if user_id == "admin" and resource_id == "secret":
#                     return "granted"
#                 return "denied"
#
#         obj = Auth_Class()
#
#         # Admin checks permission (gets cached)
#         assert obj.check_permission("admin", "secret") == "granted"
#
#         # Due to collision bug, attacker could craft args that produce same cache key
#         # For example, if they know the concatenated string is "adminsecret"
#         assert obj.check_permission("admins", "ecret") == "granted"  # BUG: Security issue!
#         assert obj.check_permission("ad", "minsecret") == "granted"  # BUG: Security issue!
#
#     # ----- Performance Tests (Extended) -----
#
#     def test__performance__cache_overhead_with_arguments(self):
#         """Test performance overhead with various argument patterns"""
#         class Performance_Test_Class:
#             def no_cache_method(self, a, b, c):
#                 return a + b + c
#
#             @cache_on_self
#             def cached_method(self, a, b, c):
#                 return a + b + c
#
#         obj = Performance_Test_Class()
#         iterations = 1000
#
#         # Warm up
#         obj.no_cache_method(1, 2, 3)
#         obj.cached_method(1, 2, 3)
#
#         # Test no cache
#         with capture_duration(precision=5) as duration_no_cache:
#             for _ in range(iterations):
#                 obj.no_cache_method(1, 2, 3)
#
#         # Test with cache (cache hit scenario)
#         with capture_duration(precision=5) as duration_cached:
#             for _ in range(iterations):
#                 obj.cached_method(1, 2, 3)
#
#         overhead_ratio = duration_cached.seconds / duration_no_cache.seconds
#         assert overhead_ratio < 300  # Should be reasonable overhead for cache hits (it's high because we can't use the main optimised path, since we need to calculate the hash of the values)
#
#     def test__performance__cache_miss_overhead(self):
#         """Test performance overhead for cache misses"""
#         class Cache_Miss_Class:
#             @cache_on_self
#             def process(self, value):
#                 return value * 2
#
#         obj = Cache_Miss_Class()
#         iterations = 100
#
#         # Each call will be a cache miss (different arguments)
#         with capture_duration(precision=5) as duration_misses:
#             for i in range(iterations):
#                 obj.process(i)
#
#         # Verify all were cache misses by checking cache size
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == iterations
#
#     def test__performance__memory_usage(self):
#         """Test memory usage with large cache"""
#         class Memory_Test_Class:
#             @cache_on_self
#             def create_large_data(self, size):
#                 return [0] * size
#
#         obj = Memory_Test_Class()
#
#         # Create multiple large cached values
#         for i in range(10):
#             obj.create_large_data(i * 1000)
#
#         # Check that all cache entries exist
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 10
#
#         # Each entry holds a reference to a large list
#         # In production, this could lead to memory issues
#
#     # ----- Complex Scenario Tests -----
#
#     def test_cache_on_self__inheritance(self):
#         """Test cache behavior with inheritance"""
#         class Base_Class:
#             @cache_on_self
#             def base_method(self):
#                 return "base"
#
#         class Child_Class(Base_Class):
#             @cache_on_self
#             def child_method(self):
#                 return "child"
#
#         base = Base_Class()
#         child = Child_Class()
#
#         # Test base class caching
#         assert base.base_method() == "base"
#
#         # Test child class caching
#         assert child.base_method() == "base"
#         assert child.child_method() == "child"
#
#         # Caches should be separate
#         base_cache_keys = [k for k in base.__dict__.keys() if k.startswith('__cache_on_self__')]
#         child_cache_keys = [k for k in child.__dict__.keys() if k.startswith('__cache_on_self__')]
#
#         assert len(base_cache_keys) == 1
#         assert len(child_cache_keys) == 2  # Both base and child methods
#
#     def test_cache_on_self__recursive_calls(self):
#         """Test caching with recursive method calls"""
#         class Recursive_Class:
#             @cache_on_self
#             def fibonacci(self, n):
#                 if n <= 1:
#                     return n
#                 # Recursive calls will also use cache
#                 return self.fibonacci(n - 1) + self.fibonacci(n - 2)
#
#         obj = Recursive_Class()
#
#         # Calculate fibonacci(5)
#         result = obj.fibonacci(5)
#         assert result == 5
#
#         # Check cache entries were created for each unique n
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         # Should have entries for 0, 1, 2, 3, 4, 5
#         assert len(cache_keys) == 6
#
#     def test_cache_on_self__exception_handling(self):
#         """Test cache behavior when methods raise exceptions"""
#         class Exception_Class:
#             call_count = 0
#
#             @cache_on_self
#             def may_fail(self, should_fail):
#                 self.call_count += 1
#                 if should_fail:
#                     raise ValueError("Intentional failure")
#                 return "success"
#
#         obj = Exception_Class()
#
#         # First call succeeds
#         assert obj.may_fail(False) == "success"
#         assert obj.call_count == 1
#
#         # Second call uses cache
#         assert obj.may_fail(False) == "success"
#         assert obj.call_count == 1  # Not incremented
#
#         # Call that raises exception
#         with Catch(expect_exception=True):
#             obj.may_fail(True)
#         assert obj.call_count == 2
#
#         # Failed calls should not be cached - calling again raises again
#         with Catch(expect_exception=True):
#             obj.may_fail(True)
#         assert obj.call_count == 3  # Incremented again
#
#     def test_cache_on_self__thread_safety_concerns(self):
#         """Test potential thread safety issues (demonstrative only)"""
#         class Thread_Unsafe_Class:
#             counter = 0
#
#             @cache_on_self
#             def increment_counter(self):
#                 # Simulate race condition potential
#                 temp = self.counter
#                 # In multi-threaded environment, another thread could modify counter here
#                 self.counter = temp + 1
#                 return self.counter
#
#         obj = Thread_Unsafe_Class()
#
#         # Single-threaded test just demonstrates the concept
#         assert obj.increment_counter() == 1
#         assert obj.increment_counter() == 1  # Cached, counter not incremented
#
#         # Force reload
#         assert obj.increment_counter(reload_cache=True) == 2
#
#         # Note: Actual thread safety testing would require threading module
#
#     def test_cache_on_self__class_method_not_supported(self):
#         """Test that class methods are not properly supported"""
#         class Class_Method_Test:
#             @classmethod
#             @cache_on_self
#             def class_method(cls):
#                 return "class method result"
#
#         # This will likely fail or behave unexpectedly
#         with Catch(expect_exception=True) as catch:
#             Class_Method_Test.class_method()
#         # The error depends on implementation details
#
#     def test_cache_on_self__static_method_not_supported(self):
#         """Test that static methods are not supported"""
#         class Static_Method_Test:
#             @staticmethod
#             @cache_on_self
#             def static_method():
#                 return "static method result"
#
#         # This will fail because there's no self parameter
#         with Catch(expect_exception=True) as catch:
#             Static_Method_Test.static_method()
#         assert "could not find self" in str(catch.exception_value)
#
#     def test_cache_on_self__property_decorator_interaction(self):
#         """Test interaction with property decorator"""
#         class Property_Test:
#             def __init__(self):
#                 self._value = 0
#
#             @property
#             @cache_on_self
#             def cached_property(self):
#                 self._value += 1
#                 return self._value
#
#         obj = Property_Test()
#
#         # Properties with cache_on_self might not work as expected
#         # This test documents the behavior rather than asserting correctness
#         try:
#             result = obj.cached_property
#             # If it works, document the behavior
#         except Exception as e:
#             # If it fails, that's also important to know
#             pass
#
#     def test_cache_on_self__generator_methods(self):
#         """Test caching with generator methods"""
#         class Generator_Class:
#             @cache_on_self
#             def generate_values(self, n):
#                 for i in range(n):
#                     yield i
#
#         obj = Generator_Class()
#
#         # First call returns a generator
#         gen1 = obj.generate_values(3)
#         values1 = list(gen1)
#         assert values1 == [0, 1, 2]
#
#         # Second call returns the SAME exhausted generator!
#         gen2 = obj.generate_values(3)
#         values2 = list(gen2)
#         assert values2 == []  # BUG: Generator is exhausted!
#
#     def test_cache_on_self__special_method_names(self):
#         """Test caching with special method names"""
#         class Special_Methods_Class:
#             @cache_on_self
#             def __str__(self):
#                 return "cached string representation"
#
#             @cache_on_self
#             def __len__(self):
#                 return 42
#
#         obj = Special_Methods_Class()
#
#         # Test __str__ caching
#         assert str(obj) == "cached string representation"
#         assert hasattr(obj, '__cache_on_self_____str____')
#
#         # Test __len__ caching
#         assert len(obj) == 42
#         assert hasattr(obj, '__cache_on_self_____len____')
#
#     def test_cache_on_self__very_long_arguments(self):
#         """Test with very long string arguments that might need hashing"""
#         class Long_Args_Class:
#             @cache_on_self
#             def process_long_string(self, text):
#                 return len(text)
#
#         obj = Long_Args_Class()
#
#         # Create a very long string
#         long_string = "x" * 10000
#
#         result = obj.process_long_string(long_string)
#         assert result == 10000
#
#         # Check that cache key was created (will use MD5 hash)
#         cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
#         assert len(cache_keys) == 1
#
#         # The key should contain an MD5 hash due to length
#         cache_key = cache_keys[0]
#         assert len(cache_key) < len(long_string)  # Key is shorter than the argument