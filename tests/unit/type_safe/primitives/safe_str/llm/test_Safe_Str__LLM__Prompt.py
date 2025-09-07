import re
import pytest
from unittest                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                             import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                     import Safe_Str
from osbot_utils.utils.Objects                                              import __, base_classes
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Prompt    import Safe_Str__LLM__Prompt


class test_Safe_Str__LLM__Prompt(TestCase):

    def test__init__(self):                                                 # Test initialization
        with Safe_Str__LLM__Prompt() as _:
            assert type(_)         is Safe_Str__LLM__Prompt
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 32768
            assert _.regex.pattern == r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F]'

    def test_permissive_content(self):                                     # Test that most content is preserved
        # Regular text
        assert Safe_Str__LLM__Prompt('Hello, world!')       == 'Hello, world!'
        assert Safe_Str__LLM__Prompt('Test 123')            == 'Test 123'

        # Special characters and punctuation
        assert Safe_Str__LLM__Prompt('!@#$%^&*()')          == '!@#$%^&*()'
        assert Safe_Str__LLM__Prompt('[]{}|\\/<>?')         == '[]{}|\\/<>?'

        # Unicode and emojis
        assert Safe_Str__LLM__Prompt('Hello 🌍')            == 'Hello 🌍'
        assert Safe_Str__LLM__Prompt('Café ☕')              == 'Café ☕'
        assert Safe_Str__LLM__Prompt('数学 → Math')          == '数学 → Math'

        # Code snippets
        code = '''def hello():
    print("Hello, world!")
    return True'''
        assert Safe_Str__LLM__Prompt(code)                  == code

        # JSON
        json_str = '{"name": "test", "value": 123}'
        assert Safe_Str__LLM__Prompt(json_str)              == json_str

        # HTML/XML
        html = '<div class="test">Content</div>'
        assert Safe_Str__LLM__Prompt(html)                  == html

    def test_control_char_replacement(self):                                   # Test control character sanitization
        # Null byte
        assert Safe_Str__LLM__Prompt('Hello\x00World')      == 'Hello_World'

        # Various control chars
        assert Safe_Str__LLM__Prompt('Test\x01Text')        == 'Test_Text'
        assert Safe_Str__LLM__Prompt('Line\x07Bell')        == 'Line_Bell'
        assert Safe_Str__LLM__Prompt('Data\x08Backspace')   == 'Data_Backspace'

        # Tab and newline are preserved (not in the removal range)
        assert Safe_Str__LLM__Prompt('Line1\tTab')          == 'Line1\tTab'
        assert Safe_Str__LLM__Prompt('Line1\nLine2')        == 'Line1\nLine2'
        assert Safe_Str__LLM__Prompt('Line1\rLine2')        == 'Line1\rLine2'

    def test_multiline_prompts(self):                                      # Test multiline content
        prompt = """You are a helpful assistant.

Please help me with the following task:
- Item 1
- Item 2
- Item 3

Thank you!"""

        result = Safe_Str__LLM__Prompt(prompt)
        assert result == prompt                                            # All preserved
        assert '\n' in result
        assert '- Item' in result

    def test_max_length_enforcement(self):                                 # Test 32KB limit
        # At max length
        long_prompt = 'A' * 32768
        assert Safe_Str__LLM__Prompt(long_prompt) == long_prompt

        # Exceeds max length
        too_long = 'A' * 32769
        error_message = "in Safe_Str__LLM__Prompt, value exceeds maximum length of 32768"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Prompt(too_long)

    def test_auto_conversion(self):                                        # Test Type_Safe auto-conversion
        # Numbers
        assert Safe_Str__LLM__Prompt(123)                   == '123'
        assert Safe_Str__LLM__Prompt(3.14)                  == '3.14'

        # None and empty
        assert Safe_Str__LLM__Prompt(None)                  == ''
        assert Safe_Str__LLM__Prompt('')                    == ''

    def test_usage_in_type_safe(self):                                     # Test integration with Type_Safe
        class Schema__LLM__Request(Type_Safe):
            prompt      : Safe_Str__LLM__Prompt
            system      : Safe_Str__LLM__Prompt = Safe_Str__LLM__Prompt('You are helpful.')

        with Schema__LLM__Request() as _:
            assert type(_.prompt) is Safe_Str__LLM__Prompt
            assert type(_.system) is Safe_Str__LLM__Prompt
            assert _.prompt       == ''
            assert _.system       == 'You are helpful.'

            # Complex prompt assignment
            _.prompt = """Write a Python function that:
1. Takes a list of numbers
2. Returns the sum
3. Handles errors"""

            assert '1. Takes' in _.prompt
            assert '\n' in _.prompt

    def test_json_serialization(self):                                     # Test JSON round-trip
        class Schema__Conversation(Type_Safe):
            user_prompt : Safe_Str__LLM__Prompt
            ai_response : Safe_Str__LLM__Prompt

        with Schema__Conversation() as original:
            original.user_prompt = 'What is 2+2?'
            original.ai_response = 'The answer is 4.'

            json_data = original.json()
            assert json_data == {
                'user_prompt': 'What is 2+2?',
                'ai_response': 'The answer is 4.'
            }

            with Schema__Conversation.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.user_prompt) is Safe_Str__LLM__Prompt
                assert type(restored.ai_response) is Safe_Str__LLM__Prompt

    def test_realistic_prompts(self):                                      # Test real-world prompt examples
        # Code generation prompt
        code_prompt = """Generate a Python class for a binary search tree with:
- insert(value) method
- search(value) method  
- delete(value) method
Include proper error handling and docstrings."""

        assert code_prompt == Safe_Str__LLM__Prompt(code_prompt)


        # Analysis prompt with special chars
        analysis_prompt = """Analyze this data: {"revenue": 1000000, "profit": 250000}
Calculate the profit margin (profit/revenue * 100%).
Format: ##.##%"""

        assert analysis_prompt == Safe_Str__LLM__Prompt(analysis_prompt)

        # Prompt with markdown
        markdown_prompt = """# Task Description
**Important**: Please follow these steps:
1. Read the input
2. Process the data
3. Return results in `JSON` format

```python
def example():
    return {"status": "success"}
```"""

        assert markdown_prompt == Safe_Str__LLM__Prompt(markdown_prompt)