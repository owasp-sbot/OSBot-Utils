from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Nodes import Sqlite__Table__Nodes, SQLITE__TABLE_NAME__NODES
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
        cls.table_nodes.set_timestamp = False

    def tearDown(self):
        self.table_nodes.clear()                     # remove any nodes created during test

    def test__init__(self):
        with self.table_nodes.database as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.db_path   == None

    def test_add_node(self):
        with self.table_nodes as _:
            assert _.allow_duplicate_keys is False
            assert _.set_timestamp        is False
            assert _.rows () == []
            assert _.nodes() == []

            row_obj_1 = _.add_node('key-1')
            assert row_obj_1.__dict__ == {'key': 'key-1', 'properties': b'\x80\x04N.', 'timestamp':0,  'value': b'\x80\x04N.'}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None, 'timestamp': 0, 'value': None}]
            assert _.keys()           == ['key-1']

            row_obj_2 = _.add_node('key-2', 'an_value')
            assert row_obj_2.__dict__ == {'key': 'key-2', 'properties': b'\x80\x04N.', 'timestamp':0,  'value': b'\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08an_value\x94.'}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None, 'timestamp': 0, 'value': None},
                                          {'id': 2, 'key': 'key-2', 'properties': None, 'timestamp': 0, 'value': 'an_value'}]
            assert _.keys()           == ['key-1', 'key-2']

            _.allow_duplicate_keys = True       # so that we can add the duplicated entry below
            row_obj_3 = _.add_node('key-2', 'duplicated-key', properties={'with': 42})
            assert row_obj_3.__dict__ == {'key'        : 'key-2', 'properties' : obj_to_bytes({'with': 42}    ),
                                          'timestamp'  : 0      , 'value'      : obj_to_bytes('duplicated-key')}
            assert _.nodes()          == [{'id': 1, 'key': 'key-1', 'properties': None        , 'timestamp': 0, 'value': None            },
                                          {'id': 2, 'key': 'key-2', 'properties': None        , 'timestamp': 0, 'value': 'an_value'      },
                                          {'id': 3, 'key': 'key-2', 'properties': {'with': 42}, 'timestamp': 0, 'value': 'duplicated-key'}]
            assert _.nodes()          == _.rows()
            assert _.keys()           == ['key-1', 'key-2']
            assert _.size()           == 3
            _.allow_duplicate_keys = False

    def test_add_node__no_duplicates(self):
        with self.table_nodes as _:
            assert _.add_node('key-1').key == 'key-1'               # add once
            assert _.add_node('key-1')     is None                  # trying to add again, will fail (since the node already exists)
            assert _.size() == 1


    def test_create_node_data(self):
        with self.table_nodes as _:
            assert _.create_node_data('an_key') == {'key': 'an_key', 'properties': None, 'value': None }
            assert _.create_node_data('an_key') == {'key': 'an_key', 'properties': None, 'value': None }

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