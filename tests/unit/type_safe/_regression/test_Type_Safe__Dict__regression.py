from unittest import TestCase

import pytest
from typing import Dict, Type, Set
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__Dict__regression(TestCase):

    def test__regression__type_keys_in_json(self):

        class Bug_Type_Keys:                                                       # Simple class for testing
            pass

        class Another_Type:                                                        # Another class for testing
            pass


        # Create a Type_Safe_Dict with Type objects as keys
        type_dict                = Type_Safe__Dict(Type, Set[str])
        type_dict[Bug_Type_Keys] = {'value1', 'value2'}
        type_dict[Another_Type]  = {'value3', 'value4'}

        # Get JSON representation
        json_data = type_dict.json()
        assert json_data == { 'test_Type_Safe__Dict__regression.Another_Type' : {'value4', 'value3'},
                              'test_Type_Safe__Dict__regression.Bug_Type_Keys': {'value2', 'value1'}}     # FIXED

        # # The bug is that the keys in json_data are still Type objects
        # # This assertion passes when the bug is present
        # self.assertTrue(any(isinstance(key, type) for key in json_data.keys()),"Bug confirmed: Type objects are not being converted to strings in JSON output" )
        #
        # # Additional verification that shows the problematic output
        # type_keys = [key for key in json_data.keys() if isinstance(key, type)]
        # self.assertGreater(len(type_keys),0,"Should find Type objects as keys in JSON output, confirming the bug")

    def test__regression__in_schema_context(self):

        class Bug_Type_Keys:                                                       # Simple class for testing
            pass


        class Schema_With_Type_Dict(Type_Safe):                                    # Schema that uses Dict[Type, Set[str]]
            values: Dict[Type, Set[str]]

        schema                       = Schema_With_Type_Dict()                      # Demonstrate the bug in the context of a schema
        schema.values[Bug_Type_Keys] = set()
        schema.values[Bug_Type_Keys].add('test1')
        schema.values[Bug_Type_Keys].add('test2')

        assert type(schema.values) is Type_Safe__Dict
        json_data = schema.json()                                                   # Get JSON representation

        #assert json_data == { 'values': { test_Type_Safe__Dict__bugs.Bug_Type_Keys: ['test1', 'test2']}}       # BUG should not be using type
        bug_type_keys = json_data.get('values').get('test_Type_Safe__Dict__regression.Bug_Type_Keys')
        assert type(bug_type_keys) is list
        assert 'test1' in bug_type_keys
        assert 'test2' in bug_type_keys
        #assert type(json_data.values['test_Type_Safe__Dict__bugs.Bug_Type_Keys']) is set
        # Verify the bug exists in schema context
        self.assertFalse(any(isinstance(key, type) for key in json_data['values'].keys()), "Bug confirmed: Type objects remain as Type objects in schema JSON output")

    def test__regression__json_not_supported(self):
        class An_Class(Type_Safe):
            an_dict: Dict[str, int]

        an_class = An_Class()
        an_class.an_dict['key'] = 42

        assert an_class.json() == {'an_dict': {'key': 42}}
        # with pytest.raises(AttributeError, match = "Type_Safe__Dict' object has no attribute 'json'"):
        #     assert an_class.an_dict.json() ==  {'key': 42}          # BUG - this should work
        assert an_class.an_dict.json() ==  {'key': 42}

    def test__regression__nested_types__not_supported__in_dict(self):       # Similar to the list test that uses forward references in nested structures
        class An_Class(Type_Safe):
            an_str: str
            an_dict: Dict[str, 'An_Class']

        an_class = An_Class()
        an_class.an_str = "top-level"
        assert type(an_class.an_dict) is Type_Safe__Dict
        assert an_class.an_dict == {}

        # Valid usage
        an_child = An_Class()
        an_child.an_str = "child"
        an_class.an_dict['child'] = an_child

        # Invalid usage
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'str'"):
            an_class.an_dict['bad_child'] = "some string"                               # Fixed: BUG didn't raise an exception