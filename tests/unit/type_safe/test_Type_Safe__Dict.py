import re
import sys
import pytest
from unittest                              import TestCase
from typing                                import Dict, Union, Optional, Any, Callable, List, Tuple
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__Dict(TestCase):

    def test_from_json_with_nested_containers(self):
        from osbot_utils.helpers.Obj_Id import Obj_Id
        from osbot_utils.type_safe.Type_Safe import Type_Safe
        from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict
        from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
        from typing import Dict, List
        import pytest

        # Define a hierarchy of nested classes
        class SimpleValue(Type_Safe):
            value: str
            tag: str = "simple"

        class NestedItem(Type_Safe):
            name: str
            values: List[SimpleValue]
            metadata: Dict[str, str]

        class ComplexContainer(Type_Safe):
            title       : str
            items       : Dict[str, NestedItem]
            tags        : List[str]
            reference_id: Obj_Id

        # Create test data as a nested JSON structure
        reference_id = Obj_Id()
        test_json = {
            "title": "Test Container",
            "items": {
                "item1": {
                    "name": "First Item",
                    "values": [
                        {"value": "value1", "tag": "custom1"},
                        {"value": "value2", 'tag': 'simple' }
                    ],
                    "metadata": {
                        "creator": "test",
                        "version": "1.0"
                    }
                },
                "item2": {
                    "name": "Second Item",
                    "values": [
                        {"value": "value3", "tag": "custom2"}
                    ],
                    "metadata": {
                        "creator": "test",
                        "version": "2.0"
                    }
                }
            },
            "tags": ["important", "test"],
            "reference_id": reference_id
        }

        # Test deserialization with from_json
        assert ComplexContainer.from_json(test_json).json() == test_json
        container = ComplexContainer.from_json(test_json)

        assert type(container             ) is ComplexContainer
        assert type(container.title       ) is str
        assert type(container.items       ) is Type_Safe__Dict
        assert type(container.tags        ) is Type_Safe__List
        assert type(container.reference_id) is Obj_Id

        # Verify the structure and types
        assert container.title == "Test Container"
        assert isinstance(container.items, Type_Safe__Dict)
        assert len(container.items) == 2

        # Check first item
        item1 = container.items["item1"]
        assert isinstance(item1, NestedItem)
        assert item1.name == "First Item"

        # Check item1's values
        assert isinstance(item1.values, Type_Safe__List)
        assert len(item1.values) == 2
        assert isinstance(item1.values[0], SimpleValue)
        assert item1.values[0].value == "value1"
        assert item1.values[0].tag == "custom1"
        assert item1.values[1].value == "value2"
        assert item1.values[1].tag == "simple"  # Default value

        # Check item1's metadata
        assert isinstance(item1.metadata, Type_Safe__Dict)
        assert item1.metadata["creator"] == "test"
        assert item1.metadata["version"] == "1.0"

        # Check second item
        item2 = container.items["item2"]
        assert isinstance(item2, NestedItem)
        assert item2.name == "Second Item"
        assert len(item2.values) == 1
        assert item2.values[0].value == "value3"

        # Check top-level properties
        assert isinstance(container.tags, Type_Safe__List)
        assert container.tags[0] == "important"
        assert container.tags[1] == "test"
        assert isinstance(container.reference_id, Obj_Id)
        assert str(container.reference_id) == reference_id

        # Test serialization back to JSON
        output_json = container.json()

        # The output should match the input (with possibly some modifications due to type conversions)
        assert output_json["title"] == test_json["title"]
        assert output_json["items"]["item1"]["name"] == test_json["items"]["item1"]["name"]
        assert output_json["items"]["item1"]["values"][0]["value"] == test_json["items"]["item1"]["values"][0]["value"]
        assert output_json["tags"] == test_json["tags"]
        assert output_json["reference_id"] == test_json["reference_id"]

        # Test full round-trip equality (if your serialization is designed to be perfectly round-trip compatible)
        # This might not pass if serialization adds or modifies fields
        container2 = ComplexContainer.from_json(output_json)
        assert container2.json() == output_json

    def test__dict_from_json__enforces_type_safety(self):
        class An_Class__Item(Type_Safe):
            an_str: str

        class An_Class(Type_Safe):
            items: Dict[str, An_Class__Item]

        json_data = {'items': {'a': {'an_str': 'abc'}}}

        an_class = An_Class.from_json(json_data)
        assert type(an_class.items     )  is Type_Safe__Dict
        assert type(an_class.items['a'])  is An_Class__Item
        assert an_class.items['a'].an_str == 'abc'

    def test__dict_with_simple_types(self):                                 # Similar to the Type_Safe__List test, but for dictionaries.
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")

        class An_Class(Type_Safe):
            an_dict_any: dict
            an_dict_str_int: dict[str, int]                                 # Python 3.9+ or 3.10+ style
            an_dict_int_str: Dict[int, str]                                 # Classic typing style

        an_class = An_Class()
        assert type(an_class.an_dict_any)     is dict
        assert type(an_class.an_dict_str_int) is Type_Safe__Dict
        assert type(an_class.an_dict_int_str) is Type_Safe__Dict

        assert an_class.an_dict_any     == {}
        assert an_class.an_dict_str_int == {}
        assert an_class.an_dict_int_str == {}

        an_class.an_dict_any    ['key'    ] = 'value'
        an_class.an_dict_any    [1        ] = 'one'
        an_class.an_dict_str_int['one'    ] = 1
        an_class.an_dict_int_str[1        ] = 'one'

        assert an_class.json() == { 'an_dict_any'    : {1    : 'one', 'key': 'value'},
                                    'an_dict_int_str': {1    : 'one'                },
                                    'an_dict_str_int': {'one': 1                    }}


        an_class.an_dict_str_int['one'] = 1                                         # Test an_dict_str_int -> Dict[str, int]
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.an_dict_str_int['two'] = '2'

        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_dict_str_int[3] = 3  # key must be str

        an_class.an_dict_int_str[1] = 'one'                                         # Test an_dict_int_str -> Dict[int, str]
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_dict_int_str[2] = 2

        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.an_dict_int_str['3'] = 'three'

    def test__dict_with_complex_types(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")

        class An_Class(Type_Safe):
            dict_str_dict_str_int: Dict[str, Dict[str, int]]
            dict_str_list_int    : Dict[str, List[int]]
            dict_union_str_int   : Dict[Union[str, int], str]

        an_class = An_Class()

        an_class.dict_str_dict_str_int['outer'] = {'inner': 42}                     # dict_str_dict_str_int -> Dict[str, Dict[str, int]]
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.dict_str_dict_str_int['outer_fail'] = {'inner': 'bad'}

        an_class.dict_str_list_int['my_list'] = [1, 2, 3]                           # dict_str_list_int -> Dict[str, List[int]]
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.dict_str_list_int['my_list2'] = [1, 'a', 3]

        an_class.dict_union_str_int['str_key'] = 'value'                            # dict_union_str_int -> Dict[Union[str, int], str]
        an_class.dict_union_str_int[123] = 'value2'
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.dict_union_str_int[456] = 789
        with pytest.raises(TypeError, match=re.escape("Expected 'Union[str, int]', but got 'dict'")):
            an_class.dict_union_str_int[{}] = 'value'

    def test__dict_with_custom_type(self):
        class CustomType(Type_Safe):
            a: int
            b: str

        class An_Class(Type_Safe):
            an_dict_custom: Dict[str, CustomType]

        an_class = An_Class()
        an_class.an_dict_custom['ok'] = CustomType(a=1, b='abc')
        with pytest.raises(TypeError, match="Expected 'CustomType', but got 'dict'"):
            an_class.an_dict_custom['fail'] = {'a': 2, 'b': 'def'}

    def test__dict_with_empty_collections(self):                            # Check that empty dict fields can be assigned without issues.
        class An_Class(Type_Safe):
            an_dict_of_dicts: Dict[str, Dict]
            an_dict_of_lists: Dict[str, list]

        an_class = An_Class()
        assert type(an_class.an_dict_of_dicts) is Type_Safe__Dict
        assert type(an_class.an_dict_of_lists) is Type_Safe__Dict


        an_class.an_dict_of_dicts['empty'     ] = {}                        # Empty dictionary
        an_class.an_dict_of_dicts['full'      ] = {'a': 1}                  # Arbitrary dict (since no type parameters)
        an_class.an_dict_of_lists['empty_list'] = []                        # Empty list
        an_class.an_dict_of_lists['mixed_list'] = [1, 'a', {}]              # Arbitrary list

    def test__dict_with_mismatched_types(self):
        class An_Class(Type_Safe):
            an_dict_str_int: Dict[str, int]

        an_class = An_Class()
        an_class.an_dict_str_int['ok'] = 123                                        # Valid assignment

        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):       # Mismatched type for value
            an_class.an_dict_str_int['fail'] = 'abc'

        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):       # Mismatched type for key
            an_class.an_dict_str_int[123] = 123

    def test__dict_with_recursive_types(self):                                      # Check a dictionary pointing to a forward reference of itself
        class TreeNode(Type_Safe):
            value: int
            children: Optional[Dict[str, 'TreeNode']]  # forward reference

        class An_Class(Type_Safe):
            tree: TreeNode

        an_class = An_Class()
        an_class.tree = TreeNode(value=1, children=None)    # OK so far

        an_class.tree.children = Type_Safe__Dict(str, TreeNode)                         # Insert a valid child node
        an_class.tree.children['child1'] = TreeNode(value=2, children=None)

        # Invalid child node (type mismatch)
        with pytest.raises(TypeError, match="Expected 'TreeNode', but got 'int'"):
            an_class.tree.children['child2'] = 42

    def test__dict_with_multiple_generics(self):                                    # Check nested generics in dict keys or values.
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")

        class An_Class(Type_Safe):
            dict_tuple_int_str: Dict[str, Tuple[int, str]]

        an_class = An_Class()
        an_class.dict_tuple_int_str['combo'] = (1, 'a')

        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.dict_tuple_int_str['combo'] = (1, 2)  # second item must be str

        with pytest.raises(TypeError, match="Expected tuple of length 2, but got 3"):
            an_class.dict_tuple_int_str['combo'] = (1, 'a', 3.0)

    def test__dict_with_any(self):
        class An_Class(Type_Safe):
            dict_with_any_value: Dict[str, Any]

        an_class = An_Class()


        an_class.dict_with_any_value['int' ] = 1                                    # Any type is acceptable for the value
        an_class.dict_with_any_value['str' ] = 'a'
        an_class.dict_with_any_value['dict'] = {}
        an_class.dict_with_any_value['list'] = [1, 2, 3]

    def test__dict_with_no_type(self):                                              # Untyped dict: any key & any value are accepted.
        class An_Class(Type_Safe):
            an_dict_untyped: dict

        an_class = An_Class()
        an_class.an_dict_untyped['int'] = 1
        an_class.an_dict_untyped[2] = 'some string'
        an_class.an_dict_untyped[None] = [1, 2, 3]

    def test__dict_with_none(self):                                                 # Ensures that None is not acceptable unless optional is specified.
        class An_Class(Type_Safe):
            an_dict_str_int: Dict[str, int]

        an_class = An_Class()

        with pytest.raises(TypeError, match="Expected 'int', but got 'NoneType'"):
            an_class.an_dict_str_int['fail'] = None

    def test__dict_with_nested_structures(self):
        class An_Class(Type_Safe):
            an_dict_str_list_int: Dict[str, List[int]]

        an_class = An_Class()
        an_class.an_dict_str_list_int['numbers'] = [1, 2, 3]

        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):               # Invalid: one element is a string
            an_class.an_dict_str_list_int['bad_numbers'] = [1, 'b', 3]

        with pytest.raises(TypeError, match=r"Expected 'list\[int\]', but got 'int'"):      # Invalid: the value is not a list at all
            an_class.an_dict_str_list_int['not_a_list'] = 123

    def test__dict_with_callable(self):
        class An_Class(Type_Safe):
            an_dict_callables: Dict[str, Callable[[int], str]]

        an_class = An_Class()

        def func(x: int) -> str:
            return str(x)

        an_class.an_dict_callables['ok'] = func

        # Not a callable
        with pytest.raises(TypeError, match=re.escape("Expected 'Callable[[<class 'int'>], str]', but got 'int'")):
            an_class.an_dict_callables['fail'] = 42


    def test__dict_with_forward_references(self):                           # Check that forward references (string-based) get enforced at runtime."""
        class An_Class(Type_Safe):
            an_dict_str_self: Dict[str, 'An_Class']

        an_class = An_Class()
        # Valid
        an_class.an_dict_str_self['me'] = An_Class()

        # Invalid
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'int'"):
            an_class.an_dict_str_self['fail'] = 123

    def test__json__with_type_safe_values(self):
        class TestTypeSafe(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        safe_dict = Type_Safe__Dict(str, TestTypeSafe)
        safe_dict["key1"] = TestTypeSafe("value1")
        safe_dict["key2"] = TestTypeSafe("value2")

        expected = {
            "key1": {"value": "value1"},
            "key2": {"value": "value2"}
        }
        assert safe_dict.json() == expected

    def test__json__with_nested_lists(self):
        class TestTypeSafe(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        safe_dict = Type_Safe__Dict(str, list)
        safe_dict["simple"] = [1, 2, 3]
        safe_dict["mixed"] = [TestTypeSafe("test"), 2, TestTypeSafe("other")]

        expected = {
            "simple": [1, 2, 3],
            "mixed": [{"value": "test"}, 2, {"value": "other"}]
        }
        assert safe_dict.json() == expected


    def test__json__with_empty_contents(self):
        safe_dict = Type_Safe__Dict(str, Any)
        assert safe_dict.json() == {}

        safe_dict["empty_list"] = []
        safe_dict["empty_dict"] = {}

        expected = {
            "empty_list": [],
            "empty_dict": {}
        }
        assert safe_dict.json() == expected



