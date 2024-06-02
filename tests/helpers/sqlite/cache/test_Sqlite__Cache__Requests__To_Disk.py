from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.utils.Files import temp_file, file_not_exists, file_exists, parent_folder, current_temp_folder


class test_Sqlite__Cache__Requests__To_Disk(TestCase):
    sqlite_cache_requests : Sqlite__Cache__Requests
    temp_db_path          : str

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path           = temp_file(extension='sqlite')
        cls.sqlite_cache_requests  = Sqlite__Cache__Requests(db_path = cls.temp_db_path)       # the db_path to the tmp file path

    @classmethod
    def tearDownClass(cls):
        cls.sqlite_cache_requests.sqlite_requests.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def tearDown(self):
        self.sqlite_cache_requests.cache_table().clear()

    def test__init__(self):
        with self.sqlite_cache_requests as _:
            db_path = _.sqlite_requests.db_path
            assert db_path                          == self.temp_db_path
            assert file_exists  (db_path          ) is True
            assert parent_folder(db_path          ) == current_temp_folder()
            assert file_exists  (self.temp_db_path) is True
            assert _.table_name                     is None
            assert _.db_name                        is None
            assert _.sqlite_requests.db_name.startswith('db_local_')        # got random name
            assert _.sqlite_requests.table_name     == 'requests'           # assigned default table name from Sqlite__Cache__Requests
            assert _.sqlite_requests.in_memory      is False                # since db_path, this is not an in-memory db