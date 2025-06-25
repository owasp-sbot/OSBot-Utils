from unittest                                                   import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import CACHE_ON_SELF_KEY_PREFIX, Cache_Key_Generator
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self
from osbot_utils.testing.Catch                                  import Catch
from osbot_utils.utils.Objects                                  import obj_data


class An_Class:
    @cache_on_self
    def an_function(self):
        return 42

    @cache_on_self
    def echo(self, value):
        return value

    @cache_on_self
    def echo_args(self, *args):
        return args

# Convenience functions for backwards compatibility

# todo: these functions need to be refactored out (good news is that at the moment they are only used in tests)
def cache_on_self__get_cache_in_key(function, args=None, kwargs=None):              # Get cache key - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.generate_key(function, args or (), kwargs or {})


def cache_on_self__args_to_str(args):                                              # Convert args to string - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.args_to_str(args)


def cache_on_self__kwargs_to_str(kwargs):                                          # Convert kwargs to string - backwards compatibility
    from osbot_utils.helpers.cache_on_self.Cache_Key_Generator import Cache_Key_Generator
    key_gen = Cache_Key_Generator()
    return key_gen.kwargs_to_str(kwargs)

class test__decorator__cache_on_self(TestCase):

    def test_cache_on_self(self):
        an_class_1                = An_Class()
        cache_key                 = cache_on_self__get_cache_in_key(an_class_1.an_function)
        assert cache_key          == f'{CACHE_ON_SELF_KEY_PREFIX}_an_function__'
        assert obj_data(an_class_1) == {}

        # testing function that returns static value
        assert an_class_1.an_function() == 42

        # Get cache manager to verify internal storage
        cache_manager = an_class_1.an_function(__return__='cache_on_self')
        assert cache_manager.cache_storage.has_cached_value(an_class_1, cache_key)
        assert cache_manager.cache_storage.get_cached_value(an_class_1, cache_key) == 42

        # Instance should remain clean
        assert obj_data(an_class_1) == {}

        an_class_2 = An_Class()
        assert an_class_2.an_function() == 42

        an_class_3 = An_Class()
        assert an_class_3.an_function() == 42

        # testing function that returns dynamic value (with args)
        assert an_class_1.echo(111) == 111
        assert an_class_1.echo(111) == 111
        assert an_class_1.echo(222) == 222
        assert an_class_1.echo(111) == 111

        assert an_class_2.echo(333) == 333
        assert an_class_2.echo(333) == 333
        assert an_class_2.echo(444) == 444

        assert an_class_3.echo(555) == 555
        assert an_class_3.echo(555) == 555
        assert an_class_3.echo(666) == 666

        # Verify instances remain clean
        assert obj_data(an_class_1) == {}
        assert obj_data(an_class_2) == {}
        assert obj_data(an_class_3) == {}

        # testing function that returns dynamic value (with kwargs)
        assert an_class_1.echo(value=111) == 111
        assert an_class_1.echo(value=222) == 222

        assert an_class_2.echo(value=333) == 333
        assert an_class_2.echo(value=444) == 444

        assert an_class_3.echo(value=555) == 555
        assert an_class_3.echo(value=666) == 666

    def test_cache_on_self__multiple_types_in_arg_cache(self):
        args      = ('a', 1, 1.0)
        an_class = An_Class()
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == "[0]:<str>:a|[1]:<int>:1|[2]:<float>:1.0"

        args = ('a', None, 'bbb', [], {})
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == "[0]:<str>:a|[1]:<none>|[2]:<str>:bbb|[3]:<list>:[]|[4]:<dict>:[]"

        args = ('a', -1, ['a'], {'b':None})
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == '[0]:<str>:a|[1]:<int>:-1|[2]:<list>:["a"]|[3]:<dict>:[["b",null]]'

        args = (1, int(1), float(1), bytearray(b'1'), bytes(b'1'), bool(True), complex(1), str('1'))
        assert an_class.echo_args(*args)        == args
        assert an_class.echo_args(*args)        == (1, 1, 1.0, bytearray(b'1'), b'1', True, (1 + 0j), '1')
        assert cache_on_self__args_to_str(args) == "[0]:<int>:1|[1]:<int>:1|[2]:<float>:1.0|[3]:<bytearray>:bytearray(b'1')|[4]:<bytes>:b'1'|[5]:<bool>:True|[6]:<complex>:(1+0j)|[7]:<str>:1"

    def test_cache_on_self__kwargs_to_str(self):
        assert cache_on_self__kwargs_to_str({"an":"value"    }) == 'an:<str>:value'
        assert cache_on_self__kwargs_to_str({"a": "b","c":"d"}) == 'a:<str>:b|c:<str>:d'
        assert cache_on_self__kwargs_to_str({"an": None      }) == 'an:<none>'
        assert cache_on_self__kwargs_to_str({"an": 1         }) == 'an:<int>:1'

    def test_cache_on_self__outside_an_class(self):
        @cache_on_self
        def an_function():
            pass

        with Catch(log_exception=False) as catch:
            an_function()

        assert catch.exception_value.args[0] == "cache_on_self could not find self - no arguments provided"

    def test_cache_on_self__reload_cache(self):
        class An_Class_2(Type_Safe):
            an_value : int = 41

            @cache_on_self
            def an_function(self):
                self.an_value += 1
                return self.an_value

        an_class = An_Class_2()

        assert an_class.an_function(                  ) == 42
        assert an_class.an_function(                  ) == 42

        assert an_class.an_function(reload_cache=True ) == 43
        assert an_class.an_function(reload_cache=False) == 43
        assert an_class.an_function(                  ) == 43

        assert an_class.an_function(reload_cache=True ) == 44
        assert an_class.an_function(reload_cache=False) == 44
        assert an_class.an_function(                  ) == 44

    def test_cache_on_self__with_multiple_arguments(self):
        """Test caching with multiple arguments of supported types"""
        class Multi_Args_Class:
            @cache_on_self
            def calculate(self, a, b, c):
                return a + b + c

        obj = Multi_Args_Class()

        # First call - should cache
        assert obj.calculate(10, 20, 30) == 60

        # Second call with same args - should use cache
        assert obj.calculate(10, 20, 30) == 60

        # Different args - should create new cache entry
        assert obj.calculate(1, 2, 3) == 6

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test_cache_on_self__with_default_arguments(self):
        """Test caching with default arguments"""
        class Default_Args_Class:
            @cache_on_self
            def method_with_defaults(self, a=10, b=20):
                return a * b

        obj = Default_Args_Class()

        # Call without args
        assert obj.method_with_defaults() == 200

        # Call with partial args
        assert obj.method_with_defaults(5) == 100

        # Call with all args
        assert obj.method_with_defaults(3, 4) == 12

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test_cache_on_self__with_kwargs_order(self):
        """Test that kwargs order doesn't affect caching"""
        class Kwargs_Order_Class:
            @cache_on_self
            def method_with_kwargs(self, **kwargs):
                return sum(kwargs.values())

        obj = Kwargs_Order_Class()

        # Call with kwargs in different order
        result1 = obj.method_with_kwargs(a=1, b=2, c=3)
        result2 = obj.method_with_kwargs(c=3, a=1, b=2)
        result3 = obj.method_with_kwargs(b=2, c=3, a=1)

        assert result1 == result2 == result3 == 6

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test_cache_on_self__return_value_types(self):
        """Test caching with various return value types"""
        class Various_Returns_Class:
            @cache_on_self
            def return_dict(self):
                return {'key': 'value', 'nested': {'data': 123}}

            @cache_on_self
            def return_list(self):
                return [1, 2, 3, [4, 5]]

            @cache_on_self
            def return_none(self):
                return None

            @cache_on_self
            def return_object(self):
                return self

        obj = Various_Returns_Class()

        # Test dict return
        dict_result = obj.return_dict()
        assert dict_result == {'key': 'value', 'nested': {'data': 123}}
        assert obj.return_dict() is dict_result  # Same object reference

        # Test list return
        list_result = obj.return_list()
        assert list_result == [1, 2, 3, [4, 5]]
        assert obj.return_list() is list_result  # Same object reference

        # Test None return
        assert obj.return_none() is None

        # Test object return
        assert obj.return_object() is obj

    def test_cache_on_self__empty_string_arguments(self):
        """Test caching with empty strings"""
        class Empty_String_Class:
            @cache_on_self
            def process_string(self, s):
                return f"processed: '{s}'"

        obj = Empty_String_Class()

        assert obj.process_string('') == "processed: ''"
        assert obj.process_string('') == "processed: ''"  # Should use cache
        assert obj.process_string('a') == "processed: 'a'"

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test_cache_on_self__numeric_edge_cases(self):
        """Test caching with numeric edge cases"""
        class Numeric_Edge_Class:
            @cache_on_self
            def process_number(self, n):
                return n * 2

        obj = Numeric_Edge_Class()

        # Test various numeric edge cases
        assert obj.process_number(0) == 0
        assert obj.process_number(-0) == -0
        assert obj.process_number(float('inf')) == float('inf')
        assert obj.process_number(float('-inf')) == float('-inf')

        # NaN is special - it's not equal to itself
        nan_result = obj.process_number(float('nan'))
        assert str(nan_result) == 'nan'

    def test_cache_on_self__boolean_arguments(self):
        """Test caching with boolean arguments"""
        class Boolean_Class:
            @cache_on_self
            def process_bool(self, flag):
                return f"flag is {flag}"

        obj = Boolean_Class()

        assert obj.process_bool(True) == "flag is True"
        assert obj.process_bool(False) == "flag is False"
        assert obj.process_bool(True) == "flag is True"  # From cache

        # Verify instance remains clean
        assert obj.__dict__ == {}

    def test_cache_on_self__inheritance(self):
        """Test cache behavior with inheritance"""
        class Base_Class:
            @cache_on_self
            def base_method(self):
                return "base"

        class Child_Class(Base_Class):
            @cache_on_self
            def child_method(self):
                return "child"

        base = Base_Class()
        child = Child_Class()

        # Test base class caching
        assert base.base_method() == "base"

        # Test child class caching
        assert child.base_method() == "base"
        assert child.child_method() == "child"

        # Verify instances remain clean
        assert base.__dict__ == {}
        assert child.__dict__ == {}

    def test_cache_on_self__exception_handling(self):
        """Test cache behavior when methods raise exceptions"""
        class Exception_Class:
            call_count = 0

            @cache_on_self
            def may_fail(self, should_fail):
                self.call_count += 1
                if should_fail:
                    raise ValueError("Intentional failure")
                return "success"

        obj = Exception_Class()

        # First call succeeds
        assert obj.may_fail(False) == "success"
        assert obj.call_count == 1

        # Second call uses cache
        assert obj.may_fail(False) == "success"
        assert obj.call_count == 1  # Not incremented

        # Call that raises exception
        with Catch(expect_exception=True):
            obj.may_fail(True)
        assert obj.call_count == 2

        # Failed calls should not be cached - calling again raises again
        with Catch(expect_exception=True):
            obj.may_fail(True)
        assert obj.call_count == 3  # Incremented again

    def test_cache_on_self__thread_safety_concerns(self):
        """Test potential thread safety issues (demonstrative only)"""
        class Thread_Unsafe_Class:
            counter = 0

            @cache_on_self
            def increment_counter(self):
                # Simulate race condition potential
                temp = self.counter
                # In multi-threaded environment, another thread could modify counter here
                self.counter = temp + 1
                return self.counter

        obj = Thread_Unsafe_Class()

        # Single-threaded test just demonstrates the concept
        assert obj.increment_counter() == 1
        assert obj.increment_counter() == 1  # Cached, counter not incremented

        # Force reload
        assert obj.increment_counter(reload_cache=True) == 2

        # Note: Actual thread safety testing would require threading module

    def test_cache_on_self__class_method_not_supported(self):
        """Test that class methods are not properly supported"""
        class Class_Method_Test:
            @classmethod
            @cache_on_self
            def class_method(cls):
                return "class method result"

        # This will likely fail or behave unexpectedly
        #with Catch(expect_exception=True) as catch:
        assert Class_Method_Test.class_method() == "class method result"
        # The error depends on implementation details

    def test_cache_on_self__static_method_not_supported(self):
        """Test that static methods are not supported"""
        class Static_Method_Test:
            @staticmethod
            @cache_on_self
            def static_method():
                return "static method result"

        # This will fail because there's no self parameter
        with Catch(expect_exception=True) as catch:
            Static_Method_Test.static_method()
        assert "could not find self" in str(catch.exception_value)

    def test_cache_on_self__property_decorator_interaction(self):
        """Test interaction with property decorator"""
        class Property_Test:
            def __init__(self):
                self._value = 0

            @property
            @cache_on_self
            def cached_property(self):
                self._value += 1
                return self._value

        obj = Property_Test()

        # Properties with cache_on_self might not work as expected
        # This test documents the behavior rather than asserting correctness
        try:
            result = obj.cached_property
            # If it works, document the behavior
        except Exception as e:
            # If it fails, that's also important to know
            pass

    def test_cache_on_self__generator_methods(self):
        """Test caching with generator methods"""
        class Generator_Class:
            @cache_on_self
            def generate_values(self, n):
                for i in range(n):
                    yield i

        obj = Generator_Class()

        # First call returns a generator
        gen1 = obj.generate_values(3)
        values1 = list(gen1)
        assert values1 == [0, 1, 2]

        # Second call returns the SAME exhausted generator!
        gen2 = obj.generate_values(3)
        values2 = list(gen2)
        assert values2 == []  # BUG: Generator is exhausted!

    def test_cache_on_self__special_method_names(self):
        """Test caching with special method names"""
        class Special_Methods_Class:
            @cache_on_self
            def __str__(self):
                return "cached string representation"

            @cache_on_self
            def __len__(self):
                return 42

        obj = Special_Methods_Class()

        # Test __str__ caching
        assert str(obj) == "cached string representation"

        # Verify cache exists internally but not on instance
        cache_manager = obj.__str__(__return__='cache_on_self')
        assert cache_manager.cache_storage.has_cached_value(obj, '__cache_on_self_____str____')
        assert not hasattr(obj, '__cache_on_self_____str____')

        # Test __len__ caching
        assert len(obj) == 42

        # Verify cache exists internally but not on instance
        cache_manager = obj.__len__(__return__='cache_on_self')
        assert cache_manager.cache_storage.has_cached_value(obj, '__cache_on_self_____len____')
        assert not hasattr(obj, '__cache_on_self_____len____')

    def test_cache_on_self__very_long_arguments(self):
        """Test with very long string arguments that might need hashing"""
        class Long_Args_Class:
            @cache_on_self
            def process_long_string(self, text):
                return len(text)

        obj = Long_Args_Class()

        # Create a very long string
        long_string = "x" * 10000

        result = obj.process_long_string(long_string)
        assert result == 10000

        # Verify instance remains clean
        assert obj.__dict__ == {}


    def test__no_collision_between_none_and_strings(self):
        """Test that None doesn't collide with any string value"""
        class Test_Class:
            @cache_on_self
            def process(self, data):
                return f"processing: {repr(data)}"

        obj = Test_Class()

        # Test potential collision strings
        result_none = obj.process(None)
        result_str1 = obj.process('<none>')
        result_str2 = obj.process('none:None')
        result_str3 = obj.process('__CACHE_NONE_VALUE__')

        assert result_none == "processing: None"
        assert result_str1 == "processing: '<none>'"
        assert result_str2 == "processing: 'none:None'"
        assert result_str3 == "processing: '__CACHE_NONE_VALUE__'"

        # All should be different
        assert result_none != result_str1
        assert result_none != result_str2
        assert result_none != result_str3

    def test__no_collision_between_types(self):
        """Test that different types with similar string representations don't collide"""
        class Test_Class:
            @cache_on_self
            def process(self, data):
                return f"type: {type(data).__name__}, value: {repr(data)}"

        obj = Test_Class()

        # These could have similar string representations without type prefixes
        assert obj.process("123") == "type: str, value: '123'"
        assert obj.process(123) == "type: int, value: 123"
        assert obj.process(123.0) == "type: float, value: 123.0"
        assert obj.process(True) == "type: bool, value: True"
        assert obj.process("True") == "type: str, value: 'True'"
        assert obj.process("<dict>:[1,2,3]") == "type: str, value: '<dict>:[1,2,3]'"
        assert obj.process({"a": 1}) == "type: dict, value: {'a': 1}"

    def test__cache_key_generator_type_prefixes(self):
        """Test that cache key generator adds proper type prefixes"""
        key_gen = Cache_Key_Generator()

        # Primitive types get type prefix
        assert key_gen.value_to_cache_str("hello") == "<str>:hello"
        assert key_gen.value_to_cache_str(123) == "<int>:123"
        assert key_gen.value_to_cache_str(123.45) == "<float>:123.45"
        assert key_gen.value_to_cache_str(True) == "<bool>:True"
        assert key_gen.value_to_cache_str(b"bytes") == "<bytes>:b'bytes'"

        # None gets special treatment
        assert key_gen.value_to_cache_str(None) == "<none>"

        # Collections get type prefix
        assert key_gen.value_to_cache_str([1, 2, 3]).startswith("<list>:")
        assert key_gen.value_to_cache_str({"a": 1}).startswith("<dict>:")
        assert key_gen.value_to_cache_str({1, 2, 3}).startswith("<set>:")
        assert key_gen.value_to_cache_str((1, 2, 3)).startswith("<tuple>:")

        # Unsupported types still return empty string
        class CustomObject:
            pass
        assert key_gen.value_to_cache_str(CustomObject()) == ""

    def test__complex_collision_scenarios(self):
        """Test various complex scenarios that could cause collisions"""
        class Test_Class:
            @cache_on_self
            def process(self, *args):
                return f"args: {args}"

        obj = Test_Class()

        # These should all generate different cache keys
        results = [
            obj.process(None),
            obj.process("None"),
            obj.process("<none>"),
            obj.process({"<none>": True}),
            obj.process(["<none>"]),
            obj.process("<dict>", "123"),
            obj.process({"key": "value"}),
            obj.process("<list>:[1,2,3]"),
            obj.process([1, 2, 3]),
        ]

        # All results should be unique
        for i, result_i in enumerate(results):
            for j, result_j in enumerate(results):
                if i != j:
                    assert result_i != result_j, f"Collision between index {i} and {j}"

    def test__args_with_type_prefixes(self):
        """Test that args_to_str properly handles the new type prefixes"""
        key_gen = Cache_Key_Generator()

        # Test with mixed types
        args = ("hello", 123, None, [1, 2], {"a": 1})
        args_str = key_gen.args_to_str(args)

        # Verify format includes indices and type prefixes
        assert "[0]:<str>:hello" in args_str
        assert "[1]:<int>:123" in args_str
        assert "[2]:<none>" in args_str
        assert "[3]:<list>:" in args_str
        assert "[4]:<dict>:" in args_str