import re
import pytest
from unittest                                                                           import TestCase
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Message__User import Safe_Str__LLM__Message__User


class test_Safe_Str__LLM__Message__User(TestCase):

    def test__init__(self):                                                         # Test initialization
        with Safe_Str__LLM__Message__User() as _:
            assert type(_)         is Safe_Str__LLM__Message__User
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 32768                                        # Full context for user input
            assert _.regex.pattern == r'[\x00-\x08\x0B\x0C\x0E-\x1F]'            # Preserves tabs/newlines

    def test_user_input_preserved(self):                                           # Test typical user messages
        # Simple questions
        assert Safe_Str__LLM__Message__User('What is Python?')      == 'What is Python?'
        assert Safe_Str__LLM__Message__User('How do I learn AI?')   == 'How do I learn AI?'

        # Complex queries with formatting
        user1 = """Please help me debug this code:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
        
It's running slowly for large values."""

        result = Safe_Str__LLM__Message__User(user1)
        assert result == user1                                              # All preserved including newlines
        assert '\n' in result                                              # Newlines preserved
        assert '    ' in result                                            # Indentation preserved

    def test_special_content_types(self):                                          # Test various content types
        # Code with special characters
        code = 'print("Hello, World!")\nx = {"key": [1, 2, 3]}'
        assert Safe_Str__LLM__Message__User(code) == code

        # Markdown
        markdown = """# Title
- Item 1
- Item 2
**Bold** and *italic* text"""
        assert Safe_Str__LLM__Message__User(markdown) == markdown

        # Data/JSON
        json_data = '{"user_id": 12345, "query": "test", "metadata": null}'
        assert Safe_Str__LLM__Message__User(json_data) == json_data

        # URLs and paths
        url = 'Check this: https://example.com/path?query=value&param=123'
        assert Safe_Str__LLM__Message__User(url) == url

    def test_whitespace_preservation(self):                                        # Test whitespace handling
        # Tabs preserved (0x09 not in removal range)
        assert Safe_Str__LLM__Message__User('Col1\tCol2\tCol3')     == 'Col1\tCol2\tCol3'

        # Newlines preserved (0x0A not in removal range)
        assert Safe_Str__LLM__Message__User('Line1\nLine2\nLine3')  == 'Line1\nLine2\nLine3'

        # Carriage returns preserved (0x0D not in removal range)
        assert Safe_Str__LLM__Message__User('Text\rMore')           == 'Text\rMore'

        # Multiple spaces
        assert Safe_Str__LLM__Message__User('Space    test')        == 'Space    test'

    def test_control_char_replacement(self):                                          # Test control character removal
        # Null byte and other controls removed
        assert Safe_Str__LLM__Message__User('Hello\x00World')       == 'Hello_World'
        assert Safe_Str__LLM__Message__User('Test\x01Text')         == 'Test_Text'
        assert Safe_Str__LLM__Message__User('Bell\x07Sound')        == 'Bell_Sound'

        # Vertical tab and form feed removed
        assert Safe_Str__LLM__Message__User('Text\x0BVTab')         == 'Text_VTab'
        assert Safe_Str__LLM__Message__User('Page\x0CBreak')        == 'Page_Break'

    def test_unicode_and_emojis(self):                                           # Test international content
        # Emojis
        assert Safe_Str__LLM__Message__User('Hello 👋 World 🌍')     == 'Hello 👋 World 🌍'

        # Various languages
        assert Safe_Str__LLM__Message__User('你好世界')              == '你好世界'
        assert Safe_Str__LLM__Message__User('مرحبا بالعالم')        == 'مرحبا بالعالم'
        assert Safe_Str__LLM__Message__User('Привет мир')           == 'Привет мир'

        # Mixed content
        assert Safe_Str__LLM__Message__User('Math: ∫x²dx = x³/3')   == 'Math: ∫x²dx = x³/3'

    def test_max_length_enforcement(self):                                       # Test 32KB limit
        # At max length
        long_message = 'A' * 32768
        assert Safe_Str__LLM__Message__User(long_message) == long_message

        # Exceeds max length
        too_long = 'A' * 32769
        error_message = "in Safe_Str__LLM__Message__User, value exceeds maximum length of 32768"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Message__User(too_long)

    def test_usage_in_type_safe(self):                                          # Test Type_Safe integration
        class Schema__Chat__Message(Type_Safe):
            user_message : Safe_Str__LLM__Message__User
            timestamp    : str

        with Schema__Chat__Message() as _:
            assert type(_.user_message) is Safe_Str__LLM__Message__User
            assert _.user_message == ''

            _.user_message = """Can you explain recursion?
Give me a simple Python example."""

            assert 'recursion' in _.user_message
            assert '\n' in _.user_message

    def test_json_serialization(self):                                          # Test JSON round-trip
        class Schema__User__Query(Type_Safe):
            question : Safe_Str__LLM__Message__User
            context  : Safe_Str__LLM__Message__User

        with Schema__User__Query() as original:
            original.question = 'What is machine learning?'
            original.context = 'I am a beginner in programming.'

            json_data = original.json()
            assert json_data == {
                'question': 'What is machine learning?',
                'context': 'I am a beginner in programming.'
            }

            with Schema__User__Query.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.question) is Safe_Str__LLM__Message__User

    def test_realistic_user_messages(self):                                     # Test real-world examples
        # Complex technical question
        tech_question = """I'm trying to implement a REST API in Python using FastAPI.
Here's my current code:

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

How can I add:
1. Request validation
2. Error handling
3. Authentication?"""

        result = Safe_Str__LLM__Message__User(tech_question)
        assert '```python' in result
        assert '@app.get' in result
        assert '1. Request validation' in result

        # Data analysis request
        data_request = """Analyze this data:
Sales Q1: $1,250,000
Sales Q2: $1,500,000  
Sales Q3: $1,100,000
Sales Q4: $2,000,000

What's the growth rate and trend?"""

        result = Safe_Str__LLM__Message__User(data_request)
        assert '$1,250,000' in result
        assert 'growth rate' in result