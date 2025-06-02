import pytest
from unittest                                               import TestCase
from osbot_utils.helpers.safe_str.Safe_Str__Text__Dangerous import Safe_Str__Text__Dangerous, TYPE_SAFE_STR__TEXT__DANGEROUS__MAX_LENGTH


class test_Safe_Str__Text__Dangerous(TestCase):

    def test_Safe_Str__Text_class(self):
        # Basic text
        assert str(Safe_Str__Text__Dangerous('Hello World'     )) == 'Hello World'
        assert str(Safe_Str__Text__Dangerous('Hello, World!'   )) == 'Hello, World!'
        assert str(Safe_Str__Text__Dangerous('This is a test.' )) == 'This is a test.'

        # Numbers and alphanumerics
        assert str(Safe_Str__Text__Dangerous('User123'         )) == 'User123'
        assert str(Safe_Str__Text__Dangerous('Product #123'    )) == 'Product #123'
        assert str(Safe_Str__Text__Dangerous('100% satisfied'  )) == '100% satisfied'

        # Punctuation and special characters
        assert str(Safe_Str__Text__Dangerous('Hello, how are you?')) == 'Hello, how are you?'
        assert str(Safe_Str__Text__Dangerous('This: is a test.')) == 'This: is a test.'
        assert str(Safe_Str__Text__Dangerous('Items: one, two, three.')) == 'Items: one, two, three.'
        assert str(Safe_Str__Text__Dangerous('This costs $10.99!')) == 'This costs $10.99!'
        assert str(Safe_Str__Text__Dangerous('Available at 50% off!')) == 'Available at 50% off!'

        # Brackets and parentheses
        assert str(Safe_Str__Text__Dangerous('This (item) is [available]')) == 'This (item) is [available]'
        assert str(Safe_Str__Text__Dangerous('Required {min: 1, max: 10}')) == 'Required {min: 1, max: 10}'
        assert str(Safe_Str__Text__Dangerous('Points (10 + 5) * 2 = 30')) == 'Points (10 + 5) * 2 = 30'

        # Mathematical symbols
        assert str(Safe_Str__Text__Dangerous('x + y = z')) == 'x + y = z'
        assert str(Safe_Str__Text__Dangerous('5 * 10 = 50')) == '5 * 10 = 50'
        assert str(Safe_Str__Text__Dangerous('Price: $10 - $5 = $5')) == 'Price: $10 - $5 = $5'

        # Quotes and apostrophes
        assert str(Safe_Str__Text__Dangerous("Don't forget")) == "Don't forget"
        assert str(Safe_Str__Text__Dangerous('"Hello," she said.')) == '"Hello," she said.'

        # Unicode characters (should be replaced)
        assert str(Safe_Str__Text__Dangerous('café'  )) == 'caf_'
        assert str(Safe_Str__Text__Dangerous('résumé')) == 'r_sum_'
        assert str(Safe_Str__Text__Dangerous('naïve' )) == 'na_ve'

        # HTML/Script tags (should NOT be replaced)
        assert str(Safe_Str__Text__Dangerous('<script>alert("XSS")</script>')) == '<script>alert("XSS")</script>'
        assert str(Safe_Str__Text__Dangerous('<b>Bold</b>'                  )) == '<b>Bold</b>'

        # Mixed valid/invalid content
        assert str(Safe_Str__Text__Dangerous('Valid 😀 emoji')) == 'Valid _ emoji'
        assert str(Safe_Str__Text__Dangerous('Line1\nLine2'  )) == 'Line1\nLine2'
        assert str(Safe_Str__Text__Dangerous('Tab\tSeparated')) == 'Tab\tSeparated'

        # No trim behavior
        assert str(Safe_Str__Text__Dangerous('  Hello  '    )) == '  Hello  '
        assert str(Safe_Str__Text__Dangerous('\n\tHello\r\n')) == '\n\tHello\r\n'

        # Security patterns
        assert str(Safe_Str__Text__Dangerous('../etc/passwd')) == '../etc/passwd'  # This is valid in Safe_Str__Text
        assert str(Safe_Str__Text__Dangerous('SELECT * FROM users')) == 'SELECT * FROM users'
        assert str(Safe_Str__Text__Dangerous("/bin/bash -c 'rm -rf /'")) == "/bin/bash -c 'rm -rf /'"
        assert Safe_Str__Text__Dangerous('❤️👍') == '___'

        Safe_Str__Text__Dangerous(None)
        Safe_Str__Text__Dangerous('')
        Safe_Str__Text__Dangerous('    ')


        # Edge cases: exceptions with specific error message checks

        with pytest.raises(ValueError) as exc_info:  # exceeds max length
            Safe_Str__Text__Dangerous('a' * (TYPE_SAFE_STR__TEXT__DANGEROUS__MAX_LENGTH + 1))
        assert f"Value exceeds maximum length of {TYPE_SAFE_STR__TEXT__DANGEROUS__MAX_LENGTH}" in str(exc_info.value)

    def test_common_text_formats(self):
        """Test common text formats and patterns."""
        # Dates and times
        assert str(Safe_Str__Text__Dangerous('Date: 2023-03-15')) == 'Date: 2023-03-15'
        assert str(Safe_Str__Text__Dangerous('Time: 14:30:45'  )) == 'Time: 14:30:45'

        # Email-like patterns (@ is allowed)
        assert str(Safe_Str__Text__Dangerous('user@example.com')) == 'user@example.com'

        # URLs (all parts allowed)
        assert str(Safe_Str__Text__Dangerous('https://example.com#abc=123')) == 'https://example.com#abc=123'

        # Common delimiters in text
        assert str(Safe_Str__Text__Dangerous('Items: A, B, and C')) == 'Items: A, B, and C'
        assert str(Safe_Str__Text__Dangerous('Options: 1) First 2) Second')) == 'Options: 1) First 2) Second'
        assert str(Safe_Str__Text__Dangerous('Product #123 - Version 2.0')) == 'Product #123 - Version 2.0'

    def test__safe_str__dangerous_text(self):
        # Text that might be considered dangerous
        dangerous = Safe_Str__Text__Dangerous("<script>alert('xss')</script>")
        # Should preserve the dangerous text but mark it as dangerous type
        assert "<script>" in str(dangerous)
        assert repr(dangerous).startswith("Safe_Str__Text__Dangerous(")