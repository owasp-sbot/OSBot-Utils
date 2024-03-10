from contextlib import contextmanager
from sqlite3 import Cursor, Connection
from unittest import TestCase

from osbot_utils.decorators.methods.obj_as_context import obj_as_context
from osbot_utils.helpers.sqlite.Sqlite import Sqlite
from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database, SQLITE_DATABASE_PATH__IN_MEMORY, \
    FOLDER_NAME_TEMP_DATABASES, TEMP_DATABASE__FILE_NAME_PREFIX, TEMP_DATABASE__FILE_EXTENSION
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, parent_folder, current_temp_folder, folder_name, folder_exists, \
    file_extension


class test_Sqlite__Database(TestCase):

    def setUp(self):
        self.database = Sqlite__Database()

    def test__init(self):
        sqlite        = self.database.sqlite
        expected_vars = {'db_path'  : ''   ,
                         'in_memory': True   ,
                         'sqlite'   : sqlite }
        assert self.database.__locals__() == expected_vars
        assert type(sqlite)               is Sqlite

    def test_connection(self):
        assert type(self.database.connection()) == Connection

    def test_connection_string(self):
        assert self.database.connection_string() == SQLITE_DATABASE_PATH__IN_MEMORY
        self.database.in_memory = False
        assert self.database.connection_string().startswith('random_sqlite_db__')

    def test_cursor(self):
        assert type(self.database.cursor()) is Sqlite__Cursor

    def test_path_temp_database(self):
        path_temp_database = self.database.path_temp_database()
        assert path_temp_database.startswith(TEMP_DATABASE__FILE_NAME_PREFIX)
        assert file_extension(path_temp_database) == TEMP_DATABASE__FILE_EXTENSION
        assert len(path_temp_database) == 10 + len(TEMP_DATABASE__FILE_NAME_PREFIX) + len(TEMP_DATABASE__FILE_EXTENSION)

    def test_path_temp_databases(self):
        with obj_as_context(self.database.path_temp_databases())  as _:
            assert parent_folder(_) == current_temp_folder()
            assert folder_name  (_) == FOLDER_NAME_TEMP_DATABASES
            assert folder_exists(_) is True

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