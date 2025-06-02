import pytest
from unittest                                    import TestCase
from osbot_utils.helpers.safe_str.Safe_Str       import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__Text import Safe_Str__Text, TYPE_SAFE_STR__TEXT__MAX_LENGTH


class test_Safe_Str__Text(TestCase):

    def test_Safe_Str__Text_class(self):
        # Basic text
        assert str(Safe_Str__Text('Hello World'     )) == 'Hello World'
        assert str(Safe_Str__Text('Hello, World!'   )) == 'Hello, World_'
        assert str(Safe_Str__Text('This is a test.' )) == 'This is a test.'

        # Numbers and alphanumerics
        assert str(Safe_Str__Text('User123'       )) == 'User123'
        assert str(Safe_Str__Text('Product #123'  )) == 'Product _123'
        assert str(Safe_Str__Text('100% satisfied')) == '100_ satisfied'

        # Punctuation and special characters
        assert str(Safe_Str__Text('Hello, how are you?'     )) == 'Hello, how are you?'
        assert str(Safe_Str__Text('This: is a test.'        )) == 'This: is a test.'
        assert str(Safe_Str__Text('Items: one, two, three.' )) == 'Items: one, two, three.'
        assert str(Safe_Str__Text('This costs $10.99!'      )) == 'This costs _10.99_'
        assert str(Safe_Str__Text('Available at 50% off!'   )) == 'Available at 50_ off_'

        # Brackets and parentheses
        assert str(Safe_Str__Text('This (item) is [available]' )) == 'This (item) is [available]'
        assert str(Safe_Str__Text('Required {min: 1, max: 10}' )) == 'Required _min: 1, max: 10_'
        assert str(Safe_Str__Text('Points (10 + 5) * 2 = 30'   )) == 'Points (10 + 5) _ 2 = 30'

        # Mathematical symbols
        assert str(Safe_Str__Text('x + y = z'           )) == 'x + y = z'
        assert str(Safe_Str__Text('5 * 10 = 50'         )) == '5 _ 10 = 50'
        assert str(Safe_Str__Text('Price: $10 - $5 = $5')) == 'Price: _10 - _5 = _5'

        # Quotes and apostrophes
        assert str(Safe_Str__Text("Don't forget"      )) == "Don_t forget"
        assert str(Safe_Str__Text('"Hello," she said.')) == '_Hello,_ she said.'

        # Unicode characters (should be replaced)
        assert str(Safe_Str__Text('café')) == 'caf_'
        assert str(Safe_Str__Text('résumé')) == 'r_sum_'
        assert str(Safe_Str__Text('naïve')) == 'na_ve'

        # HTML/Script tags (should be replaced)
        assert str(Safe_Str__Text('<script>alert("XSS")</script>')) == '_script_alert(_XSS_)__script_'
        assert str(Safe_Str__Text('<b>Bold</b>'                   )) == '_b_Bold__b_'

        # Mixed valid/invalid content
        assert str(Safe_Str__Text('Valid 😀 emoji' )) == 'Valid _ emoji'
        assert str(Safe_Str__Text('Line1\nLine2'    )) == 'Line1_Line2'
        assert str(Safe_Str__Text('Tab\tSeparated'  )) == 'Tab_Separated'

        # Trimming behavior
        assert str(Safe_Str__Text('  Hello  ')) == '  Hello  '
        assert str(Safe_Str__Text('\n\tHello\r\n')) == '__Hello__'

        # Security patterns
        assert str(Safe_Str__Text('../etc/passwd'          )) == '.._etc_passwd'  # This is valid in Safe_Str__Text
        assert str(Safe_Str__Text('SELECT * FROM users'    )) == 'SELECT _ FROM users'
        assert str(Safe_Str__Text("/bin/bash -c 'rm -rf /'")) == "_bin_bash -c _rm -rf __"

        # Edge cases: exceptions with specific error message checks
        Safe_Str__Text(None)
        Safe_Str__Text('')
        Safe_Str__Text('❤️👍')
        Safe_Str__Text('    ')



        with pytest.raises(ValueError) as exc_info:  # exceeds max length
            Safe_Str__Text('a' * (TYPE_SAFE_STR__TEXT__MAX_LENGTH + 1))
        assert f"Value exceeds maximum length of {TYPE_SAFE_STR__TEXT__MAX_LENGTH}" in str(exc_info.value)

    def test_common_text_formats(self):
        """Test common text formats and patterns."""
        # Dates and times
        assert str(Safe_Str__Text('Date: 2023-03-15')) == 'Date: 2023-03-15'
        assert str(Safe_Str__Text('Time: 14:30:45'  )) == 'Time: 14:30:45'

        # Email-like patterns (@ is likely not allowed)
        assert str(Safe_Str__Text('user@example.com')) == 'user_example.com'

        # URLs (some parts likely not allowed)
        assert str(Safe_Str__Text('https://example.com')) == 'https:__example.com'

        # Common delimiters in text
        assert str(Safe_Str__Text('Items: A, B, and C'          )) == 'Items: A, B, and C'
        assert str(Safe_Str__Text('Options: 1) First 2) Second' )) == 'Options: 1) First 2) Second'
        assert str(Safe_Str__Text('Product #123 - Version 2.0'  )) == 'Product _123 - Version 2.0'

    def test__safe_str_text__string_representation(self):
        # Regular text
        text = Safe_Str__Text("This is a test message")
        assert str(text) == "This is a test message"
        assert f"{text}!" == "This is a test message!"
        assert repr(text) == "Safe_Str__Text('This is a test message')"

    def test__safe_str__edge_cases(self):
        # Empty string
        empty = Safe_Str("")
        assert str(empty)   == ""
        assert f"[{empty}]" == "[]"
        assert repr(empty)  == "Safe_Str('')"

        # Special characters that will be escaped
        special = Safe_Str__Text("Line1\nLine2\tTab")
        assert str(special)     == "Line1_Line2_Tab"
        assert "\n"         not in str(special)     # Newlines not preserved
        assert "\t"         not in str(special)     # Tabs not preserved

        # Unicode
        unicode_str = Safe_Str__Text("Hello __ _")
        assert str(unicode_str)          == "Hello __ _"
        assert f"Unicode: {unicode_str}" == "Unicode: Hello __ _"