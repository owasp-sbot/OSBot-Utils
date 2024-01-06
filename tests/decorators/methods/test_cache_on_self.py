from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.decorators.methods.cache_on_self import cache_on_self, cache_on_self__get_cache_in_key, \
    CACHE_ON_SELF_KEY_PREFIX, cache_on_self__args_to_str, cache_on_self__kwargs_to_str
from osbot_utils.testing.Catch import Catch
from osbot_utils.utils.Objects import obj_data


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
        assert obj_data(an_class_1)     == { cache_key : 42}                                # confirm attribute has been set in class
        pprint(obj_data(an_class_1))
        assert an_class_1.cache_on_self_an_function__ == 42                                 # which can be accessed directly
        an_class_1.cache_on_self_an_function__         = 12                                 # if we change the attribute directly
        assert obj_data(an_class_1)     == { cache_key : 12}                                # confirm value changes (via obj data)
        assert an_class_1.cache_on_self_an_function__ == 12                                 # confirm value change (directly)

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

        assert obj_data(an_class_1) == {'cache_on_self_an_function__'                         : 12  ,
                                        'cache_on_self_echo_698d51a19d8a121ce581499d7b701668_': 111 ,
                                        'cache_on_self_echo_bcbe3365e6ac95ea2c0343a2395834dd_': 222 }

        assert obj_data(an_class_2) == {'cache_on_self_an_function__'                         : 42  ,
                                        'cache_on_self_echo_310dcbbf4cce62f762a2aaa148d556bd_': 333 ,
                                        'cache_on_self_echo_550a141f12de6341fba65b0ad0433500_': 444 }

        assert obj_data(an_class_3) == {'cache_on_self_an_function__'                         : 42  ,
                                        'cache_on_self_echo_15de21c670ae7c3f6f3f1f37029303c9_': 555 ,
                                        'cache_on_self_echo_fae0b27c451c728867a567e8c1bb4e53_': 666 }

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

        assert catch.exception_value.args[0] == "In Method_Wrappers.cache_on_self could not find self"