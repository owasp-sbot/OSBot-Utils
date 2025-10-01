import re
import sys
import pytest
from typing                                                                              import List, Dict, Union, Optional, Any
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Int                                      import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_Str                                      import Safe_Str
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo import Safe_Str__GitHub__Repo
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__IP_Address      import Safe_Str__IP_Address
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                    import Type_Safe__List
from osbot_utils.utils.Objects                                                           import __


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

    def test__type_safe_list__primitive_conversions(self):      # Test that Type_Safe__List handles various primitive conversions

        # Test with different Safe_Str variants
        class Schema(Type_Safe):
            ips: List[Safe_Str__IP_Address]
            ids: List[Safe_Id]

        # Should work
        schema = Schema(ips=['192.168.1.1'], ids=['test-id'])
        assert schema.json() == {'ips': ['192.168.1.1'], 'ids': ['test-id']}

        # Should fail with invalid IP
        with pytest.raises(TypeError):
            Schema(ips=['not-an-ip'])

    def test__type_safe_list__primitive_conversions_with_detailed_errors(self): # Test that Type_Safe__List handles various primitive conversions and provides detailed error messages

        
        # Test with different Safe_Str variants
        class Schema(Type_Safe):
            ips    : List[Safe_Str__IP_Address]
            ids    : List[Safe_Id]
            repos  : List[Safe_Str__GitHub__Repo]
            numbers: List[Safe_Int]

        # Should work - valid conversions
        schema = Schema(
            ips=['192.168.1.1', '10.0.0.1'],
            ids=['test-id', 'another_id'],
            repos=['owner/repo', 'microsoft/vscode'],
            numbers=[1, 2, '3', '42']
        )
        assert schema.json() == {
            'ips': ['192.168.1.1', '10.0.0.1'],
            'ids': ['test-id', 'another_id'],
            'repos': ['owner/repo', 'microsoft/vscode'],
            'numbers': [1, 2, 3, 42]
        }

        # Test roundtrip
        schema_roundtrip = Schema.from_json(schema.json())
        assert schema_roundtrip.json() == schema.json()

        # Should fail with invalid IP - check detailed error message
        error_msg = r"In Type_Safe__List: Could not convert str to Safe_Str__IP_Address: Invalid IP address: not-an-ip"
        with pytest.raises(TypeError, match=error_msg):
            Schema(
                ips=['192.168.1.1', 'not-an-ip'],  # Invalid IP
                ids=['test'],
                repos=['owner/repo'],
                numbers=[1]
            )

        # Should fail with invalid GitHub repo format
        error_msg = r"In Type_Safe__List: Could not convert str to Safe_Str__GitHub__Repo: in Safe_Str__GitHub__Repo, gitHub repository must be in 'owner/repo' format: invalid"
        with pytest.raises(TypeError, match=error_msg):
            Schema(
                ips=['192.168.1.1'],
                ids=['test'],
                repos=['invalid'],  # Missing owner/repo format
                numbers=[1]
            )

        # Should fail with invalid number
        error_msg = r"In Type_Safe__List: Could not convert str to Safe_Int: Cannot convert 'not-a-number' to integer"
        with pytest.raises(TypeError, match=error_msg):
            Schema(
                ips=['192.168.1.1'],
                ids=['test'],
                repos=['owner/repo'],
                numbers=[1, 'not-a-number']  # Invalid number
            )

        # Test with nested Type_Safe objects containing primitive lists
        class NestedSchema(Type_Safe):
            name: Safe_Str
            data: List[Schema]

        # Should work with nested conversion
        nested = NestedSchema(
            name='test',
            data=[
                {'ips': ['127.0.0.1'], 'ids': ['id1'], 'repos': ['user/repo'], 'numbers': [1, 2]},
                {'ips': ['::1'], 'ids': ['id2'], 'repos': ['org/project'], 'numbers': ['3', 4]}
            ]
        )
        assert nested.json() == {
            'name': 'test',
            'data': [
                {'ips': ['127.0.0.1'], 'ids': ['id1'], 'repos': ['user/repo'], 'numbers': [1, 2]},
                {'ips': ['::1'], 'ids': ['id2'], 'repos': ['org/project'], 'numbers': [3, 4]}
            ]
        }

        # Test edge cases
        class EdgeCaseSchema(Type_Safe):
            empty_list: List[Safe_Str]
            mixed_types: List[Safe_Id]

        # Empty lists should work
        edge_case = EdgeCaseSchema(
            empty_list=[],
            mixed_types=[]
        )
        assert edge_case.json() == {'empty_list': [], 'mixed_types': []}

        # Test with very long strings that exceed Safe_Id max length
        error_msg = r"In Type_Safe__List: Could not convert str to Safe_Id: Invalid ID: The ID must not exceed 512 characters (was 1000)."
        with pytest.raises(TypeError, match=re.escape(error_msg)):
            EdgeCaseSchema(
                empty_list=[],
                mixed_types=['a' * 1000]  # Exceeds Safe_Id max length of 512
            )

        # Test that original TypeError from validation still works for non-convertible types
        class StrictSchema(Type_Safe):
            strings: List[str]

        # Should fail when trying to append a non-string, non-convertible type
        error_msg = r"In Type_Safe__List: Invalid type for item: Expected 'str', but got 'dict'"
        with pytest.raises(TypeError, match=error_msg):
            StrictSchema(strings=[{'not': 'a string'}])


    def test__contains__with_type_safe_primitive(self):
        # Test with Safe_Str type
        safe_str_list = Type_Safe__List(Safe_Str)
        safe_str_list.append(Safe_Str('hello'))
        safe_str_list.append(Safe_Str('world'))

        # Direct Safe_Str instance lookup
        assert Safe_Str('hello') in safe_str_list
        assert Safe_Str('world') in safe_str_list
        assert Safe_Str('foo')   not in safe_str_list

        # String primitive lookup (should be converted)
        assert 'hello' in safe_str_list
        assert 'world' in safe_str_list
        assert 'foo'   not in safe_str_list

    def test__contains__with_safe_int(self):
        # Test with Safe_Int type
        safe_int_list = Type_Safe__List(Safe_Int)
        safe_int_list.append(Safe_Int(42))
        safe_int_list.append(Safe_Int(100))

        # Direct Safe_Int instance lookup
        assert Safe_Int(42)  in safe_int_list
        assert Safe_Int(100) in safe_int_list
        assert Safe_Int(999) not in safe_int_list

        # Integer primitive lookup (should be converted)
        assert 42  in safe_int_list
        assert 100 in safe_int_list
        assert 999 not in safe_int_list

        # String that can be converted to int
        assert '42'  in safe_int_list
        assert '100' in safe_int_list
        assert '999' not in safe_int_list

    def test__contains__with_regular_types(self):
        # Test that regular types still work normally
        string_list = Type_Safe__List(str)
        string_list.append('hello')
        string_list.append('world')

        assert 'hello' in string_list
        assert 'world' in string_list
        assert 'foo'   not in string_list

        # These should not be found (no conversion for regular types)
        assert 123 not in string_list

    def test__contains__with_enum(self):
        from enum import Enum

        class Color(Enum):
            RED = 'red'
            GREEN = 'green'
            BLUE = 'blue'

        color_list = Type_Safe__List(Color)
        color_list.append(Color.RED)
        color_list.append(Color.GREEN)

        # Direct enum instance lookup
        assert Color.RED   in color_list
        assert Color.GREEN in color_list
        assert Color.BLUE  not in color_list

        # Lookup by enum name (string)
        assert 'RED'   in color_list
        assert 'GREEN' in color_list
        assert 'BLUE'  not in color_list

        # Lookup by enum value (string)
        assert 'red'   in color_list
        assert 'green' in color_list
        assert 'blue'  not in color_list

    def test__contains__with_int_enum(self):
        from enum import Enum

        class Status(Enum):
            PENDING  = 1
            APPROVED = 2
            REJECTED = 3

        status_list = Type_Safe__List(Status)
        status_list.append(Status.PENDING)
        status_list.append(Status.APPROVED)

        # Direct enum instance lookup
        assert Status.PENDING  in status_list
        assert Status.APPROVED in status_list
        assert Status.REJECTED not in status_list

        # Lookup by enum name (string)
        assert 'PENDING'  in status_list
        assert 'APPROVED' in status_list
        assert 'REJECTED' not in status_list

        # Note: Integer values won't work with current implementation
        # since we only handle string conversions for enums
        assert 1 not in status_list  # This won't find Status.PENDING
        assert 2 not in status_list  # This won't find Status.APPROVED

    def test__contains__with_mixed_enum_values(self):
        from enum import Enum

        class MixedEnum(Enum):
            ALPHA = 'a'
            BETA = 'b'
            ONE = 1
            TWO = 2

        mixed_list = Type_Safe__List(MixedEnum)
        mixed_list.append(MixedEnum.ALPHA)
        mixed_list.append(MixedEnum.ONE)

        # Direct enum instance lookup
        assert MixedEnum.ALPHA in mixed_list
        assert MixedEnum.ONE   in mixed_list
        assert MixedEnum.BETA  not in mixed_list
        assert MixedEnum.TWO   not in mixed_list

        # Lookup by enum name (string)
        assert 'ALPHA' in mixed_list
        assert 'ONE'   in mixed_list
        assert 'BETA'  not in mixed_list

        # Lookup by string value (only works for string-valued enums)
        assert 'a' in mixed_list
        assert 'b' not in mixed_list

        # Integer values won't work with string conversion
        assert 1 not in mixed_list  # Won't find MixedEnum.ONE