from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests           import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.TestCase__Sqlite__Cache__Requests import TestCase__Sqlite__Cache__Requests
from osbot_utils.utils.Json                                             import from_json_str
from osbot_utils.utils.Misc                                             import list_set


class test_TestCase__Sqlite__Cache__Requests(TestCase__Sqlite__Cache__Requests):

    def test_setUpClass(self):
        with self.sqlite_cache_requests  as _:
            assert type(_) == Sqlite__Cache__Requests
            assert _.config.add_timestamp is False

    def test__add_test_requests(self):
        with self.sqlite_cache_requests as _:
            assert _.cache_entries() == []
            self.add_test_requests()
            assert len(_.cache_entries()) == 10
            for entry in _.cache_entries():
                request_data   = from_json_str(entry.get('request_data'))
                request_args   = request_data.get('request_args'  )
                request_kwargs = request_data.get('request_kwargs')
                response_data = from_json_str(entry.get('response_data'))
                assert list_set(request_data )            == ['args', 'kwargs']
                assert list_set(response_data)            == ['request_args', 'request_kwargs', 'source', 'type']
                assert response_data.get('args'         ) == request_args
                assert response_data.get('target_kwargs') == request_kwargs
                assert list_set(entry)                    == ['comments', 'id', 'metadata', 'request_data', 'request_hash',
                                                              'request_type', 'response_bytes', 'response_data', 'response_hash',
                                                              'response_type', 'source', 'timestamp']
            self.add_test_requests(3)
            assert len(_.cache_entries()) == 13