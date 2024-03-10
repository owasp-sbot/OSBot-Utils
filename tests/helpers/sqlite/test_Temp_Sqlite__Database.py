from unittest import TestCase

from osbot_utils.helpers.sqlite.Temp_Sqlite__Database import Temp_Sqlite__Database, SQLITE_DATABASE_PATH__IN_MEMORY


class test_Temp_Sqlite__Table(TestCase):

    def setUp(self):
        self.temp_sqlite_database = Temp_Sqlite__Database()
        #self.database             =

    def test__init__(self):
        assert self.temp_sqlite_database.path == SQLITE_DATABASE_PATH__IN_MEMORY
