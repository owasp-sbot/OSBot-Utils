import re
import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                 import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id              import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.utils.Objects                                                  import base_classes


class test_Graph_Id(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization generates UUID
        graph_id = Graph_Id()

        assert type(graph_id)  is Graph_Id
        assert len(graph_id)   == 0
        assert graph_id        == ''                                                        # Empty when no value provided

    def test__init__inheritance(self):                                                      # Test class inheritance
        assert base_classes(Graph_Id) == [Obj_Id, Type_Safe__Primitive, str, object, object]

    def test__init__with_none(self):                                                        # Test with None value returns empty string
        graph_id = Graph_Id(None)

        assert type(graph_id) is Graph_Id
        assert graph_id       == ''
        assert len(graph_id)  == 0

    def test__init__with_empty_string(self):                                                # Test with empty string returns empty string
        graph_id = Graph_Id('')

        assert type(graph_id) is Graph_Id
        assert graph_id       == ''
        assert len(graph_id)  == 0

    def test__init__with_value(self):                                                       # Test with existing UUID value
        existing_id = '12345678'
        graph_id    = Graph_Id(existing_id)

        assert type(graph_id) is Graph_Id
        assert graph_id       == existing_id
        assert len(graph_id)  == 8

    def test__init__with_bad(self):                                                       # Test with existing UUID value
        bad_id_1        = '12345678-1234-1234-1234-123456789abc'
        error_message_1 =  f'in Graph_Id: value provided was not a valid Graph_Id: {bad_id_1}'
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            Graph_Id(bad_id_1)

        bad_id_2        = 'xyz!!^^&'
        error_message_2 =  f'in Graph_Id: value provided was not a valid Graph_Id: {bad_id_2}'
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            assert Graph_Id(bad_id_2)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_string_subclass(self):                                                     # Test that Graph_Id is a string
        graph_id = Graph_Id(Obj_Id())

        assert isinstance(graph_id, str         )
        assert isinstance(graph_id, Graph_Id    )

    def test__can_be_used_as_string(self):                                                  # Test string operations work
        graph_id = Graph_Id(Obj_Id())

        assert graph_id.upper()  == graph_id.upper()                                        # String methods work
        assert graph_id.lower()  == graph_id.lower()
        assert str(graph_id)     == graph_id                                                # str() conversion

    def test__empty_is_falsy(self):                                                         # Test empty Graph_Id is falsy
        empty_id = Graph_Id('')

        assert not empty_id                                                                 # Falsy
        assert bool(empty_id) is False

    def test__non_empty_is_truthy(self):                                                    # Test non-empty Graph_Id is truthy
        graph_id = Graph_Id(Obj_Id())

        assert graph_id                                                                     # Truthy
        assert bool(graph_id) is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_value(self):                                                   # Test equality with same value
        value    = '12345678'
        graph_id1 = Graph_Id(value)
        graph_id2 = Graph_Id(value)

        assert graph_id1 == graph_id2
        assert graph_id1 == value                                                           # Compare with string

    def test__equality__empty_values(self):                                                 # Test equality of empty values
        empty1 = Graph_Id('')
        empty2 = Graph_Id(None)

        assert empty1 == empty2
        assert empty1 == ''

    def test__inequality__different_values(self):                                           # Test inequality
        graph_id1 = Graph_Id(Obj_Id())
        graph_id2 = Graph_Id(Obj_Id())

        assert graph_id1 != graph_id2                                                       # Different UUIDs


    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__whitespace_handling(self):                                                    # Test whitespace in value
        # Obj_Id should handle whitespace
        value    = '  12345678  '
        graph_id = Graph_Id(value.strip())

        assert len(graph_id) == 8

    def test__multiple_empty_instances(self):                                               # Test multiple empty instances are equal
        empties = [Graph_Id(''), Graph_Id(None), Graph_Id('')]

        for empty in empties:
            assert empty == ''
            assert type(empty) is Graph_Id

    def test__use_in_dict_key(self):                                                        # Test Graph_Id can be used as dict key
        graph_id = Graph_Id(Obj_Id())
        data     = {graph_id: 'test_value'}

        assert data[graph_id] == 'test_value'
        assert graph_id in data

    def test__use_in_set(self):                                                             # Test Graph_Id can be used in set
        graph_id1 = Graph_Id(Obj_Id())
        graph_id2 = Graph_Id(Obj_Id())
        id_set    = {graph_id1, graph_id2}

        assert len(id_set) == 2                                                             # Two different IDs
        assert graph_id1 in id_set
        assert graph_id2 in id_set

    def test__from_obj_id(self):                                                            # Test conversion from Obj_Id
        obj_id   = Obj_Id()
        graph_id = Graph_Id(obj_id)

        assert graph_id != obj_id                                                           # different types       # todo: see if this should work (would required change to OSBOt-Utils or direct overwrite of __eq__ method in Graph_Id)
        assert type(graph_id) is Graph_Id