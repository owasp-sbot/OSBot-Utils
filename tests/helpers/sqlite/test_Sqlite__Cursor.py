from sqlite3 import Cursor, OperationalError
from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
from osbot_utils.helpers.sqlite.Temp_Sqlite_Table import Temp_Sqlite_Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info


class test_Sqlite__Cursor(TestCase):

    def setUp(self):
        self.cursor = Sqlite__Cursor()

    def test_execute(self):
        assert self.cursor.execute(''   ) == {'data': None, 'error': None, 'message': '', 'status': 'ok'}
        assert self.cursor.execute('aaa') == {'data': None, 'error': 'near "aaa": syntax error', 'message': '', 'status': 'exception'}

    def test_execute__fetch_all(self):
        sql_query = "select * from sqlite_schema"
        result = self.cursor.execute__fetch_all(sql_query)
        assert result == []

    #@capture_sqlite_error
    def test_table_create(self):
        table_name = 'test_table'
        fields     = ['id INTEGER PRIMARY KEY', 'name TEXT NOT NULL','email TEXT UNIQUE NOT NULL']
        assert self.cursor.tables() == []
        self.cursor.table_create(table_name=table_name, fields=fields)

        assert self.cursor.tables() == [{ 'name'     : 'test_table'        ,
                                                       'rootpage' : 2                   ,
                                                       'sql'      : 'CREATE TABLE test_table (id INTEGER PRIMARY KEY, name '
                                                                    'TEXT NOT NULL, email TEXT UNIQUE NOT NULL)',
                                                       'tbl_name' : 'test_table'        ,
                                                       'type'     : 'table'             }]

        #self.cursor.table__sqlite_master()

        assert self.cursor.table__sqlite_master() == [{'name'     : 'test_table'                           ,
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

        table__schema = self.cursor.table_schema(table_name=table_name)
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

        table__schema = self.cursor.table_schema(table_name='sqlite_master')
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

        self.cursor.table_delete(table_name)
        assert self.cursor.tables() == []

    def test_table_schema(self):
        with Temp_Sqlite_Table() as table:
            table_schema = table.cursor().table_schema(table.table_name)
            assert table_schema == [{'cid': 0, 'name': 'id', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}]

    def test_tables(self):
        assert self.cursor.tables() == []