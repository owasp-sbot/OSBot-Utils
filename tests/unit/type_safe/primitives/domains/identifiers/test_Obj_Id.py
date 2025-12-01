import re
from unittest                                                       import TestCase
import pytest
from osbot_utils.helpers.duration.decorators.capture_duration       import capture_duration
from osbot_utils.testing.__                                         import __
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id    import Obj_Id, is_obj_id, new_obj_id
from osbot_utils.utils.Env                                          import in_github_action
from osbot_utils.utils.Objects                                      import base_classes


class test_Obj_Id(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization generates valid ID
        obj_id = Obj_Id()

        assert type(obj_id)            is Obj_Id
        assert len(obj_id)             == 8
        assert isinstance(obj_id, str) is True
        assert is_obj_id(obj_id)       is True

    def test__init__inheritance(self):                                                      # Test class inheritance
        assert base_classes(Obj_Id) == [Type_Safe__Primitive, str, object, object]

    def test__init__with_valid_value(self):                                                 # Test with valid 8-char hex value
        valid_id = 'a1234567'
        obj_id   = Obj_Id(valid_id)

        assert type(obj_id) is Obj_Id
        assert obj_id       == valid_id
        assert len(obj_id)  == 8

    def test__init__with_obj_id_instance(self):                                             # Test with existing Obj_Id instance
        obj_id_1 = Obj_Id()
        obj_id_2 = Obj_Id(obj_id_1)

        assert type(obj_id_2) is Obj_Id
        assert obj_id_1       == obj_id_2

    def test__init__generates_unique_ids(self):                                             # Test that each call generates unique ID
        ids = [Obj_Id() for _ in range(100)]

        assert len(set(ids)) == 100                                                         # All unique

    # ═══════════════════════════════════════════════════════════════════════════════
    # Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__invalid_length_short(self):                                             # Test too short value raises error
        with pytest.raises(ValueError, match="in Obj_Id: value provided was not a valid Obj_Id: abc"):
            Obj_Id('abc')

    def test__init__invalid_length_long(self):                                              # Test too long value raises error
        with pytest.raises(ValueError, match="in Obj_Id: value provided was not a valid Obj_Id: a123456789"):
            Obj_Id('a123456789')

    def test__init__invalid_characters(self):                                               # Test non-hex characters raise error
        invalid_values = ['ghijklmn',                                                       # Non-hex letters
                          '1234567!',                                                       # Special character
                          'aaaa_bbb',                                                       # Underscore
                          '1234 567',                                                       # Space
                          '1234-567',                                                       # Hyphen
                          'ABCD1234']                                                       # Uppercase (enforcing lowercase)

        for invalid in invalid_values:
            with pytest.raises(ValueError):
                Obj_Id(invalid)

    def test__init__valid_hex_values(self):                                                 # Test all valid hex patterns
        valid_values = ['00000000',                                                         # All zeros
                        'ffffffff',                                                         # All f's
                        'a1b2c3d4',                                                         # Mixed
                        '12345678',                                                         # All numbers
                        'abcdef12']                                                         # Letters and numbers

        for valid in valid_values:
            obj_id = Obj_Id(valid)
            assert obj_id == valid
            assert type(obj_id) is Obj_Id

    # ═══════════════════════════════════════════════════════════════════════════════
    # is_obj_id Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_obj_id__with_obj_id_instance(self):                                        # Test is_obj_id with Obj_Id instance
        obj_id = Obj_Id()

        assert is_obj_id(obj_id) is True

    def test__is_obj_id__with_valid_string(self):                                           # Test is_obj_id with valid string
        assert is_obj_id('a1234567') is True
        assert is_obj_id('00000000') is True
        assert is_obj_id('ffffffff') is True

    def test__is_obj_id__with_invalid_string(self):                                         # Test is_obj_id with invalid strings
        assert is_obj_id('abc')          is False                                           # Too short
        assert is_obj_id('a123456789')   is False                                           # Too long
        assert is_obj_id('ghijklmn')     is False                                           # Non-hex
        assert is_obj_id('ABCD1234')     is False                                           # Uppercase
        assert is_obj_id('')             is False                                           # Empty
        assert is_obj_id('aaaa_bbb')     is False                                           # Invalid char

    def test__is_obj_id__with_non_string(self):                                             # Test is_obj_id with non-string types
        assert is_obj_id(12345678)  is False
        assert is_obj_id(None)      is False
        assert is_obj_id(['a'] * 8) is False
        assert is_obj_id({})        is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # new_obj_id Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__new_obj_id__format(self):                                                     # Test new_obj_id generates correct format
        obj_id = new_obj_id()

        assert len(obj_id)       == 8
        assert is_obj_id(obj_id) is True
        assert re.fullmatch(r"[a-z0-9]{8}", obj_id)                                         # Always lowercase
        #assert obj_id.islower()  is True                                                   # we can't use this , since when obj_id is all numbers, islower returns false

    def test__new_obj_id__uniqueness(self):                                                 # Test new_obj_id generates unique values
        ids = [new_obj_id() for _ in range(1000)]

        assert len(set(ids)) == 1000                                                        # All unique

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_string_subclass(self):                                                     # Test that Obj_Id is a string
        obj_id = Obj_Id()

        assert isinstance(obj_id, str)
        assert isinstance(obj_id, Type_Safe__Primitive)
        assert isinstance(obj_id, Obj_Id)

    def test__can_be_used_as_string(self):                                                  # Test string operations work
        obj_id = Obj_Id('abcd1234')

        assert obj_id.upper()  == 'ABCD1234'
        assert obj_id.lower()  == 'abcd1234'
        assert str(obj_id)     == 'abcd1234'
        assert len(obj_id)     == 8

    def test__truthy(self):                                                                 # Test Obj_Id is always truthy (always has value)
        obj_id = Obj_Id()

        assert obj_id
        assert bool(obj_id) is True

    def test__context_manager(self):                                                        # Test context manager support
        with Obj_Id() as obj_id:
            assert type(obj_id) is Obj_Id
            assert len(obj_id)  == 8

        with Obj_Id('a1234567') as obj_id:
            assert obj_id == 'a1234567'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_value(self):                                                   # Test equality with same value
        value   = 'a1234567'
        obj_id1 = Obj_Id(value)
        obj_id2 = Obj_Id(value)

        assert obj_id1 == obj_id2
        assert obj_id1 == value                                                             # Compare with string

    def test__inequality__different_values(self):                                           # Test inequality
        obj_id1 = Obj_Id()
        obj_id2 = Obj_Id()

        assert obj_id1 != obj_id2                                                           # Different IDs

    def test__hash__consistency(self):                                                      # Test hash is consistent for same value
        value   = 'a1234567'
        obj_id1 = Obj_Id(value)
        obj_id2 = Obj_Id(value)

        assert hash(obj_id1) == hash(obj_id2)

    def test__hash__uniqueness(self):                                                       # Test different values have different hashes
        obj_id1 = Obj_Id()
        obj_id2 = Obj_Id()

        assert hash(obj_id1) != hash(obj_id2)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__json(self):                                                                   # Test JSON serialization
        value  = 'a1234567'
        obj_id = Obj_Id(value)

        assert obj_id.json() == f'"{value}"'

    def test__obj(self):                                                                    # Test obj() method
        obj_id = Obj_Id('a1234567')

        assert obj_id.obj() == __()                                                         # Primitive returns empty namespace

    def test__str(self):                                                                    # Test str() conversion
        value  = 'a1234567'
        obj_id = Obj_Id(value)

        assert str(obj_id) == value

    def test__repr(self):                                                                   # Test repr output
        value  = 'a1234567'
        obj_id = Obj_Id(value)

        assert repr(obj_id) == f"Obj_Id('{value}')"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__use_in_dict_key(self):                                                        # Test Obj_Id can be used as dict key
        obj_id = Obj_Id()
        data   = {obj_id: 'test_value'}

        assert data[obj_id] == 'test_value'
        assert obj_id in data

    def test__use_in_set(self):                                                             # Test Obj_Id can be used in set
        obj_id1 = Obj_Id()
        obj_id2 = Obj_Id()
        id_set  = {obj_id1, obj_id2}

        assert len(id_set) == 2
        assert obj_id1 in id_set
        assert obj_id2 in id_set

    def test__string_concatenation(self):                                                   # Test string concatenation
        obj_id = Obj_Id('a1234567')

        result = 'prefix_' + obj_id + '_suffix'
        assert result == 'prefix_a1234567_suffix'

    def test__string_formatting(self):                                                      # Test string formatting
        obj_id = Obj_Id('a1234567')

        assert f"id:{obj_id}"       == 'id:a1234567'
        assert "id:{}".format(obj_id) == 'id:a1234567'

    # ═══════════════════════════════════════════════════════════════════════════════
    # Performance Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__perf__new__(self):                                                            # Test Obj_Id creation performance
        with Performance_Measure__Session() as _:
            _.measure(lambda: Obj_Id()).assert_time__less_than(1000)

    def test__perf__new_obj_id(self):                                                       # Test new_obj_id performance
        with Performance_Measure__Session() as _:
            _.measure(lambda: new_obj_id()).assert_time__less_than(500)

    def test__perf__is_obj_id(self):                                                        # Test is_obj_id performance
        with Performance_Measure__Session() as _:
            _.measure(lambda: is_obj_id('a1234567' )).assert_time__less_than(900)
            _.measure(lambda: is_obj_id('invalid!!')).assert_time__less_than(900)

    def test__perf__regex_validation(self):                                                 # Test regex validation performance at scale
        import re

        _hex_regex = re.compile(r'^[0-9a-f]{8}$')
        value      = 'a1234567'

        def with_regex(v):
            return _hex_regex.match(v) is not None

        size = 100000                                                                       # 100k iterations

        with capture_duration() as duration:
            for _ in range(size):
                with_regex(value)

        if in_github_action():
            assert duration.seconds < 0.5
        else:
            assert duration.seconds < 0.05                                                    # ~0.016 on dev laptop

    # def test_performance_regex_vs_other(self):
    #     import re
    #
    #     _hex_chars = set('0123456789abcdef')
    #     _hex_regex = re.compile(r'^[0-9a-f]{8}$')
    #
    #     value = 'a1234567'
    #
    #     def with_set(v):
    #         return len(v) == 8 and all(c in _hex_chars for c in v.lower())
    #
    #     def with_regex(v):
    #         return _hex_regex.match(v.lower()) is not None
    #
    #     def with_set_direct(v):
    #         return len(v) == 8 and set(v).issubset(_hex_chars)
    #
    #     size =  100000      # 100k                         # results are liner 1M = 10 x 100k result
    #     # with capture_duration() as duration_mode_1:
    #     #     for _ in range(1, size):
    #     #         with_set(value)
    #
    #     with capture_duration() as duration_mode_2:
    #         for _ in range(1, size):
    #             with_regex(value)
    #
    #     # with capture_duration() as duration_mode_3:
    #     #     for _ in range(1, size):
    #     #         with_set_direct(value)
    #     # print()
    #     # print(f"mode 1 duration for {size}: {duration_mode_1.seconds}")      # 0.037 # on dev laptop
    #     # print(f"mode 2 duration for {size}: {duration_mode_2.seconds}")      # 0.016
    #     # print(f"mode 3 duration for {size}: {duration_mode_3.seconds}")      # 0.022
    #     if in_github_action():
    #         assert duration_mode_2.seconds < 0.5
    #     else:
    #         assert duration_mode_2.seconds < 0.05           # 0.016 on dev laptop