import sqlite3
from sqlite3 import Connection, Cursor
from unittest import TestCase


from osbot_utils.helpers.sqlite.Capture_Sqlite_Error import capture_sqlite_error, Capture_Sqlite_Error
from osbot_utils.helpers.sqlite.Sqlite3 import Sqlite3
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, in_github_action, wait_for
from osbot_utils.utils.Objects import obj_data, obj_info


class test_Sqlite3(TestCase):

    def setUp(self):
        self.db_name = ':memory:'               # create an in-memory database    #'test_Sqlite3.db'
        self.sqlite3 = Sqlite3()

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
        connection = self.sqlite3.connect(self.db_name)
        assert type(connection) is Connection
        assert list_set(obj_data(connection)) == expected_obj_items
        assert connection.autocommit     == -1
        assert connection.in_transaction is False
        assert connection.row_factory    == self.sqlite3.dict_factory
        assert connection.total_changes   == 0

        assert connection == self.sqlite3.connect(self.db_name)         # confirm @cache is working since we get the same object every time
        assert connection == self.sqlite3.connect(self.db_name)


    def test_execute(self):
        cursor = self.sqlite3.execute(self.db_name, '')
        assert type(cursor) is Cursor
        assert cursor.description is None

    def test_execute__fetch_all(self):
        sql_query = "select * from sqlite_schema"
        result = self.sqlite3.execute__fetch_all(self.db_name, sql_query)
        assert result == []

    #@capture_sqlite_error
    def test_table_create(self):
        table_name = 'test_table'
        fields     = ['id INTEGER PRIMARY KEY', 'name TEXT NOT NULL','email TEXT UNIQUE NOT NULL']
        assert self.sqlite3.tables(self.db_name) == []
        self.sqlite3.table_create(db_name=self.db_name, table_name=table_name, fields=fields)
        assert self.sqlite3.tables(self.db_name) == [{ 'name'     : 'test_table'        ,
                                                       'rootpage' : 2                   ,
                                                       'sql'      : 'CREATE TABLE test_table (id INTEGER PRIMARY KEY, name '
                                                                    'TEXT NOT NULL, email TEXT UNIQUE NOT NULL)',
                                                       'tbl_name' : 'test_table'        ,
                                                       'type'     : 'table'             }]

        self.sqlite3.table__sqlite_master(self.db_name)

        assert self.sqlite3.table__sqlite_master(self.db_name) == [{'name'     : 'test_table'                           ,
                                                                    'rootpage' : 2                                      ,
                                                                    'sql'      : 'CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL)',
                                                                    'tbl_name' : 'test_table'                           ,
                                                                    'type'     : 'table'
                                                                   },
                                                                   {'name'     : 'sqlite_autoindex_test_table_1'        ,
                                                                    'rootpage' : 3                                      ,
                                                                    'sql'      : None                                   ,
                                                                    'tbl_name' : 'test_table'                           ,
                                                                    'type'     : 'index'
                                                                   }]
        table__schema = self.sqlite3.table__schema(db_name=self.db_name, table_name=table_name)
        assert table__schema == [{ 'cid'       : 0        ,
                                   'name'      : 'id'     ,
                                   'type'      : 'INTEGER',
                                   'notnull'   : 0        ,
                                   'dflt_value': None     ,
                                   'pk'        : 1        },
                                 { 'cid'       : 1        ,
                                   'name'      : 'name'   ,
                                   'type'      : 'TEXT'   ,
                                   'notnull'   : 1        ,
                                   'dflt_value': None     ,
                                   'pk'        : 0        },
                                 { 'cid'       : 2        ,
                                   'name'      : 'email'  ,
                                   'type'      : 'TEXT'   ,
                                   'notnull'   : 1        ,
                                   'dflt_value': None     ,
                                   'pk'        : 0        }]

        table__schema = self.sqlite3.table__schema(db_name=self.db_name, table_name='sqlite_master')
        assert table__schema == [{ 'cid'       : 0        ,
                                   'dflt_value': None     ,
                                   'name'      : 'type'   ,
                                   'notnull'   : 0        ,
                                   'pk'        : 0        ,
                                   'type'      : 'TEXT'   },
                                 { 'cid'       : 1        ,
                                   'dflt_value': None     ,
                                   'name'      : 'name'   ,
                                   'notnull'   : 0        ,
                                   'pk'        : 0        ,
                                   'type'      : 'TEXT'   },
                                 { 'cid'       : 2        ,
                                   'dflt_value': None     ,
                                   'name'      : 'tbl_name',
                                   'notnull'   : 0        ,
                                   'pk'        : 0        ,
                                   'type'      : 'TEXT'   },
                                 { 'cid'       : 3        ,
                                   'dflt_value': None     ,
                                   'name'      : 'rootpage',
                                   'notnull'   : 0        ,
                                   'pk'        : 0        ,
                                   'type'      : 'INT'    },
                                 { 'cid'       : 4        ,
                                   'dflt_value': None     ,
                                   'name'      : 'sql'    ,
                                   'notnull'   : 0        ,
                                   'pk'        : 0        ,
                                   'type'      : 'TEXT'   }]

        self.sqlite3.table_delete(self.db_name, table_name)
        assert self.sqlite3.tables(self.db_name) == []
        # #pprint(table__sqlite_master)

    def test_tables(self):
        tables = self.sqlite3.tables(self.db_name)
        assert tables == []





#         """CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL
# );"""