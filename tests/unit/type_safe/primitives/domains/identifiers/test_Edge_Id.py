from typing                                                         import List
from unittest                                                       import TestCase
import pytest
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id, is_obj_id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Json                                         import json_to_str, json_round_trip
from osbot_utils.utils.Objects                                      import base_classes


class test_Edge_Id(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization returns empty string
        edge_id = Edge_Id()

        assert type(edge_id)  is Edge_Id
        assert len(edge_id)   == 0
        assert edge_id        == ''                                                         # Empty when no value provided

    def test__init__inheritance(self):                                                      # Test class inheritance
        assert base_classes(Edge_Id) == [Obj_Id, Type_Safe__Primitive, str, object, object]

    def test__init__with_none(self):                                                        # Test with None value returns empty string
        edge_id = Edge_Id(None)

        assert type(edge_id) is Edge_Id
        assert edge_id       == ''
        assert len(edge_id)  == 0

    def test__init__with_empty_string(self):                                                # Test with empty string returns empty string
        edge_id = Edge_Id('')

        assert type(edge_id) is Edge_Id
        assert edge_id       == ''
        assert len(edge_id)  == 0

    def test__init__with_valid_obj_id(self):                                                # Test with valid 8-char hex value
        valid_id = 'a1234567'
        edge_id  = Edge_Id(valid_id)

        assert type(edge_id) is Edge_Id
        assert edge_id       == valid_id
        assert len(edge_id)  == 8

    def test__init__with_obj_id_instance(self):                                             # Test with existing Obj_Id instance
        obj_id  = Obj_Id()
        edge_id = Edge_Id(obj_id)

        assert type(edge_id)  is Edge_Id
        assert edge_id        == str(obj_id)
        assert edge_id.obj()  == obj_id.obj()
        assert edge_id.json() == obj_id.json()

    def test__init__with_invalid_value(self):                                               # Test invalid values raise ValueError
        invalid_id    = 'aaaa_bbb_cccc'
        error_message = "in Edge_Id: value provided was not a valid Edge_Id: aaaa_bbb_cccc"

        with pytest.raises(ValueError, match=error_message):
            Edge_Id(invalid_id)

    def test__init__validates_like_obj_id(self):                                            # Test that Edge_Id validates same as Obj_Id
        invalid_values = ['too_long_value_here',
                          'short'              ,
                          '123'                ,
                          'ghijklmn'           ,                                            # Non-hex letters
                          '1234567!'           ,                                            # Special character
                          'ABCD1234'           ]                                            # Uppercase

        for invalid in invalid_values:
            with pytest.raises(ValueError):
                Edge_Id(invalid)

    def test__init__valid_hex_values(self):                                                 # Test all valid hex patterns
        valid_values = ['00000000',
                        'ffffffff',
                        'a1b2c3d4',
                        '12345678',
                        'abcdef12']

        for valid in valid_values:
            edge_id = Edge_Id(valid)
            assert edge_id == valid
            assert type(edge_id) is Edge_Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_string_subclass(self):                                                     # Test that Edge_Id is a string
        edge_id = Edge_Id()

        assert isinstance(edge_id, str)
        assert isinstance(edge_id, Obj_Id)
        assert isinstance(edge_id, Edge_Id)

    def test__can_be_used_as_string(self):                                                  # Test string operations work
        edge_id = Edge_Id('abcd1234')

        assert edge_id.upper()  == 'ABCD1234'
        assert edge_id.lower()  == 'abcd1234'
        assert str(edge_id)     == 'abcd1234'
        assert len(edge_id)     == 8

    def test__empty_is_falsy(self):                                                         # Test empty Edge_Id is falsy
        empty_id = Edge_Id('')

        assert not empty_id                                                                 # Falsy
        assert bool(empty_id) is False

    def test__non_empty_is_truthy(self):                                                    # Test non-empty Edge_Id is truthy
        edge_id = Edge_Id(Obj_Id())

        assert edge_id                                                                      # Truthy
        assert bool(edge_id) is True

    def test__context_manager(self):                                                        # Test context manager support
        with Edge_Id() as edge_id:
            assert type(edge_id) is Edge_Id
            assert edge_id       == ''

        with Edge_Id('a1234567') as edge_id:
            assert edge_id == 'a1234567'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_value(self):                                                   # Test equality with same value
        value    = 'a1234567'
        edge_id1 = Edge_Id(value)
        edge_id2 = Edge_Id(value)

        assert edge_id1 == edge_id2
        assert edge_id1 == value                                                            # Compare with string

    def test__equality__empty_values(self):                                                 # Test equality of empty values
        empty1 = Edge_Id('')
        empty2 = Edge_Id(None)

        assert empty1 == empty2
        assert empty1 == ''

    def test__inequality__different_values(self):                                           # Test inequality
        edge_id1 = Edge_Id(Obj_Id())
        edge_id2 = Edge_Id(Obj_Id())

        assert edge_id1 != edge_id2                                                         # Different IDs

    def test__inequality__with_obj_id(self):                                                # Test Edge_Id != Obj_Id even with same value
        obj_id  = Obj_Id()
        edge_id = Edge_Id(obj_id)

        assert edge_id != obj_id                                                            # Different types

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__json__empty(self):                                                            # Test JSON serialization of empty Edge_Id
        edge_id = Edge_Id()

        assert edge_id.json() == '""'

    def test__json__with_value(self):                                                       # Test JSON serialization with value
        value   = 'a1234567'
        edge_id = Edge_Id(value)

        assert edge_id.json() == f'"{value}"'

    def test__json_round_trip(self):                                                        # Test JSON round-trip
        obj_id  = Obj_Id()
        edge_id = Edge_Id(obj_id)

        assert json_to_str(edge_id)           == f'"{edge_id}"'
        assert json_round_trip(edge_id)       == str(edge_id)
        assert type(json_round_trip(edge_id)) is str

    def test__obj__empty(self):                                                             # Test obj() method for empty Edge_Id
        edge_id = Edge_Id()

        assert edge_id.obj() == __()

    def test__obj__with_value(self):                                                        # Test obj() method with value
        edge_id = Edge_Id('a1234567')

        assert edge_id.obj() == __()                                                        # Primitive returns empty namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # String Operations Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__string_concatenation(self):                                                   # Test string concatenation returns plain str
        edge_id = Edge_Id('a1234567')

        result1 = edge_id + '_suffix'
        assert result1 == 'a1234567_suffix'
        assert type(result1) is str

        result2 = 'prefix_' + edge_id
        assert result2 == 'prefix_a1234567'
        assert type(result2) is str

        result3 = 'prefix_' + edge_id + '_suffix'
        assert result3 == 'prefix_a1234567_suffix'
        assert type(result3) is str

    def test__string_formatting(self):                                                      # Test string formatting
        edge_id = Edge_Id('a1234567')

        assert f"edge:{edge_id}"       == 'edge:a1234567'
        assert "edge:{}".format(edge_id) == 'edge:a1234567'

    def test__string_slicing(self):                                                         # Test string slicing
        edge_id = Edge_Id('a1234567')

        assert edge_id[:4]  == 'a123'
        assert edge_id[-4:] == '4567'
        assert edge_id[2:6] == '2345'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type_Safe Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__in_type_safe_schema(self):                                                    # Test usage in Type_Safe classes
        class Schema__Edge(Type_Safe):
            edge_id   : Edge_Id
            source_id : Edge_Id = None
            target_id : Edge_Id

        with Schema__Edge() as _:
            assert type(_.edge_id)   is Edge_Id
            assert type(_.target_id) is Edge_Id
            assert _.source_id       is None                                                # Explicit None preserved

            # Empty Edge_Id fields
            assert _.edge_id   == ''
            assert _.target_id == ''

            # Can set values later
            _.edge_id = Edge_Id(Obj_Id())
            assert is_obj_id(_.edge_id)

    def test__json_serialization_in_schema(self):                                           # Test JSON round-trip in Type_Safe
        class Schema__EdgeData(Type_Safe):
            edge_id   : Edge_Id
            from_node : Edge_Id
            to_node   : Edge_Id

        original         = Schema__EdgeData()
        original.edge_id   = Edge_Id(Obj_Id())
        original.from_node = Edge_Id(Obj_Id())
        original.to_node   = Edge_Id(Obj_Id())

        # Serialize
        json_data = original.json()
        assert 'edge_id'   in json_data
        assert 'from_node' in json_data
        assert 'to_node'   in json_data

        # All should be valid Obj_Id strings
        assert is_obj_id(json_data['edge_id'])
        assert is_obj_id(json_data['from_node'])
        assert is_obj_id(json_data['to_node'])

        # Deserialize
        restored = Schema__EdgeData.from_json(json_data)

        # Should preserve exact values
        assert restored.edge_id   == original.edge_id
        assert restored.from_node == original.from_node
        assert restored.to_node   == original.to_node

        # Types should be preserved
        assert type(restored.edge_id)   is Edge_Id
        assert type(restored.from_node) is Edge_Id
        assert type(restored.to_node)   is Edge_Id

    def test__use_in_collections(self):                                                     # Test in Type_Safe collections
        class Schema__EdgeBatch(Type_Safe):
            batch_id : Edge_Id
            edge_ids : List[Edge_Id]

        with Schema__EdgeBatch() as _:
            assert type(_.batch_id) is Edge_Id
            assert type(_.edge_ids) is Type_Safe__List

            # Set batch_id
            _.batch_id = Edge_Id(Obj_Id())

            # Add edges
            for i in range(5):
                _.edge_ids.append(Edge_Id(Obj_Id()))

            # All should be unique and valid
            all_ids = [_.batch_id] + list(_.edge_ids)
            assert len(set(str(id) for id in all_ids)) == 6

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph-Specific Use Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__edge_relationship(self):                                                      # Test edge representing relationship
        from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id

        class Schema__GraphEdge(Type_Safe):
            edge_id   : Edge_Id
            from_node : Node_Id
            to_node   : Node_Id
            weight    : float = 1.0

        with Schema__GraphEdge() as edge:
            edge.edge_id   = Edge_Id(Obj_Id())
            edge.from_node = Node_Id(Obj_Id())
            edge.to_node   = Node_Id(Obj_Id())
            edge.weight    = 0.5

            assert type(edge.edge_id)   is Edge_Id
            assert type(edge.from_node) is Node_Id
            assert type(edge.to_node)   is Node_Id
            assert edge.weight          == 0.5

    def test__adjacency_list(self):                                                         # Test in adjacency list structure
        from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id

        class Schema__AdjacencyEntry(Type_Safe):
            node_id  : Node_Id
            edge_ids : List[Edge_Id]

        with Schema__AdjacencyEntry() as entry:
            entry.node_id = Node_Id(Obj_Id())

            # Add connected edges
            for _ in range(3):
                entry.edge_ids.append(Edge_Id(Obj_Id()))

            assert len(entry.edge_ids) == 3
            assert all(type(e) is Edge_Id for e in entry.edge_ids)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__multiple_empty_instances(self):                                               # Test multiple empty instances are equal
        empties = [Edge_Id(''), Edge_Id(None), Edge_Id()]

        for empty in empties:
            assert empty == ''
            assert type(empty) is Edge_Id

    def test__use_in_dict_key(self):                                                        # Test Edge_Id can be used as dict key
        edge_id = Edge_Id('a1234567')
        data    = {edge_id: 'test_value'}

        assert data[edge_id] == 'test_value'
        assert edge_id in data

    def test__use_in_set(self):                                                             # Test Edge_Id can be used in set
        edge_id1 = Edge_Id(Obj_Id())
        edge_id2 = Edge_Id(Obj_Id())
        id_set   = {edge_id1, edge_id2}

        assert len(id_set) == 2
        assert edge_id1 in id_set
        assert edge_id2 in id_set

    def test__from_obj_id(self):                                                            # Test conversion from Obj_Id
        obj_id  = Obj_Id()
        edge_id = Edge_Id(obj_id)

        assert edge_id != obj_id                                                            # Different types
        assert type(edge_id) is Edge_Id
        assert str(edge_id)  == str(obj_id)                                                 # Same string value

    def test__hash__consistency(self):                                                      # Test hash is consistent for same value
        value    = 'a1234567'
        edge_id1 = Edge_Id(value)
        edge_id2 = Edge_Id(value)

        assert hash(edge_id1) == hash(edge_id2)

    def test__hash__different_from_obj_id(self):                                            # Test hash differs from Obj_Id with same value
        value   = 'a1234567'
        obj_id  = Obj_Id(value)
        edge_id = Edge_Id(value)

        assert hash(edge_id) != hash(obj_id)                                                # Different types have different hashes

    def test__repr__(self):                                                                 # Test repr output
        value   = 'a1234567'
        edge_id = Edge_Id(value)

        assert repr(edge_id) == f"Edge_Id('{value}')"

    def test__str__(self):                                                                  # Test str output
        value   = 'a1234567'
        edge_id = Edge_Id(value)

        assert str(edge_id) == value

    def test__empty_vs_populated_behavior(self):                                            # Test difference between empty and populated
        empty_id     = Edge_Id()
        populated_id = Edge_Id(Obj_Id())

        # Empty is falsy, populated is truthy
        assert not empty_id
        assert populated_id

        # Empty has length 0, populated has length 8
        assert len(empty_id)     == 0
        assert len(populated_id) == 8

        # Both are Edge_Id type
        assert type(empty_id)     is Edge_Id
        assert type(populated_id) is Edge_Id