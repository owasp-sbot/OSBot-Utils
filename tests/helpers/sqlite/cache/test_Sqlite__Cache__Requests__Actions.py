from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests import Sqlite__Cache__Requests
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Actions import Sqlite__Cache__Requests__Actions
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row import Sqlite__Cache__Requests__Row
from osbot_utils.utils.Files import temp_file, file_not_exists
from osbot_utils.utils.Json import json_dumps


class test_Sqlite__Cache__Requests__Actions(TestCase):
    sqlite_cache_requests: Sqlite__Cache__Requests
    temp_db_path: str       # todo: refactor to use in memory db

    @classmethod
    def setUpClass(cls):
        cls.temp_db_path = temp_file(extension='sqlite')
        cls.sqlite_cache_requests = Sqlite__Cache__Requests(db_path=cls.temp_db_path)  # the db_path to the tmp file path
        cls.sqlite_cache_requests.set__add_timestamp(False)                                                 # disabling timestamp since it complicates the test data verification below

    @classmethod
    def tearDownClass(cls):
        cls.sqlite_cache_requests.sqlite_requests.delete()
        assert file_not_exists(cls.temp_db_path) is True

    def setUp(self):
        self.cache_request_actions = Sqlite__Cache__Requests__Actions()

