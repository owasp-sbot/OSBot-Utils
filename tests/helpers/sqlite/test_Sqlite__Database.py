from contextlib import contextmanager
from sqlite3 import Cursor, Connection
from unittest import TestCase

import pytest

from osbot_utils.decorators.methods.obj_as_context import obj_as_context
from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database, SQLITE_DATABASE_PATH__IN_MEMORY, \
    FOLDER_NAME_TEMP_DATABASES, TEMP_DATABASE__FILE_NAME_PREFIX, TEMP_DATABASE__FILE_EXTENSION
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, parent_folder, current_temp_folder, folder_name, folder_exists, \
    file_extension, file_name
from osbot_utils.utils.Misc import in_github_action, list_set
from osbot_utils.utils.Objects import obj_data


class test_Sqlite__Database(TestCase):

    def setUp(self):
        self.database = Sqlite__Database()

    def test__init(self):
        expected_vars = { 'db_path'  : None  ,
                          'closed'   : False ,
                          'connected': False ,
                          'deleted'  : False ,
                          'in_memory': True  }
        assert self.database.__locals__() == expected_vars

    @pytest.mark.skip('todo: fix bug caused by side effect of closing the db')
    def test_close(self):
        with self.database as db:
            assert db.tables() == []
            assert db.closed is False
            assert db.close() is True
            assert db.closed is True
            assert db.close() is False
            #assert db.tables() == []
            with self.assertRaises(Exception) as context:
                db.tables()
            assert context.exception.args[0] == 'Cannot operate on a closed database.'

    def test_connect(self):
        expected_obj_items = [ 'DataError'         , 'DatabaseError'         , 'Error'           , 'IntegrityError', 'InterfaceError', 'InternalError'                       ,
                               'NotSupportedError' , 'OperationalError'      , 'ProgrammingError', 'Warning'                                                                 ,
                               'autocommit'        , 'backup'                , 'blobopen'        , 'close'         , 'commit'        , 'create_aggregate', 'create_collation',
                               'create_function'   , 'create_window_function', 'cursor'          , 'deserialize'   , 'execute'       , 'executemany'                         ,
                               'executescript'     , 'getconfig'             , 'getlimit'        , 'in_transaction', 'interrupt'     , 'isolation_level'                     ,
                               'iterdump'          , 'rollback'                   , 'serialize'     , 'set_authorizer', 'set_progress_handler'                ,
                               'set_trace_callback', 'setconfig'             , 'setlimit'        , 'text_factory'  , 'total_changes'                                         ]

        if in_github_action():
            expected_obj_items.extend(['enable_load_extension', 'load_extension'])
            expected_obj_items.sort()
        connection = self.database.connect()
        assert type(connection) is Connection
        assert list_set(obj_data(connection)) == expected_obj_items
        assert connection.autocommit     == -1
        assert connection.in_transaction is False
        assert connection.row_factory    == self.database.dict_factory
        assert connection.total_changes   == 0

        assert connection == self.database.connect()         # confirm @cache is working since we get the same object every time
        assert connection == self.database.connect()

    def test_connection(self):
        assert type(self.database.connection()) == Connection

    def test_connection_string(self):
        assert self.database.connection_string() == SQLITE_DATABASE_PATH__IN_MEMORY
        self.database.in_memory = False
        assert self.database.db_path is None
        connection_string = self.database.connection_string()
        assert connection_string == self.database.db_path
        assert parent_folder(connection_string) == self.database.path_temp_databases()
        assert folder_name  (connection_string).startswith('random_sqlite_db__')

    def test_cursor(self):
        assert type(self.database.cursor()) is Sqlite__Cursor


    def test_delete(self):
        with self.database as db:
            assert db.in_memory is True                                                 # confirm we are in-memory mode
            assert db.db_path   is None                                                 # where the db_path value should not be set
            assert db.delete()  is False                                                # conform can't delete an in-memory db

            db.in_memory = False                                                        # change mode to not be in_memory
            db.connect()                                                                # trigger the creation of the connection
            db_path = db.db_path                                                        # get the value for db_path
            assert file_extension(db_path) == TEMP_DATABASE__FILE_EXTENSION             # confirm that is set and has correct ext
            assert file_exists(db_path)    is True                                      # confirm file exists

            assert db.__locals__() == { #'cache_on_self_connect__': db.connection(),     # FIXED: was BUG this value should not be here
                                        'closed'                 : False          ,
                                        'connected'              : True           ,
                                        'db_path'                : db_path        ,
                                        'deleted'                : False          ,
                                        'in_memory'              : False          }

            assert db.delete()  is True                                                 #  confirm we can delete the file

            assert file_exists(db_path)    is False                                     # after deletion the file doesn't exist
            assert db.__locals__() == { #'cache_on_self_connect__': db.connection(),    # FIXED: was BUG this value should not be here
                                        'closed'                 : True           ,     # was False
                                        'connected'              : False          ,     # was True
                                        'db_path'                : db_path        ,
                                        'deleted'                : True           ,     # # was False
                                        'in_memory'              : False          }

    def test_exists(self):
        assert self.database.exists()

    def test_path_temp_database(self):
        path_temp_database                = self.database.path_temp_database()
        path_temp_database__file_name     = file_name(path_temp_database, check_if_exists=False)
        path_temp_database__parent_folder = parent_folder(path_temp_database)

        assert path_temp_database__parent_folder             == self.database.path_temp_databases()
        assert file_extension(path_temp_database__file_name) == TEMP_DATABASE__FILE_EXTENSION
        assert len(path_temp_database__file_name)            == 10 + len(TEMP_DATABASE__FILE_NAME_PREFIX) + len(TEMP_DATABASE__FILE_EXTENSION)
        assert path_temp_database__file_name.startswith(TEMP_DATABASE__FILE_NAME_PREFIX)


    def test_path_temp_databases(self):
        with obj_as_context(self.database.path_temp_databases())  as _:
            assert parent_folder(_) == current_temp_folder()
            assert folder_name  (_) == FOLDER_NAME_TEMP_DATABASES
            assert folder_exists(_) is True

    def test_save_to(self):
        target_file = '/tmp/test.db'
        result = self.database.save_to(target_file)
        assert file_exists(target_file)

    def test_table(self):
        table_name = 'an_table'
        table      = self.database.table(table_name)
        assert type(table) is Sqlite__Table
        assert table.exists() is False

    def test_tables(self):
        assert self.database.tables() == []