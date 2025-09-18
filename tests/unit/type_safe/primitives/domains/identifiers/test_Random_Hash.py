import re

import pytest
from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Hash                       import Random_Hash
from osbot_utils.utils.Misc                                                                 import bytes_sha256

EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH = re.escape("in Random_Hash, value does not match required pattern: ^[a-f0-9]{10,96}$")

class test_Random_Hash(TestCase):

    def test__init__(self):                                      # Test basic initialization and inheritance
        with Random_Hash() as _:
            assert type(_)           is Random_Hash
            assert len(_)            == 16                      # Should be 16 chars as per Safe_Str__Cache_Hash
            assert isinstance(_, str) is True                   # Should be a string type
            assert isinstance(_, Safe_Str__Cache_Hash) is True  # Should inherit from Safe_Str__Cache_Hash

            # Verify it's a valid hex string
            assert all(c in '0123456789abcdef' for c in str(_))

    def test_auto_generation(self):                             # Test that Random_Hash generates unique values
        hash1 = Random_Hash()
        hash2 = Random_Hash()
        hash3 = Random_Hash()

        # Each should be unique (statistically)
        assert hash1 != hash2
        assert hash2 != hash3
        assert hash1 != hash3

        # All should be 16 characters
        assert len(hash1) == 16
        assert len(hash2) == 16
        assert len(hash3) == 16

    def test_with_explicit_value(self):                         # Test providing explicit value
        explicit_value = 'abc123def4567890'

        with Random_Hash(explicit_value) as _:
            assert str(_) == explicit_value
            assert len(_) == 16

        # Test that explicit value goes through Safe_Str__Cache_Hash validation

        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            Random_Hash('invalid!')                                         # Invalid characters for hash

        # Test length validation from Safe_Str__Cache_Hash
        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            Random_Hash('abc')                                  # Too short

        expected_error_2 = "in Random_Hash, value exceeds maximum length of 96 characters (was 190)"
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            Random_Hash('abc123def4567890abc'*10)                  # Too long


    def test_none_value(self):                                  # Test None generates random hash
        hash_with_none = Random_Hash(None)

        assert hash_with_none is not None
        assert len(hash_with_none) == 16
        assert isinstance(hash_with_none, Random_Hash)

        # Should generate different value each time
        hash_with_none2 = Random_Hash(None)
        assert hash_with_none != hash_with_none2

    def test_string_operations(self):                           # Test string behavior
        hash_val = Random_Hash()

        # String concatenation
        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            result = hash_val + '_suffix'                                       # concat needs to be valid hash values
        result = hash_val + '001122'
        assert type(result) is Random_Hash                                      # doesn't lose type safety
        assert len(result) == 22
        assert result == f'{hash_val}001122'

        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            'prefix_' + hash_val
        result = '001122' + hash_val
        assert type(result) is Random_Hash                                      # doesn't lose type safety
        assert len(result)  == 22
        assert result       == f'001122{hash_val}'

        # String formatting
        assert f"Hash: {hash_val}"         == f"Hash: {str(hash_val)}"
        assert "Hash: {}".format(hash_val) == f"Hash: {str(hash_val)}"

    def test_repr_and_str(self):                                # Test string representations
        explicit_hash = Random_Hash('1234567890abcdef')

        assert str(explicit_hash)  == '1234567890abcdef'
        assert repr(explicit_hash) == "Random_Hash('1234567890abcdef')"

        # Random hash should have predictable repr format
        random_hash = Random_Hash()
        assert repr(random_hash).startswith("Random_Hash('")
        assert repr(random_hash).endswith("')")

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Cached_Item(Type_Safe):
            cache_hash     : Random_Hash                        # Auto-generates on init
            backup_hash    : Random_Hash = None                 # Explicitly nullable
            reference_hash : Safe_Str__Cache_Hash               # Parent type

        with Schema__Cached_Item() as _:
            # Auto-initialization creates random hash
            assert type(_.cache_hash) is Random_Hash
            assert len(_.cache_hash)  == 16

            # Backup hash is None by default
            assert _.backup_hash is None

            # Reference hash uses parent type
            assert type(_.reference_hash) is Safe_Str__Cache_Hash

            # Setting explicit value
            _.backup_hash = Random_Hash('fedcba0987654321')
            assert _.backup_hash == 'fedcba0987654321'

            # Can assign Random_Hash to Safe_Str__Cache_Hash field
            _.reference_hash = Random_Hash()
            assert len(_.reference_hash) == 16

            # JSON serialization
            json_data = _.json()
            assert len(json_data['cache_hash']) == 16
            assert json_data['backup_hash'] == 'fedcba0987654321'
            assert len(json_data['reference_hash']) == 16

    def test_deterministic_generation_from_bytes(self):         # Test internal hash generation logic
        # The implementation uses bytes_sha256 with random_bytes
        # We can't test exact values due to randomness, but can verify format

        test_bytes = b'test_data_123'
        hash_from_bytes = bytes_sha256(test_bytes)[:16]

        # Should be valid hex
        assert all(c in '0123456789abcdef' for c in hash_from_bytes)
        assert len(hash_from_bytes) == 16

    def test_type_hierarchy(self):                              # Test inheritance chain
        hash_val = Random_Hash()

        # Check inheritance
        assert isinstance(hash_val, Random_Hash)
        assert isinstance(hash_val, Safe_Str__Cache_Hash)
        assert isinstance(hash_val, str)

        # Should work anywhere Safe_Str__Cache_Hash is expected
        def process_cache_hash(hash_val: Safe_Str__Cache_Hash) -> str:
            return f"Processing: {hash_val}"

        result = process_cache_hash(hash_val)
        assert result.startswith("Processing: ")

    def test_multiple_instantiations_are_unique(self):          # Test randomness property
        hashes = [Random_Hash() for _ in range(100)]

        # All should be unique (statistically)
        unique_hashes = set(hashes)
        assert len(unique_hashes) == 100                        # No collisions in 100 generations

        # All should be valid format
        for h in hashes:
            assert len(h) == 16
            assert all(c in '0123456789abcdef' for c in str(h))

    def test_edge_cases(self):                                              # Test edge cases
        hash_from_empty_value = Random_Hash('')
        assert hash_from_empty_value!= ''                                   # empty string will create a valid hash
        assert Random_Hash(hash_from_empty_value) == hash_from_empty_value  # has confirmed here

        # Non-hex characters should fail
        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            Random_Hash('ghijklmnopqrstuv')                     # 16 chars but not hex


        # Mixed case should work (lowercase in hex)
        lower_hash = Random_Hash('abcdef0123456789')
        assert str(lower_hash) == 'abcdef0123456789'

        # Uppercase should fail (Safe_Str__Cache_Hash expects lowercase)
        with pytest.raises(ValueError, match=EXPECTED__VALUE_ERROR_MESSAGE__RANDOM_HASH):
            Random_Hash('ABCDEF0123456789')

    def test_comparison_operations(self):                       # Test comparison with strings and other hashes
        hash1 = Random_Hash('1234567890abcdef')
        hash2 = Random_Hash('1234567890abcdef')
        hash3 = Random_Hash('fedcba0987654321')

        # Same value comparisons
        assert hash1 == hash2
        assert hash1 == '1234567890abcdef'
        assert '1234567890abcdef' == hash1

        # Different value comparisons
        assert hash1 != hash3
        assert hash1 != 'fedcba0987654321'

        # Ordering comparisons (lexicographic)
        assert hash1 < hash3  # '1' < 'f'
        assert hash3 > hash1


    # note: the test below helped to identify and eventually fix the nasty bug described in
    #       test__regression__type_safety_assignments__on_obj__bool_assigned_to_int
    def test_use_in_cache_service(self):
        class Cache_Entry(Type_Safe):
            entry_id    : Random_Hash                            # Auto-generates
            #random_guid : Random_Guid
            parent_hash: Random_Hash = None
        entry1 = Cache_Entry()
        entry2 = Cache_Entry()

        assert entry1.entry_id    != entry2.entry_id
        # Can link entries
        entry2.parent_hash = entry1.entry_id
        assert entry2.parent_hash == entry1.entry_id

        # Can use as dict keys (hashable)
        cache_map = {
            entry1.entry_id: entry1,
            entry2.entry_id: entry2
        }
        assert len(cache_map) == 2
        assert cache_map[entry1.entry_id] is entry1