import pytest
from unittest                                                       import TestCase
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__LastModified import Safe_Str__Http__LastModified


class test_Safe_Str__Http__LastModified(TestCase):

    def test_Safe_Str__Http__LastModified_class(self):
        # Standard RFC formats
        assert Safe_Str__Http__LastModified('Wed, 21 Oct 2023 07:28:00 GMT') == 'Wed, 21 Oct 2023 07:28:00 GMT'
        assert Safe_Str__Http__LastModified('Mon, 15 May 2024 12:30:45 GMT') == 'Mon, 15 May 2024 12:30:45 GMT'
        assert Safe_Str__Http__LastModified('Sat, 01 Jan 2022 00:00:00 GMT') == 'Sat, 01 Jan 2022 00:00:00 GMT'

        # Different date formats that might be used
        assert Safe_Str__Http__LastModified('2023-10-21T07:28:00Z') == '2023-10-21T07:28:00Z'
        assert Safe_Str__Http__LastModified('21 Oct 2023 07:28:00 GMT') == '21 Oct 2023 07:28:00 GMT'

        # Whitespace handling (trim_whitespace = True)
        assert Safe_Str__Http__LastModified('  Wed, 21 Oct 2023 07:28:00 GMT  ') == 'Wed, 21 Oct 2023 07:28:00 GMT'

        # Invalid characters get replaced
        assert Safe_Str__Http__LastModified('Wed, 21 Oct 2023<script>') == 'Wed, 21 Oct 2023_script_'
        assert Safe_Str__Http__LastModified('Wed; 21 Oct 2023') == 'Wed_ 21 Oct 2023'
        assert Safe_Str__Http__LastModified('Wed, 21/Oct/2023') == 'Wed, 21_Oct_2023'

        # Numeric conversion
        assert Safe_Str__Http__LastModified(20231021) == '20231021'

        # Edge cases and exceptions
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__LastModified(None)
        assert "Value cannot be None when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__LastModified('')
        assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__LastModified('<?&*^?>')  # All invalid chars
        assert "Sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__LastModified('   ')  # Spaces only (will be trimmed)
        assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__LastModified('a' * 65)  # Exceeds max length
        assert "Value exceeds maximum length of 64" in str(exc_info.value)