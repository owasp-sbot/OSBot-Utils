import pytest
from unittest                                                            import TestCase
from osbot_utils.type_safe.primitives.safe_str.http.Safe_Str__Http__ETag import Safe_Str__Http__ETag


class test_Safe_Str__Http__ETag(TestCase):

    def test_Safe_Str__Http__ETag_class(self):
        # Strong ETags
        assert str(Safe_Str__Http__ETag('"abc123"')) == '"abc123"'
        assert str(Safe_Str__Http__ETag('"67890"')) == '"67890"'
        assert str(Safe_Str__Http__ETag('"a1b2c3d4e5f6"')) == '"a1b2c3d4e5f6"'
        assert str(Safe_Str__Http__ETag('"0123456789abcdef"')) == '"0123456789abcdef"'

        # Weak ETags
        assert str(Safe_Str__Http__ETag('W/"abc123"')) == 'W/"abc123"'
        assert str(Safe_Str__Http__ETag('W/"67890"')) == 'W/"67890"'
        assert str(Safe_Str__Http__ETag('W/"a1b2c3d4e5f6"')) == 'W/"a1b2c3d4e5f6"'

        # ETags with special characters
        assert str(Safe_Str__Http__ETag('"abc-123"')) == '"abc-123"'
        assert str(Safe_Str__Http__ETag('"file.txt"')) == '"file.txt"'
        assert str(Safe_Str__Http__ETag('"resource:123"')) == '"resource:123"'
        assert str(Safe_Str__Http__ETag('"v1.0/api"')) == '"v1.0/api"'
        assert str(Safe_Str__Http__ETag('"v1_2"')) == '"v1_2"'

        # Without quotes (still valid as HTTP servers can return them)
        assert str(Safe_Str__Http__ETag('abc123')) == 'abc123'
        assert str(Safe_Str__Http__ETag('67890')) == '67890'

        # Whitespace handling (trim_whitespace = True)
        assert str(Safe_Str__Http__ETag('  "abc123"  ')) == '"abc123"'
        assert str(Safe_Str__Http__ETag('W/"abc123"  ')) == 'W/"abc123"'

        # Numeric conversion
        assert str(Safe_Str__Http__ETag(12345)) == '12345'

        # Invalid characters get replaced
        assert Safe_Str__Http__ETag('"abc<script>123"'         ) == '"abc_script_123"'
        assert Safe_Str__Http__ETag('"abc!@#$%^&*()123"'       ) == '"abc__________123"'
        assert Safe_Str__Http__ETag('W/"abc+=[]{};\'\\<>?,123"') == 'W/"abc_____________123"'
        assert Safe_Str__Http__ETag('<?&*^?>'                  ) == '_______'

        # empty values
        assert Safe_Str__Http__ETag(None ) == ''
        assert Safe_Str__Http__ETag(''   ) == ''
        assert Safe_Str__Http__ETag('   ') == ''                # Spaces only (will be trimmed)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__ETag('a' * 129)  # Exceeds max length
        assert "in Safe_Str__Http__ETag, value exceeds maximum length of 128" in str(exc_info.value)

    def test_special_etag_formats(self):
        # More complex ETags that servers might generate
        assert str(Safe_Str__Http__ETag('"5d8e-3f4-f2340"')) == '"5d8e-3f4-f2340"'
        assert str(Safe_Str__Http__ETag('"5d8e_3f4_f2340"')) == '"5d8e_3f4_f2340"'
        assert str(Safe_Str__Http__ETag('"a.b.c.d"')) == '"a.b.c.d"'
        assert str(Safe_Str__Http__ETag('"v1.2.3:4567"')) == '"v1.2.3:4567"'

        # Non-standard but potentially used formats
        assert str(Safe_Str__Http__ETag('W/"v1-5d8e3f4f2340"')) == 'W/"v1-5d8e3f4f2340"'
        assert str(Safe_Str__Http__ETag('W/"a/b/c:12345"')) == 'W/"a/b/c:12345"'