import pytest
from unittest import TestCase

from osbot_utils.helpers.safe_str.http.Safe_Str__Http__ContentType import Safe_Str__Http__ContentType


class test_Safe_Str__Http__ContentType(TestCase):

    def test_Safe_Str__Http__ContentType_class(self):
        # Standard MIME types
        assert Safe_Str__Http__ContentType('text/html'       ) == 'text/html'
        assert Safe_Str__Http__ContentType('application/json') == 'application/json'
        assert Safe_Str__Http__ContentType('image/jpeg'      ) == 'image/jpeg'
        assert Safe_Str__Http__ContentType('audio/mpeg'      ) == 'audio/mpeg'
        assert Safe_Str__Http__ContentType('video/mp4'       ) == 'video/mp4'

        # With parameters
        assert Safe_Str__Http__ContentType('text/html; charset=utf-8'       ) == 'text/html; charset=utf-8'
        assert Safe_Str__Http__ContentType('application/json; charset=utf-8') == 'application/json; charset=utf-8'
        assert Safe_Str__Http__ContentType('text/plain; charset=iso-8859-1' ) == 'text/plain; charset=iso-8859-1'

        # Complex content types
        assert Safe_Str__Http__ContentType('application/vnd.api+json'       ) == 'application/vnd.api+json'
        assert Safe_Str__Http__ContentType('application/ld+json'            ) == 'application/ld+json'
        assert Safe_Str__Http__ContentType('application/vnd.ms-excel'       ) == 'application/vnd.ms-excel'

        # Whitespace handling (trim_whitespace = True)
        assert Safe_Str__Http__ContentType('  text/html  '                    ) == 'text/html'
        assert Safe_Str__Http__ContentType('application/json; charset=utf-8  ') == 'application/json; charset=utf-8'

        # Numeric conversion
        assert Safe_Str__Http__ContentType(12345) == '12345'

        # Invalid characters get replaced
        assert Safe_Str__Http__ContentType('text/html<script>'                ) == 'text/html_script_'
        assert Safe_Str__Http__ContentType('text/html:invalid'                ) == 'text/html_invalid'
        assert Safe_Str__Http__ContentType('text@html'                        ) == 'text_html'

        # Edge cases and exceptions
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ContentType(None)
        assert "Value cannot be None when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ContentType('')
        assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ContentType('<?&*^?>')  # All invalid chars
        assert "Sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ContentType('   ')  # Spaces only (will be trimmed)
        assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ContentType('a' * 257)  # Exceeds max length
        assert "Value exceeds maximum length of 256" in str(exc_info.value)