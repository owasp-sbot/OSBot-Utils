from typing                                                         import List
from unittest                                                       import TestCase
import pytest
from osbot_utils.testing.__                                         import __
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id  import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Json                                         import json_to_str, json_round_trip
from osbot_utils.utils.Misc                                         import is_guid
from osbot_utils.utils.Objects                                      import base_classes


class test_Cache_Id(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization returns empty string
        cache_id = Cache_Id()

        assert type(cache_id)  is Cache_Id
        assert len(cache_id)   == 0
        assert cache_id        == ''                                                        # Empty when no value provided

    def test__init__inheritance(self):                                                      # Test class inheritance
        assert base_classes(Cache_Id) == [Random_Guid, Type_Safe__Primitive, str, object, object]

    def test__init__with_none(self):                                                        # Test with None value returns empty string
        cache_id = Cache_Id(None)

        assert type(cache_id) is Cache_Id
        assert cache_id       == ''
        assert len(cache_id)  == 0

    def test__init__with_empty_string(self):                                                # Test with empty string returns empty string
        cache_id = Cache_Id('')

        assert type(cache_id) is Cache_Id
        assert cache_id       == ''
        assert len(cache_id)  == 0

    def test__init__with_valid_guid(self):                                                  # Test with valid GUID value
        valid_guid = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id   = Cache_Id(valid_guid)

        assert type(cache_id) is Cache_Id
        assert cache_id       == valid_guid
        assert len(cache_id)  == 36

    def test__init__with_random_guid_instance(self):                                        # Test with existing Random_Guid instance
        random_guid = Random_Guid()
        cache_id    = Cache_Id(random_guid)

        assert type(cache_id) is Cache_Id
        assert cache_id       == str(random_guid)
        assert is_guid(cache_id)

    def test__init__with_invalid_value(self):                                               # Test invalid values raise ValueError
        invalid_guid  = 'not-a-valid-guid'
        error_message = f"in Random_Guid: value provided was not a Guid: {invalid_guid}"

        with pytest.raises(ValueError, match=error_message):
            Cache_Id(invalid_guid)

    def test__init__validates_like_random_guid(self):                                       # Test that Cache_Id validates same as Random_Guid
        invalid_values = ['too-short'              ,
                          '12345678'               ,
                          'not-valid-guid-format'  ,
                          'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx']  # Wrong chars

        for invalid in invalid_values:
            with pytest.raises(ValueError):
                Cache_Id(invalid)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__is_string_subclass(self):                                                     # Test that Cache_Id is a string
        cache_id = Cache_Id()

        assert isinstance(cache_id, str)
        assert isinstance(cache_id, Random_Guid)
        assert isinstance(cache_id, Cache_Id)

    def test__can_be_used_as_string(self):                                                  # Test string operations work
        cache_id = Cache_Id(Random_Guid())

        assert cache_id.upper()  == cache_id.upper()                                        # String methods work
        assert cache_id.lower()  == cache_id.lower()
        assert str(cache_id)     == cache_id                                                # str() conversion

    def test__empty_is_falsy(self):                                                         # Test empty Cache_Id is falsy
        empty_id = Cache_Id('')

        assert not empty_id                                                                 # Falsy
        assert bool(empty_id) is False

    def test__non_empty_is_truthy(self):                                                    # Test non-empty Cache_Id is truthy
        cache_id = Cache_Id(Random_Guid())

        assert cache_id                                                                     # Truthy
        assert bool(cache_id) is True

    def test__context_manager(self):                                                        # Test context manager support
        with Cache_Id() as cache_id:
            assert type(cache_id) is Cache_Id
            assert cache_id       == ''

        valid_guid = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        with Cache_Id(valid_guid) as cache_id:
            assert cache_id == valid_guid

    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__equality__same_value(self):                                                   # Test equality with same value
        value     = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id1 = Cache_Id(value)
        cache_id2 = Cache_Id(value)

        assert cache_id1 == cache_id2
        assert cache_id1 == value                                                           # Compare with string

    def test__equality__empty_values(self):                                                 # Test equality of empty values
        empty1 = Cache_Id('')
        empty2 = Cache_Id(None)

        assert empty1 == empty2
        assert empty1 == ''

    def test__inequality__different_values(self):                                           # Test inequality
        cache_id1 = Cache_Id(Random_Guid())
        cache_id2 = Cache_Id(Random_Guid())

        assert cache_id1 != cache_id2                                                       # Different GUIDs

    def test__inequality__with_random_guid(self):                                           # Test Cache_Id != Random_Guid even with same value
        random_guid = Random_Guid()
        cache_id    = Cache_Id(random_guid)

        assert cache_id != random_guid                                                      # Different types

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__json__empty(self):                                                            # Test JSON serialization of empty Cache_Id
        cache_id = Cache_Id()

        assert cache_id.json() == '""'

    def test__json__with_value(self):                                                       # Test JSON serialization with value
        value    = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id = Cache_Id(value)

        assert cache_id.json() == f'"{value}"'

    def test__json_round_trip(self):                                                        # Test JSON round-trip
        random_guid = Random_Guid()
        cache_id    = Cache_Id(random_guid)

        assert json_to_str(cache_id)           == f'"{cache_id}"'
        assert json_round_trip(cache_id)       == str(cache_id)
        assert type(json_round_trip(cache_id)) is str

    def test__obj__empty(self):                                                             # Test obj() method for empty Cache_Id
        cache_id = Cache_Id()

        assert cache_id.obj() == __()

    def test__obj__with_value(self):                                                        # Test obj() method with value
        cache_id = Cache_Id(Random_Guid())

        assert cache_id.obj() == __()                                                       # Primitive returns empty namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # String Operations Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__string_concatenation(self):                                                   # Test string concatenation returns plain str
        cache_id = Cache_Id(Random_Guid())

        result1 = cache_id + '-suffix'
        assert result1 == f"{cache_id}-suffix"
        assert type(result1) is str

        result2 = 'prefix-' + cache_id
        assert result2 == f"prefix-{cache_id}"
        assert type(result2) is str

        result3 = 'prefix-' + cache_id + '-suffix'
        assert result3 == f"prefix-{cache_id}-suffix"
        assert type(result3) is str

    def test__string_formatting(self):                                                      # Test string formatting
        cache_id = Cache_Id(Random_Guid())

        assert f"cache:{cache_id}"       == f"cache:{str(cache_id)}"
        assert "cache:{}".format(cache_id) == f"cache:{str(cache_id)}"

    def test__string_slicing(self):                                                         # Test string slicing
        cache_id = Cache_Id(Random_Guid())

        assert cache_id[:8]  == str(cache_id)[:8]
        assert cache_id[-12:] == str(cache_id)[-12:]
        assert '-' in cache_id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type_Safe Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__in_type_safe_schema(self):                                                    # Test usage in Type_Safe classes
        class Schema__CacheEntry(Type_Safe):
            cache_id    : Cache_Id
            parent_id   : Cache_Id = None
            tracking_id : Cache_Id

        with Schema__CacheEntry() as _:
            assert type(_.cache_id)    is Cache_Id
            assert type(_.tracking_id) is Cache_Id
            assert _.parent_id         is None                                              # Explicit None preserved

            # Empty Cache_Id fields
            assert _.cache_id    == ''
            assert _.tracking_id == ''

            # Can set values later
            _.cache_id = Cache_Id(Random_Guid())
            assert is_guid(_.cache_id)

    def test__json_serialization_in_schema(self):                                           # Test JSON round-trip in Type_Safe
        class Schema__CacheData(Type_Safe):
            cache_id   : Cache_Id
            session_id : Cache_Id

        original         = Schema__CacheData()
        original.cache_id   = Cache_Id(Random_Guid())
        original.session_id = Cache_Id(Random_Guid())

        # Serialize
        json_data = original.json()
        assert 'cache_id'   in json_data
        assert 'session_id' in json_data

        # All should be valid UUID strings
        assert is_guid(json_data['cache_id'])
        assert is_guid(json_data['session_id'])

        # Deserialize
        restored = Schema__CacheData.from_json(json_data)

        # Should preserve exact values
        assert restored.cache_id   == original.cache_id
        assert restored.session_id == original.session_id

        # Types should be preserved
        assert type(restored.cache_id)   is Cache_Id
        assert type(restored.session_id) is Cache_Id

    def test__use_in_collections(self):                                                     # Test in Type_Safe collections
        class Schema__CacheBatch(Type_Safe):
            batch_id  : Cache_Id
            entry_ids : List[Cache_Id]

        with Schema__CacheBatch() as _:
            assert type(_.batch_id)  is Cache_Id
            assert type(_.entry_ids) is Type_Safe__List

            # Set batch_id
            _.batch_id = Cache_Id(Random_Guid())

            # Add entries
            for i in range(5):
                _.entry_ids.append(Cache_Id(Random_Guid()))

            # All should be unique and valid
            all_ids = [_.batch_id] + list(_.entry_ids)
            assert len(set(str(id) for id in all_ids)) == 6

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__multiple_empty_instances(self):                                               # Test multiple empty instances are equal
        empties = [Cache_Id(''), Cache_Id(None), Cache_Id()]

        for empty in empties:
            assert empty == ''
            assert type(empty) is Cache_Id

    def test__use_in_dict_key(self):                                                        # Test Cache_Id can be used as dict key
        cache_id = Cache_Id(Random_Guid())
        data     = {cache_id: 'test_value'}

        assert data[cache_id] == 'test_value'
        assert cache_id in data

    def test__use_in_set(self):                                                             # Test Cache_Id can be used in set
        cache_id1 = Cache_Id(Random_Guid())
        cache_id2 = Cache_Id(Random_Guid())
        id_set    = {cache_id1, cache_id2}

        assert len(id_set) == 2
        assert cache_id1 in id_set
        assert cache_id2 in id_set

    def test__from_random_guid(self):                                                       # Test conversion from Random_Guid
        random_guid = Random_Guid()
        cache_id    = Cache_Id(random_guid)

        assert cache_id != random_guid                                                      # Different types
        assert type(cache_id) is Cache_Id
        assert str(cache_id)  == str(random_guid)                                           # Same string value

    def test__hash__consistency(self):                                                      # Test hash is consistent for same value
        value     = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id1 = Cache_Id(value)
        cache_id2 = Cache_Id(value)

        assert hash(cache_id1) == hash(cache_id2)

    def test__hash__different_from_random_guid(self):                                       # Test hash differs from Random_Guid with same value
        value       = 'a1b2c3d4-e5f6-4890-abcd-ef1234567890'
        random_guid = Random_Guid(value)
        cache_id    = Cache_Id(value)

        assert hash(cache_id) != hash(random_guid)                                          # Different types have different hashes

    def test__repr__(self):                                                                 # Test repr output
        value    = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id = Cache_Id(value)

        assert repr(cache_id) == f"Cache_Id('{value}')"

    def test__str__(self):                                                                  # Test str output
        value    = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        cache_id = Cache_Id(value)

        assert str(cache_id) == value

    def test__empty_vs_populated_behavior(self):                                            # Test difference between empty and populated
        empty_id     = Cache_Id()
        populated_id = Cache_Id(Random_Guid())

        # Empty is falsy, populated is truthy
        assert not empty_id
        assert populated_id

        # Empty has length 0, populated has length 36
        assert len(empty_id)     == 0
        assert len(populated_id) == 36

        # Both are Cache_Id type
        assert type(empty_id)     is Cache_Id
        assert type(populated_id) is Cache_Id