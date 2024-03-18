from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook
from osbot_utils.helpers.sqlite.sql_builder.SQL_Builder__Select import SQL_Builder__Select
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint


class test_SQL_Builder__Select(TestCase):
    db_chinook : Sqlite__Database
    table      : Sqlite__Table

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_chinook = Sqlite__Sample_Data__Chinook().load_db_from_disk()
        cls.table      = cls.db_chinook.table('Genre')
        cls.table.row_schema__set_from_field_types()

    def setUp(self):
        self.sql_builder_select = SQL_Builder__Select(table=self.table)

    def test__setup(self):
        assert self.db_chinook.tables_names() == ['Genre', 'MediaType', 'Artist', 'Album', 'Track', 'Employee', 'Customer', 'Invoice', 'InvoiceLine', 'Playlist', 'PlaylistTrack']
        assert self.table.size() == 25

    def test_build(self):
        assert self.sql_builder_select.build()  == 'SELECT * FROM *'

    # def test_validate_query_data(self):
    #     self.validate_query_data()§