from unittest                                                           import TestCase
from osbot_utils.base_classes.Kwargs_To_Self                            import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database                        import Sqlite__Database
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests           import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local               import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests            import Sqlite__DB__Requests, SQLITE_TABLE__REQUESTS
from osbot_utils.helpers.sqlite.domains.schemas.Schema__Table__Requests import Schema__Table__Requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files                                            import temp_file, current_temp_folder, parent_folder, file_exists, file_not_exists
from osbot_utils.utils.Json                                             import from_json_str, json_dump, to_json_str, json_loads, json_dumps
from osbot_utils.utils.Misc                                             import random_text, list_set, random_string, str_sha256
from osbot_utils.utils.Objects                                          import base_types, pickle_load_from_bytes, pickle_save_to_bytes, pickle_from_bytes


class test_Sqlite__Cache__Requests(TestCase):
    sqlite_cache_requests : Sqlite__Cache__Requests
    temp_db_path          : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path                        = temp_file(extension='sqlite')
        cls.sqlite_cache_requests               = Sqlite__Cache__Requests(db_path = cls.temp_db_path)       # the db_path to the tmp file path
        cls.sqlite_cache_requests.set__add_timestamp(False)                                                 # disabling timestamp since it complicates the test data verification below
        assert parent_folder(cls.sqlite_cache_requests.sqlite_requests.db_path) == current_temp_folder()
        assert file_exists  (cls.temp_db_path)                                 is True

    @classmethod
    def tearDownClass(cls):
        cls.sqlite_cache_requests.sqlite_requests.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def tearDown(self):
        self.sqlite_cache_requests.cache_table().clear()

    # test's helper  methods

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

    # Sqlite__Cache__Requests: methods tests

    def test___init__(self):
        with self.sqlite_cache_requests as _:
            assert type      (_)                  is Sqlite__Cache__Requests
            assert base_types(_)                  == [Kwargs_To_Self, object]
            assert type      (_.sqlite_requests)  is Sqlite__DB__Requests
            assert base_types(_.sqlite_requests)  == [Sqlite__DB__Local, Sqlite__Database, Kwargs_To_Self, object]
            assert _.sqlite_requests.db_name.startswith('db_local_')
            assert _.sqlite_requests.table_name   == SQLITE_TABLE__REQUESTS

    def test_cache_add(self):
        self.sqlite_cache_requests.sqlite_requests.table_requests__reset()
        request_data         = {'the':'request_data', 'random_value' : random_string()}
        request_data_json    = json_dump(request_data)
        request_data_sha256  = str_sha256(request_data_json)
        response_data        = {'the':'response_data'}
        response_data_json   = json_dump(response_data)
        response_data_sha256 = str_sha256(response_data_json)
        expected_new_row     = { 'comments'       : ''                   ,
                                 'metadata'       : ''                   ,
                                 'request_data'   : request_data_json    ,
                                 'request_hash'   : request_data_sha256  ,
                                 'request_type'   : ''                   ,
                                 'response_bytes' : b''                  ,
                                 'response_data'  : response_data_json   ,
                                 'response_hash'  : response_data_sha256 ,
                                 'response_type'  : 'dict'               ,
                                 'source'         : ''                   ,
                                 'timestamp'      : 0                    }
        expected_row_entry   = { **expected_new_row                      ,
                                 'id'            : 1                     }

        new_row = self.sqlite_cache_requests.cache_add(request_data, response_data)
        assert new_row.json() == expected_new_row

        with self.sqlite_cache_requests.cache_table() as _:
            rows = _.select_rows_where(request_hash=request_data_sha256)
            assert len(rows) == 1
            row = rows [0]
            assert row == expected_row_entry

            assert self.sqlite_cache_requests.cache_entry(request_data) == expected_row_entry   # confirm we can get the row via it's row_data
            _.rows_delete_where(request_hash=request_data_sha256)                       # delete added row
            assert _.rows() == []                                                       # confirm we are back to having an empty table
            assert self.sqlite_cache_requests.cache_entry(request_data) == {}                   # confirm entry is not available anymore

    def test_cache_delete(self):
        request_data  = {'an': 'request' }
        response_data = {'an': 'response'}
        with self.sqlite_cache_requests as _:
            row = _.cache_add(request_data, response_data)
            assert row.request_data         == to_json_str(request_data )
            assert row.response_data        == to_json_str(response_data)
            assert len (_.cache_entries())  == 1
            assert _.cache_delete(request_data).get('status') == 'ok'
            assert len(_.cache_entries())   == 0

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


    def test_create_new_cache_data(self):
        model_id                 = 'aaaa'
        body                     = {'the': 'request data'}
        response_data            = {'the': 'return value'}
        request_data             = self.sqlite_cache_requests.cache_request_data(model_id=model_id, body=body)
        new_cache_entry          = self.sqlite_cache_requests.create_new_cache_row_data(request_data, response_data)
        expected_new_cache_entry = { 'comments'     : ''                                                                  ,
                                     'metadata'     : ''                                                                  ,
                                     'request_data'  : json_dumps(request_data)                                           ,
                                     'request_hash'  : 'f917e6f5658f5b761a77416d487c5d9a70253abce68b348bc360a6f39657753a' ,
                                     'request_type'  : ''                                                                 ,
                                     'response_bytes': b''                                                                ,
                                     'response_data' : json_dumps(response_data)                                          ,
                                     'response_hash' : '69e330ec7bf6334aa41ecaf56797fa86345d3cf85da4c622821aa42d4bee1799' ,
                                     'response_type' : 'dict'                                                             ,
                                     'source'        : ''                                                                 ,
                                     'timestamp'     :  0                                                                 }
        expected_new_cache_obj   = { **expected_new_cache_entry,
                                     'timestamp'    : 0 }
        assert new_cache_entry == expected_new_cache_entry
        new_cache_obj = self.sqlite_cache_requests.cache_table().new_row_obj(new_cache_entry)
        assert new_cache_obj.__locals__() == expected_new_cache_obj
        assert self.sqlite_cache_requests.cache_entries() ==[]

        self.sqlite_cache_requests.set__add_timestamp(True)

        new_cache_entry = self.sqlite_cache_requests.create_new_cache_row_data(request_data, response_data)
        assert new_cache_entry.get('timestamp') != 0
        assert new_cache_entry.get('timestamp') > 0
        self.sqlite_cache_requests.set__add_timestamp(False)

        self.sqlite_cache_requests.cache_actions.cache_row_config.add_timestamp = self.sqlite_cache_requests.add_timestamp  # todo: remove this temp fix for passing in the timestamp

    # TODO : Finish test asserts
    def test_create_new_cache_data__pickle_response_is_True(self):
        row_count = 2
        with self.sqlite_cache_requests as _:
            assert _.pickle_response is False           # default value
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

    def test_disable(self):
        with self.sqlite_cache_requests as _:
            assert _.enabled is True
            _.disable()
            assert _.enabled is False
            _.enable()
            assert _.enabled is True

    def test_only_from_cache(self):
        with self.sqlite_cache_requests as _:
            assert _.cache_only_mode is False
            _.only_from_cache()
            assert _.cache_only_mode is True
            _.only_from_cache(False)
            assert _.cache_only_mode is False

    def test_response_data_serialize(self):
        with self.sqlite_cache_requests as _:
            assert _.pickle_response == False
            response_data_original_1   = {'an_str': 'an_str', 'an_int': 42}
            response_data_serialised_1 = _.response_data_serialize(response_data_original_1)
            assert type(response_data_serialised_1) is dict
            assert response_data_original_1         == response_data_serialised_1

            _.pickle_response = True
            response_data_original_2   = {'an_str': 'an_str', 'an_int': 42}
            response_data_serialised_2 = _.response_data_serialize(response_data_original_2)
            assert type(response_data_serialised_2) is bytes
            assert response_data_serialised_2 == pickle_save_to_bytes(response_data_original_2)
            assert response_data_original_2   == pickle_load_from_bytes(response_data_serialised_2)

            cache_entry = {'response_bytes' : response_data_serialised_2}
            assert response_data_original_2 == _.response_data_deserialize(cache_entry)



    def test_response_data_for__request_hash(self):
        assert self.sqlite_cache_requests.response_data_for__request_hash('aaaa') == {}


    def test_requests_data__all(self):
        count = 2
        self.add_test_requests(count)

        with self.sqlite_cache_requests as _:
            for requests_data in _.requests_data__all():
                assert list_set(requests_data) == ['_comments','_hash', '_id', 'request_data']
            assert _.cache_table().size() == count


    def test_setup(self):
        with self.sqlite_cache_requests.sqlite_requests as _:
            assert type(_)   is Sqlite__DB__Requests
            assert _.db_path != Sqlite__DB__Requests().path_local_db()
            assert _.db_path == self.temp_db_path

        with self.sqlite_cache_requests.cache_table() as _:

            _._table_create().add_fields_from_class(Schema__Table__Requests).sql_for__create_table()

            assert _.exists()   is True
            assert _.row_schema is Schema__Table__Requests
            assert _.schema__by_name_type() == { 'comments'      : 'TEXT'    ,
                                                 'id'            : 'INTEGER' ,
                                                 'metadata'      : 'TEXT'    ,
                                                 'request_data'  : 'TEXT'    ,
                                                 'request_hash'  : 'TEXT'    ,
                                                 'request_type'  : 'TEXT'    ,
                                                 'response_bytes': 'BLOB'    ,
                                                 'response_data' : 'TEXT'    ,
                                                 'response_hash' : 'TEXT'    ,
                                                 'response_type' : 'TEXT'    ,
                                                 'source'        : 'TEXT'    ,
                                                 'timestamp'     : 'INTEGER' }
            assert _.indexes() == ['idx__requests__request_hash']


    def test_update(self):
        with self.sqlite_cache_requests as _:
            assert _.update_mode is False
            _.update()
            assert _.update_mode is True
            _.update(False)
            assert _.update_mode is False


    def test__bug__cache_request_data__overide_is_not_working(self):

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
