import threading
import pytest
from unittest                                                          import TestCase
from osbot_utils.testing.__                                            import __
from osbot_utils.type_safe.Type_Safe                                   import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                        import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple import Type_Safe__Tuple


class test_Type_Safe__Tuple(TestCase):

    def test__tuple_with_type_safe_primitives(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class Schema(Type_Safe):
            str_tuple: tuple[An_Safe_Str, An_Safe_Str, An_Safe_Str]

        schema     = Schema(str_tuple=('a', 'b', 'c'))
        round_trip = Schema.from_json(schema.json())
        assert type(schema)                is Schema
        assert type(round_trip)            is Schema
        assert type(schema.str_tuple    )  is Type_Safe__Tuple
        assert type(round_trip.str_tuple)  is Type_Safe__Tuple
        assert schema.json()               == {'str_tuple': ['a', 'b', 'c']}
        assert schema.obj()                == __(str_tuple=['a', 'b', 'c'])
        assert round_trip.json()           == schema.json()
        assert round_trip.obj ()           == schema.obj ()


    def test__tuple_with_mixed_primitive_types(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class An_Safe_Int(Type_Safe__Primitive, int):
            pass

        class Schema(Type_Safe):
            mixed_tuple: tuple[An_Safe_Str, An_Safe_Int, float, str]

        schema = Schema(mixed_tuple=('hello', 42, 3.14, 'world'))

        # Verify types are correctly converted/preserved
        assert isinstance(schema.mixed_tuple[0], An_Safe_Str)
        assert isinstance(schema.mixed_tuple[1], An_Safe_Int)
        assert isinstance(schema.mixed_tuple[2], float)
        assert isinstance(schema.mixed_tuple[3], str)

        # JSON should have pure primitives
        assert schema.json() == {'mixed_tuple': ['hello', 42, 3.14, 'world']}

    def test__tuple_with_type_safe_objects(self):
        class Inner(Type_Safe):
            value: int

        class Schema(Type_Safe):
            obj_tuple: tuple[Inner, Inner]

        # Test with dict conversion
        schema = Schema(obj_tuple=({'value': 1}, {'value': 2}))

        assert isinstance(schema.obj_tuple[0], Inner)
        assert isinstance(schema.obj_tuple[1], Inner)
        assert schema.obj_tuple[0].value == 1
        assert schema.obj_tuple[1].value == 2

        # JSON should serialize properly
        assert schema.json() == {'obj_tuple': [{'value': 1}, {'value': 2}]}

    def test__tuple_validation_errors(self):
        class An_Safe_Int(Type_Safe__Primitive, int):
            pass

        class Schema(Type_Safe):
            int_tuple: tuple[An_Safe_Int, An_Safe_Int]

        # Wrong number of elements
        with pytest.raises(ValueError, match="Expected 2 elements, got 3"):
            Schema(int_tuple=(1, 2, 3))

        with pytest.raises(ValueError, match="Expected 2 elements, got 1"):
            Schema(int_tuple=(1,))

        # Invalid conversion
        with pytest.raises(TypeError, match="In Type_Safe__Tuple: Could not convert"):
            Schema(int_tuple=('not_an_int', 2))

    def test__empty_tuple(self):
        class Schema(Type_Safe):
            empty_tuple: tuple[()]

        schema = Schema(empty_tuple=())
        assert schema.empty_tuple == ()
        assert schema.json() == {'empty_tuple': []}

        # Should reject non-empty tuples
        with pytest.raises(ValueError, match="Expected 0 elements, got 1"):
            Schema(empty_tuple=(1,))

    def test__tuple_round_trip(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class Inner(Type_Safe):
            name: str
            count: int

        class Schema(Type_Safe):
            complex_tuple: tuple[An_Safe_Str, Inner, int]

        original = Schema(complex_tuple=('test', {'name': 'item', 'count': 5}, 42))

        # Serialize to JSON
        json_data = original.json()
        assert json_data == {'complex_tuple': ['test', {'name': 'item', 'count': 5}, 42]}

        # Deserialize back
        restored = Schema.from_json(json_data)

        # Verify types are restored correctly
        assert type(restored.complex_tuple[0]) is not str
        assert type(restored.complex_tuple[0]) is     An_Safe_Str

        assert isinstance(restored.complex_tuple[0], An_Safe_Str)
        assert isinstance(restored.complex_tuple[1], Inner      )
        assert isinstance(restored.complex_tuple[2], int        )
        assert restored.complex_tuple[1].name == 'item'
        assert restored.complex_tuple[1].count == 5

    def test__tuple_with_nested_collections(self):
        class Schema(Type_Safe):
            nested: tuple[list[int], dict[str, str]]

        schema = Schema(nested=([1, 2, 3], {'key': 'value'}))

        assert schema.nested[0] == [1, 2, 3]
        assert schema.nested[1] == {'key': 'value'}
        assert schema.json() == {'nested': [[1, 2, 3], {'key': 'value'}]}

    def test__tuple_repr(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple import Type_Safe__Tuple

        # Test repr with different types
        tuple_instance = Type_Safe__Tuple(expected_types=(An_Safe_Str, int, str),
                                          items=('a', 1, 'b'))

        assert 'tuple[An_Safe_Str, int, str] with 3 elements' in repr(tuple_instance)

    def test__tuple_with_safe_id(self):
        from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id

        class Schema(Type_Safe):
            id_tuple: tuple[Safe_Id, Safe_Id]

        schema = Schema(id_tuple=('id-1', 'id-2'))

        assert isinstance(schema.id_tuple[0], Safe_Id)
        assert isinstance(schema.id_tuple[1], Safe_Id)
        assert schema.id_tuple[0] == 'id-1'
        assert schema.id_tuple[1] == 'id-2'

        # JSON should have pure strings
        assert schema.json() == {'id_tuple': ['id-1', 'id-2']}

    def test__tuple_immutability(self):
        class Schema(Type_Safe):
            int_tuple: tuple[int, int, int]

        schema = Schema(int_tuple=(1, 2, 3))

        # Tuples should be immutable
        with pytest.raises(TypeError, match="'Type_Safe__Tuple' object does not support item assignment"):
            schema.int_tuple[0] = 10

        # But can replace the whole tuple
        schema.int_tuple = (4, 5, 6)
        assert schema.int_tuple == (4, 5, 6)

    def test_json__with_unserializable_items(self):             # Test that Type_Safe__Tuple.json() handles unserializable items gracefully
        import socket

        # Create tuple with mixed serializable and unserializable items
        items = Type_Safe__Tuple(expected_types=(str, int, object, bool, object, object),
                                 items=('hello', 42, threading.RLock(), True, 3 + 4j, socket.socket()))

        result = items.json()

        # Verify serialization
        assert result[0] == 'hello'
        assert result[1] == 42
        assert result[2] is None  # RLock becomes None
        assert result[3] is True
        assert result[4] is None  # Complex number becomes None
        assert result[5] is None  # Socket becomes None

        items[5].close()  # Clean up socket

    def test_json__with_nested_dict_containing_unserializable(self):        # Test Type_Safe__Tuple with nested dict containing unserializable objects

        rlock = threading.RLock()
        data = Type_Safe__Tuple(
            expected_types=(str, dict, int),
            items=( 'config',
                    {'host': 'localhost', '_lock': rlock, 'port': 8080},
                    100 ) )

        result = data.json()

        assert result[0]          == 'config'
        assert result[1]['host' ] == 'localhost'
        assert result[1]['_lock'] is None       # FIXED: Nested unserializable becomes None
        #assert result[1]['_lock'] is not None  # BUG
        #assert result[1]['_lock'] == rlock     # BUG
        assert result[1]['port' ] == 8080
        assert result[2]          == 100

    def test_json__with_nested_list_containing_unserializable(self):            # Test Type_Safe__Tuple with nested list containing unserializable objects

        data = Type_Safe__Tuple(
            expected_types=(str, list, bool),
            items=(
                'items',
                [1, threading.RLock(), 3, 3 + 4j, 5],
                False
            )
        )

        result = data.json()

        assert result[0] == 'items'
        assert result[1][0] == 1
        assert result[1][1] is None  # RLock becomes None
        assert result[1][2] == 3
        assert result[1][3] is None  # Complex becomes None
        assert result[1][4] == 5
        assert result[2] is False

    def test_obj__with_unserializable_items(self):      # Test that Type_Safe__Tuple.obj() works with unserializable items

        data = Type_Safe__Tuple(
            expected_types=(str, object, int),
            items=('start', threading.RLock(), 42)
        )

        result = data.obj()

        assert result == ['start', None, 42]

    def test_json__with_all_unserializable(self):           # Test Type_Safe__Tuple with all unserializable items

        data = Type_Safe__Tuple(
            expected_types=(object, object, object),
            items=(threading.RLock(), 3 + 4j, threading.Semaphore())
        )

        result = data.json()

        # All items should become None or their serializable representation
        assert result[0] is None  # RLock
        assert result[1] is None  # Complex number
        # Semaphore might serialize to dict with _cond and _value, or None

    def test_roundtrip__preserves_serializable_values(self):        # Test that round-trip preserves serializable values and handles unserializable

        original = Type_Safe__Tuple(
            expected_types=(str, int, object, bool),
            items=('data', 100, threading.RLock(), True)
        )

        json_data = original.json()

        # Verify JSON output
        assert json_data[0] == 'data'
        assert json_data[1] == 100
        assert json_data[2] is None  # Unserializable becomes None
        assert json_data[3] is True