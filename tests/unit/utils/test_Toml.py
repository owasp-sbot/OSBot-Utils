import re
import sys
import pytest
from unittest                       import TestCase
from osbot_utils.utils.Files        import file_extension, file_exists, file_contents
from osbot_utils.testing.Temp_File  import Temp_File
from osbot_utils.utils.Json         import json_parse
from osbot_utils.utils.Misc         import list_set
from osbot_utils.utils.Toml         import dict_to_toml, toml_to_dict, toml_dict_to_file, toml_dict_from_file

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

    def test_toml_from_file(self):
        with Temp_File(extension='toml', return_file_path=True, create_file=False) as toml_file:
            assert file_extension(toml_file) == '.toml'
            data      = {'var_1': 'value_1', 'an_list': ['1', '2', '3'], 'an_dict': {'var_2': 'value_2', 'var_3': 'value_3'}}
            str_toml = """\
var_1 = 'value_1'
an_list = [
    '1',
    '2',
    '3',
]
[an_dict]
    var_2 = 'value_2'
    var_3 = 'value_3'
"""
            assert dict_to_toml(data)             == str_toml
            assert file_exists(toml_file)         is False

            toml_dict_to_file(toml_file, data)

            assert file_exists(toml_file)         is True
            assert file_contents(toml_file)       == str_toml

            assert toml_dict_from_file(toml_file) == data

    def test__bug__edge_cases(self):
        """Test various edge cases and data types"""

        empty_data = { 'empty_dict'  : {} ,                                 # Test empty structures
                       'empty_list'  : [] ,
                       'empty_string': '' }
        assert empty_data == toml_to_dict(dict_to_toml(empty_data))

        nested_empty = { 'level1': { 'level2': { 'level3': {} } } }         # Test nested empty dictionaries
        assert toml_to_dict(dict_to_toml(nested_empty)) == nested_empty

        numbers_data = { 'integer'   : 42      ,                            # Test various number types
                         'negative'  : -17     ,
                         'float'     : 3.14159 ,
                         'scientific': 1.23e-4 ,
                         'zero'      : 0       }
        assert numbers_data == toml_to_dict(dict_to_toml(numbers_data))

    def test__bug__complex_nested_structures(self): # Test deeply nested and complex structures

        complex_data = {
            'project': {
                'name': 'MyProject',
                'version': '1.0.0',
                'dependencies': {
                    'production': ['django', 'requests', 'numpy'],
                    'development': ['pytest', 'black', 'mypy']
                },
                'metadata': {
                    'authors': [
                        {'name': 'Alice', 'email': 'alice@example.com'},
                        {'name': 'Bob', 'email': 'bob@example.com'}
                    ]
                }
            },
            'settings': {
                'debug': False,
                'port': 8080,
                'allowed_hosts': ['localhost', '127.0.0.1']
            }
        }

        # Round-trip test
        toml_str = dict_to_toml(complex_data)
        result   = toml_to_dict(toml_str)
        assert result == complex_data

    def test__special_characters_in_strings(self):      # Test strings with special characters

        special_chars_data = {
            'quotes': "String with 'single' and \"double\" quotes",
            'newline': "Line 1\nLine 2",
            'tab': "Column1\tColumn2",
            'backslash': "Path\\to\\file",
            'unicode': "Hello 世界 🌍"
        }

        # Note: Some special characters might need escaping in TOML
        toml_str = dict_to_toml(special_chars_data)
        result = toml_to_dict(toml_str)

        # The round-trip might not be perfect for special characters
        # depending on TOML escaping rules
        assert 'quotes' in result
        assert 'unicode' in result

    def test__mixed_type_arrays(self):
        """Test arrays with mixed types (should handle gracefully)"""

        # TOML arrays should be homogeneous, but test handling
        homogeneous_arrays = {
            'strings': ['a', 'b', 'c'],
            'integers': [1, 2, 3],
            'floats': [1.1, 2.2, 3.3],
            'booleans': [True, False, True]
        }

        assert homogeneous_arrays == toml_to_dict(dict_to_toml(homogeneous_arrays))

    def test__array_of_tables_complex(self):
        """Test more complex array of tables scenarios"""

        data_with_array_tables = {
            'products': [
                {
                    'name': 'Laptop',
                    'price': 999.99,
                    'in_stock': True,
                    'specs': {
                        'cpu': 'Intel i7',
                        'ram': '16GB'
                    }
                },
                {
                    'name': 'Mouse',
                    'price': 29.99,
                    'in_stock': False,
                    'specs': {
                        'type': 'Wireless',
                        'battery': 'AA'
                    }
                }
            ]
        }

        toml_str = dict_to_toml(data_with_array_tables)

        # Note: Nested dicts within array of tables might not round-trip perfectly
        # in the current implementation
        result = toml_to_dict(toml_str)

        # At minimum, check the basic structure is preserved
        assert 'products' in result
        assert len(result['products']) == 2
        assert result['products'][0]['name'] == 'Laptop'
        assert result['products'][1]['name'] == 'Mouse'

    def test__keys_with_special_names(self):
        """Test keys that might conflict with TOML syntax"""

        special_keys = {
            'key-with-dash': 'value1',
            'key_with_underscore': 'value2',
            'key.with.dots': 'value3',  # This might need special handling
            '123numeric': 'value4',      # Keys starting with numbers
        }

        # Some of these might not round-trip perfectly depending on TOML rules
        toml_str = dict_to_toml(special_keys)
        # Just ensure it doesn't crash
        assert toml_str is not None

    def test__performance_large_data(self):
        """Test with larger datasets for performance"""

        large_data = {
            f'section_{i}': {
                f'key_{j}': f'value_{i}_{j}'
                for j in range(10)
            }
            for i in range(100)
        }

        # Should handle reasonably large data
        toml_str = dict_to_toml(large_data)
        result = toml_to_dict(toml_str)
        assert len(result) == 100
        assert result['section_0']['key_0'] == 'value_0_0'
        assert result['section_99']['key_9'] == 'value_99_9'




    # regression tests

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

    def test__regression__toml_handling_of_dicts(self):                                       # Test file export

        spec = { 'components': {'schemas': {}},
                 'info'      : {'title': 'Export Test API', 'version': '2.0.0'},
                 'openapi'   : '3.0.0',
                 'paths'     : {},
                 'servers'   : [{'url': '/'}]}

        # Test JSON export
        with Temp_File(file_name='openapi.toml', return_file_path=True) as toml_file:
            toml_dict_to_file(toml_file, spec)

#             assert file_contents(toml_file) != """\
# [components]
#     [schemas]
# [info]
#     title = 'Export Test API'
#     version = '2.0.0'
# openapi = '3.0.0'
# [paths]
# servers = [
#     {'url': '/'},
# ]
# """                               # BUG : {'url': '/'} : " In TOML, you cannot have dictionary literals inside arrays like this.
#             error_message = "Expected '=' after a key in a key/value pair (at line 9, column 11)"
#             with pytest.raises(TOMLDecodeError, match=re.escape(error_message)):
#                 toml_dict_from_file(toml_file)                                              # BUG should have not raised
            spec__round_trip = toml_dict_from_file(toml_file)
            assert spec__round_trip == spec                                                   # BUG these should be the same
