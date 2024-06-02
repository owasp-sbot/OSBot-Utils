from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.utils.Misc import random_text


class TestCase__Sqlite__Cache__Requests(TestCase):
    sqlite_cache_requests : Sqlite__Cache__Requests

    @classmethod
    def setUpClass(cls):
        cls.sqlite_cache_requests = Sqlite__Cache__Requests()
        cls.sqlite_cache_requests.set__add_timestamp(False)                   # disabling timestamp since it complicates the test data verification below
        assert cls.sqlite_cache_requests.sqlite_requests.in_memory is True    # confirm we have an in-memory db

    def tearDown(self):
        self.sqlite_cache_requests.cache_table.clear()

    def add_test_requests(self, count=10):
        def invoke_target(*args, **target_kwargs):
            return {'type'          : 'response'                       ,
                    'source'        : 'add_test_requests.invoke_target',
                    'request_args'  : args                             ,
                    'request_kwargs': target_kwargs                    }

        for i in range(count):
            an_key        = random_text('an_key')
            an_dict       = {'the': random_text('random_request')}
            target        = invoke_target
            target_args   = ['abc']
            target_kwargs = {'an_key': an_key, 'an_dict': an_dict}
            response = self.sqlite_cache_requests.invoke(target, target_args, target_kwargs)
            # todo add comments to the entry
            #self.sqlite_cache_requests.cache_entry_comments_update()
            #pprint(response)