from sqlite3 import Cursor, Connection
from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite import Sqlite
from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists


class test_Sqlite__Database(TestCase):

    def setUp(self):
        self.database = Sqlite__Database()

    def test__init(self):
        sqlite        = self.database.sqlite
        expected_vars = {'db_name': ':memory:',
                         'sqlite' : sqlite   }
        assert self.database.__locals__() == expected_vars
        assert type(sqlite)               is Sqlite

    def test_connection(self):
        assert type(self.database.connection()) == Connection

    def test_cursor(self):
        assert type(self.database.cursor()) is Sqlite__Cursor

    def test_save_to(self):
        target_file = '/tmp/test.db'
        result = self.database.save_to(target_file)
        pprint(result)
        assert file_exists(target_file)

    def test_table(self):
        table_name = 'an_table'
        table      = self.database.table(table_name)
        assert type(table) is Sqlite__Table
        assert table.exists() is False

    def test_tables(self):
        assert self.database.tables() == []