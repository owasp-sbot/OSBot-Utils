from datetime import datetime
from unittest import TestCase

import pytest

from osbot_utils.testing.Log_To_String import Log_To_String
from osbot_utils.utils.Files import file_exists, load_file_gz, file_lines_gz, file_contents
from osbot_utils.utils.Json import json_save_tmp_file, json_parse, json_loads, json_dumps, json_format, \
    json_load_file, json_load_file_and_delete, json_save_file_gz, json_save_file_pretty_gz, json_load_file_gz, \
    json_round_trip, Json, logger_json, json_load_file_gz_and_delete, json_save_file_pretty, json_save_file, json_load
from osbot_utils.utils.Misc import list_set


class test_Json(TestCase):

    def test_dumps__bad_object(self):
        serializer       = None                             # need to set this since json_dumps uses default=str for the default json serializer
        bad_obj          = { "date": datetime.now() }
        expected_message = "TypeError: Object of type datetime is not JSON serializable"

        with Log_To_String(logger_json) as log_to_string:
            assert json_dumps(bad_obj, default=serializer) is None
            assert expected_message in log_to_string.contents()

        # confirm that we get a string in date object with default json_dumps
        round_trip = json_load(json_dumps(bad_obj))
        assert list_set(round_trip.keys())  == ['date']
        assert type(round_trip.get('date')) is str

    def test_json_parse__json_format__json_dumps__json_loads(self):
        data = {'answer': 42 }
        assert json_dumps (data) == '{\n    "answer": 42\n}'
        assert json_format(data) == '{\n    "answer": 42\n}'
        assert json_parse (json_dumps(data)) == data
        assert json_loads (json_dumps(data)) == data

        assert json_dumps (None) is None
        assert json_format(None) is None
        assert json_parse (None) == {}
        assert json_loads (None) == {}

    def test_json_loads__bad_json(self):
        bad_json         = "{ bad : json }"
        expected_message = 'json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)\n'
        with Log_To_String(logger_json) as log_to_string:
            assert json_loads(bad_json) == {}
            assert expected_message in log_to_string.contents()

    def test_json_load_file__json_save_tmp_file(self):
        data = {'answer': 42 }
        json_file = json_save_tmp_file(data)
        assert file_exists(json_file)
        assert json_load_file(json_file) == data
        assert file_exists(json_file)

    def test_json_load_file_and_delete(self):
        data = {'answer': 42 }
        json_file = json_save_tmp_file(data)
        assert file_exists(json_file) is True
        assert json_load_file_and_delete(json_file) == data
        assert file_exists(json_file) is False

    def test_json_load_file_gz__json_save_file_pretty_gz(self):
        data = {'answer': 42}
        gz_file = json_save_file_pretty_gz(data)
        assert json_load_file_gz(gz_file) == data
        assert file_exists(gz_file) is True
        assert json_load_file_gz_and_delete(gz_file) == data
        assert file_exists(gz_file) is False

    def test_save_file_pretty(self):
        data = {'answer': 42}
        print()
        assert file_contents(json_save_file(data))        == '{"answer": 42}'
        assert file_contents(json_save_file_pretty(data)) == '{\n  "answer": 42\n}'

    def test_json_round_trip(self):
        data = {'answer': 42}
        assert json_round_trip(data) == data
