import pytest
from unittest                                                                                    import TestCase

from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__SHA1__Short import Safe_Str__SHA1__Short


class test_Safe_Str__SHA1__Short(TestCase):
    """Test short 7-character SHA validation."""

    def test_valid_short_sha(self):
        # Valid 7-character SHAs
        assert str(Safe_Str__SHA1__Short('7fd1a60')) == '7fd1a60'
        assert str(Safe_Str__SHA1__Short('abc1234')) == 'abc1234'
        assert str(Safe_Str__SHA1__Short('0000000')) == '0000000'
        assert str(Safe_Str__SHA1__Short('fffffff')) == 'fffffff'

        # Mixed case
        assert str(Safe_Str__SHA1__Short('ABCDEF1')) == 'ABCDEF1'
        assert str(Safe_Str__SHA1__Short('AbCdEf1')) == 'AbCdEf1'

        # Whitespace trimming
        assert str(Safe_Str__SHA1__Short('  abc1234  ')) == 'abc1234'

    def test_invalid_short_sha(self):
        # Wrong length (too short)
        with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value must be exactly 7 characters long"):
            Safe_Str__SHA1__Short('abc123')  # Only 6 chars

        # Wrong length (too long)
        with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value must be exactly 7 characters long"):
            Safe_Str__SHA1__Short('abc12345')  # 8 chars

        # Invalid characters
        with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value does not match required pattern"):
            Safe_Str__SHA1__Short('abc123g')  # 'g' is not hex

        with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value does not match required pattern"):
            Safe_Str__SHA1__Short('abc-123')  # '-' is not hex

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value cannot be None when allow_empty is False"):
        assert Safe_Str__SHA1__Short(None) == ''

        #with pytest.raises(ValueError, match="in Safe_Str__SHA1__Short, value cannot be empty when allow_empty is False"):
        assert Safe_Str__SHA1__Short('') == ''


