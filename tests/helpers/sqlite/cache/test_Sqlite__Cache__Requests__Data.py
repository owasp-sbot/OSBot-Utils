from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Data         import Sqlite__Cache__Requests__Data
from osbot_utils.helpers.sqlite.cache.TestCase__Sqlite__Cache__Requests     import TestCase__Sqlite__Cache__Requests
from osbot_utils.utils.Json                                                 import json_loads
from osbot_utils.utils.Misc import random_string, list_set
from osbot_utils.utils.Objects                                              import pickle_save_to_bytes, pickle_load_from_bytes


class test_Sqlite__Cache__Requests__Data(TestCase__Sqlite__Cache__Requests):

    def setUp(self):
        self.cache_request_data = Sqlite__Cache__Requests__Data()                    # todo: refactor tests below to use this one, instead of the one from self.sqlite_cache_requests

    def test_cache_entry_comments(self):
        with self.sqlite_cache_requests as _:
            assert _.cache_entries() == []
            model_id      = 'an_model'
            body          = {'answer': 42}
            new_comment   = random_string(prefix='new_comment')
            request_data  = _.cache_request_data(model_id=model_id, body= body)
            response_data = {'in': 'response'}

            _.cache_add(request_data, response_data)

            cache_entry = _.cache_entries()[0]
            assert len(_.cache_entries()) ==1
            assert request_data           == json_loads(cache_entry.get('request_data'))
            assert response_data          == json_loads(cache_entry.get('response_data'))

            assert _.cache_entry_for_request_params (             model_id=model_id, body=body)               == cache_entry
            assert _.cache_entry_comments           (             model_id=model_id, body=body)               == ''
            assert _.cache_entry_comments_update    (new_comment, model_id=model_id, body=body).get('status') == 'ok'
            assert _.cache_entry_comments           (             model_id=model_id, body= body)              == new_comment

            assert _.cache_table__clear().get('status')   == 'ok'
            assert _.cache_entries()                      == []

    # TODO : Finish test asserts
    def test_create_new_cache_data__pickle_response_is_True(self):
        row_count = 2
        with self.sqlite_cache_requests as _:
            assert _.config.pickle_response is False           # default value
            _.pickle_response = True                    # enable pickle_response
            self.add_test_requests(2)                   # add 2 rows
            entry_1, entry_2, = _.cache_entries()
            #pprint(entry_1)
            response_data_all_1 = _.response_data__all()
            _.pickle_response = False

            # pprint(response_data_all_1[0])
            # pprint(dict(request_hash  =                   entry_1.get('request_hash'  ),
            #             response_data = pickle_from_bytes(entry_1.get('response_bytes')),
            #             response_hash  =                  entry_1.get('response_hash'  ),
            #             ))
            # #assert response_data_all_1 == [entry_1, entry_2]
            # _.pickle_response = False
            # return
            #
            # self.add_test_requests(2)
            # pprint(_.response_data__all())
            # _.pickle_response = True
            # pprint(_.response_data__all())
            # assert len(_.response_data__all()) == 4
            # _.pickle_response = False

    def test_response_data_for__request_hash(self):
        assert self.sqlite_cache_requests.response_data_for__request_hash('aaaa') == {}


    def test_response_data_serialize(self):
        with self.sqlite_cache_requests as _:
            assert _.config.pickle_response == False
            response_data_original_1   = {'an_str': 'an_str', 'an_int': 42}
            response_data_serialised_1 = _.response_data_serialize(response_data_original_1)
            assert type(response_data_serialised_1) is dict
            assert response_data_original_1         == response_data_serialised_1

            _.config.pickle_response = True
            response_data_original_2   = {'an_str': 'an_str', 'an_int': 42}
            response_data_serialised_2 = _.response_data_serialize(response_data_original_2)
            assert type(response_data_serialised_2) is bytes
            assert response_data_serialised_2 == pickle_save_to_bytes(response_data_original_2)
            assert response_data_original_2   == pickle_load_from_bytes(response_data_serialised_2)

            cache_entry = {'response_bytes' : response_data_serialised_2}
            assert response_data_original_2 == _.response_data_deserialize(cache_entry)

    def test_requests_data__all(self):
        count = 2
        self.add_test_requests(count)

        with self.sqlite_cache_requests as _:
            for requests_data in _.requests_data__all():
                assert list_set(requests_data) == ['_comments','_hash', '_id', 'request_data']
            assert _.cache_table().size() == count
