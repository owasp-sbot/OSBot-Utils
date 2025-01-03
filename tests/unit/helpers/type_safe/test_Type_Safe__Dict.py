import re
import sys
import pytest
from unittest                                 import TestCase
from typing                                   import Dict, Union, Optional, Any, Callable, List, Tuple
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict


class test_Type_Safe__Dict(TestCase):

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
            an_class.an_dict['bad_child'] = "some string"
