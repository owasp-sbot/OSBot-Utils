from unittest import TestCase

from osbot_utils.helpers.sqlite.Temp_Sqlite__Table import Temp_Sqlite__Table
from osbot_utils.utils.Dev import pprint


class test_Temp_Sqlite__Table(TestCase):

    def setUp(self):
        self.temp_sqlite_table = Temp_Sqlite__Table()

    def test__init__(self):
        table_name = self.temp_sqlite_table.table_name
        assert table_name.startswith('random_table')   is True
        assert self.temp_sqlite_table.table.table_name == table_name

    def test__enter__exit__(self):
        with self.temp_sqlite_table as table:
            assert table.exists() is True
        assert table.exists() is False