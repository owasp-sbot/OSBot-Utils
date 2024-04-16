from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqite__Table__Nodes import Sqlite__Table__Nodes, SQLITE__TABLE_NAME__NODES
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_to_bytes


class test_Sqlite__Table__Nodes(TestCase):
    table_nodes: Sqlite__Table__Nodes
    database   : Sqlite__Database

    @classmethod
    def setUpClass(cls):
        cls.table_nodes = Sqlite__Table__Nodes()
        cls.database     = cls.table_nodes.database
        cls.table_nodes.setup()
        cls.table_nodes.add_timestamp = False

    def tearDown(self):
        self.table_nodes.clear()                     # remove any nodes created during test

    def test__init__(self):
        with self.table_nodes.database as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.db_path   == None

    def test_add_node(self):
        with self.table_nodes as _:
            assert _.allow_duplicate_keys is True
            assert _.add_timestamp        is False
            assert _.rows() == []

            row_obj_1 = _.add_node('key-1')
            assert row_obj_1.__dict__ == {'key': 'key-1', 'properties': b'\x80\x04N.', 'timestamp':0,  'value': b'\x80\x04N.'}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None, 'timestamp': 0, 'value': None}]
            assert _.keys()           == ['key-1']

            row_obj_2 = _.add_node('key-2', 'an_value')
            assert row_obj_2.__dict__ == {'key': 'key-2', 'properties': b'\x80\x04N.', 'timestamp':0,  'value': b'\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08an_value\x94.'}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None, 'timestamp': 0, 'value': None},
                                          {'id': 2, 'key': 'key-2', 'properties': None, 'timestamp': 0, 'value': 'an_value'}]
            assert _.keys()           == ['key-1', 'key-2']

            row_obj_3 = _.add_node('key-2', 'duplicated-key', properties={'with': 42})
            assert row_obj_3.__dict__ == {'key'        : 'key-2', 'properties' : obj_to_bytes({'with': 42}    ),
                                          'timestamp'  : 0      , 'value'      : obj_to_bytes('duplicated-key')}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None        , 'timestamp': 0, 'value': None            },
                                          {'id': 2, 'key': 'key-2', 'properties': None        , 'timestamp': 0, 'value': 'an_value'      },
                                          {'id': 3, 'key': 'key-2', 'properties': {'with': 42}, 'timestamp': 0, 'value': 'duplicated-key'}]
            assert _.keys() == ['key-1', 'key-2']
            assert _.size() == 3

    def test_add_node__no_duplicates(self):
        with self.table_nodes as _:
            _.allow_duplicate_keys = False
            assert _.add_node('key-1').key == 'key-1'               # add once
            assert _.add_node('key-1')     is None                  # trying to add again, will fail (since the node already exists)
            assert _.size() == 1


    def test_create_node_data(self):
        with self.table_nodes as _:
            assert _.create_node_data('an_key') == {'key': 'an_key', 'properties': b'\x80\x04N.'     , 'value': b'\x80\x04N.'}
            assert _.create_node_data('an_key') == {'key': 'an_key', 'properties': obj_to_bytes(None), 'value': obj_to_bytes(None)}

    def test_deserialize_sqlite_node_data(self):
        with self.table_nodes as _:
            node_data_2        = dict(key='an_key', value='an_string', properties={'a': 42})
            node_data_3        = dict(key='an_key', value=b'now using bytes an no properties')
            node_data_4        = dict(key='an_key', properties = {'and': 'no value'})
            node_data_5        = dict(key='an_key', value={'value': 'as object', 'an_int': 42})
            sqlite_node_data_1 = _.create_node_data('an_key')
            sqlite_node_data_2 = _.create_node_data(**node_data_2)
            sqlite_node_data_3 = _.create_node_data(**node_data_3)
            sqlite_node_data_4 = _.create_node_data(**node_data_4)
            sqlite_node_data_5 = _.create_node_data(**node_data_5)
            assert _.deserialize_sqlite_node_data(None) is None
            assert _.deserialize_sqlite_node_data({}                ) == {'properties': None, 'value': None}
            assert _.deserialize_sqlite_node_data(dict(key='a')     ) == {'key':'a', 'properties': None, 'value': None}
            assert _.deserialize_sqlite_node_data(sqlite_node_data_1) == {'key': 'an_key', 'properties': None, 'value': None}
            assert _.deserialize_sqlite_node_data(sqlite_node_data_2) == node_data_2
            assert _.deserialize_sqlite_node_data(sqlite_node_data_3) == dict(**node_data_3, properties=None)
            assert _.deserialize_sqlite_node_data(sqlite_node_data_4) == dict(**node_data_4, value     =None)
            assert _.deserialize_sqlite_node_data(sqlite_node_data_5) == dict(**node_data_5, properties=None)


    def test___init__(self):
        with self.database as _:
            assert _.exists()  is True
            assert _.db_path   is None
            assert _.in_memory is True

        with self.table_nodes as _:
            assert _.exists()                   is True
            assert _.table_name                 == SQLITE__TABLE_NAME__NODES
            assert _.schema__by_name_type()     == {'id'        : 'INTEGER',
                                                    'key'       : 'TEXT'   ,
                                                    'properties': 'BLOB'   ,
                                                    'timestamp' : 'INTEGER',
                                                    'value'     : 'BLOB'   }
            assert _.new_row_obj().__locals__() == {'key': '', 'properties': b'', 'timestamp': 0, 'value': b''}
            assert _.indexes()                  == ['idx__nodes__key']