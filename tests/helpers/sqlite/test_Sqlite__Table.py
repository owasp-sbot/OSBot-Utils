from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


TEST_TABLE_FIELDS = ['id INTEGER PRIMARY KEY', 'value TEXT NOT NULL']
TEST_TABLE_NAME   = 'an_table'

class test_Sqlite__Table(TestCase):
    table        : Sqlite__Table
    #table_fields : list
    #table_name   : str

    @classmethod
    def setUpClass(cls):
        cls.table        = Sqlite__Table(table_name=TEST_TABLE_NAME, table_fields=TEST_TABLE_FIELDS)
        cls.table.create()
        #assert cls.table.create() == True

    @classmethod
    def tearDownClass(cls):
        cls.table.delete()
        #assert cls.table.delete() is True





    def test__init__(self):
        expected_vars = dict(database=self.table.database, table_fields=TEST_TABLE_FIELDS, table_name=TEST_TABLE_NAME)
        assert self.table.__locals__() == expected_vars

    def test_create(self):
        assert self.table.delete() is True                  # confirm table exists
        assert self.table.delete() is False                 # confirm that deleting table when it doesn't exist returns False
        assert self.table.create() is True                  # created ok
        assert self.table.create() is False                 # can't create if already exists
        assert self.table.exists() is True                  # confirm table exists
        assert self.table.database.tables() == [ { 'name'       : 'an_table'    ,
                                                    'rootpage'  : 2             ,
                                                    'sql'       : 'CREATE TABLE an_table (id INTEGER PRIMARY KEY, value TEXT NOT NULL)',
                                                    'tbl_name'  : 'an_table'    ,
                                                    'type'      : 'table'       }]


    def test_exists(self):
        assert self.table.exists() is True

    def test_schema(self):
        table_schema = self.table.schema()
        print()
        assert table_schema == [{'cid': 0, 'name': 'id'   , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                                {'cid': 1, 'name': 'value', 'type': 'TEXT'   , 'notnull': 1, 'dflt_value': None, 'pk': 0}]