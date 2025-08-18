import re
import sys
import pytest
from unittest                                        import TestCase
from osbot_utils.utils.Files                         import file_contents, file_exists
from osbot_utils.testing.Temp_File                   import Temp_File
from osbot_utils.utils.Toml                          import Dict__To__Toml, toml_to_dict, toml_dict_to_file

if sys.version_info >= (3, 11):
    from tomllib import TOMLDecodeError


class test_Dict__To__Toml(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 11):
            pytest.skip("TOML parsing is not supported in Python versions earlier than 3.11")

    def setUp(self):                                                                  # Initialize test instance
        self.converter = Dict__To__Toml()

    # Basic functionality tests

    def test__init(self):                                                            # Test basic initialization
        assert type(self.converter)      is Dict__To__Toml

    def test__convert__empty_dict(self):                                            # Test empty dictionary
        result = self.converter.convert({})
        assert result == ""

    def test__convert__simple_values(self):                                         # Test basic value types
        data = {
            'string_val'  : 'hello world'  ,
            'int_val'     : 42             ,
            'float_val'   : 3.14           ,
            'bool_true'   : True           ,
            'bool_false'  : False
        }

        result = self.converter.convert(data)

        assert "string_val = 'hello world'\n"  in result
        assert "int_val = 42\n"                in result
        assert "float_val = 3.14\n"            in result
        assert "bool_true = true\n"            in result
        assert "bool_false = false\n"          in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__none_values(self):                                           # Test None value handling
        data = {
            'explicit_none' : None         ,
            'string_val'    : 'not none'
        }

        result = self.converter.convert(data)

        assert "explicit_none" not in result                                        # None values should be skipped
        assert "string_val = 'not none'\n" in result

    # Array/List tests

    def test__convert__empty_arrays(self):                                          # Test empty collections
        data = {
            'empty_list'  : []   ,
            'empty_tuple' : ()   ,
            'empty_set'   : set()
        }

        result = self.converter.convert(data)

        assert "empty_list = []\n"  in result
        assert "empty_tuple = []\n" in result
        assert "empty_set = []\n"   in result

    def test__convert__simple_arrays(self):                                         # Test arrays of simple types
        data = {
            'strings'  : ['a', 'b', 'c']      ,
            'integers' : [1, 2, 3]            ,
            'floats'   : [1.1, 2.2, 3.3]      ,
            'booleans' : [True, False, True]  ,
            'mixed'    : ['text', 42, 3.14]
        }

        result = self.converter.convert(data)

        # Check strings array
        assert "strings = [\n    'a',\n    'b',\n    'c',\n]\n" in result

        # Check integers array
        assert "integers = [\n    1,\n    2,\n    3,\n]\n" in result

        # Check booleans array
        assert "booleans = [\n    true,\n    false,\n    true,\n]\n" in result

        # Verify round-trip (sets become lists)
        parsed = toml_to_dict(result)
        assert parsed['strings']  == ['a', 'b', 'c']
        assert parsed['integers'] == [1, 2, 3]
        assert parsed['booleans'] == [True, False, True]

    def test__convert__tuples_and_sets(self):                                       # Test tuple and set conversion
        data = {
            'tuple_data' : (1, 2, 3)         ,
            'set_data'   : {'x', 'y', 'z'}
        }

        result = self.converter.convert(data)

        # Both should be converted to arrays
        assert "tuple_data = [\n" in result
        assert "set_data = [\n"   in result

        # Round-trip converts to lists
        parsed = toml_to_dict(result)
        assert parsed['tuple_data'] == [1, 2, 3]
        assert set(parsed['set_data']) == {'x', 'y', 'z'}                          # Order may vary for sets

    # Section/Dictionary tests

    def test__convert__simple_sections(self):                                       # Test dictionary as sections
        data = {
            'database': {
                'host'    : 'localhost' ,
                'port'    : 5432       ,
                'enabled' : True
            }
        }

        result = self.converter.convert(data)

        assert "[database]\n"                    in result
        assert "    host = 'localhost'\n"       in result
        assert "    port = 5432\n"              in result
        assert "    enabled = true\n"           in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__nested_sections(self):                                       # Test deeply nested dictionaries
        data = {
            'level1': {
                'value1': 'top',
                'level2': {
                    'value2': 'middle',
                    'level3': {
                        'value3': 'deep'
                    }
                }
            }
        }

        result = self.converter.convert(data)

        assert "[level1]\n"                     in result
        assert "    value1 = 'top'\n"          in result
        assert "[level1.level2]\n"             in result
        assert "    value2 = 'middle'\n"       in result
        assert "[level1.level2.level3]\n"      in result
        assert "    value3 = 'deep'\n"         in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__empty_nested_dicts(self):                                    # Test empty nested dictionaries
        data = {
            'level1': {
                'level2': {
                    'level3': {}
                }
            }
        }

        result = self.converter.convert(data)

        assert "[level1]\n"               in result
        assert "[level1.level2]\n"        in result
        assert "[level1.level2.level3]\n" in result

        # Verify round-trip preserves structure
        parsed = toml_to_dict(result)
        assert parsed == {'level1': {'level2': {'level3': {}}}}

    # Array of tables tests

    def test__convert__array_of_tables(self):                                       # Test array of dictionaries
        data = {
            'servers': [
                {'name': 'server1', 'ip': '10.0.0.1'},
                {'name': 'server2', 'ip': '10.0.0.2'}
            ]
        }

        result = self.converter.convert(data)

        assert "[[servers]]\n"           in result
        assert "    name = 'server1'\n" in result
        assert "    ip = '10.0.0.1'\n"  in result
        assert "    name = 'server2'\n" in result
        assert "    ip = '10.0.0.2'\n"  in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__array_of_tables_with_nested_dicts(self):                     # Test complex array of tables
        data = {
            'products': [
                {
                    'name'  : 'Laptop'  ,
                    'price' : 999.99    ,
                    'specs' : {
                        'cpu' : 'Intel i7' ,
                        'ram' : '16GB'
                    }
                },
                {
                    'name'  : 'Mouse'    ,
                    'price' : 29.99      ,
                    'specs' : {
                        'type'    : 'Wireless' ,
                        'battery' : 'AA'
                    }
                }
            ]
        }

        result = self.converter.convert(data)

        assert "[[products]]\n"                in result
        assert "    name = 'Laptop'\n"        in result
        assert "    price = 999.99\n"         in result
        assert "[products.specs]\n"           in result
        assert "    cpu = 'Intel i7'\n"       in result
        assert "    ram = '16GB'\n"           in result
        assert "    name = 'Mouse'\n"         in result
        assert "    type = 'Wireless'\n"      in result


        # Verify round-trip
        assert toml_to_dict(result) == data

    # Complex integration tests

    def test__convert__mixed_structure(self):                                       # Test complex mixed structure
        data = {
            'title'    : 'TOML Example'      ,
            'owner'    : {
                'name' : 'John Doe'          ,
                'dob'  : '1990-01-01'
            },
            'database' : {
                'server'         : '192.168.1.1'    ,
                'ports'          : [8001, 8002]     ,
                'connection_max' : 5000             ,
                'enabled'        : True
            }
        }

        result = self.converter.convert(data)

        assert "title = 'TOML Example'\n"       in result
        assert "[owner]\n"                      in result
        assert "    name = 'John Doe'\n"       in result
        assert "[database]\n"                   in result
        assert "    server = '192.168.1.1'\n"  in result
        assert "    connection_max = 5000\n"   in result
        assert "    enabled = true\n"          in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__openapi_spec(self):                                          # Test OpenAPI spec structure
        spec = {
            'openapi'   : '3.0.0'                                    ,
            'info'      : {
                'title'   : 'Test API'   ,
                'version' : '1.0.0'
            },
            'paths'     : {}                                         ,
            'components': {'schemas': {}}                            ,
            'servers'   : [{'url': '/'}]
        }

        result = self.converter.convert(spec)

        assert "openapi = '3.0.0'\n"       in result
        assert "[info]\n"                  in result
        assert "    title = 'Test API'\n"  in result
        assert "[paths]\n"                 in result
        assert "[components]\n"            in result
        assert "[components.schemas]\n"    in result
        assert "[[servers]]\n"             in result
        assert "    url = '/'\n"           in result

        # Verify round-trip
        assert toml_to_dict(result) == spec

    # Special character tests

    def test__convert__special_characters(self):                                    # Test special character handling
        data_1 = { 'backslash' : "Path\\to\\file"               ,
                   'newline'   : "Line 1\nLine 2"               ,
                   'tab'       : "Column1\tColumn2"             ,
                   'unicode'   : "Hello 世界 🌍"                ,
                   'quotes'    : "String with 'single' quotes"  }

        result_1 = self.converter.convert(data_1)
        # Verify round-trip
        assert toml_to_dict(result_1) == data_1

        # Edge cases

    def test__convert__numeric_edge_cases(self):                                    # Test numeric edge cases
        data = {
            'zero'       : 0         ,
            'negative'   : -42       ,
            'large_int'  : 999999999 ,
            'tiny_float' : 0.0001    ,
            'scientific' : 1.23e-4
        }

        result = self.converter.convert(data)

        assert "zero = 0\n"              in result
        assert "negative = -42\n"        in result
        assert "large_int = 999999999\n" in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    def test__convert__deep_nesting(self):                                          # Test very deep nesting
        data = {
            'l1': {
                'l2': {
                    'l3': {
                        'l4': {
                            'l5': {
                                'deep_value': 'bottom'
                            }
                        }
                    }
                }
            }
        }

        result = self.converter.convert(data)

        assert "[l1.l2.l3.l4.l5]\n"          in result
        assert "    deep_value = 'bottom'\n" in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    # Performance test

    def test__convert__large_dataset(self):                                         # Test with large dataset
        data = {
            f'section_{i}': {
                f'key_{j}': f'value_{i}_{j}'
                for j in range(10)
            }
            for i in range(100)
        }

        result = self.converter.convert(data)

        assert '[section_0]'   in result
        assert '[section_99]'  in result
        assert "key_0 = 'value_0_0'" in result
        assert "key_9 = 'value_99_9'" in result

        # Verify round-trip
        assert toml_to_dict(result) == data

    # Integration with file operations

    def test__integration_with_file_operations(self):                               # Test file write integration
        data = {
            'config': {
                'debug'   : True      ,
                'timeout' : 30        ,
                'servers' : ['a', 'b']
            }
        }

        with Temp_File(extension='toml', return_file_path=True) as toml_file:
            toml_str = Dict__To__Toml().convert(data)
            toml_dict_to_file(toml_file, data)

            assert file_exists(toml_file)    is True
            assert file_contents(toml_file)  == toml_str

            # Verify round-trip through file
            loaded = toml_to_dict(file_contents(toml_file))
            assert loaded == data

    # Method-specific tests

    def test___process_simple_values(self):                                         # Test _process_simple_values method
        data = {
            'str_val'   : 'test'  ,
            'int_val'   : 42      ,
            'bool_val'  : True    ,
            'none_val'  : None    ,
            'dict_val'  : {}      ,
            'list_val'  : []
        }

        result = self.converter._process_simple_values(data, indent_level=0)

        assert "str_val = 'test'\n"  in result
        assert "int_val = 42\n"      in result
        assert "bool_val = true\n"   in result
        assert "none_val"            not in result                                  # None skipped
        assert "dict_val"            not in result                                  # Dict skipped
        assert "list_val"            not in result                                  # List skipped

    def test___process_simple_arrays(self):                                         # Test _process_simple_arrays method
        data = {
            'empty'      : []                ,
            'strings'    : ['a', 'b']        ,
            'with_dict'  : [{'a': 1}]        ,
            'not_array'  : 'string'
        }

        result = self.converter._process_simple_arrays(data, indent_level=0)

        assert "empty = []\n"        in result
        assert "strings = [\n"       in result
        assert "    'a',\n"          in result
        assert "with_dict"           not in result                                  # Has dict, skipped
        assert "not_array"           not in result                                  # Not array, skipped

    def test___process_sections(self):                                              # Test _process_sections method
        data = {
            'section1' : {'key': 'value'}   ,
            'simple'   : 'not_dict'
        }

        result = self.converter._process_sections(data, parent_key="")

        assert "[section1]\n"        in result
        assert "key = 'value'\n"     in result
        assert "simple"              not in result                                  # Not dict, skipped

    def test___process_array_of_tables(self):                                       # Test _process_array_of_tables method
        data = {
            'items'     : [{'id': 1}, {'id': 2}]  ,
            'not_array' : {'id': 3}               ,
            'simple'    : [1, 2, 3]
        }

        result = self.converter._process_array_of_tables(data, parent_key="")

        assert "[[items]]\n"         in result
        assert "    id = 1\n"        in result
        assert "    id = 2\n"        in result
        assert "not_array"           not in result                                  # Not array, skipped
        assert "simple"              not in result                                  # No dicts, skipped