import pytest
from unittest                                                                     import TestCase
from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__SHA1 import Safe_Str__SHA1


class test_Safe_Str__SHA1(TestCase):
    """Test full 40-character SHA validation."""

    def test_valid_full_sha(self):
        # Valid 40-character SHAs
        assert str(Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d')) == '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'
        assert str(Safe_Str__SHA1('abc1234567890abcdef1234567890abcdef12345')) == 'abc1234567890abcdef1234567890abcdef12345'
        assert str(Safe_Str__SHA1('0000000000000000000000000000000000000000')) == '0000000000000000000000000000000000000000'
        assert str(Safe_Str__SHA1('ffffffffffffffffffffffffffffffffffffffff')) == 'ffffffffffffffffffffffffffffffffffffffff'

        # Mixed case (both should work)
        assert str(Safe_Str__SHA1('ABCDEF1234567890ABCDEF1234567890ABCDEF12')) == 'ABCDEF1234567890ABCDEF1234567890ABCDEF12'
        assert str(Safe_Str__SHA1('AbCdEf1234567890aBcDeF1234567890AbCdEf12')) == 'AbCdEf1234567890aBcDeF1234567890AbCdEf12'

        # Whitespace trimming
        assert str(Safe_Str__SHA1('  7fd1a60b01f91b314f59955a4e4d4e80d8edf11d  ')) == '7fd1a60b01f91b314f59955a4e4d4e80d8edf11d'

    def test_invalid_full_sha(self):
        # Wrong length (too short)
        with pytest.raises(ValueError, match="in Safe_Str__SHA1, value must be exactly 40 characters long"):
            Safe_Str__SHA1('7fd1a60')  # Only 7 chars

        with pytest.raises(ValueError, match="in Safe_Str__SHA1, value must be exactly 40 characters long"):
            Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11')  # 39 chars

        # Wrong length (too long)
        with pytest.raises(ValueError, match="in Safe_Str__SHA1, value must be exactly 40 characters long"):
            Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11d0')  # 41 chars

        # Invalid characters
        with pytest.raises(ValueError, match="in Safe_Str__SHA1, value does not match required pattern"):
            Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11g')  # 'g' is not hex

        with pytest.raises(ValueError, match="in Safe_Str__SHA1, value does not match required pattern"):
            Safe_Str__SHA1('7fd1a60b01f91b314f59955a4e4d4e80d8edf11-')  # '-' is not hex

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__SHA1, value cannot be None when allow_empty is False"):
        assert Safe_Str__SHA1(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__SHA1, value cannot be empty when allow_empty is False"):
        assert Safe_Str__SHA1('') == ''


