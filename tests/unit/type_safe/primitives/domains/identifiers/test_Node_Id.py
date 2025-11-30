from unittest                                                       import TestCase
import pytest
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id
from osbot_utils.utils.Objects                                      import base_classes


class test_Node_Id(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization returns empty string
        node_id = Node_Id()

        assert type(node_id)  is Node_Id
        assert len(node_id)   == 0
        assert node_id        == ''                                                         # Empty when no value provided

    def test__init__inheritance(self):                                                      # Test class inheritance
        assert base_classes(Node_Id) == [Obj_Id, Type_Safe__Primitive, str, object, object]

    def test__init__with_none(self):                                                        # Test with None value returns empty string
        node_id = Node_Id(None)

        assert type(node_id) is Node_Id
        assert node_id       == ''
        assert len(node_id)  == 0

    def test__init__with_empty_string(self):                                                # Test with empty string returns empty string
        node_id = Node_Id('')

        assert type(node_id) is Node_Id
        assert node_id       == ''
        assert len(node_id)  == 0

    def test__init__with_valid_obj_id(self):                                                # Test with valid 8-char hex value
        valid_id = 'a1234567'
        node_id  = Node_Id(valid_id)

        assert type(node_id) is Node_Id
        assert node_id       == valid_id
        assert len(node_id)  == 8

    def test__init__with_obj_id_instance(self):                                             # Test with existing Obj_Id instance
        obj_id  = Obj_Id()
        node_id = Node_Id(obj_id)

        assert type(node_id)   is Node_Id
        assert node_id         == str(obj_id)
        assert node_id.obj()   == obj_id.obj()
        assert node_id.json()  == obj_id.json()

    def test__init__with_invalid_value(self):                                               # Test invalid values raise ValueError
        invalid_id    = 'aaaa_bbb_cccc'
        error_message = "in Node_Id: value provided was not a valid Node_Id: aaaa_bbb_cccc"

        with pytest.raises(ValueError, match=error_message):
            Node_Id(invalid_id)

    def test__init__validates_like_obj_id(self):                                            # Test that Node_Id validates same as Obj_Id
        invalid_values = ['too_long_value_here',
                          'short'              ,
                          '123'                ,
                          'not-valid-hex!'     ,
                          'qqqqqqqq'           ,
                          'q2345678'           ]

        for invalid in invalid_values:
            with pytest.raises(ValueError):
                Node_Id(invalid)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_string_subclass(self):                                                     # Test that Node_Id is a string
        node_id = Node_Id()

        assert isinstance(node_id, str)
        assert isinstance(node_id, Obj_Id)
        assert isinstance(node_id, Node_Id)

    def test__can_be_used_as_string(self):                                                  # Test string operations work
        node_id = Node_Id('abcd1234')

        assert node_id.upper()  == 'ABCD1234'                                               # String methods work
        assert node_id.lower()  == 'abcd1234'
        assert str(node_id)     == node_id                                                  # str() conversion

    def test__empty_is_falsy(self):                                                         # Test empty Node_Id is falsy
        empty_id = Node_Id('')

        assert not empty_id                                                                 # Falsy
        assert bool(empty_id) is False

    def test__non_empty_is_truthy(self):                                                    # Test non-empty Node_Id is truthy
        node_id = Node_Id(Obj_Id())

        assert node_id                                                                      # Truthy
        assert bool(node_id) is True

    def test__context_manager(self):                                                        # Test context manager support
        with Node_Id() as node_id:
            assert type(node_id) is Node_Id
            assert node_id       == ''

        with Node_Id('a1234567') as node_id:
            assert node_id == 'a1234567'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_value(self):                                                   # Test equality with same value
        value    = 'a1234567'
        node_id1 = Node_Id(value)
        node_id2 = Node_Id(value)

        assert node_id1 == node_id2
        assert node_id1 == value                                                            # Compare with string

    def test__equality__empty_values(self):                                                 # Test equality of empty values
        empty1 = Node_Id('')
        empty2 = Node_Id(None)

        assert empty1 == empty2
        assert empty1 == ''

    def test__inequality__different_values(self):                                           # Test inequality
        node_id1 = Node_Id(Obj_Id())
        node_id2 = Node_Id(Obj_Id())

        assert node_id1 != node_id2                                                         # Different IDs

    def test__inequality__with_obj_id(self):                                                # Test Node_Id != Obj_Id even with same value
        obj_id  = Obj_Id()
        node_id = Node_Id(obj_id)

        assert node_id != obj_id                                                            # Different types

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__json__empty(self):                                                            # Test JSON serialization of empty Node_Id
        node_id = Node_Id()

        assert node_id.json() == '""'

    def test__json__with_value(self):                                                       # Test JSON serialization with value
        value   = 'a1234567'
        node_id = Node_Id(value)

        assert node_id.json() == f'"{value}"'

    def test__obj__empty(self):                                                             # Test obj() method for empty Node_Id
        node_id = Node_Id()

        assert node_id.obj() == __()

    def test__obj__with_value(self):                                                        # Test obj() method with value
        value   = 'a1234567'
        node_id = Node_Id(value)

        assert node_id.obj() == __()                                                        # Primitive returns empty namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__multiple_empty_instances(self):                                               # Test multiple empty instances are equal
        empties = [Node_Id(''), Node_Id(None), Node_Id()]

        for empty in empties:
            assert empty == ''
            assert type(empty) is Node_Id

    def test__use_in_dict_key(self):                                                        # Test Node_Id can be used as dict key
        node_id = Node_Id('a1234567')
        data    = {node_id: 'test_value'}

        assert data[node_id] == 'test_value'
        assert node_id in data

    def test__use_in_set(self):                                                             # Test Node_Id can be used in set
        node_id1 = Node_Id(Obj_Id())
        node_id2 = Node_Id(Obj_Id())
        id_set   = {node_id1, node_id2}

        assert len(id_set) == 2                                                             # Two different IDs
        assert node_id1 in id_set
        assert node_id2 in id_set

    def test__from_obj_id(self):                                                            # Test conversion from Obj_Id
        obj_id  = Obj_Id()
        node_id = Node_Id(obj_id)

        assert node_id != obj_id                                                            # Different types
        assert type(node_id) is Node_Id
        assert str(node_id)  == str(obj_id)                                                 # Same string value

    def test__hash__consistency(self):                                                      # Test hash is consistent for same value
        value    = 'a1234567'
        node_id1 = Node_Id(value)
        node_id2 = Node_Id(value)

        assert hash(node_id1) == hash(node_id2)

    def test__hash__different_from_obj_id(self):                                            # Test hash differs from Obj_Id with same value
        value   = 'a1234567'
        obj_id  = Obj_Id(value)
        node_id = Node_Id(value)

        assert hash(node_id) != hash(obj_id)                                                # Different types have different hashes

    def test__repr__(self):                                                                 # Test repr output
        value   = 'a1234567'
        node_id = Node_Id(value)

        assert repr(node_id) == f"Node_Id('{value}')"

    def test__str__(self):                                                                  # Test str output
        value   = 'a1234567'
        node_id = Node_Id(value)

        assert str(node_id) == value