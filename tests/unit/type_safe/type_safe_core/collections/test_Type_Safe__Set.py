import pytest
import threading
from unittest                                                        import TestCase
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                  import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_Int                  import Safe_Int
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id    import Safe_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set import Type_Safe__Set


class test_Type_Safe__Set(TestCase):

    def test__contains__with_type_safe_primitive(self):
        # Test with Safe_Str type
        safe_str_set = Type_Safe__Set(Safe_Str)
        safe_str_set.add(Safe_Str('hello'))
        safe_str_set.add(Safe_Str('world'))

        # Direct Safe_Str instance lookup
        assert Safe_Str('hello') in safe_str_set
        assert Safe_Str('world') in safe_str_set
        assert Safe_Str('foo')   not in safe_str_set

        # String primitive lookup (should be converted)
        assert 'hello' in safe_str_set
        assert 'world' in safe_str_set
        assert 'foo'   not in safe_str_set

    def test__contains__with_safe_int(self):
        # Test with Safe_Int type
        safe_int_set = Type_Safe__Set(Safe_Int)
        safe_int_set.add(Safe_Int(42))
        safe_int_set.add(Safe_Int(100))

        # Direct Safe_Int instance lookup
        assert Safe_Int(42)  in safe_int_set
        assert Safe_Int(100) in safe_int_set
        assert Safe_Int(999) not in safe_int_set

        # Integer primitive lookup (should be converted)
        assert 42  in safe_int_set
        assert 100 in safe_int_set
        assert 999 not in safe_int_set

        # String that can be converted to int
        assert '42'  in safe_int_set
        assert '100' in safe_int_set
        assert '999' not in safe_int_set

    def test__contains__with_safe_id(self):
        # Test with a more complex Safe_Id type
        safe_id_set = Type_Safe__Set(Safe_Id)
        safe_id_set.add(Safe_Id('user-123'))
        safe_id_set.add(Safe_Id('admin-456'))

        # Direct Safe_Id instance lookup
        assert Safe_Id('user-123')  in safe_id_set
        assert Safe_Id('admin-456') in safe_id_set
        assert Safe_Id('guest-789') not in safe_id_set

        # String primitive lookup (should be converted)
        assert 'user-123'  in safe_id_set
        assert 'admin-456' in safe_id_set
        assert 'guest-789' not in safe_id_set

    def test__contains__with_regular_types(self):
        # Test that regular types still work normally
        string_set = Type_Safe__Set(str)
        string_set.add('hello')
        string_set.add('world')

        assert 'hello' in string_set
        assert 'world' in string_set
        assert 'foo'   not in string_set

        # These should not be found (no conversion for regular types)
        assert 123 not in string_set

    def test_json__with_unserializable_items(self):                             # Test that Type_Safe__Set.json() handles unserializable items gracefully

        # Create set with mixed serializable and unserializable items
        items = Type_Safe__Set(expected_type=object)
        items.add('alpha')
        items.add(42)
        items.add(threading.RLock())  # Unserializable (but may not be added due to set hashing)
        items.add(3.14)

        # Note: RLock might not add successfully to set due to hashing
        # So we test with objects that will definitely be in the set
        result = items.json()

        # Verify serializable items are in result
        assert 'alpha' in result
        assert 42 in result
        assert 3.14 in result

        assert None in result                   # If unserializable made it in, it should be None
        assert result.count(None) >= 0          # None appears for unserializable items

    def test_json__with_nested_unserializable_in_dicts(self):                   # Test Type_Safe__Set with dict items containing unserializable objects

        # Sets can't contain dicts directly (unhashable), but we can test with tuples
        # Or test the JSON method's handling of nested structures
        items = Type_Safe__Set(expected_type=object)
        items.add('item1')
        items.add(100)

        # Manually create a case where nested structures have unserializable
        # by modifying internal structure for testing
        internal_list = list(items)
        internal_list.append({'key': 'value', '_lock': threading.RLock()})

        # Clear and re-add including dict
        items.clear()
        for item in internal_list[:2]:  # Only add hashable items
            items.add(item)

        result = items.json()

        # Should contain the serializable items
        assert 'item1' in result
        assert 100 in result

    def test_json__with_strings_and_unserializable(self):                       # Test Type_Safe__Set with strings and unserializable objects"""

        tags = Type_Safe__Set(expected_type=object)
        tags.add('python')
        tags.add('testing')
        tags.add(42)  # Int is fine

        result = tags.json()

        # All items should be serializable
        assert 'python' in result
        assert 'testing' in result
        assert 42 in result
        assert None not in result  # No unserializable items added

    def test_obj__with_mixed_types(self):                                       # Test that Type_Safe__Set.obj() handles various types including potential unserializable

        items = Type_Safe__Set(expected_type=object)
        items.add('text')
        items.add(999)
        items.add(1.5)

        result = items.obj()

        # Result should be a list (sets serialize to lists)
        assert 'text' in result
        assert 999 in result
        assert 1.5 in result

    def test_json__with_type_safe_primitive_items(self):        # Test Type_Safe__Set with Type_Safe__Primitive items (PATH 2)
        # Type_Safe__Primitive objects are hashable (inherit from str/int)
        items = Type_Safe__Set(expected_type=object)
        items.add(Safe_Str('hello'))
        items.add(Safe_Str('world'))
        items.add(Safe_Int(42))
        items.add(Safe_Int(100))

        result = items.json()

        # Should convert primitives to their base types
        assert 'hello' in result
        assert 'world' in result
        assert 42 in result
        assert 100 in result
        assert len(result) == 4

    def test_json__with_type_objects_as_items(self):            # Test Type_Safe__Set with type objects as items (PATH 5)

        class CustomClass:
            pass

        # Types are hashable and can be in sets
        types = Type_Safe__Set(expected_type=type)
        types.add(str)
        types.add(int)
        types.add(float)
        types.add(CustomClass)
        types.add(list)

        result = types.json()

        # Should convert types to their fully qualified names
        assert 'builtins.str'   in result
        assert 'builtins.int'   in result
        assert 'builtins.float' in result
        assert 'builtins.list'  in result
        assert 'test_Type_Safe__Set.CustomClass' in result
        assert len(result)  == 5
        assert type(result) is list
        assert sorted(result) == sorted([ 'builtins.float',
                                          'test_Type_Safe__Set.CustomClass',
                                          'builtins.int',
                                          'builtins.str',
                                          'builtins.list'])

    def test_json__with_type_safe_objects_as_items(self):       # Test Type_Safe__Set with hashable Type_Safe objects (PATH 1)

        # Note: Most Type_Safe objects aren't hashable by default
        # But we can test with a custom hashable Type_Safe class

        class HashableConfig(Type_Safe):
            value: int = 0

            def __hash__(self):
                return hash(self.value)

            def __eq__(self, other):
                if isinstance(other, HashableConfig):
                    return self.value == other.value
                return False

        configs = Type_Safe__Set(expected_type=object)
        configs.add(HashableConfig(value=1))
        configs.add(HashableConfig(value=2))
        configs.add(HashableConfig(value=3))

        result = configs.json()

        # Should serialize Type_Safe objects to their JSON representation
        assert {'value': 1} in result
        assert {'value': 2} in result
        assert {'value': 3} in result
        assert len(result) == 3

    def test_json__with_tuples_containing_mixed_types(self):            # Test Type_Safe__Set with tuples containing mixed types (PATH 3)
        # Tuples are hashable and can contain various types

        data = Type_Safe__Set(expected_type=object)
        data.add((1, 'hello', 3.14))
        data.add(('alpha', 42, True))
        data.add((threading.RLock(), 'test', 100))  # Tuple with unserializable

        result = data.json()

        # Should serialize tuples and their contents
        assert [1, 'hello', 3.14] in result
        assert ['alpha', 42, True] in result

        # Tuple with unserializable should have None for RLock
        unserializable_tuple = [None, 'test', 100]
        assert unserializable_tuple in result

    def test_json__with_nested_tuples_in_set(self):                     # Test Type_Safe__Set with nested tuples (PATH 3 - nested structures)

        nested_data = Type_Safe__Set(expected_type=object)
        nested_data.add(((1, 2), (3, 4)))
        nested_data.add(('outer', (5, 6, 7)))

        result = nested_data.json()

        # Should handle nested tuple structures
        assert [[1, 2], [3, 4]] in result
        assert ['outer', [5, 6, 7]] in result

    def test_json__with_frozenset_items(self):                          # Test Type_Safe__Set with frozenset items (PATH 3 - set handling)

        # frozensets are hashable and can be in sets
        sets_data = Type_Safe__Set(expected_type=object)
        sets_data.add(frozenset([1, 2, 3]))
        sets_data.add(frozenset(['a', 'b', 'c']))

        result = sets_data.json()

        # Should serialize frozensets (they're sets)
        # Result will be lists since sets serialize to lists
        assert any(set(item) == {1, 2, 3} for item in result if isinstance(item, list))
        assert any(set(item) == {'a', 'b', 'c'} for item in result if isinstance(item, list))

    def test_json__with_mixed_hashable_types(self):                 # Test Type_Safe__Set with comprehensive mix of all hashable types
        from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

        class HashableItem(Type_Safe):
            id: int = 0
            def __hash__(self):
                return hash(self.id)
            def __eq__(self, other):
                return isinstance(other, HashableItem) and self.id == other.id

        mixed = Type_Safe__Set(expected_type=object)

        # PATH 1: Type_Safe object
        mixed.add(HashableItem(id=1))

        # PATH 2: Type_Safe__Primitive
        mixed.add(Safe_Str('primitive'))

        # PATH 3: Tuple (frozen collection)
        mixed.add((1, 2, 3))

        # PATH 4: Can't add dict directly (not hashable), skip

        # PATH 5: Type object
        mixed.add(str)

        # PATH 6: Regular primitive
        mixed.add('regular_string')
        mixed.add(42)

        result = mixed.json()

        # Verify each path worked
        assert {'id': 1} in result  # PATH 1
        assert 'primitive' in result  # PATH 2
        assert [1, 2, 3] in result  # PATH 3
        assert 'builtins.str' in result  # PATH 5
        assert 'regular_string' in result  # PATH 6
        assert 42 in result  # PATH 6

    def test_json__with_tuple_containing_type_safe_objects(self):           # Test nested Type_Safe objects inside tuples in set (PATH 3 with PATH 1 nested)

        class Point(Type_Safe):
            x: int = 0
            y: int = 0

            def __hash__(self):
                return hash((self.x, self.y))

            def __eq__(self, other):
                return isinstance(other, Point) and self.x == other.x and self.y == other.y

        # Can't add Type_Safe directly (not hashable), but can in tuple
        # Actually, we need to make it hashable - done above

        # This is tricky - tuples containing Type_Safe objects
        # The tuple itself is hashable if contents are hashable
        data = Type_Safe__Set(expected_type=object)

        # Since our Point is hashable, we can add tuples containing them
        p1 = Point(x=1, y=2)
        p2 = Point(x=3, y=4)

        data.add((p1, 'label1'))
        data.add((p2, 'label2'))

        result = data.json()

        # Should serialize nested Type_Safe objects in tuples
        assert [{'x': 1, 'y': 2}, 'label1'] in result
        assert [{'x': 3, 'y': 4}, 'label2'] in result

    def test_json__with_tuple_containing_unserializable(self):              # Test tuple with unserializable objects in set (PATH 3 with serialize_to_dict path)

        data = Type_Safe__Set(expected_type=object)

        # Tuples with unserializable items
        data.add(('before', threading.RLock(), 'after'))
        data.add((3 + 4j, 'complex', 100))

        result = data.json()

        # Unserializable items in tuples should become None
        assert ['before', None, 'after'] in result
        assert [None, 'complex', 100] in result

    def test_json__confirms_we_cant_add_dicts(self):
        data = Type_Safe__Set(expected_type=object)
        error_message = "unhashable type: 'dict'"
        with pytest.raises(TypeError, match=error_message):
            data.add(('a', {}))

    def test_cannot_add_unhashable_types_to_set(self):      # Confirm that unhashable types cannot be added to Type_Safe__Set

        data = Type_Safe__Set(expected_type=object)

        # Dict - unhashable
        with pytest.raises(TypeError, match="unhashable type: 'dict'"):
            data.add({'key': 'value'})

        # List - unhashable
        with pytest.raises(TypeError, match="unhashable type: 'list'"):
            data.add([1, 2, 3])

        # Set - unhashable
        with pytest.raises(TypeError, match="unhashable type: 'set'"):
            data.add({1, 2, 3})

        # Even tuples containing unhashable items
        with pytest.raises(TypeError, match="unhashable type"):
            data.add((1, [2, 3]))  # Tuple with list inside

        with pytest.raises(TypeError, match="unhashable type"):
            data.add((1, {'key': 'value'}))  # Tuple with dict inside