import pytest
from unittest                                                            import TestCase
from osbot_utils.utils.Str                                               import trim
from osbot_utils.type_safe.primitives.safe_str.http.Safe_Str__Http__Text import Safe_Str__Http__Text, TYPE_SAFE_STR__TEXT__MAX_LENGTH



class test_Safe_Str__Http__Text(TestCase):

    def test_Safe_Str__Http__Text_basic(self):
        # Basic text with various allowed characters
        assert str(Safe_Str__Http__Text("Hello, world!"         )) == "Hello, world!"
        assert str(Safe_Str__Http__Text("This is a test. 123"   )) == "This is a test. 123"
        assert str(Safe_Str__Http__Text("Line 1\nLine 2"        )) == "Line 1\nLine 2"

        # Text with various punctuation and special characters
        assert str(Safe_Str__Http__Text("Symbols: !@#$%^&*()_+-=[]{}|;':\",./<>?")) == "Symbols: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        assert str(Safe_Str__Http__Text("Math: 5 + 5 = 10, 10 * 10 = 100")) == "Math: 5 + 5 = 10, 10 * 10 = 100"
        assert str(Safe_Str__Http__Text("Currency: $100, €50, £75, ¥500")) == "Currency: $100, €50, £75, ¥500"

        # Whitespace handling (trim_whitespace = True)
        assert str(Safe_Str__Http__Text("  Hello  ")) == "Hello"
        assert str(Safe_Str__Http__Text("\tTabbed text\t")) == "Tabbed text"
        assert str(Safe_Str__Http__Text("\nText with newlines\n")) == "Text with newlines"

        # Newline normalization (normalize_newlines = True)
        assert str(Safe_Str__Http__Text("Windows\r\nLine\r\nBreaks" )) == "Windows\nLine\nBreaks"
        assert str(Safe_Str__Http__Text("Mac\rLine\rBreaks"         )) == "Mac\nLine\nBreaks"
        assert str(Safe_Str__Http__Text("Mixed\nLine\r\nBreaks\r"   )) == "Mixed\nLine\nBreaks"

        # Empty and None handling (allow_empty = True)
        assert str(Safe_Str__Http__Text("")) == ""
        assert str(Safe_Str__Http__Text(None)) == ""

        # Unicode text
        assert str(Safe_Str__Http__Text("Unicode: ☺ ♥ ★ ☆ ☂ ☃ ♫ ♪")) == "Unicode: ☺ ♥ ★ ☆ ☂ ☃ ♫ ♪"
        assert str(Safe_Str__Http__Text("Languages: English, Español, Français, Deutsch, 日本語, 中文, Русский")) == "Languages: English, Español, Français, Deutsch, 日本語, 中文, Русский"

    def test_Safe_Str__Http__Text_control_chars(self):
        # Text with control characters (should be filtered out)
        input_with_control = "Text with control chars: \x00\x01\x02\x03"
        expected = "Text with control chars: ____"
        assert str(Safe_Str__Http__Text(input_with_control)) == expected

        # Text with other problematic sequences
        input_with_escape = "Text with escape sequences: \x1B[31mRed\x1B[0m" # ANSI color codes
        expected = "Text with escape sequences: _[31mRed_[0m"
        assert str(Safe_Str__Http__Text(input_with_escape)) == expected

    def test_Safe_Str__Http__Text_length_limits(self):
        # Text at the limit
        text_at_limit = "a" * TYPE_SAFE_STR__TEXT__MAX_LENGTH
        assert len(str(Safe_Str__Http__Text(text_at_limit))) == TYPE_SAFE_STR__TEXT__MAX_LENGTH

        # Text exceeding the limit
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Text("a" * (TYPE_SAFE_STR__TEXT__MAX_LENGTH + 1))
        assert f"in Safe_Str__Http__Text, value exceeds maximum length of {TYPE_SAFE_STR__TEXT__MAX_LENGTH}" in str(exc_info.value)

    def test_Safe_Str__Http__Text_code_snippets(self):
        # Python code snippet
        python_code = """def hello_world():
    print("Hello, world!")
    return True
"""
        assert str(Safe_Str__Http__Text(python_code)) == trim(python_code)

        # JavaScript code snippet
        js_code = """function helloWorld() {
    console.log("Hello, world!");
    return true;
}
"""
        assert str(Safe_Str__Http__Text(js_code)) == trim(js_code)

        # HTML snippet
        html_snippet = """<div class="container">
    <h1>Hello, world!</h1>
    <p>This is a paragraph.</p>
</div>
"""
        assert str(Safe_Str__Http__Text(html_snippet)) == trim(html_snippet)

        # SQL snippet
        sql_snippet = """SELECT id, name, email 
FROM users 
WHERE status = 'active' 
ORDER BY name ASC;
"""
        assert str(Safe_Str__Http__Text(sql_snippet)) == trim(sql_snippet)

    def test_Safe_Str__Http__Text_multiline(self):
        # Multiline text with various formatting
        multiline = """# Title
        
## Subtitle

This is a paragraph with *emphasis* and **strong** text.

- List item 1
- List item 2
- List item 3

1. Numbered item 1
2. Numbered item 2
3. Numbered item 3

> This is a blockquote.

```python
def hello():
    print("Hello, world!")
```    
"""
        assert str(Safe_Str__Http__Text(multiline)) == multiline.strip()  # because trim_whitespace=True