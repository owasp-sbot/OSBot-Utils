from unittest import TestCase

import pytest

from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field__Type, Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_text
from osbot_utils.utils.Objects import obj_info


class test_Sqlite__Table__Create(TestCase):
    table_name :str =  random_text(prefix='random_table')

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self) -> None:
        self.table_create = Sqlite__Table__Create()

    def test_create_table(self):
        # sqlite_field__use_case_1 = dict(name="id", type=Sqlite__Field__Type.INTEGER, pk=True, autoincrement=True)
        # sqlite_field__sql_text_1 = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        # assert Sqlite__Field(**sqlite_field__use_case_1).text_for_create_table() == sqlite_field__sql_text_1
        # return
        #field_data =  dict(name="id", type=int, pk=True, autoincrement=True)
        field_data =  dict(name="id", type="INTEGER", pk=True, autoincrement=True)
        sqlite_field = Sqlite__Field.from_json(field_data)
        assert sqlite_field.text_for_create_table()== 'id INTEGER PRIMARY KEY AUTOINCREMENT'
        #self.table_create.add_field(field_data)
        #pprint(self.table_create.fields)

