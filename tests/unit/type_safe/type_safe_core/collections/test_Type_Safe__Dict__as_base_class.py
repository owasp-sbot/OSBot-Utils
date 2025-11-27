import re
import pytest
from unittest                                                                       import TestCase
from typing                                                                         import Dict
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Base                                          import Type_Safe__Base
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                   import Safe_Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict
from osbot_utils.utils.Objects                                                      import base_types


class test_Type_Safe__Dict__as_base_class(TestCase):

    def test__basic_subclass_creation(self):            # Test creating a simple Type_Safe__Dict subclass with class-level type definitions

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        # Create instance without arguments (uses class-level types)
        hash_map = Hash_Mapping()

        assert type(hash_map)               is Hash_Mapping
        assert hash_map.expected_key_type   is Safe_Str__Hash
        assert hash_map.expected_value_type is str
        assert len(hash_map)                == 0

        assert hash_map.obj() == __()

        error_message_1 = "Expected 'Safe_Str__Hash', but got 'bool'"
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            hash_map[True] = 'abc'                                       # confirm run-time type safety is working

        error_message_2 = "Expected 'str', but got 'bool'"
        with pytest.raises(TypeError, match=re.escape(error_message_2)):
            hash_map['abc1234567'] = True                                       # confirm run-time type safety is working

        hash_map['aaa1234567'] = 'aaa'
        hash_map['bbb1234567'] = 'bbb'

        assert hash_map.obj() == __(aaa1234567='aaa' ,
                                    bbb1234567='bbb' )

        assert base_types(hash_map) == [Type_Safe__Dict, Type_Safe__Base, dict, object, object]

        assert hash_map.expected_key_type   is Safe_Str__Hash
        assert hash_map.expected_value_type is str
        assert len(hash_map)                == 2

    def test__subclass_with_initial_data(self):         # Test creating subclass instance with initial data

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        # Create with initial data
        hash_map = Hash_Mapping({'aaa1234567': 'Some text'})

        assert hash_map.obj () == __(aaa1234567='Some text')
        assert hash_map.json() == {'aaa1234567': 'Some text'}


        assert dict({'aaa1234567': 'Some text'}) == {'aaa1234567': 'Some text'}

        error_message_1 = "Type Dict cannot be instantiated; use dict() instead"
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            Dict({'aaa1234567': 'Some text'})

        assert len(hash_map) == 1
        assert hash_map['aaa1234567'] == 'Some text'
        assert isinstance(list(hash_map.keys())[0], Safe_Str__Hash)

        error_message_2 = "in Safe_Str__Hash, value must be exactly 10 characters long (was 6)"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            Hash_Mapping({'abc123': 'Some text'})

        error_message_3 = "Expected 'str', but got 'int'"
        with pytest.raises(TypeError, match=re.escape(error_message_3)):
            Hash_Mapping({'aaa1234567': 42})

    def test__subclass_type_enforcement(self):      # Test that subclass enforces types from class-level definitions

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()

        # Valid assignments (with auto-conversion)
        hash_map['aaa1234567'] = 'Text value'
        hash_map[Safe_Str__Hash('bbb1234567')] = 'Another value'

        assert len(hash_map) == 2
        assert all(isinstance(k, Safe_Str__Hash) for k in hash_map.keys())

        # Invalid assignments should raise
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            hash_map['ccc1234567'] = 123

    def test__subclass_in_type_safe_class(self):
        """Test using Type_Safe__Dict subclass as a field in Type_Safe class"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            content: str
            hashes: Hash_Mapping

        doc = Document()

        assert type(doc.hashes) is Hash_Mapping
        assert doc.hashes.expected_key_type is Safe_Str__Hash
        assert doc.hashes.expected_value_type is str

        # Use the hash mapping
        doc.hashes['abc1234567'] = 'Content A'
        doc.hashes['def4567890'] = 'Content B'

        assert len(doc.hashes) == 2
        assert doc.hashes['abc1234567'] == 'Content A'

    def test__subclass_json_serialization(self):
        """Test that subclass serializes to plain dict structure"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Hash_Mapping

        doc = Document(title='Test Doc')
        doc.hashes['abc1234567'] = 'Value A'
        doc.hashes['def4567890'] = 'Value B'

        json_data = doc.json()

        # Should serialize to plain dict
        assert json_data == {
            'title': 'Test Doc',
            'hashes': {
                'abc1234567': 'Value A',
                'def4567890': 'Value B'
            }
        }

        # Keys should be plain strings in JSON
        assert type(json_data['hashes']) is dict
        assert all(type(k) is str for k in json_data['hashes'].keys())

    def test__subclass_from_json_deserialization(self):
        """Test that subclass can be deserialized from JSON"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Hash_Mapping

        json_data = {
            'title': 'Test Doc',
            'hashes': {
                'abc1234567': 'Value A',
                'def4567890': 'Value B'
            }
        }

        doc = Document.from_json(json_data)

        assert type(doc) is Document
        assert type(doc.hashes) is Hash_Mapping
        assert doc.hashes.expected_key_type is Safe_Str__Hash
        assert doc.hashes.expected_value_type is str

        # Keys should be Safe_Str__Hash instances
        assert all(isinstance(k, Safe_Str__Hash) for k in doc.hashes.keys())

        # Values correct
        assert doc.hashes['abc1234567'] == 'Value A'
        assert doc.hashes['def4567890'] == 'Value B'

    def test__subclass_round_trip(self):
        """Test full round-trip: create → json → from_json"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Hash_Mapping

        # Create original
        original = Document(title='Original')
        original.hashes['aaa1111111'] = 'First'
        original.hashes['bbb2222222'] = 'Second'

        # Serialize
        json_data = original.json()

        # Deserialize
        restored = Document.from_json(json_data)

        # Should be equivalent
        assert restored.title == original.title
        assert len(restored.hashes) == len(original.hashes)
        assert restored.hashes['aaa1111111'] == 'First'
        assert restored.hashes['bbb2222222'] == 'Second'

        # Should serialize to same JSON
        assert restored.json() == json_data

    def test__subclass_with_type_safe_values(self):
        """Test subclass with Type_Safe objects as values"""

        class Item(Type_Safe):
            name: str
            value: int

        class Item_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Id
            expected_value_type = Item

        class Container(Type_Safe):
            items: Item_Mapping

        container = Container()

        # Add items
        container.items['item-1'] = Item(name='First', value=10)
        container.items['item-2'] = Item(name='Second', value=20)

        assert len(container.items) == 2
        assert type(container.items['item-1']) is Item
        assert container.items['item-1'].name == 'First'

        # Test JSON
        json_data = container.json()
        assert json_data == {
            'items': {
                'item-1': {'name': 'First', 'value': 10},
                'item-2': {'name': 'Second', 'value': 20}
            }
        }

        # Test round-trip
        restored = Container.from_json(json_data)
        assert type(restored.items['item-1']) is Item
        assert restored.items['item-1'].name == 'First'

    def test__subclass_with_nested_dict_values(self):
        """Test subclass with nested dict as values"""

        class Config_Section_Mapping(Type_Safe__Dict):
            expected_key_type   = str
            expected_value_type = Dict[str, str]

        class Config(Type_Safe):
            sections: Config_Section_Mapping

        config = Config()
        config.sections['database'] = {'host': 'localhost', 'port': '5432'}
        config.sections['cache'] = {'enabled': 'true', 'ttl': '300'}

        json_data = config.json()
        assert json_data == {
            'sections': {
                'database': {'host': 'localhost', 'port': '5432'},
                'cache': {'enabled': 'true', 'ttl': '300'}
            }
        }

    def test__multiple_subclasses(self):
        """Test multiple different subclasses in same Type_Safe class"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Id_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Id
            expected_value_type = int

        class Multi_Map(Type_Safe):
            hashes: Hash_Mapping
            ids: Id_Mapping

        multi = Multi_Map()

        # Populate different mappings
        multi.hashes['abc1234567'] = 'Hash value'
        multi.ids['id-001'] = 42

        assert type(multi.hashes) is Hash_Mapping
        assert type(multi.ids) is Id_Mapping

        # Different type enforcement
        assert all(isinstance(k, Safe_Str__Hash) for k in multi.hashes.keys())
        assert all(isinstance(k, Safe_Id) for k in multi.ids.keys())

        # JSON serialization
        json_data = multi.json()
        assert json_data == {
            'hashes': {'abc1234567': 'Hash value'},
            'ids': {'id-001': 42}
        }

    def test__subclass_inheritance_chain(self):
        """Test creating subclass of a subclass"""

        class Base_Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Extended_Hash_Mapping(Base_Hash_Mapping):
            # Inherits expected types from Base_Hash_Mapping
            pass

        mapping = Extended_Hash_Mapping()

        assert mapping.expected_key_type is Safe_Str__Hash
        assert mapping.expected_value_type is str

        mapping['abc1234567'] = 'Value'
        assert isinstance(list(mapping.keys())[0], Safe_Str__Hash)

    def test__subclass_with_obj_id(self):
        """Test subclass using Obj_Id as key type"""

        class Obj_Id_Mapping(Type_Safe__Dict):
            expected_key_type   = Obj_Id
            expected_value_type = str

        class Registry(Type_Safe):
            objects: Obj_Id_Mapping

        registry = Registry()

        obj_id_1 = Obj_Id()
        obj_id_2 = Obj_Id()

        registry.objects[obj_id_1] = 'Object One'
        registry.objects[obj_id_2] = 'Object Two'

        assert len(registry.objects) == 2
        assert registry.objects[obj_id_1] == 'Object One'
        assert all(isinstance(k, Obj_Id) for k in registry.objects.keys())

    def test__subclass_empty_dict_json(self):
        """Test that empty subclass serializes to empty dict"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Hash_Mapping

        doc = Document(title='Empty Doc')

        json_data = doc.json()
        assert json_data == {
            'title': 'Empty Doc',
            'hashes': {}
        }

    def test__subclass_with_get_method(self):
        """Test that get() method works correctly with subclass"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()
        hash_map['abc1234567'] = 'Value'

        # Test get with existing key
        assert hash_map.get('abc1234567') == 'Value'
        assert hash_map.get(Safe_Str__Hash('abc1234567')) == 'Value'

        # Test get with missing key
        assert hash_map.get('ccc1234567') is None
        assert hash_map.get('ddd1234567', 'default') == 'default'

    def test__subclass_with_keys_and_values(self):
        """Test keys() and values() methods return Type_Safe__List"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()
        hash_map['aaa1111111'] = 'First'
        hash_map['bbb2222222'] = 'Second'

        from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List

        keys = hash_map.keys()
        assert type(keys) is Type_Safe__List
        assert keys.expected_type is Safe_Str__Hash
        assert len(keys) == 2

        values = hash_map.values()
        assert type(values) is Type_Safe__List
        assert values.expected_type is str
        assert len(values) == 2

    def test__subclass_with_contains(self):
        """Test __contains__ works with type conversion"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()
        hash_map['abc1234567'] = 'Value'

        # Should work with both string and Safe_Str__Hash
        assert 'abc1234567' in hash_map
        assert Safe_Str__Hash('abc1234567') in hash_map
        assert 'missing123' not in hash_map

    def test__subclass_initialization_validates_types(self):
        """Test that initialization with invalid types raises errors"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        # Valid initialization
        hash_map = Hash_Mapping({'abc1234567': 'Valid'})
        assert len(hash_map) == 1

        # Invalid value type
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            Hash_Mapping({'abc1234567': 123})

    def test__subclass_obj_method(self):
        """Test that obj() method works correctly with subclass"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Hash_Mapping

        doc = Document(title='Test')
        doc.hashes['abc1234567'] = 'Value A'
        doc.hashes['def4567890'] = 'Value B'

        obj = doc.obj()

        assert obj == __(title='Test',
                        hashes=__(abc1234567='Value A',
                                 def4567890='Value B'))

    def test__subclass_with_primitive_key_and_primitive_value(self):
        """Test subclass with both key and value as Type_Safe__Primitive"""

        class Safe_Key(Type_Safe__Primitive, str):
            pass

        class Safe_Value(Type_Safe__Primitive, str):
            pass

        class Primitive_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Key
            expected_value_type = Safe_Value

        mapping = Primitive_Mapping()
        mapping['key1'] = 'value1'

        # Both should be converted
        keys = list(mapping.keys())
        values = list(mapping.values())

        assert type(keys[0]) is Safe_Key
        assert type(values[0]) is Safe_Value

        # JSON should have primitives
        json_data = mapping.json()
        assert json_data == {'key1': 'value1'}
        assert type(list(json_data.keys())[0]) is str
        assert type(list(json_data.values())[0]) is str

    def test__subclass_with_none_in_optional(self):
        """Test subclass can handle None values in Optional fields"""

        from typing import Optional

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Document(Type_Safe):
            title: str
            hashes: Optional[Hash_Mapping]

        # Can be None
        doc1 = Document(title='No hashes', hashes=None)
        assert doc1.hashes is None

        # Can be mapping
        doc2 = Document(title='With hashes')
        doc2.hashes = Hash_Mapping()
        doc2.hashes['abc1234567'] = 'Value'
        assert len(doc2.hashes) == 1

    def test__subclass_error_message_clarity(self):
        """Test that error messages clearly identify the subclass"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()

        # Error should mention the actual types
        with pytest.raises(TypeError) as exc_info:
            hash_map['abc1234567'] = 123

        error_msg = str(exc_info.value)
        assert 'str' in error_msg
        assert 'int' in error_msg

    def test__subclass_comparison_with_regular_dict(self):
        """Test that subclass can be compared with regular dict"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()
        hash_map['abc1234567'] = 'Value'

        # Compare with dict
        regular_dict = {'abc1234567': 'Value'}

        # Note: Type_Safe__Dict won't be equal to regular dict due to keys being different types
        # But json() should match
        assert hash_map.json() == regular_dict

    def test__subclass_nested_in_lists(self):
        """Test subclass used as element type in lists"""

        from typing import List

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            mappings: List[Hash_Mapping]

        container = Container()

        # Add mappings
        map1 = Hash_Mapping({'aaa1111111': 'First'})
        map2 = Hash_Mapping({'bbb2222222': 'Second'})

        container.mappings = [map1, map2]

        assert len(container.mappings) == 2
        assert type(container.mappings[0]) is Hash_Mapping
        assert container.mappings[0]['aaa1111111'] == 'First'

        # JSON serialization
        json_data = container.json()
        assert json_data == {
            'mappings': [
                {'aaa1111111': 'First'},
                {'bbb2222222': 'Second'}
            ]
        }

    def test__real_world_html_transformation_use_case(self):
        """Test the actual use case: HTML transformation hash mapping"""

        class Safe_Str__Comprehend__Text(Type_Safe__Primitive, str):
            """Simulating the AWS Comprehend text type"""
            pass

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = Safe_Str__Comprehend__Text

        class HTML_Transformation_Step_1(Type_Safe):
            html_dict: Dict
            hash_mapping: Hash_Mapping

        # Create transformation step
        step = HTML_Transformation_Step_1()
        step.html_dict = {'tag': 'html', 'content': 'example'}

        # Add hash mappings (simulating content extraction)
        step.hash_mapping['9b68eca2b0'] = 'Test content!'
        step.hash_mapping['a1b2c3d4e5'] = 'More content!'

        # Verify types
        assert type(step.hash_mapping) is Hash_Mapping
        assert all(isinstance(k, Safe_Str__Hash) for k in step.hash_mapping.keys())
        assert all(isinstance(v, Safe_Str__Comprehend__Text) for v in step.hash_mapping.values())

        # Test JSON
        json_data = step.json()
        assert json_data['hash_mapping'] == {
            '9b68eca2b0': 'Test content!',
            'a1b2c3d4e5': 'More content!'
        }

        # Test obj()
        obj = step.obj()
        assert obj.hash_mapping._9b68eca2b0 == 'Test content!'
        assert obj.hash_mapping.a1b2c3d4e5 == 'More content!'

        # Test round-trip
        restored = HTML_Transformation_Step_1.from_json(json_data)
        assert type(restored.hash_mapping) is Hash_Mapping
        assert restored.hash_mapping['9b68eca2b0'] == 'Test content!'

    def test__subclass_update_method(self):
        """Test that update() works with subclass"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping()
        hash_map['aaa1111111'] = 'First'


        # Update with dict
        hash_map.update({'bbb2222222': 'Second', 'ccc3333333': 'Third'})            # BUG

        assert hash_map.obj() == __(aaa1111111='First',
                                    bbb2222222='Second',
                                    ccc3333333='Third')
        assert len(hash_map) == 3
        assert hash_map['bbb2222222'] == 'Second'

        keys = hash_map.keys()
        assert type(keys[0]) is Safe_Str__Hash
        assert type(keys[1]) is Safe_Str__Hash
        assert type(keys[2]) is Safe_Str__Hash

        assert all(isinstance(k, Safe_Str__Hash) for k in hash_map.keys())

    def test__subclass_clear_method(self):
        """Test that clear() works with subclass"""

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping({'aaa1111111': 'First', 'bbb2222222': 'Second'})
        assert len(hash_map) == 2

        hash_map.clear()
        assert len(hash_map) == 0

        # Should still enforce types after clear
        hash_map['ccc3333333'] = 'Third'
        assert isinstance(list(hash_map.keys())[0], Safe_Str__Hash)


    def test__compatible_type_safe_dict_subclasses(self):
        '''Test assignment between compatible Type_Safe__Dict subclasses'''

        class Hash_Mapping_A(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Hash_Mapping_B(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container_A(Type_Safe):
            data: Hash_Mapping_A

        class Container_B(Type_Safe):
            data: Hash_Mapping_B

        # Create instance with A
        mapping_a = Hash_Mapping_A({'abc1234567': 'value'})

        # Should be able to use in B (compatible types)
        container_b = Container_B(data=mapping_a)  # ✅ Works!

        assert type(container_b.data) is Hash_Mapping_B  # Converted
        assert container_b.data['abc1234567'] == 'value'


    def test__incompatible_type_safe_dict_subclasses(self):
        '''Test that incompatible subclasses still fail'''

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Id_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Id  # Different!
            expected_value_type = int      # Different!

        class Container(Type_Safe):
            data: Hash_Mapping

        id_mapping = Id_Mapping({'id-1': 42})

        # Should fail - incompatible types
        error_message = "Expected 'Safe_Str__Hash', but got 'Safe_Id'"
        with pytest.raises(TypeError, match=re.escape(error_message)):
            Container(data=id_mapping)  # ❌ Fails correctly


    def test__type_safe_dict_to_generic_dict_annotation(self):                  # Test that Type_Safe__Dict subclass can be assigned to generic Dict annotation

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            data: Dict[Safe_Str__Hash, str]  # Generic Dict, not subclass

        mapping = Hash_Mapping({'abc1234567': 'value'})

        # Should work - compatible with generic Dict annotation
        container = Container(data=mapping)

        assert type(container.data) is Type_Safe__Dict  # Becomes Type_Safe__Dict
        assert container.data['abc1234567'] == 'value'



    def test__type_safe_dict_subclass_in_from_json(self):           # Test that from_json handles Type_Safe__Dict subclass conversion

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            data: Hash_Mapping

        json_data = {
            'data': {
                'abc1234567': 'value',
                'def4567890': 'another'
            }
        }

        container = Container.from_json(json_data)

        assert type(container.data) is Hash_Mapping
        assert len(container.data) == 2
        assert all(isinstance(k, Safe_Str__Hash) for k in container.data.keys())


    def test__type_safe_dict_subclass_round_trip_with_conversion(self):     # Test full round-trip with subclass conversion

        class Hash_Mapping_A(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Hash_Mapping_B(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container_A(Type_Safe):
            data: Hash_Mapping_A

        class Container_B(Type_Safe):
            data: Hash_Mapping_B

        # Create with A
        container_a = Container_A()
        container_a.data['abc1234567'] = 'value'

        # Serialize
        json_data = container_a.json()

        # Deserialize as B
        container_b = Container_B.from_json(json_data)

        # Should work and be correct type
        assert type(container_b.data) is Hash_Mapping_B
        assert container_b.data['abc1234567'] == 'value'



    def test__empty_type_safe_dict_subclass_conversion(self):           # Test conversion of empty Type_Safe__Dict subclasses

        class Hash_Mapping_A(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Hash_Mapping_B(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            data: Hash_Mapping_B

        # Empty mapping of type A
        empty_a = Hash_Mapping_A()

        # Should convert to B (even though empty)
        container = Container(data=empty_a)

        assert type(container.data) is Hash_Mapping_B
        assert len(container.data) == 0


    def test__type_safe_dict_subclass_with_incompatible_values(self):       # Test that conversion fails cleanly when values are incompatible

        class String_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Int_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = int

        class Container(Type_Safe):
            data: Int_Mapping

        string_mapping = String_Mapping({'abc1234567': 'not_an_int'})

        # Should fail - can't convert string to int
        error_message = "Expected 'int', but got 'str'"
        with pytest.raises(TypeError, match=re.escape(error_message)):
            Container(data=string_mapping)


    def test__plain_dict_to_type_safe_dict_subclass(self):          # Test that plain dict is converted to Type_Safe__Dict subclass

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            data: Hash_Mapping

        # Plain dict with compatible data
        plain_dict = {'abc1234567': 'value'}

        container = Container(data=plain_dict)

        assert type(container.data) is Hash_Mapping
        assert container.data['abc1234567'] == 'value'

    def test__nested_type_safe_dict_subclass_conversion(self):      # Test conversion with nested Type_Safe__Dict subclasses

        class Inner_Mapping(Type_Safe__Dict):
            expected_key_type   = str
            expected_value_type = int

        class Outer_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Id
            expected_value_type = Inner_Mapping

        class Container(Type_Safe):
            data: Outer_Mapping

        #error_message = "On Container, invalid type for attribute 'data'. Expected '<class 'test_Type_Safe__Dict__as_base_class.test_Type_Safe__Dict__as_base_class.test__bug__nested_type_safe_dict_subclass_conversion.<locals>.Outer_Mapping'>' but got '<class 'dict'>'"
        #with pytest.raises(ValueError, match=re.escape(error_message)):
        # error_message = "Expected 'Inner_Mapping', but got 'dict'"
        # with pytest.raises(TypeError, match=re.escape(error_message)):
        #     container = Container(data={'outer-1':{}})

        container = Container(data={'outer-1':{}})
        assert container.obj()     == __(data=__(outer_1=__()))
        assert type(container.data) is Outer_Mapping

        container = Container(data={
            'outer-1': {'inner-1': 1, 'inner-2': 2},
            'outer-2': {'inner-3': 3}
        })

        assert container.obj() == __(data=__(outer_1=__(inner_1=1, inner_2=2), outer_2=__(inner_3=3)))
        assert type(container.data['outer-1']) is Inner_Mapping

        assert type(container.data) is Outer_Mapping
        assert container.data['outer-1']['inner-1'] == 1

    def test__deeply_nested_type_safe_dict_subclass(self):
        class Level3_Mapping(Type_Safe__Dict):
            expected_key_type = str
            expected_value_type = int

        class Level2_Mapping(Type_Safe__Dict):
            expected_key_type = str
            expected_value_type = Level3_Mapping

        class Level1_Mapping(Type_Safe__Dict):
            expected_key_type = str
            expected_value_type = Level2_Mapping

        class Container(Type_Safe):
            data: Level1_Mapping

        # Triple nested plain dict
        container = Container(data={
            'level1': {
                'level2': {
                    'level3': 42
                }
            }
        })

        assert type(container.data) is Level1_Mapping
        assert type(container.data['level1']) is Level2_Mapping
        assert type(container.data['level1']['level2']) is Level3_Mapping


    def test__from_json_with_nested_dict_subclasses(self):
        class Inner_Mapping(Type_Safe__Dict):
            expected_key_type = str
            expected_value_type = int

        class Outer_Mapping(Type_Safe__Dict):
            expected_key_type = Safe_Id
            expected_value_type = Inner_Mapping

        class Container(Type_Safe):
            data: Outer_Mapping

        json_data = {
            'data': {
                'outer-1': {'inner-1': 1, 'inner-2': 2},
                'outer-2': {'inner-3': 3}
            }
        }

        container = Container.from_json(json_data)

        assert type(container.data) is Outer_Mapping
        assert type(container.data['outer-1']) is Inner_Mapping


    def test__assign_plain_dict_to_existing_field(self):
        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            data: Hash_Mapping

        container = Container()

        # Assign plain dict after initialization
        container.data = {'abc1234567': 'value'}

        # Should convert to Hash_Mapping
        assert type(container.data) is Hash_Mapping

    def test__type_safe_object_containing_dict_subclass(self):
        class Item(Type_Safe):
            name: str
            value: int

        class Item_Mapping(Type_Safe__Dict):
            expected_key_type = Safe_Id
            expected_value_type = Item

        class Container(Type_Safe):
            items: Item_Mapping

        # Plain dict with plain dict values
        container = Container(items={
            'item-1': {'name': 'First', 'value': 10}
        })

        assert type(container.items) is Item_Mapping
        assert type(container.items['item-1']) is Item

    def test__subclass_preserves_type_on_copy_and_or(self):
        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping({'abc1234567': 'value'})

        # copy() should return Hash_Mapping, not Type_Safe__Dict
        copied = hash_map.copy()
        assert type(copied) is Hash_Mapping

        # | should return Hash_Mapping
        merged = hash_map | {'def1234567': 'other'}
        assert type(merged) is Hash_Mapping

        # fromkeys should return Hash_Mapping
        from_keys = Hash_Mapping.fromkeys(['aaa1234567', 'bbb1234567'], 'default')
        assert type(from_keys) is Hash_Mapping


    def test__regression__type_safe_dict_subclass__operations_dont_preserve_subclass_type(self):

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type   = Safe_Str__Hash
            expected_value_type = str

        hash_map = Hash_Mapping({'abc1234567': 'value'})
        assert type(hash_map) is Hash_Mapping

        # BUG 1: copy() returns Type_Safe__Dict instead of Hash_Mapping
        copied = hash_map.copy()
        assert type(copied) is not Type_Safe__Dict            # FIXED: should be Hash_Mapping
        assert type(copied) is      Hash_Mapping              # FIXED: should be Hash_Mapping
        # assert type(copied) is Type_Safe__Dict               # BUG: should be Hash_Mapping
        # assert type(copied) is not Hash_Mapping              # BUG: should be Hash_Mapping

        # BUG 2: | operator returns Type_Safe__Dict instead of Hash_Mapping
        merged = hash_map | {'def1234567': 'other'}
        assert type(merged) is not Type_Safe__Dict               # FIXED
        assert type(merged) is Hash_Mapping                      # FIXED
        # assert type(merged) is Type_Safe__Dict               # BUG: should be Hash_Mapping
        # assert type(merged) is not Hash_Mapping              # BUG: should be Hash_Mapping

        # BUG 3: |= works correctly (modifies in place, so type is preserved)
        hash_map |= {'aaa1234567': 'third'}                  # FIXED
        assert type(hash_map) is Hash_Mapping                # This one is OK

        # BUG 4: fromkeys returns Type_Safe__Dict instead of Hash_Mapping
        from_keys = Hash_Mapping.fromkeys(['aaa1234567', 'bbb1234567'], 'default')
        assert type(from_keys) is not Type_Safe__Dict          # FIXED
        assert type(from_keys) is Hash_Mapping                 # FIXED
        # assert type(from_keys) is Type_Safe__Dict            # BUG: should be Hash_Mapping
        # assert type(from_keys) is not Hash_Mapping           # BUG: should be Hash_Mapping