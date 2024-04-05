from unittest import TestCase

from osbot_utils.decorators.methods.cache_on_function import cache_on_function
from osbot_utils.utils.Misc import random_string


class An_Class:
    @cache_on_function
    def an_function(self):
        return random_string()

    @cache_on_function
    def an_function_with_params(self, prefix):
        return random_string(prefix=prefix)

class test_cache_on_function(TestCase):

    def test_cache_on_function(self):
        an_class = An_Class()
        assert an_class.an_function() == an_class.an_function()
        prefix = 'an_prefix'
        assert an_class.an_function_with_params(prefix       ) == an_class.an_function_with_params(prefix       )
        assert an_class.an_function_with_params(prefix=prefix) == an_class.an_function_with_params(prefix=prefix)
        assert an_class.an_function_with_params(prefix       ) != an_class.an_function_with_params(prefix=prefix)           #interesting side effect of the way the cache key is created


        value_before_reload = an_class.an_function_with_params(prefix)
        assert an_class.an_function_with_params(prefix) != an_class.an_function_with_params(prefix, reload_cache=True)      # setting reload_cache will make the method to be executed again
        assert an_class.an_function_with_params(prefix) == an_class.an_function_with_params(prefix)                         # if we don't use it, we get the same value everytime
        value_after_reload = an_class.an_function_with_params(prefix)
        assert value_before_reload != value_after_reload                                                                    # confirm that we indeed got a new value