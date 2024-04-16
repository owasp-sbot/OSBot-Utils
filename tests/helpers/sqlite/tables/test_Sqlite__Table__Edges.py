from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Edges import Sqlite__Table__Edges, SQLITE__TABLE_NAME__EDGES

class test_Sqlite__Table__Nodes(TestCase):
    table_edges: Sqlite__Table__Edges
    database   : Sqlite__Database

    @classmethod
    def setUpClass(cls):
        cls.table_edges = Sqlite__Table__Edges()
        cls.database     = cls.table_edges.database
        cls.table_edges.setup()
        cls.table_edges.add_timestamp = False

    def tearDown(self):
        self.table_edges.clear()                     # remove any nodes created during test

    def test__init__(self):
        with self.table_edges.database as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.db_path   == None


    def test_add_edge(self):
        with self.table_edges as _:
            assert _.add_timestamp        is False
            assert _.rows () == []
            assert _.edges() == []

            row_obj_1 = _.add_edge('key-1', 'key-2')
            assert row_obj_1.__dict__ == { 'properties' : b'\x80\x04N.' ,
                                           'source_key' : 'key-1'       ,
                                           'target_key' : 'key-2'       ,
                                           'timestamp'  : 0             ,
                                           'value'      : b'\x80\x04N.' }
            assert _.edges()          == [{'id'         : 1             ,
                                           'properties' : None          ,
                                           'source_key' : 'key-1'       ,
                                           'target_key' : 'key-2'       ,
                                           'timestamp'  : 0             ,
                                           'value'      : None          }]

            row_obj_2 = _.add_edge('key-1', 'key-3', b'an value as bytes', {'props': 'as dict'})
            assert row_obj_2.__dict__ == {'properties'  : b'\x80\x04\x95\x16\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x05props\x94\x8c\x07as dict\x94s.',
                                          'source_key'  : 'key-1'   ,
                                          'target_key'  : 'key-3'   ,
                                          'timestamp'   : 0         ,
                                          'value'       : b'\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00C\x11an value as bytes\x94.'}
            assert _.edges()          == [{'id': 1, 'properties': None                , 'source_key': 'key-1', 'target_key': 'key-2', 'timestamp': 0, 'value': None                },
                                          {'id': 2, 'properties': {'props': 'as dict'}, 'source_key': 'key-1', 'target_key': 'key-3', 'timestamp': 0, 'value': b'an value as bytes'}]

    def test___init__(self):
        with self.database as _:
            assert _.exists()  is True
            assert _.db_path   is None
            assert _.in_memory is True

        with self.table_edges as _:
            assert _.exists()                   is True
            assert _.table_name                 == SQLITE__TABLE_NAME__EDGES
            assert _.schema__by_name_type()     == {'id'        : 'INTEGER',
                                                    'source_key': 'TEXT'   ,
                                                    'target_key': 'TEXT'   ,
                                                    'properties': 'BLOB'   ,
                                                    'timestamp' : 'INTEGER',
                                                    'value'     : 'BLOB'   }
            assert _.new_row_obj().__locals__() == {'source_key': '', 'target_key': '', 'value': b'', 'properties': b'', 'timestamp': 0}
            assert _.indexes()                  == ['idx__edges__source_key', 'idx__edges__target_key']