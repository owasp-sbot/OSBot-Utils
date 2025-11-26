import re
import pytest
from unittest                                                                            import TestCase
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
