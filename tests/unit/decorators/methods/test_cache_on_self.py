from unittest                                                   import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator      import CACHE_ON_SELF_KEY_PREFIX
from osbot_utils.helpers.cache_on_self.Cache_On_Self            import Cache_On_Self
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self, cache_on_self__get_cache_in_key, cache_on_self__args_to_str, cache_on_self__kwargs_to_str
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

class test_cache_on_self(TestCase):

    def test_cache_on_self(self):

        an_class_1                = An_Class()                                              # create 1st instance
        cache_key                 = cache_on_self__get_cache_in_key(an_class_1.an_function)  # get key from self
        assert cache_key          == f'{CACHE_ON_SELF_KEY_PREFIX}_an_function__'            # confirm cache key value
        assert obj_data(an_class_1) == {}                                                   # confirm cache key has not been added to self

        # testing function that returns static value
        assert an_class_1.an_function() == 42                                               # invoke method, set cache and confirm return value
        assert obj_data(an_class_1, show_internals=True).get(cache_key) == 42                # confirm attribute has been set in class

        assert an_class_1.__cache_on_self___an_function__               == 42               # which can be accessed directly
        an_class_1.__cache_on_self___an_function__                      = 12                # if we change the attribute directly
        assert obj_data(an_class_1, show_internals=True).get(cache_key) == 12               # confirm value changes (via obj data)
        assert an_class_1.__cache_on_self___an_function__               == 12               # confirm value change (directly)

        an_class_2 = An_Class()                                                             # create 2nd instance
        assert an_class_2.an_function() == 42                                               # confirm previous version was not affected

        an_class_3 = An_Class()                                                             # create 3rd instance
        assert an_class_3.an_function() == 42                                               # confirm previous version was not affected

        # testing function that returns dynamic value (with args)
        assert an_class_1.echo(111) == 111                                                  # confirm returns echo value
        assert an_class_1.echo(111) == 111
        assert an_class_1.echo(222) == 222                                                  # config, new value has been set
        assert an_class_1.echo(111) == 111

        assert an_class_2.echo(333) == 333                                                  # confirm returns echo value
        assert an_class_2.echo(333) == 333
        assert an_class_2.echo(444) == 444                                                  # config, new value has been set

        assert an_class_3.echo(555) == 555                                                  # confirm returns echo value
        assert an_class_3.echo(555) == 555
        assert an_class_3.echo(666) == 666                                                  # config, new value has been set

        obj_data__class_1 = obj_data(an_class_1, show_internals=True)
        obj_data__class_2 = obj_data(an_class_2, show_internals=True)
        obj_data__class_3 = obj_data(an_class_3, show_internals=True)
        cache_items__class_1 = {k: v for k, v in obj_data__class_1.items() if k.startswith('__cache_on_self__')}
        cache_items__class_2 = {k: v for k, v in obj_data__class_2.items() if k.startswith('__cache_on_self__')}
        cache_items__class_3 = {k: v for k, v in obj_data__class_3.items() if k.startswith('__cache_on_self__')}

        assert cache_items__class_1 == {'__cache_on_self___an_function__'                         : 12  ,
                                        '__cache_on_self___echo_698d51a19d8a121ce581499d7b701668_': 111 ,
                                        '__cache_on_self___echo_bcbe3365e6ac95ea2c0343a2395834dd_': 222 }

        assert cache_items__class_2 == {'__cache_on_self___an_function__'                         : 42  ,
                                        '__cache_on_self___echo_310dcbbf4cce62f762a2aaa148d556bd_': 333 ,
                                        '__cache_on_self___echo_550a141f12de6341fba65b0ad0433500_': 444 }

        assert cache_items__class_3 == {'__cache_on_self___an_function__'                         : 42  ,
                                        '__cache_on_self___echo_15de21c670ae7c3f6f3f1f37029303c9_': 555 ,
                                        '__cache_on_self___echo_fae0b27c451c728867a567e8c1bb4e53_': 666 }

        # testing function that returns dynamic value (with kargs)
        assert an_class_1.echo(value=111) == 111                                                    # confirm returns echo value
        assert an_class_1.echo(value=222) == 222                                                    # confirms new value

        assert an_class_2.echo(value=333) == 333                                                    # confirm returns echo value
        assert an_class_2.echo(value=444) == 444                                                    # confirms new value

        assert an_class_3.echo(value=555) == 555                                                    # confirm returns echo value
        assert an_class_3.echo(value=666) == 666                                                    # confirms new value

    def test_cache_on_self__multiple_types_in_arg_cache(self):
        args      = ('a', 1, 1.0)
        an_class = An_Class()
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == "a11.0"

        args = ('a', None, 'bbb', [], {})
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == "abbb"

        args = ('a', -1, ['a'], {'b':None})
        assert an_class.echo_args(*args) == args
        assert cache_on_self__args_to_str(args) == "a-1"

        args = (1, int(1), float(1), bytearray(b'1'), bytes(b'1'), bool(True), complex(1), str('1'))
        assert an_class.echo_args(*args)        == args
        assert an_class.echo_args(*args)        == (1, 1, 1.0, bytearray(b'1'), b'1', True, (1 + 0j), '1')
        assert cache_on_self__args_to_str(args) == "111.0bytearray(b'1')b'1'True(1+0j)1"

    def test_cache_on_self__kwargs_to_str(self):
        assert cache_on_self__kwargs_to_str({"an":"value"    }) == 'an:value|'
        assert cache_on_self__kwargs_to_str({"a": "b","c":"d"}) == 'a:b|c:d|'
        assert cache_on_self__kwargs_to_str({"an": None      }) == ''
        assert cache_on_self__kwargs_to_str({"an": 1         }) == 'an:1|'


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

    def test__bug__cache_on_self__caching__mutable_arguments(self):
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
        assert result_2 == "processed: value_1"             # BUG: should be "processed: value_2"


        # Test with list
        items = [1, 2, 3]
        list_result_1 = obj.process_list(items)
        assert list_result_1 == "count: 3"

        items.append(4)
        list_result_2 = obj.process_list(items)
        assert list_result_2 == "count: 3"                  # BUG: should be "count: 4"


        # Check the actual cache keys and values
        cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
        assert cache_keys == ['__cache_on_self___process_dict__',
                              '__cache_on_self___process_list__']

        assert obj.__getattribute__('__cache_on_self___process_dict__') == 'processed: value_1'
        assert obj.__getattribute__('__cache_on_self___process_list__') == 'count: 3'

    def test__bug__cache_on_self__complete_cache_collision(self):
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
        assert result_1 == "processing: {'a': 1}"
        assert result_2 == "processing: {'a': 1}"  # BUG!
        assert result_3 == "processing: {'a': 1}"  # BUG!
        assert result_4 == "processing: {'a': 1}"  # BUG!
        assert result_5 == "processing: {'a': 1}"  # BUG!
        assert result_6 == "processing: {'a': 1}"  # BUG!

        # Only one cache entry exists
        cache_keys = [k for k in obj.__dict__.keys() if k.startswith('__cache_on_self__')]
        assert len(cache_keys) == 1
        assert cache_keys[0] == '__cache_on_self___process__'

    def test__performance__confirm__cache_on_self__current_invocation_overhead(self):
        class Performance_Host:
            def an_function(self):
                return 42

            @cache_on_self
            def an_function_with_cache(self):
                return 42

        host = Performance_Host()
        host.an_function()                                                                          # warm up both functions
        host.an_function_with_cache()                                                               # especially the one with the cache, since we are not measuring here the overhead of the cache creation (the focus is on the overhead of the cache check)

        invocation_count = 1000
        with capture_duration(precision=5) as duration__an_function:
            for i in range(invocation_count):
                assert host.an_function() is 42
        #assert duration__an_function.seconds < 0.0001                                               # confirm that 1000 invocations happen in less than 0.1 ms

        cache = host.an_function_with_cache(__return__='cache_on_self')
        assert type(cache) is Cache_On_Self
        assert cache.disabled is False
        #cache.disabled = False
        with capture_duration(precision=5) as duration__an_function_with_cache:
            for i in range(invocation_count):
                assert host.an_function_with_cache() is 42

        # todo: remove this from the final version since we are better doing the comparison with the
        assert 0.0001 < duration__an_function_with_cache.seconds < 0.0005                   # confirm that 1000 invocations now happen in between 0.1 and 0.5 ms

        overhead_ratio = duration__an_function_with_cache.seconds / duration__an_function.seconds   # Calculate the overhead ratio instead

        # print()
        # print(f'duration__an_function           : {duration__an_function.seconds}')
        # print(f'duration__an_function_with_cache: {duration__an_function_with_cache.seconds}')
        # print(f'overhead_ratio                  : {overhead_ratio}')

        #assert overhead_ratio > 20          # confirm that the cached version is significantly slower
        assert overhead_ratio < 5          # confirm that the cache overhead is less than 5




