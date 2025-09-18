import pytest
import re
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                      import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode              import Enum__Safe_Str__Regex_Mode
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash


class test_Safe_Str__Cache_Hash(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Cache_Hash() as _:
            assert type(_)                is Safe_Str__Cache_Hash
            assert _.regex.pattern        == r'^[a-f0-9]{10,96}$'
            assert _.regex_mode           == Enum__Safe_Str__Regex_Mode.MATCH
            assert _.min_length           == 10
            assert _.max_length           == 96
            assert _.strict_validation    is True
            assert _.allow_empty          is True
            assert _.trim_whitespace      is True

            # Empty initialization should be empty string
            assert str(_) == ''

    def test_valid_hashes(self):                                # Test valid hash patterns
        # Minimum length (10 chars)
        assert str(Safe_Str__Cache_Hash('a1b2c3d4e5'        )) == 'a1b2c3d4e5'
        assert str(Safe_Str__Cache_Hash('0123456789'        )) == '0123456789'
        assert str(Safe_Str__Cache_Hash('abcdefabcd'        )) == 'abcdefabcd'

        # Common lengths (16, 32, 40, 64)
        assert str(Safe_Str__Cache_Hash('a' * 16            )) == 'a' * 16  # MD5 subset
        assert str(Safe_Str__Cache_Hash('1234567890abcdef'  )) == '1234567890abcdef'
        assert str(Safe_Str__Cache_Hash('f' * 32            )) == 'f' * 32  # MD5 full
        assert str(Safe_Str__Cache_Hash('0' * 40            )) == '0' * 40  # SHA1
        assert str(Safe_Str__Cache_Hash('9' * 64            )) == '9' * 64  # SHA256

        # Maximum length (96 chars)
        assert str(Safe_Str__Cache_Hash('a' * 96            )) == 'a' * 96
        assert str(Safe_Str__Cache_Hash('0123456789abcdef' * 6)) == '0123456789abcdef' * 6

        # Mixed valid hex characters
        assert str(Safe_Str__Cache_Hash('a1b2c3d4e5f6a7b8c9d0')) == 'a1b2c3d4e5f6a7b8c9d0'
        assert str(Safe_Str__Cache_Hash('fedcba9876543210'    )) == 'fedcba9876543210'

        # Edge cases
        assert str(Safe_Str__Cache_Hash(None)) == ''
        assert str(Safe_Str__Cache_Hash(''  )) == ''

    def test_invalid_hashes(self):                              # Test invalid hash patterns

        error_msg_1 = re.escape("in Safe_Str__Cache_Hash, value does not match required pattern: ^[a-f0-9]{10,96}$")
        error_msg_2 = re.escape("in Safe_Str__Cache_Hash, value exceeds maximum length of 96 characters (was 97)")

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('abc')                                             # Too short (less than 10)

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('123456789')                                        # 9 chars

        with pytest.raises(ValueError, match=error_msg_2):
            Safe_Str__Cache_Hash('a' * 97)                                          # Too long (more than 96)

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('ABCDEFABCD')                                      # Uppercase not allowed

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('AbCdEfAbCd')                                      # Mixed case

        # Invalid characters (non-hex)
        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('ghijklmnop')                  # g-p not hex


        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('0123456789z')                 # 'z' not hex

        # Special characters
        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('abc-def-123')                 # Hyphens

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('abc_def_123')                 # Underscores

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('abc.def.123')                 # Dots

        with pytest.raises(ValueError, match=error_msg_1):
            Safe_Str__Cache_Hash('abc def 123')                 # Spaces


    def test_regex_mode_match(self):                            # Test MATCH mode behavior
        # MATCH mode means entire string must match pattern
        # Valid: exactly matches pattern
        valid_hash = 'a1b2c3d4e5'
        with Safe_Str__Cache_Hash(valid_hash) as _:
            assert str(_) == valid_hash

        # Invalid: partial match not enough in MATCH mode
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('a1b2c3d4e5 extra')            # Extra characters

        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('prefix a1b2c3d4e5')           # Prefix added

        # The regex is anchored with ^ and $
        assert Safe_Str__Cache_Hash.regex.pattern.startswith('^')
        assert Safe_Str__Cache_Hash.regex.pattern.endswith('$')

    def test_strict_validation(self):                           # Test strict validation mode
        # strict_validation = True means errors are raised, not replacements
        assert Safe_Str__Cache_Hash.strict_validation is True

        # This means invalid input raises ValueError immediately
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('INVALID')

        # No silent conversion or replacement happens
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('abc!def@123#')                # Special chars not replaced

    def test_trimming(self):                                    # Test whitespace trimming
        # Leading/trailing whitespace should be trimmed
        assert str(Safe_Str__Cache_Hash('  abcdef1234  '    )) == 'abcdef1234'
        assert str(Safe_Str__Cache_Hash('\tabcdef1234\t'    )) == 'abcdef1234'
        assert str(Safe_Str__Cache_Hash('\nabcdef1234\n'    )) == 'abcdef1234'
        assert str(Safe_Str__Cache_Hash('  \t abcdef1234 \n ')) == 'abcdef1234'

        # But internal spaces still invalid after trimming
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('  abc def 123  ')             # Spaces inside

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer (should convert to string then validate)
        with pytest.raises(ValueError):                         # Too short
            Safe_Str__Cache_Hash(123)

        # Valid length integer
        assert str(Safe_Str__Cache_Hash(1234567890  )) == '1234567890'

        # From another Safe_Str
        other = Safe_Str('abcdef1234')
        assert str(Safe_Str__Cache_Hash(other)) == 'abcdef1234'

        # Boolean should fail (converts to 'True'/'False' which aren't hex)
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash(True)

        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash(False)

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Cache_Entry(Type_Safe):
            primary_hash   : Safe_Str__Cache_Hash
            secondary_hash : Safe_Str__Cache_Hash = None
            backup_hash    : Safe_Str__Cache_Hash

        with Schema__Cache_Entry() as _:
            # Auto-initialization to empty string
            assert type(_.primary_hash  ) is Safe_Str__Cache_Hash
            assert type(_.backup_hash   ) is Safe_Str__Cache_Hash
            assert _.primary_hash        == ''
            assert _.backup_hash         == ''
            assert _.secondary_hash      is None

            # Setting with raw strings
            _.primary_hash = 'abc123def456'
            assert _.primary_hash == 'abc123def456'

            # Setting with invalid raises error
            with pytest.raises(ValueError):
                _.backup_hash = 'INVALID'

            # Setting nullable field
            _.secondary_hash = 'fedcba9876543210'
            assert _.secondary_hash == 'fedcba9876543210'

            # JSON serialization
            json_data = _.json()
            assert json_data['primary_hash'  ] == 'abc123def456'
            assert json_data['secondary_hash'] == 'fedcba9876543210'
            assert json_data['backup_hash'   ] == ''

    def test_common_hash_formats(self):                         # Test real-world hash patterns
        # MD5 subset (16 chars)
        md5_subset = 'd41d8cd98f00b204'
        assert str(Safe_Str__Cache_Hash(md5_subset)) == md5_subset

        # MD5 full (32 chars)
        md5_full = 'd41d8cd98f00b204e9800998ecf8427e'
        assert str(Safe_Str__Cache_Hash(md5_full)) == md5_full

        # SHA1 (40 chars)
        sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        assert str(Safe_Str__Cache_Hash(sha1)) == sha1

        # SHA256 (64 chars)
        sha256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        assert str(Safe_Str__Cache_Hash(sha256)) == sha256

        # Custom short hash (10 chars - minimum)
        short_hash = 'a1b2c3d4e5'
        assert str(Safe_Str__Cache_Hash(short_hash)) == short_hash

        # Custom long hash (96 chars - maximum)
        long_hash = 'a' * 96
        assert str(Safe_Str__Cache_Hash(long_hash)) == long_hash

    def test_edge_cases(self):                                  # Test edge cases
        # Empty string is allowed
        assert str(Safe_Str__Cache_Hash('')) == ''

        # Exactly at boundaries
        assert str(Safe_Str__Cache_Hash('0' * 10)) == '0' * 10  # Min length
        assert str(Safe_Str__Cache_Hash('f' * 96)) == 'f' * 96  # Max length

        # One char off boundaries
        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('0' * 9)                       # One too short

        with pytest.raises(ValueError):
            Safe_Str__Cache_Hash('f' * 97)                      # One too long

        # All same character (valid if hex)
        assert str(Safe_Str__Cache_Hash('aaaaaaaaaa'  )) == 'aaaaaaaaaa'
        assert str(Safe_Str__Cache_Hash('0000000000'  )) == '0000000000'
        assert str(Safe_Str__Cache_Hash('ffffffffff'  )) == 'ffffffffff'

        # Sequential characters
        assert str(Safe_Str__Cache_Hash('0123456789'  )) == '0123456789'
        assert str(Safe_Str__Cache_Hash('abcdefabcd'  )) == 'abcdefabcd'
        assert str(Safe_Str__Cache_Hash('9876543210'  )) == '9876543210'
        assert str(Safe_Str__Cache_Hash('fedcba9876'  )) == 'fedcba9876'

    def test_string_operations(self):                           # Test string behavior
        hash_val = Safe_Str__Cache_Hash('abc123def456')

        # String concatenation
        result = hash_val + '789'
        assert type(result) is Safe_Str__Cache_Hash             # Type preserved
        assert str(result)  == 'abc123def456789'

        # But invalid concatenation raises error
        with pytest.raises(ValueError):
            _ = hash_val + 'XYZ'                                # Non-hex chars

        # String formatting
        assert f"Hash: {hash_val}"         == "Hash: abc123def456"
        assert "Hash: {}".format(hash_val) == "Hash: abc123def456"

    def test_repr_and_str(self):                                # Test string representations
        hash_val = Safe_Str__Cache_Hash('fedcba9876543210')

        assert str(hash_val)  == 'fedcba9876543210'
        assert repr(hash_val) == "Safe_Str__Cache_Hash('fedcba9876543210')"

        # Empty hash
        empty = Safe_Str__Cache_Hash('')
        assert str(empty)  == ''
        assert repr(empty) == "Safe_Str__Cache_Hash('')"

    def test_comparison_operations(self):                       # Test comparisons
        hash1 = Safe_Str__Cache_Hash('abc123def456')
        hash2 = Safe_Str__Cache_Hash('abc123def456')
        hash3 = Safe_Str__Cache_Hash('fedcba987654')

        # Equality
        assert hash1 == hash2
        assert hash1 == 'abc123def456'
        assert 'abc123def456' == hash1

        # Inequality
        assert hash1 != hash3
        assert hash1 != 'fedcba987654'

        # Ordering (lexicographic)
        assert hash1 < hash3                                    # 'a' < 'f'
        assert hash3 > hash1
        assert hash1 <= hash2
        assert hash1 >= hash2

    def test_inheritance_from_safe_str(self):                   # Test Safe_Str inheritance
        hash_val = Safe_Str__Cache_Hash('abcdef1234')

        # Should inherit from Safe_Str
        assert isinstance(hash_val, Safe_Str__Cache_Hash)
        assert isinstance(hash_val, Safe_Str)
        assert isinstance(hash_val, str)

        # Should have Safe_Str attributes
        assert hasattr(hash_val, 'regex')
        assert hasattr(hash_val, 'regex_mode')
        assert hasattr(hash_val, 'max_length')
        assert hasattr(hash_val, 'min_length')

    def test_use_as_dict_key(self):                             # Test hashability
        hash1 = Safe_Str__Cache_Hash('abc123def456')
        hash2 = Safe_Str__Cache_Hash('fedcba987654')

        # Should work as dict keys
        cache_map = {
            hash1: 'value1',
            hash2: 'value2'
        }

        assert cache_map[hash1] == 'value1'
        assert cache_map[hash2] == 'value2'
        assert len(cache_map)   == 2

        # Same value should map to same key
        hash3 = Safe_Str__Cache_Hash('abc123def456')
        cache_map[hash3] = 'value3'
        assert len(cache_map)   == 2                            # Still 2, not 3
        assert cache_map[hash1] == 'value3'                     # Overwritten

    def test_variable_length_feature(self):                     # Test the variable-length aspect
        # This class specifically supports variable-length hashes (10-96)
        # unlike fixed-length hash classes

        lengths_to_test = [10, 16, 20, 32, 40, 48, 64, 80, 96]

        for length in lengths_to_test:
            hash_val = 'a' * length
            result = Safe_Str__Cache_Hash(hash_val)
            assert len(result) == length
            assert str(result) == hash_val

        # This flexibility allows different hash algorithms:
        # - Short custom hashes (10+)
        # - MD5 subsets (16)
        # - MD5 full (32)
        # - SHA1 (40)
        # - SHA256 (64)
        # - SHA384 (96)