import re
import sys
import pytest
from decimal                                                                         import Decimal
from enum                                                                            import Enum
from typing                                                                          import Dict, List, Set, Any, Optional, ForwardRef
from unittest                                                                        import TestCase
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash   import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid_Short          import Random_Guid_Short
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                    import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Timestamp_Now              import Timestamp_Now
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
        result      = self.step_from_json.deserialize_dict_value(Dict[str, str], nested_dict)
        assert type(result)   is Type_Safe__Dict
        assert result['key']  == 'value'

        # Type_Safe values
        class Value_Class(Type_Safe):
            data: str

        value_dict = {'data': 'test'}
        result     = self.step_from_json.deserialize_dict_value(Value_Class, value_dict)
        assert type(result) is Value_Class
        assert result.data  == 'test'

        # Any type
        assert self.step_from_json.deserialize_dict_value(Any, 'anything') == 'anything'

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
        assert elapsed < 0.01                                    # Should complete in under 10ms

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
