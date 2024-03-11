from unittest import TestCase

from osbot_utils.helpers.sqlite.Temp_Sqlite__Database__Disk import Temp_Sqlite__Database__Disk
from osbot_utils.utils.Dev import pprint


class test_Temp_Sqlite__Table(TestCase):

    def setUp(self):
        self.temp_sqlite_database = Temp_Sqlite__Database__Disk()
        self.database             = self.temp_sqlite_database.database

    def test__init__(self):
        assert self.database.in_memory is False


    def test__enter__exit__(self):
        with self.temp_sqlite_database as _:
            pass
            #pprint(self.database.connection_string())
            #pprint(self.database.db_path)