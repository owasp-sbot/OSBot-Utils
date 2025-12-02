import re
import sys
import pytest
from decimal                                                                         import Decimal
from enum                                                                            import Enum
from typing                                                                          import Dict, List, Set, Any, Optional, ForwardRef
from unittest                                                                        import TestCase
from osbot_utils.utils.Env                                                           import in_github_action
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash   import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid_Short          import Random_Guid_Short
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                    import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now     import Timestamp_Now
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                 import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple               import Type_Safe__Tuple
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__From_Json           import Type_Safe__Step__From_Json, type_safe_step_from_json
from osbot_utils.utils.Objects                                                       import base_classes


class test_Type_Safe__Step__From_Json(TestCase):

    @classmethod
    def setUpClass(cls):                                                                # One-time expensive setup
        cls.step_from_json = Type_Safe__Step__From_Json()                              # Reuse single instance

    # Core deserialization methods

    def test__init__(self):                                                            # Test class initialization
        assert base_classes(Type_Safe__Step__From_Json()) == [object]

    def test_from_json(self):                                                          # Test main entry point
        class An_Class(Type_Safe):
            an_str : str
            an_int : int

        json_data = {'an_str': 'value', 'an_int': 42}
        result    = self.step_from_json.from_json(An_Class, json_data)

        assert type(result)  is An_Class
        assert result.an_str == 'value'
        assert result.an_int == 42

    def test_from_json__with_string_input(self):                                       # Test JSON string parsing
        class An_Class(Type_Safe):
            value: str

        json_string = '{"value": "test"}'
        result      = self.step_from_json.from_json(An_Class, json_string)

        assert result.value == 'test'

    def test_from_json__empty_data(self):                                             # Test empty/null data handling
        class An_Class(Type_Safe):
            value: str = 'default'

        assert self.step_from_json.from_json(An_Class, None).value == 'default'
        assert self.step_from_json.from_json(An_Class, {}).value   == 'default'

    # deserialize_from_dict tests

    def test_deserialize_from_dict__basic(self):                                      # Test basic deserialization
        class An_Class(Type_Safe):
            name : str
            age  : int

        obj  = An_Class()
        data = {'name': 'Alice', 'age': 30}

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.name == 'Alice'
        assert obj.age  == 30

    def test_deserialize_from_dict__nested_type_safe(self):                          # Test nested Type_Safe objects
        class Inner_Class(Type_Safe):
            value: str

        class Outer_Class(Type_Safe):
            inner: Inner_Class
            name : str

        obj  = Outer_Class()
        data = {'inner': {'value': 'nested'}, 'name': 'outer'}

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.name        == 'outer'
        assert obj.inner.value == 'nested'
        assert type(obj.inner) is Inner_Class

    def test_deserialize_from_dict__raise_on_not_found(self):                        # Test strict mode
        class An_Class(Type_Safe):
            existing: str

        obj  = An_Class()
        data = {'existing': 'value', 'unknown': 'extra'}

        error_message = "Attribute 'unknown' not found in 'An_Class'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_from_dict(obj, data, raise_on_not_found=True)

    def test_deserialize_from_dict__invalid_data_type(self):                         # Test invalid input handling
        error_message = "Expected a dictionary, but got '<class 'list'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_from_dict(object(), [1, 2, 3])

    # Type object deserialization

    def test_deserialize_type__using_value(self):                                    # Test type reconstruction
        # Built-in types
        assert self.step_from_json.deserialize_type__using_value('builtins.str')  is str
        assert self.step_from_json.deserialize_type__using_value('builtins.int')  is int
        assert self.step_from_json.deserialize_type__using_value('builtins.list') is list

        # Special case for NoneType
        import types
        assert self.step_from_json.deserialize_type__using_value('builtins.NoneType') is types.NoneType

        # Custom classes
        type_string = 'osbot_utils.type_safe.Type_Safe.Type_Safe'
        assert self.step_from_json.deserialize_type__using_value(type_string) is Type_Safe

    def test_deserialize_type__using_value__errors(self):
        # Test 1: Invalid module that doesn't exist
        error_message = "Could not import module 'invalid.module': No module named 'invalid'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_type__using_value('invalid.module.Class')

        # Test 2: Valid module but trying to deserialize a function (not a class)
        error_message = "Security alert, in deserialize_type__using_value only classes are allowed, got builtin_function_or_method for 'builtins.print'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_type__using_value('builtins.print')

        # Test 3: Valid module but type doesn't exist
        error_message = "Type 'NonExistentClass' not found in module 'builtins'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_type__using_value('builtins.NonExistentClass')

        # Test 4: Blacklisted dangerous type
        error_message = "Type 'eval' is deny listed for security"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.step_from_json.deserialize_type__using_value('builtins.eval')

        # Test 5: Module not in allow listed and not Type_Safe
        error_message = "Security alert, in deserialize_type__using_value only classes are allowed, got module for 'os.path'"
        with pytest.raises(ValueError, match=error_message):
            self.step_from_json.deserialize_type__using_value('os.path')

    # Dict annotation handling

    def test_deserialize_dict__using_key_value_annotations(self):                    # Test typed dict deserialization
        class An_Class(Type_Safe):
            mapping: Dict[str, int]

        obj   = An_Class()
        value = {'key1': 1, 'key2': 2}

        result = self.step_from_json.deserialize_dict__using_key_value_annotations(obj, 'mapping', value)

        assert type(result)    is Type_Safe__Dict
        assert result['key1']  == 1
        assert result['key2']  == 2

    def test_deserialize_dict__nested_dict_annotations(self):                        # Test Dict[str, Dict[str, Any]]
        class An_Class(Type_Safe):
            nested: Dict[str, Dict[str, Any]]

        obj   = An_Class()
        value = {'outer': {'inner': 'value', 'number': 42}}

        result = self.step_from_json.deserialize_dict__using_key_value_annotations(obj, 'nested', value)

        assert type(result)               is Type_Safe__Dict
        assert type(result['outer'])      is Type_Safe__Dict
        assert result['outer']['inner']   == 'value'
        assert result['outer']['number']  == 42

    def test_deserialize_dict_key(self):                                             # Test key deserialization
        # Type[T] keys
        type_key = self.step_from_json.deserialize_dict_key(type, 'builtins.str')
        assert type_key is str

        # Type_Safe keys
        class Key_Class(Type_Safe):
            value: str

        key_dict = {'value': 'test'}
        result   = self.step_from_json.deserialize_dict_key(Key_Class, key_dict)
        assert type(result)  is Key_Class
        assert result.value  == 'test'

        # Regular keys
        assert self.step_from_json.deserialize_dict_key(str, 'simple') == 'simple'

    def test_deserialize_dict_value(self):                                           # Test value deserialization
        # Dict[K, V] values
        from typing import Dict
        nested_dict = {'key': 'value'}
        _self       = None
        result      = self.step_from_json.deserialize_dict_value(_self, Dict[str, str], nested_dict)
        assert type(result)   is Type_Safe__Dict
        assert result['key']  == 'value'

        # Type_Safe values
        class Value_Class(Type_Safe):
            data: str

        value_dict = {'data': 'test'}
        result     = self.step_from_json.deserialize_dict_value(_self, Value_Class, value_dict)
        assert type(result) is Value_Class
        assert result.data  == 'test'

        # Any type
        assert self.step_from_json.deserialize_dict_value(_self, Any, 'anything') == 'anything'

    # Special identifier types

    def test_deserialize_special_types(self):                                        # Test special type handling
        class An_Class(Type_Safe):
            safe_id    : Safe_Id
            guid       : Random_Guid
            guid_short : Random_Guid_Short
            timestamp  : Timestamp_Now
            obj_id     : Obj_Id
            hash_value : Safe_Str__Hash
            decimal    : Decimal

        data = {
            'safe_id'    : 'test-id'                ,
            'guid'       : '12345678-1234-5678-1234-567812345678',
            'guid_short' : 'abc123'                 ,
            'timestamp'  : 1234567890               ,
            'obj_id'     : '12345678'               ,
            'hash_value' : 'abcdef1234'             ,
            'decimal'    : '123.45'
        }

        obj = An_Class()
        self.step_from_json.deserialize_from_dict(obj, data)

        assert type(obj.safe_id)     is Safe_Id
        assert type(obj.guid)        is Random_Guid
        assert type(obj.guid_short)  is Random_Guid_Short
        assert type(obj.timestamp)   is Timestamp_Now
        assert type(obj.obj_id)      is Obj_Id
        assert type(obj.hash_value)  is Safe_Str__Hash
        assert type(obj.decimal)     is Decimal
        assert obj.decimal           == Decimal('123.45')

    # Enum handling

    def test_enum_deserialization(self):                                             # Test enum handling
        class Status_Enum(Enum):
            PENDING   = 'pending'
            COMPLETED = 'completed'

        class An_Class(Type_Safe):
            status: Status_Enum

        data = {'status': 'completed'}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.status            == Status_Enum.COMPLETED
        assert type(obj.status)      is Status_Enum

    def test_optional_enum_deserialization(self):                                    # Test Optional[Enum]
        class Priority_Enum(Enum):
            LOW  = 1
            HIGH = 2

        class An_Class(Type_Safe):
            priority: Optional[Priority_Enum]

        data = {'priority': 2}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.priority == Priority_Enum.HIGH

    # Collection handling

    def test_list_deserialization(self):                                             # Test list handling
        class An_Class(Type_Safe):
            items: List[str]

        data = {'items': ['a', 'b', 'c']}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert type(obj.items) is Type_Safe__List
        assert obj.items       == ['a', 'b', 'c']

    def test_list_with_type_safe_objects(self):                                      # Test List[Type_Safe]
        class Item_Class(Type_Safe):
            name: str

        class Container_Class(Type_Safe):
            items: List[Item_Class]

        data = {'items': [{'name': 'item1'}, {'name': 'item2'}]}
        obj  = Container_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert len(obj.items)           == 2
        assert type(obj.items[0])       is Item_Class
        assert obj.items[0].name        == 'item1'

    def test_list_with_forward_ref(self):                                            # Test List['Self']
        if sys.version_info < (3, 9):
            pytest.skip("Forward refs need Python 3.9+")

        class Tree_Node(Type_Safe):
            value   : str
            children: List['Tree_Node']

        data = {'value': 'root', 'children': [{'value': 'child1', 'children': []},
                                               {'value': 'child2', 'children': []}]}
        obj = Tree_Node()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.value                  == 'root'
        assert len(obj.children)          == 2
        assert obj.children[0].value      == 'child1'
        assert type(obj.children[0])      is Tree_Node

    def test_set_deserialization(self):                                              # Test set handling
        class An_Class(Type_Safe):
            unique: Set[int]

        data = {'unique': [1, 2, 2, 3]}                                             # Duplicates in source
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert type(obj.unique) is Type_Safe__Set
        assert obj.unique       == {1, 2, 3}                                        # Duplicates removed

    def test_tuple_deserialization(self):                                            # Test tuple handling
        from typing import Tuple

        class An_Class(Type_Safe):
            coords: Tuple[int, int, str]

        data = {'coords': [10, 20, 'label']}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert type(obj.coords) is Type_Safe__Tuple
        assert obj.coords       == (10, 20, 'label')

    # Complex nested scenarios

    def test_complex_nested_structure(self):                                         # Test deep nesting
        class Level3(Type_Safe):
            value: str

        class Level2(Type_Safe):
            level3: Level3
            items : List[str]

        class Level1(Type_Safe):
            level2: Level2
            data  : Dict[str, int]

        data = {
            'level2': {
                'level3': {'value': 'deep'},
                'items' : ['a', 'b']
            },
            'data': {'x': 1, 'y': 2}
        }

        obj = Level1()
        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.level2.level3.value == 'deep'
        assert obj.level2.items        == ['a', 'b']
        assert obj.data['x']           == 1

    def test_node_type_handling(self):                                               # Test dynamic type resolution
        class Base_Node(Type_Safe):
            node_type: str

        class Type_A(Base_Node):
            value_a: str

        class Type_B(Base_Node):
            value_b: int

        class Container(Type_Safe):
            nodes: Dict[str, Base_Node]

        # This tests the 'node_type' special handling
        # Currently requires manual type registration
        # This is a placeholder for when dynamic resolution is implemented

    # Round-trip serialization

    def test_round_trip_serialization(self):                                         # Test complete round-trip
        class Complex_Class(Type_Safe):
            id       : Safe_Id
            name     : str
            items    : List[str]
            metadata : Dict[str, Any]
            nested   : 'Complex_Class'

        original          = Complex_Class()
        original.id       = Safe_Id('test-123')
        original.name     = 'Test Object'
        original.items    = ['item1', 'item2']
        original.metadata = {'key': 'value', 'number': 42}
        original.nested   = Complex_Class(name='Nested Object')

        # Serialize
        json_data = original.json()

        # Deserialize
        # error_message = "On Complex_Class, invalid type for attribute 'nested'. Expected 'Complex_Class' but got '<class 'dict'>"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     restored = Complex_Class.from_json(json_data)           # BUG

        restored = Complex_Class.from_json(json_data)
        assert restored.json() == json_data                         # Verify perfect round-trip
        assert restored.id     == 'test-123'
        assert restored.name   == 'Test Object'

    # Error scenarios

    def test_error_handling(self):                                                   # Test various error conditions
        class An_Class(Type_Safe):
            value: str

        # Non-dict input to deserialize_from_dict
        with pytest.raises(ValueError, match="Expected a dictionary"):
            self.step_from_json.deserialize_from_dict(An_Class(), "not a dict")

        # None input handling
        obj = An_Class()
        result = self.step_from_json.deserialize_from_dict(obj, None)
        assert result is None

    # Regression tests

    def test__regression__nested_dict_serialization(self):                           # Test the fix we just implemented
        if sys.version_info < (3, 9):
            pytest.skip("Dict[str, Dict[str, Any]] needs Python 3.9+")

        class An_Class(Type_Safe):
            dict_field: Dict[Random_Guid, Dict[Random_Guid, Random_Guid]]

        # This used to fail with "Type Dict cannot be instantiated"
        guid1 = Random_Guid()
        guid2 = Random_Guid()
        guid3 = Random_Guid()

        json_data = {'dict_field': {str(guid1): {str(guid2): str(guid3)}}}

        result = An_Class.from_json(json_data)
        assert type(result.dict_field)           is Type_Safe__Dict
        assert type(result.dict_field[str(guid1)]) is Type_Safe__Dict

    # Edge cases and special scenarios

    def test_empty_collections(self):                                                # Test empty collection handling
        class An_Class(Type_Safe):
            items : List[str]
            data  : Dict[str, int]
            unique: Set[int]

        data = {'items': [], 'data': {}, 'unique': []}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.items  == []
        assert obj.data   == {}
        assert obj.unique == set()

    def test_none_values(self):                                                      # Test None handling
        class An_Class(Type_Safe):
            optional_str  : Optional[str]
            optional_int  : Optional[int]
            required_str  : str

        data = {'optional_str': None, 'optional_int': None, 'required_str': 'value'}
        obj  = An_Class()

        self.step_from_json.deserialize_from_dict(obj, data)

        assert obj.optional_str is None
        assert obj.optional_int is None
        assert obj.required_str == 'value'

    # Performance test marker

    #@pytest.mark.skip(reason="Performance test - run manually")
    def test_performance_large_dataset(self):                                        # Test with large data
        class Large_Class(Type_Safe):
            items: List[dict[str, Any]]

        # Create large dataset
        data = {'items': [{'id': i, 'value': f'item_{i}'} for i in range(1000)]}

        import time
        start = time.time()

        obj = Large_Class()
        self.step_from_json.deserialize_from_dict(obj, data)

        elapsed = time.time() - start

        assert len(obj.items) == 1000
        if in_github_action():
            assert elapsed < 0.05                                    # in GH Actions this is about ~10ms
        else:
            assert elapsed < 0.01                                    # on dev laptop this is ~2ms

    def test__forward_ref_in_list_works(self):                              # Forward refs in List work correctly """

        class Tree_Node(Type_Safe):
            value    : str
            children : List['Tree_Node']

        root         = Tree_Node(value='root')
        root.children = [Tree_Node(value='child1'), Tree_Node(value='child2')]

        json_data = root.json()
        restored  = Tree_Node.from_json(json_data)  # This works!

        assert type(restored)              is Tree_Node
        assert len(restored.children)      == 2
        assert restored.children[0].value  == 'child1'
        assert type(restored.children[0])  is Tree_Node

        assert restored.json() == json_data
        assert restored.obj()  == restored.obj()

    def test__regression__dict_with_list_values(self):                                  # Test Dict[K, List[V]] handling

        class An_Class(Type_Safe):
            all_paths: Dict[Safe_Id, List[Safe_Str__File__Path]]

        data = { 'by_hash': [ 'refs/by-hash/e1/5b/e15b31f87df1896e.json'        ,
                              'refs/by-hash/e1/5b/e15b31f87df1896e.json.config' ,
                              'refs/by-hash/e1/5b/e15b31f87df1896e.json.metadata'],
                 'by_id'  : [ 'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json'        ,
                              'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config' ,
                              'refs/by-id/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata'],
                 'data'   : [ 'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json'        ,
                              'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.config' ,
                              'data/direct/be/40/be40eef6-9785-4be1-a6b1-b8da6cee51a4.json.metadata']}

        # Test assignment (runtime type conversion)
        an_class = An_Class()
        an_class.all_paths = data                                                       # Should handle conversion

        assert type(an_class.all_paths)           is Type_Safe__Dict
        assert type(an_class.all_paths['by_hash']) is Type_Safe__List
        assert len(an_class.all_paths['by_hash']) == 3

        # Verify Safe type conversion happened
        for path in an_class.all_paths['by_hash']:
            assert type(path) is Safe_Str__File__Path

        # Test JSON round-trip
        json_data = an_class.json()
        restored  = An_Class.from_json(json_data)

        assert restored.json() == json_data
        assert type(restored.all_paths)               is Type_Safe__Dict
        assert type(restored.all_paths['by_hash'])    is Type_Safe__List
        assert type(restored.all_paths['by_hash'][0]) is Safe_Str__File__Path

    def test_deserialize_list_in_dict_value__with_type_safe_objects(self):             # Test List[Type_Safe] in dict values
        class Item_Class(Type_Safe):
            name : str
            value: int

        class Container(Type_Safe):
            categories: Dict[str, List[Item_Class]]

        data = {
            'categories': {
                'group1': [{'name': 'item1', 'value': 10},
                          {'name': 'item2', 'value': 20}],
                'group2': [{'name': 'item3', 'value': 30}]
            }
        }

        result = Container.from_json(data)

        assert type(result.categories)           is Type_Safe__Dict
        assert type(result.categories['group1']) is Type_Safe__List
        assert len(result.categories['group1'])  == 2
        assert type(result.categories['group1'][0]) is Item_Class
        assert result.categories['group1'][0].name  == 'item1'
        assert result.categories['group1'][0].value == 10

    def test_deserialize_list_in_dict_value__empty_lists(self):                       # Test empty List[T] in dict values
        from typing import Dict, List

        class An_Class(Type_Safe):
            mapping: Dict[str, List[str]]

        data = {'mapping': {'key1': [], 'key2': ['item1'], 'key3': []}}

        result = An_Class.from_json(data)

        assert result.mapping['key1'] == []
        assert result.mapping['key2'] == ['item1']
        assert result.mapping['key3'] == []
        assert type(result.mapping['key1']) is Type_Safe__List
        assert type(result.mapping['key2']) is Type_Safe__List

    def test_deserialize_list_in_dict_value__primitive_types(self):                   # Test List[primitive] in dict values
        from typing import Dict, List

        class An_Class(Type_Safe):
            int_lists   : Dict[str, List[int]]
            float_lists : Dict[str, List[float]]
            bool_lists  : Dict[str, List[bool]]

        data = {
            'int_lists'   : {'odds': [1, 3, 5], 'evens': [2, 4, 6]},
            'float_lists' : {'decimals': [1.1, 2.2, 3.3]},
            'bool_lists'  : {'flags': [True, False, True]}
        }

        result = An_Class.from_json(data)

        assert result.int_lists['odds']       == [1, 3, 5]
        assert result.float_lists['decimals'] == [1.1, 2.2, 3.3]
        assert result.bool_lists['flags']     == [True, False, True]

        # All should be Type_Safe__List
        assert type(result.int_lists['odds'])       is Type_Safe__List
        assert type(result.float_lists['decimals']) is Type_Safe__List
        assert type(result.bool_lists['flags'])     is Type_Safe__List

    def test_deserialize_list_in_dict_value__nested_complexity(self):                 # Test Dict[str, List[Dict[str, Any]]]
        from typing import Dict, List, Any

        class An_Class(Type_Safe):
            complex: Dict[str, List[Dict[str, Any]]]

        data = {
            'complex': {
                'section1': [
                    {'id': 1, 'name': 'first' , 'active': True },
                    {'id': 2, 'name': 'second', 'active': False}
                ],
                'section2': [
                    {'type': 'A', 'count': 100}
                ]
            }
        }

        result = An_Class.from_json(data)

        assert type(result.complex)             is Type_Safe__Dict
        assert type(result.complex['section1']) is Type_Safe__List
        assert len(result.complex['section1'])  == 2
        assert result.complex['section1'][0]['id'] == 1
        assert result.complex['section2'][0]['type'] == 'A'

    def test_deserialize_list_in_dict_value__with_forward_refs(self):                # Test List[ForwardRef] in dict values
        if sys.version_info < (3, 9):
            pytest.skip("Forward refs need Python 3.9+")

        class Node(Type_Safe):
            name     : str
            children : Dict[str, List['Node']]

        data = {
            'name': 'root',
            'children': {
                'left' : [{'name': 'left1' , 'children': {}},
                         {'name': 'left2' , 'children': {}}],
                'right': [{'name': 'right1', 'children': {}}]
            }
        }

        result = Node.from_json(data)

        assert result.name                         == 'root'
        assert len(result.children['left'])        == 2
        assert type(result.children['left'][0])    is Node
        assert result.children['left'][0].name     == 'left1'             # ['left'][0] is not Node
        assert result.children['right'][0].name    == 'right1'            # so we can't access it directly


    def test_deserialize_list_in_dict_value__with_safe_primitives(self):             # Test multiple Safe primitive types
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url import Safe_Str__Url
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Email import Safe_Str__Email
        from typing import Dict, List

        class An_Class(Type_Safe):
            urls_by_category : Dict[str, List[Safe_Str__Url]]
            emails_by_domain : Dict[str, List[Safe_Str__Email]]

        data = {
            'urls_by_category': {
                'docs'  : ['https://docs.example.com', 'https://api.example.com/docs'],
                'apis'  : ['https://api.example.com/v1', 'https://api.example.com/v2']
            },
            'emails_by_domain': {
                'work'     : ['alice@company.com', 'bob@company.com'],
                'personal' : ['alice@gmail.com']
            }
        }

        result = An_Class.from_json(data)

        # Check URL conversion
        assert type(result.urls_by_category['docs'][0]) is Safe_Str__Url
        assert result.urls_by_category['docs'][0] == 'https://docs.example.com'

        # Check Email conversion
        assert type(result.emails_by_domain['work'][0]) is Safe_Str__Email
        assert result.emails_by_domain['work'][0] == 'alice@company.com'

    def test_deserialize_list_in_dict_value__validation_errors(self):                # Test validation failures
        from osbot_utils.type_safe.primitives.domains.network.safe_uint.Safe_UInt__Port import Safe_UInt__Port
        from typing import Dict, List

        class An_Class(Type_Safe):
            ports_by_service: Dict[str, List[Safe_UInt__Port]]

        # Invalid port number (>65535)
        data = {'ports_by_service': {'web': [80, 443, 99999]}}  # 99999 is invalid

        error_message = "Safe_UInt__Port must be <= 65535, got 99999"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            An_Class.from_json(data)

    def test_deserialize_list_in_dict_value__mixed_types_in_union(self):            # Test Union types in lists
        from typing import Dict, List, Union

        class An_Class(Type_Safe):
            mixed: Dict[str, List[Union[str, int]]]

        data = {'mixed': {'values': ['text', 42, 'more text', 100]}}

        result = An_Class.from_json(data)

        assert result.mixed['values'] == ['text', 42, 'more text', 100]
        assert type(result.mixed['values']) is Type_Safe__List

    def test_deserialize_list_in_dict_value__performance(self):                     # Test performance with large datasets
        from typing import Dict, List
        import time

        class An_Class(Type_Safe):
            large_data: Dict[str, List[str]]

        # Create large dataset
        data = {
            'large_data': {
                f'key_{i}': [f'item_{j}' for j in range(100)]
                for i in range(10)
            }
        }

        start = time.time()
        result = An_Class.from_json(data)
        elapsed = time.time() - start

        assert len(result.large_data) == 10
        assert len(result.large_data['key_0']) == 100
        assert elapsed < 0.2                                                        # Should be fast even with 1000 items

    def test__regression__documented__dict_with_typing_List(self):                         # Document that typing.List now works
        from typing import Dict, List as TypingList                                # Explicit import name

        class An_Class(Type_Safe):
            paths: Dict[str, TypingList[str]]                                      # Using typing.List

        data = {'paths': {'root': ['/home', '/usr', '/var']}}

        result = An_Class.from_json(data)                                           # This used to fail with "Type List cannot be instantiated"

        assert result.paths['root'] == ['/home', '/usr', '/var']
        assert type(result.paths['root']) is Type_Safe__List

    def test__regression__documented__dict_with_lowercase_list(self):                      # Document that list[T] now works
        if sys.version_info < (3, 9):
            pytest.skip("list[T] syntax needs Python 3.9+")

        from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int

        class An_Class(Type_Safe):
            counts: Dict[str, list[Safe_Int]]                                      # Using lowercase list

        data = {'counts': {'items': [1, 2, 3], 'totals': [10, 20]}}

        result = An_Class.from_json(data)                                           # This used to fail with type mismatch errors

        assert type(result.counts['items'][0]) is Safe_Int
        assert result.counts['items'] == [1, 2, 3]