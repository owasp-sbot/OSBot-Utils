import re
import sys
import pytest
from typing                                import List, Dict, Union, Optional, Any
from unittest                              import TestCase
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
from osbot_utils.helpers.Random_Guid       import Random_Guid
from osbot_utils.utils.Objects import __


class test_Type_Safe__List(TestCase):

    def test__list_from_json__enforces_type_safety(self):
        class An_Class__Item(Type_Safe):
            an_str: str

        class An_Class(Type_Safe):
            items : List[An_Class__Item]

        json_data = {'items': [{'an_str': 'abc'}]}

        an_class = An_Class.from_json(json_data)
        assert type(an_class.items) is Type_Safe__List
        assert type(an_class.items[0]) is An_Class__Item

    def test__list_from_json__enforces_type_safety__random_guids(self):
        class An_Class(Type_Safe):
            items : List[Random_Guid]

        json_data_1 = {'items': [Random_Guid(), Random_Guid()]}
        assert An_Class.from_json(json_data_1).json() == json_data_1

        json_data_2 = {'items': [Random_Guid(), Random_Guid(), 123]}
        with pytest.raises(ValueError, match=re.escape("in Random_Guid: value provided was not a Guid: 123")):
            An_Class.from_json(json_data_2)

    def test__type_safe_list_with_simple_types(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        class An_Class(Type_Safe):
            an_list       : list
            an_list__dict : list[dict]
            an_list__int  : list[int]
            an_list__str  : list[str]

        an_class = An_Class()
        assert type(an_class.an_list      ) is list             # Untyped list
        assert type(an_class.an_list__dict) is Type_Safe__List  # Typed lists
        assert type(an_class.an_list__int ) is Type_Safe__List
        assert type(an_class.an_list__str ) is Type_Safe__List

        assert an_class.an_list__dict.expected_type == dict     # Expected types
        assert an_class.an_list__int .expected_type == int
        assert an_class.an_list__str .expected_type == str

        # Testing untyped list
        an_class.an_list.append(1)
        an_class.an_list.append('b')
        an_class.an_list.append({})

        # Testing list[int]
        an_class.an_list__int.append(1)
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.an_list__int.append('b')
        with pytest.raises(TypeError, match="Expected 'int', but got 'dict'"):
            an_class.an_list__int.append({})

        # Testing list[str]
        an_class.an_list__str.append('a')
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_list__str.append(1)
        with pytest.raises(TypeError, match="Expected 'str', but got 'dict'"):
            an_class.an_list__str.append({})

        # Testing list[dict]
        an_class.an_list__dict.append({})
        with pytest.raises(TypeError, match="Expected 'dict', but got 'int'"):
            an_class.an_list__dict.append(1)
        with pytest.raises(TypeError, match="Expected 'dict', but got 'str'"):
            an_class.an_list__dict.append('a')


    def test__type_safe_list_with_complex_types(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        class An_Class__Complex(Type_Safe):
            an_list__dict_str_str     : List[Dict[str, str]]
            an_list__dict_str_int     : List[Dict[str, int]]
            an_list__list_int         : List[List[int]]
            an_list__union_int_str    : List[Union[int, str]]
            an_list__optional_int     : List[Optional[int]]
            an_list__dict_str_list_int: List[Dict[str, List[int]]]

        an_class = An_Class__Complex()

        assert type(an_class.an_list__dict_str_str     ) is Type_Safe__List
        assert type(an_class.an_list__dict_str_int     ) is Type_Safe__List
        assert type(an_class.an_list__list_int         ) is Type_Safe__List
        assert type(an_class.an_list__union_int_str    ) is Type_Safe__List
        assert type(an_class.an_list__optional_int     ) is Type_Safe__List
        assert type(an_class.an_list__dict_str_list_int) is Type_Safe__List

        # Testing List[Dict[str, str]]
        an_class.an_list__dict_str_str.append({'a': 'b'})
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_list__dict_str_str.append({'a': 1})
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_list__dict_str_str.append({1: 'b'})

        # Testing List[Dict[str, int]]
        an_class.an_list__dict_str_int.append({'a': 1})
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.an_list__dict_str_int.append({'a': 'b'})
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_list__dict_str_int.append({1: 2})

        # Testing List[List[int]]
        an_class.an_list__list_int.append([1, 2, 3])
        return
        with pytest.raises(TypeError, match="Expected 'int', but got 'str'"):
            an_class.an_list__list_int.append([1, 'b', 3])

        with pytest.raises(TypeError, match=re.escape("Expected 'list[int]', but got 'int'")):
            an_class.an_list__list_int.append(1)

        # Testing List[Union[int, str]]
        an_class.an_list__union_int_str.append(1)
        an_class.an_list__union_int_str.append('a')
        with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, str]', but got 'dict'")):
            an_class.an_list__union_int_str.append({})

        # Testing List[Optional[int]]
        an_class.an_list__optional_int.append(1)
        an_class.an_list__optional_int.append(None)

        with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, NoneType]', but got 'str'")):
            an_class.an_list__optional_int.append('a')

        # Testing List[Dict[str, List[int]]]
        an_class.an_list__dict_str_list_int.append({'numbers': [1, 2, 3]})
        with pytest.raises(TypeError, match=re.escape("Expected 'int', but got 'str'")):
            an_class.an_list__dict_str_list_int.append({'numbers': [1, 'b', 3]})
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: In dict value for key 'numbers': Expected 'list[int]', but got 'int'")):
            an_class.an_list__dict_str_list_int.append({'numbers': 1})

    def test__type_safe_list_with_custom_types(self):
        class CustomType(Type_Safe):
            a: int
            b: str

        class An_Class(Type_Safe):
            an_list__custom: List[CustomType]

        an_class = An_Class()
        assert type(an_class.an_list__custom) is Type_Safe__List

        # Valid CustomType instance
        custom_item = CustomType(a=1, b='test')
        an_class.an_list__custom.append(custom_item)
        an_class.an_list__custom.append({'a'     : 1})                      # will be converted to a valid class
        an_class.an_list__custom.append({'aaaaaa': 1})                      # not relevant variables will be ignored
        assert an_class.obj() == __(an_list__custom=[__(a=1, b='test'),
                                                     __(a=1, b=''    ),
                                                     __(a=0, b=''    )])

        # Incorrect type
        with pytest.raises(TypeError, match="Expected 'CustomType', but got 'int'"):
            an_class.an_list__custom.append(1)

    def test__type_safe_list_with_empty_collections(self):
        class An_Class(Type_Safe):
            an_list__empty_dicts: List[Dict]
            an_list__empty_lists: List[List]

        an_class = An_Class()
        assert type(an_class.an_list__empty_dicts) is Type_Safe__List
        assert type(an_class.an_list__empty_lists) is Type_Safe__List

        # Append empty dict
        an_class.an_list__empty_dicts.append({})
        # Append dict with data (since Dict has no type parameters, any dict is acceptable)
        an_class.an_list__empty_dicts.append({'a': 1})

        # Append empty list
        an_class.an_list__empty_lists.append([])
        # Append list with data (since List has no type parameters, any list is acceptable)
        an_class.an_list__empty_lists.append([1, 'a', {}])

    def test__type_safe_list_with_mismatched_types(self):
        class An_Class(Type_Safe):
            an_list__int: List[int]

        an_class = An_Class()

        # Append incorrect type
        with pytest.raises(TypeError, match="Expected 'int', but got 'float'"):
            an_class.an_list__int.append(1.0)

        with pytest.raises(TypeError, match="Expected 'int', but got 'NoneType'"):
            an_class.an_list__int.append(None)

        # check edge case caused by isinstance(True, int ) being true
        assert isinstance(True, bool) is True           # expected to be True
        assert isinstance(True, int ) is True           # BUG in python, expected to be False
        assert type(True)             is bool           # using type(..)
        assert type(True)             is not int        #    does produce the expected result

        with pytest.raises(TypeError, match="Expected 'int', but got 'bool'"):
            an_class.an_list__int.append(True)          # BUG, expected to raise an exception

    def test__type_safe_list_with_recursive_types(self):
        class TreeNode(Type_Safe):
            value: int
            children: Optional[List['TreeNode']]

        # Note: Forward references in type annotations require string literals

        class An_Class(Type_Safe):
            tree: TreeNode

        an_class = An_Class()
        an_class.tree = TreeNode(value=1, children=None)

        # Valid recursive structure
        child_node = TreeNode(value=2, children=[])
        an_class.tree.children = Type_Safe__List(TreeNode)
        an_class.tree.children.append(child_node)

        # Invalid child node
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'TreeNode', but got 'int'")):
            an_class.tree.children.append(3)

        # Invalid grandchild node
        grandchild_node = TreeNode(value=3, children=None)
        child_node.children = Type_Safe__List(TreeNode)
        child_node.children.append(grandchild_node)
        with pytest.raises(TypeError, match="Expected 'TreeNode', but got 'str'"):
            child_node.children.append('invalid')

    def test__type_safe_list_with_multiple_generics(self):
        from typing import Tuple

        class An_Class(Type_Safe):
            an_list__tuple: List[Tuple[int, str]]

        an_class = An_Class()

        # Valid entry
        an_class.an_list__tuple.append((1, 'a'))

        # Invalid entries
        with pytest.raises(TypeError, match=re.escape("In tuple at index 0: Expected 'int', but got 'str'")):
            an_class.an_list__tuple.append(('a', 1))

        with pytest.raises(TypeError, match="Expected tuple of length 2, but got 1"):
            an_class.an_list__tuple.append((1,))

        with pytest.raises(TypeError, match="Expected tuple of length 2, but got 3"):
            an_class.an_list__tuple.append((1, 'a', 3.0))

    def test__type_safe_list_with_any(self):
        from typing import Any

        class An_Class(Type_Safe):
            an_list__any: List[Any]

        an_class = An_Class()

        # Any type is acceptable
        an_class.an_list__any.append(1)
        an_class.an_list__any.append('a')
        an_class.an_list__any.append({})
        an_class.an_list__any.append([1, 2, 3])

    def test__type_safe_list_with_no_type(self):
        class An_Class(Type_Safe):
            an_list__untyped: list

        an_class = An_Class()

        # Since the list is untyped, any type is acceptable
        an_class.an_list__untyped.append(1)
        an_class.an_list__untyped.append('a')
        an_class.an_list__untyped.append({})
        an_class.an_list__untyped.append([1, 2, 3])


    def test__type_safe_list_with_none(self):
        class An_Class(Type_Safe):
            an_list__int: List[int]

        an_class = An_Class()

        with pytest.raises(TypeError, match="Expected 'int', but got 'NoneType'"):
            an_class.an_list__int.append(None)

    def test__type_safe_list_with_type_mismatch_in_nested_structures(self):
        class An_Class(Type_Safe):
            an_list__dict_str_list_int: List[Dict[str, List[int]]]

        an_class = An_Class()

        # Valid entry
        an_class.an_list__dict_str_list_int.append({'numbers': [1, 2, 3]})

        # Invalid value in inner list
        with pytest.raises(TypeError, match="In list at index 1: Expected 'int', but got 'str'"):
            an_class.an_list__dict_str_list_int.append({'numbers': [1, 'a', 3]})

        # Invalid key type in dict
        with pytest.raises(TypeError, match="In dict key '1': Expected 'str', but got 'int'"):
            an_class.an_list__dict_str_list_int.append({1: [1, 2, 3]})

        # Invalid type for value in dict
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: In dict value for key 'numbers': Expected 'list[int]', but got 'int'")):
            an_class.an_list__dict_str_list_int.append({'numbers': 1})

    def test_type_safe_list_with_callable(self):
        from typing import Callable

        class An_Class(Type_Safe):
            an_list__callable: List[Callable[[int], str]]

        an_class = An_Class()

        def func(x: int) -> str:            # Valid callable
            return str(x)

        an_class.an_list__callable.append(func)

        # Not a callable
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'Callable[[<class 'int'>], str]', but got 'int'")):
            an_class.an_list__callable.append(1)



    # this test will cause the List[Union[Dict[str, int], List[str], int]] to be cached (inside python, which will impact the next two tests)
    def test__type_safe_list_with_complex_union_types(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        class An_Class(Type_Safe):
            an_list__complex_union: List[Union[Dict[str, int], List[str], int]]

        an_class = An_Class()

        # Valid entries
        an_class.an_list__complex_union.append({'a': 1})
        an_class.an_list__complex_union.append(['a', 'b'])
        an_class.an_list__complex_union.append(42)

        # Invalid entries
        with pytest.raises(TypeError,
                           match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'dict'")):
            an_class.an_list__complex_union.append({1: 'a'})

        with pytest.raises(TypeError,
                           match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'list'")):
            an_class.an_list__complex_union.append([1, 2, 3])

        with pytest.raises(TypeError,
                           match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'str'")):
            an_class.an_list__complex_union.append('invalid')


    # test #1 impacted by test__type_safe_list_with_complex_union_types
    def test__type_safe_list_with_nested_unions(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        class An_Class(Type_Safe):
            an_list__nested_union: List[Union[int, List[str], Dict[str, int]]]

        an_class = An_Class()
        assert type(an_class.an_list__nested_union) is Type_Safe__List

        # Valid entries
        an_class.an_list__nested_union.append(1)
        an_class.an_list__nested_union.append(['a', 'b'])
        an_class.an_list__nested_union.append({'a': 1})

        # Invalid entries
        #with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, list[str], dict[str, int]]', but got 'str'")):     # due to the cache issues, this test only works when the test is executed directly
        with pytest.raises(TypeError, match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'str'")):
            an_class.an_list__nested_union.append('a')

        #with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, list[str], dict[str, int]]', but got 'list'")):
        with pytest.raises(TypeError, match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'list'")):
            an_class.an_list__nested_union.append([1, 2, 3])

        #with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, list[str], dict[str, int]]', but got 'dict'")):
        with pytest.raises(TypeError, match=re.escape("Expected 'Union[dict[str, int], list[str], int]', but got 'dict'")):
             an_class.an_list__nested_union.append({1: 'a'})

    # test #2 impacted by test__type_safe_list_with_complex_union_types
    def test__type_safe_list_with_mixed_types(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        class An_Class(Type_Safe):
            an_list__mixed: List[Union[int, List[str], Dict[str, int]]]

        an_class = An_Class()

        # Valid entries
        an_class.an_list__mixed.append(1)
        an_class.an_list__mixed.append(['a', 'b'])
        an_class.an_list__mixed.append({'a': 1})

        # Invalid entries
        #with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'Union[int, list[str], dict[str, int]]', but got 'str'")):      # see cache issue description above
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'Union[dict[str, int], list[str], int]', but got 'str'")):
            an_class.an_list__mixed.append('a')

        #with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, list[str], dict[str, int]]', but got 'list'")):
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'Union[dict[str, int], list[str], int]', but got 'list'")):
            an_class.an_list__mixed.append([1, 2])

        #with pytest.raises(TypeError, match=re.escape("Expected 'Union[int, list[str], dict[str, int]]', but got 'dict'")):
        with pytest.raises(TypeError, match=re.escape("Invalid type for item: Expected 'Union[dict[str, int], list[str], int]', but got 'dict'")):
            an_class.an_list__mixed.append({'a': 'b'})

    def test_json_with_simple_types(self):
        int_list = Type_Safe__List(int)
        int_list.append(1)
        int_list.append(2)
        int_list.append(3)

        assert int_list.json() == [1, 2, 3]

    def test_json_with_type_safe_objects(self):
        class TestType(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        safe_list = Type_Safe__List(TestType)
        safe_list.append(TestType("one"))
        safe_list.append(TestType("two"))

        expected = [
            {"value": "one"},
            {"value": "two"}
        ]
        assert safe_list.json() == expected

    def test_json_with_nested_lists(self):
        class TestType(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        nested_list = Type_Safe__List(list)
        nested_list.append([1, 2, 3])
        nested_list.append([TestType("test"), TestType("other")])

        expected = [
            [1, 2, 3],
            [{"value": "test"}, {"value": "other"}]
        ]
        assert nested_list.json() == expected

    def test_json_with_mixed_content(self):
        class TestType(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        mixed_list = Type_Safe__List(Any)
        mixed_list.append(42)
        mixed_list.append("text")
        mixed_list.append(TestType("safe"))
        mixed_list.append([1, TestType("in_list")])
        mixed_list.append({
            "normal": "value",
            "safe": TestType("in_dict")
        })

        expected = [
            42,
            "text",
            {"value": "safe"},
            [1, {"value": "in_list"}],
            {
                "normal": "value",
                "safe": {"value": "in_dict"}
            }
        ]
        assert mixed_list.json() == expected

    def test_json_with_empty_list(self):
        empty_list = Type_Safe__List(Any)
        assert empty_list.json() == []

        # Test with nested empty structures
        empty_list.append([])
        empty_list.append({})
        assert empty_list.json() == [[], {}]

    def test_json_with_tuples(self):
        class TestType(Type_Safe):
            value: str

            def __init__(self, value):
                self.value = value

        tuple_list = Type_Safe__List(tuple)
        tuple_list.append((1, 2, 3))
        tuple_list.append((TestType("test"), TestType("other")))

        expected = [
            [1, 2, 3],
            [{"value": "test"}, {"value": "other"}]
        ]
        assert tuple_list.json() == expected