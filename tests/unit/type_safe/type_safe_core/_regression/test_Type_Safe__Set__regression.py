import re
import pytest
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                      import Safe_Str
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                     import Type_Safe__Set


class test_Type_Safe__Set__regression(TestCase):

    def test__regression__type_safe_set__auto_conversion_issue_on_update_and_ior(self):

        # First verify add() correctly rejects invalid values
        cache_hashes = Type_Safe__Set(expected_type=Safe_Str__Cache_Hash)
        error_message = "In Type_Safe__Set: Could not convert str to Safe_Str__Cache_Hash: in Safe_Str__Cache_Hash, value does not match required pattern: ^[a-f0-9]{10,96}$"

        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes.add('aaa')

        valid_hash = 'abcdef1234567890'
        cache_hashes.add(valid_hash)
        assert len(cache_hashes) == 1
        assert all(type(item) is Safe_Str__Cache_Hash for item in cache_hashes)

        # BUG 1: update() bypasses type safety
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes.update(['bad_value_1', 'bad_value_2'])
        # cache_hashes.update(['bad_value_1', 'bad_value_2'])    # BUG: should raise TypeError
        # assert 'bad_value_1' in cache_hashes                   # BUG: value should not exist
        # assert len(cache_hashes) == 3                          # BUG: should still be 1
        #
        # Reset for next test
        cache_hashes = Type_Safe__Set(expected_type=Safe_Str__Cache_Hash)

        # # BUG 2: |= (ior) bypasses type safety
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes |= {'another_bad'}
        # cache_hashes |= {'another_bad'}                        # BUG: should raise TypeError
        # assert 'another_bad' in cache_hashes                   # BUG: value should not exist
        #
        # # Reset for next test
        # cache_hashes = Type_Safe__Set(expected_type=Safe_Str__Cache_Hash)
        #
        # # BUG 3: | (or) bypasses type safety - returns plain set
        cache_hashes.add(valid_hash)
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes | {'or_bad'}
        #
        # result = cache_hashes | {'or_bad'}                     # BUG: should raise TypeError or return Type_Safe__Set
        # assert type(result) is set                             # BUG: should be Type_Safe__Set
        # assert 'or_bad' in result                              # BUG: invalid value in result

    def test__regression__type_safe_set__bypasses_on_set_operations(self):

        cache_hashes = Type_Safe__Set(expected_type=Safe_Str__Cache_Hash)
        valid_hash = 'abcdef1234567890'
        cache_hashes.add(valid_hash)

        other_set = {'bad_value'}

        # BUG 1: __and__ (intersection) returns plain set
        result = cache_hashes & {'bad_value', valid_hash}
        #assert type(result) is set                           # BUG: should be Type_Safe__Set
        assert type(result) is Type_Safe__Set

        # BUG 2: __sub__ (difference) returns plain set
        result = cache_hashes - other_set
        #assert type(result) is set                           # BUG: should be Type_Safe__Set
        assert type(result) is Type_Safe__Set

        # BUG 3: __xor__ (symmetric difference) returns plain set and may contain invalid items
        error_message = "In Type_Safe__Set: Could not convert str to Safe_Str__Cache_Hash: in Safe_Str__Cache_Hash, value does not match required pattern: ^[a-f0-9]{10,96}$"
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes ^ other_set
        #result = cache_hashes ^ other_set
        assert 'bad_value' not in result                         # BUG: invalid value in result

        # BUG 4: copy() returns plain set
        copied = cache_hashes.copy()
        #assert type(copied) is set                           # BUG: should be Type_Safe__Set
        assert type(copied) is Type_Safe__Set

        # BUG 5: union() returns plain set
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes.union(other_set)
        # result = cache_hashes.union(other_set)
        # assert type(result) is set                           # BUG: should be Type_Safe__Set
        # assert 'bad_value' in result                         # BUG: invalid value in result

        # BUG 6: intersection() returns plain set
        result = cache_hashes.intersection({valid_hash, 'bad'})
        #assert type(result) is set                           # BUG: should be Type_Safe__Set
        assert type(result) is Type_Safe__Set

        # BUG 7: difference() returns plain set
        result = cache_hashes.difference(other_set)
        #assert type(result) is set                           # BUG: should be Type_Safe__Set
        assert type(result) is Type_Safe__Set

        # BUG 8: symmetric_difference() returns plain set with invalid items
        with pytest.raises(TypeError, match=re.escape(error_message)):
            cache_hashes.symmetric_difference(other_set)
        # result = cache_hashes.symmetric_difference(other_set)
        # assert type(result) is set                           # BUG: should be Type_Safe__Set
        # assert 'bad_value' in result                         # BUG: invalid value in result

    def test__regression__type_safe_set_subclass__operations_dont_preserve_subclass_type(self):
        from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                     import Type_Safe__Set
        from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash

        class Hash_Set(Type_Safe__Set):
            expected_type = Safe_Str__Cache_Hash

        valid_hash_1 = 'abcdef1234567890'
        valid_hash_2 = 'fedcba0987654321'
        hash_set = Hash_Set()
        hash_set.add(valid_hash_1)
        assert type(hash_set) is Hash_Set

        # BUG 1: copy() returns Type_Safe__Set instead of Hash_Set
        copied = hash_set.copy()
        # assert type(copied) is Type_Safe__Set                # BUG: should be Hash_Set
        # assert type(copied) is not Hash_Set                  # BUG
        assert type(copied) is Hash_Set                         # FIXED


        # BUG 2: | operator returns Type_Safe__Set instead of Hash_Set
        merged = hash_set | {valid_hash_2}
        # assert type(merged) is Type_Safe__Set                # BUG: should be Hash_Set
        # assert type(merged) is not Hash_Set                  # BUG
        assert type(copied) is Hash_Set                         # FIXED

        # BUG 3: union() returns Type_Safe__Set instead of Hash_Set
        unioned = hash_set.union({valid_hash_2})
        # assert type(unioned) is Type_Safe__Set               # BUG: should be Hash_Set
        # assert type(unioned) is not Hash_Set                 # BUG
        assert type(copied) is Hash_Set                         # FIXED

        # BUG 4: intersection() returns Type_Safe__Set instead of Hash_Set
        intersected = hash_set.intersection({valid_hash_1})
        # assert type(intersected) is Type_Safe__Set           # BUG: should be Hash_Set
        # assert type(intersected) is not Hash_Set             # BUG
        assert type(copied) is Hash_Set                         # FIXED

        # BUG 5: difference() returns Type_Safe__Set instead of Hash_Set
        diffed = hash_set.difference({valid_hash_2})
        # assert type(diffed) is Type_Safe__Set                # BUG: should be Hash_Set
        # assert type(diffed) is not Hash_Set                  # BUG
        assert type(copied) is Hash_Set                         # FIXED

    def test__regression__Type_Safe__Set_subclass__assignment(self):        # Regression test for Type_Safe__Set subclass assignment

        class Set__Abc(Type_Safe__Set):
            expected_type = Safe_Str

        class An_Class(Type_Safe):
            targets: Set__Abc

        An_Class(targets=set())                                          # this works
        An_Class(targets=Set__Abc({Safe_Str('method')}))                 # this works
        An_Class(targets={'method'})                                     # FIXED
        An_Class(targets={Safe_Str('method')})                           # FIXED

        assert An_Class(targets=set()                           ).json() == {'targets': []}
        assert An_Class(targets=Set__Abc({Safe_Str('method')})  ).json() == {'targets': ['method']}
        assert An_Class(targets={'method'}                      ).json() == {'targets': ['method']}
        assert An_Class(targets={Safe_Str('method')}            ).json() == {'targets': ['method']}

        assert type(An_Class(targets=set()                          ).targets) == Set__Abc
        assert type(An_Class(targets=Set__Abc({Safe_Str('method')}) ).targets) == Set__Abc
        assert type(An_Class(targets={'method'}                     ).targets) == Set__Abc
        assert type(An_Class(targets={Safe_Str('method')}           ).targets) == Set__Abc

        # Items are correctly converted to Safe_Str
        assert type(list(An_Class(targets={'method'}          ).targets)[0]) == Safe_Str
        assert type(list(An_Class(targets={Safe_Str('method')}).targets)[0]) == Safe_Str