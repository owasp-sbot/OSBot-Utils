import pytest
from unittest                                                               import TestCase
from osbot_utils.utils.Env                                                  import not_in_github_action
from osbot_utils.helpers.sqlite.Sqlite__Database                            import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table                               import Sqlite__Table
from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook    import Sqlite__Sample_Data__Chinook
from osbot_utils.helpers.sqlite.sql_builder.SQL_Builder__Select             import SQL_Builder__Select

class test_SQL_Builder__Select(TestCase):
    db_chinook : Sqlite__Database
    table      : Sqlite__Table

    @classmethod
    def setUpClass(cls) -> None:
        if not_in_github_action():
            pytest.skip("Skip test locally since needs the Sqlite__Sample_Data__Chinook data")  # todo: change this test so that It doesn't need this anymore
        cls.db_chinook = Sqlite__Sample_Data__Chinook().load_db_from_disk()
        cls.table      = cls.db_chinook.table('Genre')

    def setUp(self):
        self.sql_builder_select = SQL_Builder__Select(table=self.table)

    def test__setup(self):
        assert self.db_chinook.tables_names() == ['Genre', 'MediaType', 'Artist', 'Album', 'Track', 'Employee', 'Customer', 'Invoice', 'InvoiceLine', 'Playlist', 'PlaylistTrack']
        assert self.table.size() == 25


    def test_validate_query_data(self):
        self.sql_builder_select.validate_query_data()

