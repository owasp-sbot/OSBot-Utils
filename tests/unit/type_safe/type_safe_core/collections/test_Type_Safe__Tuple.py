import pytest
from unittest                                   import TestCase
from osbot_utils.testing.__                     import __
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class test_Type_Safe__Tuple(TestCase):

    def test__tuple_with_type_safe_primitives(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class Schema(Type_Safe):
            str_tuple: tuple[An_Safe_Str, An_Safe_Str, An_Safe_Str]

        schema = Schema(str_tuple=('a', 'b', 'c'))
        assert schema.json() == {'str_tuple': ['a', 'b', 'c']}
        assert schema.obj()  == __(str_tuple=['a', 'b', 'c'])

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
        from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id

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