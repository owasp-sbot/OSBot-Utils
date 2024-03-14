from unittest import TestCase

import pytest

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field__Type, Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_delete, file_exists
from osbot_utils.utils.Misc import random_text
from osbot_utils.utils.Objects import obj_info

FIELD_DATA__ID_INT_PK = dict(name="id", type="INTEGER", pk=True, autoincrement=True)

class test_Sqlite__Table__Create(TestCase):
    table_name :str =  random_text(prefix='random_table')

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self) -> None:
        self.table_name = 'an_test_table'
        self.table_create = Sqlite__Table__Create(table_name=self.table_name)

    def test_add_field(self):
        field_data   = FIELD_DATA__ID_INT_PK
        with self.table_create as _:
            assert len(_.fields) == 1                       # there is a default id field on all tables
            assert _.add_field(field_data) is True
            assert _.add_field(None      ) is False
            assert _.add_field('aaa'     ) is False
            assert _.add_field({}        ) is False

    def test_add_field_with_type(self):
        with self.table_create as _:
            _.add_field_with_type('an_field', 'TEXT')
            assert _.fields__by_name_type() == {'an_field': 'TEXT', 'id': 'INTEGER'}
            _.fields_reset()
            assert _.fields_json() == []
            _.add_field_with_type('an_str'  , str  )
            _.add_field_with_type('an_int'  , int  )
            _.add_field_with_type('an_bytes', bytes)
            assert _.fields__by_name_type() == {'an_bytes': 'BLOB', 'an_int': 'INTEGER', 'an_str': 'TEXT'}


    def test_add_field__text(self):
        with self.table_create as _:
            _.add_field__text('an_text_field')
            assert _.fields_json(only_show=['name', 'type']) == [{'name': 'id'           , 'type': 'INTEGER'},
                                                                 {'name': 'an_text_field', 'type': 'TEXT'   }]

    def test_add_fields__text(self):
        with self.table_create as _:
            _.add_fields__text('field_1', 'field_2')
            assert _.fields__by_name_type()  == {'field_1': 'TEXT', 'field_2': 'TEXT', 'id': 'INTEGER'}

    def test__check_test_data(self):
        field_data = FIELD_DATA__ID_INT_PK
        sqlite_field = Sqlite__Field.from_json(field_data)
        assert sqlite_field.text_for_create_table() == 'id INTEGER PRIMARY KEY AUTOINCREMENT'

    def test_create_table(self):
        with self.table_create as _:
            assert _.create_table() is True                     # create_table
            assert _.create_table() is False                    # should only return True once
            target_file = '/tmp/test.db'
            file_delete(target_file)
            _.database().save_to(target_file)
            assert file_exists(target_file) is True




    def test_sql_for__create_table(self):
        with self.table_create as _:
            sql_query = _.sql_for__create_table()
            assert sql_query == f'CREATE TABLE {self.table_name} (id INTEGER PRIMARY KEY);'

        # todo: add support for composite primary and for foreign key constraints
