from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Misc import random_string, random_int

#TEST_TABLE_FIELDS = ['id INTEGER PRIMARY KEY', 'an_str TEXT NOT NULL', 'an_int INTEGER']
TEST_TABLE_FIELDS = [dict(name='an_str', type=str, notnull=True), dict(name='an_int', type=int)]
TEST_TABLE_NAME   = 'an_table'

class test_Sqlite__Table(TestCase):
    table        : Sqlite__Table
    #table_fields : list
    #table_name   : str

    @classmethod
    def setUpClass(cls):
        cls.table        = Sqlite__Table(table_name=TEST_TABLE_NAME)
        cls.table.create(fields=TEST_TABLE_FIELDS)
        #assert cls.table.create() == True

    @classmethod
    def tearDownClass(cls):
        cls.table.delete()
        #assert cls.table.delete() is True

    def create_test_data(self, size=10):
        return [{'an_str': f'an_str_{i}', 'an_int': i} for i in range(size)]

    def test__init__(self):
        expected_vars = dict(database=self.table.database, table_name=TEST_TABLE_NAME)
        assert self.table.__locals__() == expected_vars

    def test_create(self):
        fields = TEST_TABLE_FIELDS
        assert self.table.delete(      ) is True                  # confirm table exists
        assert self.table.delete(      ) is False                 # confirm that deleting table when it doesn't exist returns False
        assert self.table.create(fields) is True                  # created ok
        assert self.table.create(      ) is False                 # can't create if already exists
        assert self.table.exists(      ) is True                  # confirm table exists

        tables_raw = self.table.database.tables_raw()
        tables     = self.table.database.tables()
        table      = tables[0]

        assert len(tables) == 1
        assert type(table) is Sqlite__Table
        assert tables_raw  == [{ 'name'       : 'an_table'   ,
                                 'rootpage'  : 2             ,
                                 'sql'       : 'CREATE TABLE an_table (id INTEGER PRIMARY KEY, an_str TEXT NOT NULL, an_int INTEGER)',
                                 'tbl_name'  : 'an_table'    ,
                                 'type'      : 'table'       }]
        assert table.schema() == [{'cid': 0, 'name': 'id'    , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                                  {'cid': 1, 'name': 'an_str', 'type': 'TEXT'   , 'notnull': 1, 'dflt_value': None, 'pk': 0},
                                  {'cid': 2, 'name': 'an_int', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}]


    def test_exists(self):
        assert self.table.exists() is True

    def test_schema(self):
        table_schema = self.table.schema()
        assert table_schema == [{'cid': 0, 'name': 'id'    , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                                {'cid': 1, 'name': 'an_str', 'type': 'TEXT'   , 'notnull': 1, 'dflt_value': None, 'pk': 0},
                                {'cid': 2, 'name': 'an_int', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}]


    def test_rows(self):
        size = 10
        test_data = self.create_test_data(size)
        self.table.rows_add(test_data)
        assert len(self.table.rows()) == len(test_data)

    def test_sql_query_for_fields(self):
        assert self.table.sql_query_for_fields(                ) == 'SELECT an_int, an_str, id FROM an_table;'
        assert self.table.sql_query_for_fields(['id'          ]) == 'SELECT id FROM an_table;'
        assert self.table.sql_query_for_fields(['an_int'      ]) == 'SELECT an_int FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str'      ]) == 'SELECT an_str FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str', 'id']) == 'SELECT an_str, id FROM an_table;'
