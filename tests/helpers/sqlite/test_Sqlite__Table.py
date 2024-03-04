from unittest import TestCase

from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint


class test_Sqlite__Table(TestCase):

    def setUp(self):
        self.table = Sqlite__Table()

    def test__init__(self):
        expected_vars = dict(database=self.table.database, table_fields=[], table_name='')
        assert self.table.__locals__() == expected_vars

    def test_create(self):
        assert self.table.create() is False
        self.table.table_name   = 'an_table'
        self.table.table_fields = ['id INTEGER PRIMARY KEY', 'value TEXT NOT NULL']
        assert self.table.create() is True
        assert self.table.exists() is True
        assert self.table.database.tables() == [ { 'name': 'an_table',
                                                    'rootpage': 2,
                                                    'sql': 'CREATE TABLE an_table (id INTEGER PRIMARY KEY, value TEXT NOT '
                                                           'NULL)',
                                                    'tbl_name': 'an_table',
                                                    'type': 'table'}]

    def test_exists(self):
        assert self.table.exists() is False