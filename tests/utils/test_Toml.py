import sys
import pytest
from unittest               import TestCase
from osbot_utils.utils.Json import json_parse
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Toml import dict_to_toml, toml_to_dict

if sys.version_info >= (3, 11):
    from tomllib import TOMLDecodeError


class test_Toml(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 11):
            pytest.skip("TOML parsing is not supported in Python versions earlier than 3.11")

    def test_dict_to_toml(self):
        data = {
            "title": "TOML Example",
            "owner": {
                "name": "Aaaaa Baaaa",
                "dob": "1111-05-12"
            },
            "database": {
                "server": "192.168.1.1",
                "ports": [8001, 8001, 8002],
                "connection_max": 5000,
                "enabled": True
            }
        }

        expected_output = """title = 'TOML Example'
[owner]
    name = 'Aaaaa Baaaa'
    dob = '1111-05-12'
[database]
    server = '192.168.1.1'
    ports = [
        8001,
        8001,
        8002,
    ]
    connection_max = 5000
    enabled = true
"""

        toml_string = dict_to_toml(data)

        assert toml_string == expected_output
        assert data        == toml_to_dict(toml_string)

    def test_toml_to_dict(self):
        toml_string = """title = 'TOML Example'
[owner]
    name = 'Aaaaa Baaaa'
    dob = '1111-05-12'
[database]
    server = '192.168.1.1'
    ports = [
        8001,
        8001,
        8002,
    ]
    connection_max = 5000
    enabled = true
"""

        expected_dict = {
            "title": "TOML Example",
            "owner": {
                "name": "Aaaaa Baaaa",
                "dob": "1111-05-12"
            },
            "database": {
                "server": "192.168.1.1",
                "ports": [8001, 8001, 8002],
                "connection_max": 5000,
                "enabled": True
            }
        }

        result_dict = toml_to_dict(toml_string)

        assert result_dict == expected_dict, f"Expected:\n{expected_dict}\n\nGot:\n{result_dict}"
        assert toml_string == dict_to_toml(result_dict)

    def test__regression__toml_to_dict__parse_issue(self):
        # this will still raise the issue since the problem is that the json_with_toml_data is malformed (at the time dict_to_toml didn't support set and dict)
        # see test__regression__replicate_tuple_issue
        json_with_toml_data = """"args = (\\"echo 'hello world'\\",)\\n[kwargs]\\nssh_host = '18.203.153.185'\\n\""""
        toml_data           = json_parse(json_with_toml_data)
        assert toml_data    == 'args = ("echo \'hello world\'",)\n[kwargs]\nssh_host = \'18.203.153.185\'\n'

        with self.assertRaises(TOMLDecodeError) as context:
            toml_to_dict(toml_data)

        assert context.exception.args == ('Invalid value (at line 1, column 8)',)

    def test__regression__replicate_tuple_issue(self):
        dict_ok = {'an_str'  : 'str',
                   'an_int'  : 42   ,
                   'an_list' : ['a', 'b', 'c'] ,
                   'an_dict' : { "answer": 42 } }

        assert dict_ok == toml_to_dict(dict_to_toml(dict_ok))

        dict_with_tuple           = {'an_tuple': (1,2,3) }
        # with self.assertRaises(TOMLDecodeError) as context:                               # FIXED: BUG this was failing noe
        #     toml_to_dict(dict_to_toml(dict_with_tuple))
        # assert context.exception.args == ('Invalid value (at line 1, column 12)',)

        dict_with_tuple__roundtrip = {'an_tuple': [1, 2, 3]}                                # FIXED: with fix now the tuple becomes a list
        assert dict_with_tuple__roundtrip == toml_to_dict(dict_to_toml(dict_with_tuple))

        an_set = set()
        an_set.add('a')
        an_set.add('b')
        dict_with_set = {'an_set': an_set }
        # with self.assertRaises(TOMLDecodeError) as context:                               # FIXED: BUG this was failing noe
        #     toml_to_dict(dict_to_toml(dict_with_set))
        # assert context.exception.args == ("Expected '=' after a key in a key/value pair (at line 1, column 14)",)

        expected_dict_with_set__roundtrip = {'an_set': ['a', 'b'] }                                  # FIXED: with fix now the tuple becomes a list
        dict_with_set__roundtrip          = toml_to_dict(dict_to_toml(dict_with_set))
        assert list_set(dict_with_set__roundtrip)== list_set(expected_dict_with_set__roundtrip)
        assert list_set(dict_with_set__roundtrip.get('an_set')) == list_set(expected_dict_with_set__roundtrip.get('an_set'))
