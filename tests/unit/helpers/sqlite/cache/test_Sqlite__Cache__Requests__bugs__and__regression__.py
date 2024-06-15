from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.utils.Misc                                   import list_set


class test_Sqlite__Cache__Requests(TestCase):

    def test__bug__cache_request_data__override_is_not_working(self):

        class Sqlite__Cache__Requests_2(Sqlite__Cache__Requests):

            def cache_request_data(self,*args, **target_kwargs):                    # override this method to have a different cache_key_strategy
                return dict(args = len(list(args)), kwargs = list_set(target_kwargs))

        args                       = ('an_arg',)
        kwargs                     = dict(an_kwarg='kwargs')
        request_data               = {'args': ['an_arg'], 'kwargs': {'an_kwarg': 'kwargs'}}

        sqlite__cache__requests__1 = Sqlite__Cache__Requests  ()
        sqlite__cache__requests__2 = Sqlite__Cache__Requests_2()

        request_data__1            = sqlite__cache__requests__1.cache_request_data(*args, **kwargs)
        request_data__2            = sqlite__cache__requests__2.cache_request_data(*args, **kwargs)

        #assert request_data__1    == request_data
        assert request_data__2    == {'args': 1, 'kwargs': ['an_kwarg']}

        sqlite__cache__requests__1.cache_add(request_data__1, {})
        sqlite__cache__requests__2.cache_add(request_data__2, {})

        row_1         = sqlite__cache__requests__1.cache_entries()[0]
        row_2         = sqlite__cache__requests__2.cache_entries()[0]

        cache_entry_1 = sqlite__cache__requests__1.cache_data.cache_entry_for_request_params(*args, **kwargs)
        cache_entry_2 = sqlite__cache__requests__2.cache_data.cache_entry_for_request_params(*args, **kwargs)

        assert cache_entry_1 == row_1                       # ok
        # assert cache_entry_2 == {}                          # BUG: this should be row_2
        # assert cache_entry_2 != row_2                       # BUG: this should be row_2
        assert cache_entry_2 == row_2                       # BUG: this should be row_2
