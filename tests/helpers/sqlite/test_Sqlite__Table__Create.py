from unittest import TestCase

import pytest

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field__Type, Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.utils.Dev import pprint
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
            assert len(_.fields) == 0
            assert _.add_field(field_data) is True
            assert _.add_field(None      ) is False
            assert _.add_field('aaa'     ) is False
            assert _.add_field({}        ) is False


    def test__check_test_data(self):
        field_data = FIELD_DATA__ID_INT_PK
        sqlite_field = Sqlite__Field.from_json(field_data)
        assert sqlite_field.text_for_create_table() == 'id INTEGER PRIMARY KEY AUTOINCREMENT'

    def test_create_table(self):
        with self.table_create as _:
            _.add_field(FIELD_DATA__ID_INT_PK)
            assert _.create_table() is True

    def test_sql_for__create_table(self):
        with self.table_create as _:
            _.add_field(FIELD_DATA__ID_INT_PK)
            sql_query = _.sql_for__create_table()
            assert sql_query == f'CREATE TABLE {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT);'

            #pprint(_.database().save_to())
