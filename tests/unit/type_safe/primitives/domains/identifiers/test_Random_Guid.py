from typing import List

import pytest
import re
from unittest                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid   import Random_Guid
from osbot_utils.type_safe.Type_Safe__Primitive                         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List
from osbot_utils.utils.Json                                             import json_to_str, json_round_trip
from osbot_utils.utils.Misc                                             import is_guid
from osbot_utils.utils.Objects                                          import base_types


class test_Random_Guid(TestCase):

    def test__init__(self):
        random_guid = Random_Guid()
        assert len(random_guid)         == 36
        assert type(random_guid)        is Random_Guid
        assert type(str(random_guid))   is  str                       # FIXED: not it is a string | BUG a bit weird why this is not a str
        assert base_types(random_guid)  == [Type_Safe__Primitive, str, object, object]
        assert str(random_guid)         == random_guid

        assert is_guid    (random_guid)
        assert isinstance (random_guid, str)

        assert Random_Guid()      != Random_Guid()
        assert str(Random_Guid()) != str(Random_Guid())


        assert json_to_str(random_guid)           == f'"{random_guid}"'
        assert json_round_trip(random_guid)       == str(random_guid)
        assert type(json_round_trip(random_guid)) is str

    def test_auto_generation_behavior(self):                    # Test that Random_Guid always auto-generates
        # Every instantiation should produce a unique value
        guids = []
        for _ in range(100):
            guid = Random_Guid()
            assert guid not in guids                            # No duplicates
            guids.append(guid)

        assert len(set(guids)) == 100                          # All unique

    def test_can_provide_explicit_value(self):                  # Test that explicit values are allowed
        explicit_guid = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'      # when we pass a value
        guid2         = Random_Guid(explicit_guid)
        assert guid2 == explicit_guid                               # that is the value that is used
        assert is_guid(guid2)

    def test_guid_format_validation(self):                      # Test UUID v4 format
        guid = Random_Guid()

        # UUID v4 format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        # where y is one of 8, 9, A, or B
        parts = str(guid).split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12

        # Version 4 UUID check
        assert parts[2][0] == '4'                              # Version 4
        assert parts[3][0] in '89ab'                           # Variant bits

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Request(Type_Safe):
            request_id  : Random_Guid                          # Auto-generates on init
            parent_id   : Random_Guid = None                   # Explicitly nullable
            tracking_id : Random_Guid

        with Schema__Request() as _:
            # All Random_Guid fields auto-generate unique values
            assert type(_.request_id ) is Random_Guid
            assert type(_.tracking_id) is Random_Guid
            assert _.parent_id        is None                  # Explicit None preserved

            assert is_guid(_.request_id)
            assert is_guid(_.tracking_id)

            # Each field has different value
            assert _.request_id != _.tracking_id

            # Can set parent_id later
            _.parent_id = Random_Guid()
            assert is_guid(_.parent_id)
            assert _.parent_id != _.request_id
            assert _.parent_id != _.tracking_id

    def test_json_serialization_in_schema(self):                # Test JSON round-trip in Type_Safe
        class Schema__Event(Type_Safe):
            event_id    : Random_Guid
            session_id  : Random_Guid
            correlation : Random_Guid

        original = Schema__Event()

        # Serialize
        json_data = original.json()
        assert 'event_id'    in json_data
        assert 'session_id'  in json_data
        assert 'correlation' in json_data

        # All should be valid UUID strings
        assert is_guid(json_data['event_id'])
        assert is_guid(json_data['session_id'])
        assert is_guid(json_data['correlation'])

        # Deserialize
        restored = Schema__Event.from_json(json_data)

        # Should preserve exact values
        assert restored.event_id    == original.event_id
        assert restored.session_id  == original.session_id
        assert restored.correlation == original.correlation

        # Types should be preserved
        assert type(restored.event_id)    is Random_Guid
        assert type(restored.session_id)  is Random_Guid
        assert type(restored.correlation) is Random_Guid

    def test_string_operations(self):                           # Test string behavior
        guid = Random_Guid()

        # Concatenation
        expected_error = f"in Random_Guid: value provided was not a Guid: {guid}-suffix"
        with pytest.raises(ValueError, match=re.escape((expected_error))):
            guid + '-suffix'


        expected_error = f"in Random_Guid: value provided was not a Guid: prefix-{guid}"
        with pytest.raises(ValueError, match=re.escape((expected_error))):
            'prefix-' + guid

        # Formatting
        assert f"ID: {guid}"         == f"ID: {str(guid)}"
        assert "ID: {}".format(guid) == f"ID: {str(guid)}"

        # Slicing (works like string)
        assert guid[:8] == str(guid)[:8]
        assert guid[-12:] == str(guid)[-12:]

    def test_comparison_operations(self):                       # Test comparisons
        guid1 = Random_Guid()
        guid2 = Random_Guid()

        # Should never be equal (statistically)
        assert guid1 != guid2

        # Can compare with strings
        assert guid1 == str(guid1)
        assert str(guid1) == guid1
        assert guid1 != str(guid2)

        # Lexicographic ordering
        if str(guid1) < str(guid2):
            assert guid1 < guid2
            assert guid2 > guid1
        else:
            assert guid1 > guid2
            assert guid2 < guid1

    def test_hashability(self):                                 # Test use as dict key
        guid1 = Random_Guid()
        guid2 = Random_Guid()
        guid3 = Random_Guid()

        # Should work as dict keys
        mapping = {
            guid1: 'value1',
            guid2: 'value2',
            guid3: 'value3'
        }

        assert mapping[guid1] == 'value1'
        assert mapping[guid2] == 'value2'
        assert mapping[guid3] == 'value3'
        assert len(mapping) == 3

        # Should work in sets
        guid_set = {guid1, guid2, guid3}
        assert len(guid_set) == 3
        assert guid1 in guid_set

    def test_type_safety_with_safe_id(self):                    # Test relationship with Safe_Id
        guid = Random_Guid()

        # Random_Guid should work anywhere Safe_Id is expected
        safe_id = Safe_Id(guid)
        assert str(safe_id) == str(guid)

        # But they're different types
        assert type(guid) is Random_Guid
        assert type(safe_id) is Safe_Id
        assert guid != safe_id                                 # Different types

    def test_statistical_uniqueness(self):                      # Test randomness quality
        # Generate many GUIDs and check for collisions
        guid_set = set()
        collision_found = False

        for _ in range(10000):
            guid = Random_Guid()
            if str(guid) in guid_set:
                collision_found = True
                break
            guid_set.add(str(guid))

        assert not collision_found                             # No collisions in 10k
        assert len(guid_set) == 10000

    def test_repr_and_str(self):                                # Test string representations
        guid = Random_Guid()

        # str should return the UUID string
        str_repr = str(guid)
        assert len(str_repr) == 36
        assert is_guid(str_repr)

        # repr should show the class
        repr_str = repr(guid)
        assert repr_str == f"Random_Guid('{guid}')"

    def test_multiple_instances_in_single_statement(self):      # Test rapid generation
        # When creating multiple instances quickly
        guids = [Random_Guid() for _ in range(10)]

        # All should be unique
        assert len(set(guids)) == 10

        # All should be valid GUIDs
        for guid in guids:
            assert is_guid(guid)

    def test_use_in_collections(self):                          # Test in Type_Safe collections
        class Schema__Batch(Type_Safe):
            batch_id : Random_Guid
            item_ids : List[Random_Guid]

        with Schema__Batch() as _:
            assert type(_.batch_id) is Random_Guid
            assert type(_.item_ids) is Type_Safe__List        # Type_Safe__List actually

            # Add items
            for i in range(5):
                _.item_ids.append(Random_Guid())

            # All should be unique
            all_ids = [_.batch_id] + _.item_ids
            assert len(set(all_ids)) == 6                      # All unique

    def test_thread_safety_simulation(self):                    # Test concurrent generation
        # Simulate concurrent GUID generation
        import threading

        results = []
        lock = threading.Lock()

        def generate_guids():
            local_guids = []
            for _ in range(100):
                guid = Random_Guid()
                local_guids.append(guid)
            with lock:
                results.extend(local_guids)

        threads = []
        for _ in range(10):
            t = threading.Thread(target=generate_guids)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Should have 1000 unique GUIDs
        assert len(results) == 1000
        assert len(set(results)) == 1000                       # All unique

    def test_memory_behavior(self):                             # Test object identity
        guid1 = Random_Guid()
        guid2 = guid1                                          # Same object reference

        assert guid1 is guid2                                  # Same object
        assert guid1 == guid2                                  # Equal values

        # But new instance is different
        guid3 = Random_Guid()
        assert guid1 is not guid3                              # Different objects
        assert guid1 != guid3                                  # Different values

    def test_inheritance_chain(self):                           # Test type hierarchy
        guid = Random_Guid()

        # Check inheritance
        assert isinstance(guid, Random_Guid)
        assert isinstance(guid, Type_Safe__Primitive)
        assert isinstance(guid, str)

        # Should work in string contexts
        assert guid.upper() == str(guid).upper()
        assert guid.lower() == str(guid).lower()
        assert '-' in guid                                     # UUID has hyphens

    def test_default_behavior_in_function_params(self):         # Test as default parameter
        def process_request(request_id: Random_Guid = None):
            if request_id is None:
                request_id = Random_Guid()
            return request_id

        # Without providing ID
        id1 = process_request()
        id2 = process_request()
        assert id1 != id2                                      # Different each time

        # With providing ID
        specific_id = Random_Guid()
        id3 = process_request(specific_id)
        assert id3 == specific_id

    def test_edge_cases(self):                                  # Test edge behaviors
        # Many rapid instantiations
        guids = [Random_Guid() for _ in range(1000)]
        assert len(set(guids)) == 1000                         # All unique

        # Check that internal random_guid() is being used
        from osbot_utils.utils.Misc import random_guid
        raw_guid = random_guid()
        assert is_guid(raw_guid)
        assert len(raw_guid) == 36

        # Random_Guid should produce similar format
        typed_guid = Random_Guid()
        assert len(typed_guid) == len(raw_guid)
        assert typed_guid.count('-') == raw_guid.count('-')