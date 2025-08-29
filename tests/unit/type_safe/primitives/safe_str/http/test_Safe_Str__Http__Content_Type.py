import pytest
from unittest                                                                    import TestCase
from osbot_utils.type_safe.primitives.safe_str.http.Safe_Str__Http__Content_Type import Safe_Str__Http__Content_Type
from osbot_utils.type_safe.primitives.safe_str.http.Safe_Str__Http__Text         import Safe_Str__Http__Text


class test_Safe_Str__Http__Content_Type(TestCase):

    def test_Safe_Str__Http__ContentType_class(self):
        # Standard MIME types
        assert Safe_Str__Http__Content_Type('text/html') == 'text/html'
        assert Safe_Str__Http__Content_Type('application/json') == 'application/json'
        assert Safe_Str__Http__Content_Type('image/jpeg') == 'image/jpeg'
        assert Safe_Str__Http__Content_Type('audio/mpeg') == 'audio/mpeg'
        assert Safe_Str__Http__Content_Type('video/mp4') == 'video/mp4'

        # With parameters
        assert Safe_Str__Http__Content_Type('text/html; charset=utf-8') == 'text/html; charset=utf-8'
        assert Safe_Str__Http__Content_Type('application/json; charset=utf-8') == 'application/json; charset=utf-8'
        assert Safe_Str__Http__Content_Type('text/plain; charset=iso-8859-1') == 'text/plain; charset=iso-8859-1'

        # Complex content types
        assert Safe_Str__Http__Content_Type('application/vnd.api+json') == 'application/vnd.api+json'
        assert Safe_Str__Http__Content_Type('application/ld+json') == 'application/ld+json'
        assert Safe_Str__Http__Content_Type('application/vnd.ms-excel') == 'application/vnd.ms-excel'

        # Whitespace handling (trim_whitespace = True)
        assert Safe_Str__Http__Content_Type('  text/html  ') == 'text/html'
        assert Safe_Str__Http__Content_Type('application/json; charset=utf-8  ') == 'application/json; charset=utf-8'

        # Numeric conversion
        assert Safe_Str__Http__Content_Type(12345) == '12345'

        # Invalid characters get replaced
        assert Safe_Str__Http__Content_Type('text/html<script>') == 'text/html_script_'
        assert Safe_Str__Http__Content_Type('text/html:invalid') == 'text/html_invalid'
        assert Safe_Str__Http__Content_Type('text@html') == 'text_html'

        # Edge cases and exceptions
        #with pytest.raises(ValueError) as exc_info:
        assert Safe_Str__Http__Content_Type(None) == ''
        #assert "in Safe_Str__Http__Content_Type, value cannot be None when allow_empty is False" in str(exc_info.value)

        #with pytest.raises(ValueError) as exc_info:
        assert Safe_Str__Http__Content_Type('') == ''
        #assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Content_Type('<?&*^?>')  # All invalid chars
        assert "in Safe_Str__Http__Content_Type, sanitized value consists entirely of '_' characters" in str(exc_info.value)

        #with pytest.raises(ValueError) as exc_info:
        assert Safe_Str__Http__Content_Type('   ') == '' # Spaces only (will be trimmed)
        #assert "in Safe_Str__Http__Content_Type, value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Content_Type('a' * 257)  # Exceeds max length
        assert "in Safe_Str__Http__Content_Type, value exceeds maximum length of 256" in str(exc_info.value)

    def test__safe_str__http_types(self):
        # HTTP Content-Type
        content_type = Safe_Str__Http__Content_Type("application/json")
        assert str(content_type) == "application/json"
        assert f"Content-Type: {content_type}" == "Content-Type: application/json"

        # HTTP Text
        http_text = Safe_Str__Http__Text("GET /api/users HTTP/1.1")
        assert str(http_text) == "GET /api/users HTTP/1.1"