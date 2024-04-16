from datetime import datetime
from unittest import TestCase
from osbot_utils.utils.Files import file_exists, file_contents, file_contents_gz
from osbot_utils.utils.Json import json_dump
from osbot_utils.utils.Json_Cache import Json_Cache


class test_Json_Cache(TestCase):
    def setUp(self) -> None:
        pass

    def test_path_cache(self):
        test_data = {"answer": 42}
        with Json_Cache() as _:
            path_cache_file = _.path_cache_file()
            assert _.path_cache_folder() == '/tmp/json_cache/__cache'
            assert _.path_cache_file()   == '/tmp/json_cache/__cache/--__cache.json.gz'
            assert _.exists()            is False
            assert _.save  (test_data)   == _.path_cache_file()
            assert _.data  ()            == test_data
            try:
                file_contents(path_cache_file)
            except UnicodeDecodeError as error:
                assert str(error) == "'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte"
            assert file_contents_gz(path_cache_file) == json_dump(test_data, pretty=False)
            assert _.exists()          is True
            assert _.delete()          is True
            assert _.exists()          is False

    def test_path_cache__no_gz(self):
        test_data = {"answer": 42}
        with Json_Cache() as _:
            _.save_as_gz = False
            path_cache_file = _.path_cache_file()
            assert _.path_cache_folder() == '/tmp/json_cache/__cache'
            assert _.path_cache_file()   == '/tmp/json_cache/__cache/--__cache.json'
            assert _.exists() is False
            assert _.save    (test_data) == path_cache_file
            assert _.data  ()           == test_data
            assert file_contents(path_cache_file) == json_dump(test_data, pretty=False)
            assert _.exists()          is True
            assert _.delete()          is True
            assert _.exists()          is False

    def test_path_cache__with_cache_type(self):
        with Json_Cache(cache_type='abc') as _:
            assert _.path_cache_folder() == '/tmp/json_cache/abc'
            assert _.path_cache_file() == '/tmp/json_cache/abc/--abc.json.gz'

    def test_path_cache__with_cache_type_and_cache_keys(self):
        date_time_from = datetime(2023, 2, 8, 11, 00, 0)
        cache_keys = date_time_from
        with Json_Cache(cache_type='abc', cache_keys=cache_keys) as _:
            assert _.path_cache_folder() == '/tmp/json_cache/abc'
            assert _.path_cache_file()   == '/tmp/json_cache/abc/--2023-02-08_11_00_00.json.gz'

        date_time_to = datetime(2023, 2, 8, 11, 00, 0)
        cache_keys = [date_time_from, date_time_to]
        with Json_Cache(cache_type='abc', cache_keys=cache_keys) as _:
            assert _.path_cache_folder() == '/tmp/json_cache/abc'
            assert _.path_cache_file()   == '/tmp/json_cache/abc/--2023-02-08_11_00_00--2023-02-08_11_00_00.json.gz'
            _.save({'answer': 42})
            assert _.delete() is True

        with Json_Cache(cache_keys=[12, "abc"]) as _:
            assert _.path_cache_folder() == '/tmp/json_cache/__cache'
            assert _.path_cache_file()   == '/tmp/json_cache/__cache/--12--abc.json.gz'
            _.save({'answer': 42})
            assert _.delete() is True

        with Json_Cache(cache_keys=[{}, {'answer': 42}]) as _:
            assert _.path_cache_folder() == '/tmp/json_cache/__cache'
            assert _.path_cache_file()   == '/tmp/json_cache/__cache/--__--__answer___42_.json.gz'
            _.save({'answer': 42})
            assert _.delete() is True
