import json
import sys
from datetime import datetime
from unittest import TestCase

import pytest

from osbot_utils.utils.Files import file_exists, file_contents
from osbot_utils.utils.Json import json_save_tmp_file, json_parse, json_loads, json_dumps, json_format, \
    json_load_file, json_load_file_and_delete, json_save_file_pretty_gz, json_load_file_gz, \
    json_round_trip, json_load_file_gz_and_delete, json_save_file_pretty, json_save_file, json_load, json_to_gz, \
    gz_to_json
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Status import send_status_to_logger, osbot_status, osbot_logger
from osbot_utils.utils.Zip import str_to_gz, gz_to_str


class test_Json(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")
        osbot_status.clear_root_logger_handlers()

    @classmethod
    def tearDownClass(self):
        osbot_status.clear_root_logger_handlers()

    def test_test_json_dumps(self):
        assert json_dumps({}       ) is None
        assert json_dumps({'a': 42}) == '{\n    "a": 42\n}'

    def test_json_dumps__bad_object(self):
        serializer       = None                             # need to set this since json_dumps uses default=str for the default json serializer
        bad_obj          = { "date": datetime.now() }
        expected_message = "TypeError: Object of type datetime is not JSON serializable"

        send_status_to_logger(True)

        assert json_dumps(bad_obj, default=serializer) is None
        # with Log_To_String(logger_json) as log_to_string:                 # todo: find another to capture these errors
        #     assert json_dumps(bad_obj, default=serializer) is None
        #     assert expected_message in log_to_string.contents()
        send_status_to_logger(False)

        with self.assertRaises(Exception) as context:
            json_dumps(bad_obj, default=serializer, raise_exception=True)
        assert context.exception.args[0] == 'Object of type datetime is not JSON serializable'

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
        send_status_to_logger(True)
        assert json_loads(bad_json) == {}
        # with Log_To_String(logger_json) as log_to_string:                          # todo: find another to capture these errors
        #     assert json_loads(bad_json) == {}
        #     assert expected_message in log_to_string.contents()
        send_status_to_logger(False)

        with self.assertRaises(Exception) as context:
            json_loads(bad_json, raise_exception=True)
        assert context.exception.args[0] == 'Expecting property name enclosed in double quotes: line 1 column 3 (char 2)'

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
        assert file_contents(json_save_file(data))        == '{"answer": 42}'
        assert file_contents(json_save_file_pretty(data)) == '{\n  "answer": 42\n}'

    def test_json_round_trip(self):
        data = {'answer': 42}
        assert json_round_trip(data) == data

    def test_json_to_gz(self):
        data    = dict(answer=42)
        gz_data = json_to_gz(data)

        assert gz_data                       == str_to_gz(json.dumps(data))
        assert gz_to_str (gz_data)           == '{"answer": 42}'
        assert gz_to_json(gz_data)           == data
        assert gz_to_str(str_to_gz('aaaaa')) == 'aaaaa'
        assert gz_to_json(json_to_gz(data))  == data
