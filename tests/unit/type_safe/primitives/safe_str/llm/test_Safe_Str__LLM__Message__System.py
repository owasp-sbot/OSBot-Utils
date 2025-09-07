import re
import pytest
from unittest                                                                      import TestCase
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                   import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                           import Safe_Str
from osbot_utils.utils.Objects                                                    import __, base_classes
from osbot_utils.type_safe.primitives.safe_str.llm.Safe_Str__LLM__Message__System import Safe_Str__LLM__Message__System


class test_Safe_Str__LLM__Message__System(TestCase):

    def test__init__(self):                                                           # Test initialization
        with Safe_Str__LLM__Message__System() as _:
            assert type(_)         is Safe_Str__LLM__Message__System
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 4096                                           # Shorter than full prompts
            assert _.regex.pattern == r'[\x00-\x08\x0B\x0C\x0E-\x1F]'             # All control chars minus tab, newline and carriage return

    def test_typical_system_prompts(self):                                           # Test common system prompts
        # Simple instructions
        assert Safe_Str__LLM__Message__System('You are a helpful assistant.') == 'You are a helpful assistant.'
        assert Safe_Str__LLM__Message__System('Be concise and accurate.')     == 'Be concise and accurate.'

        # Role definitions
        system1 = 'You are an expert Python programmer. Help users write clean, efficient code.'
        assert Safe_Str__LLM__Message__System(system1) == system1

        # Behavioral constraints
        system2 = 'Always respond in JSON format. Never use profanity. Be respectful.'
        assert Safe_Str__LLM__Message__System(system2) == system2

        # Complex instructions with formatting
        system3 = """You are a code reviewer. Follow these rules:
1. Check for bugs
2. Suggest improvements
3. Rate code quality (1-10)"""

        assert Safe_Str__LLM__Message__System(system3) == system3 # BUG (here and in line below)

    def test_control_char_removal(self):                                             # Test control character sanitization
        # All control chars (0x00-0x1F) are removed
        assert Safe_Str__LLM__Message__System('Test\x00Null')       == 'Test_Null'
        assert Safe_Str__LLM__Message__System('Test\x01SOH')        == 'Test_SOH'
        assert Safe_Str__LLM__Message__System('Test\x07Bell')       == 'Test_Bell'

        # Tab and newline ARE kept
        assert Safe_Str__LLM__Message__System('Line1\tTab')         == 'Line1\tTab'
        assert Safe_Str__LLM__Message__System('Line1\nLine2')       == 'Line1\nLine2'
        assert Safe_Str__LLM__Message__System('Line1\rLine2')       == 'Line1\rLine2'

        # Form feed, vertical tab also removed
        assert Safe_Str__LLM__Message__System('Text\x0BVTab')       == 'Text_VTab'
        assert Safe_Str__LLM__Message__System('Text\x0CFF')         == 'Text_FF'

    def test_special_characters_preserved(self):                                     # Test non-control chars preserved
        # Punctuation and symbols
        assert Safe_Str__LLM__Message__System('Use @mentions and #tags')      == 'Use @mentions and #tags'
        assert Safe_Str__LLM__Message__System('Cost: $10/month')              == 'Cost: $10/month'
        assert Safe_Str__LLM__Message__System('Rate: 95.5%')                  == 'Rate: 95.5%'

        # Unicode
        assert Safe_Str__LLM__Message__System('Support émojis: ✓')            == 'Support émojis: ✓'
        assert Safe_Str__LLM__Message__System('Multiple languages: 中文, العربية') == 'Multiple languages: 中文, العربية'

    def test_max_length_enforcement(self):                                           # Test 4096 character limit
        # At max length
        long_system = 'A' * 4096
        assert Safe_Str__LLM__Message__System(long_system) == long_system

        # Exceeds max length
        too_long = 'A' * 4097
        error_message = "in Safe_Str__LLM__Message__System, value exceeds maximum length of 4096"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Message__System(too_long)

    def test_usage_in_type_safe(self):                                              # Test integration with Type_Safe
        class Schema__LLM__Config(Type_Safe):
            system_prompt : Safe_Str__LLM__Message__System
            temperature   : float = 0.7

        with Schema__LLM__Config() as _:
            assert type(_.system_prompt) is Safe_Str__LLM__Message__System
            assert _.system_prompt == ''

            _.system_prompt = 'You are a technical writer. Be precise and clear.'
            assert 'technical writer' in _.system_prompt

    def test_json_serialization(self):                                              # Test JSON round-trip
        class Schema__System__Config(Type_Safe):
            primary_prompt   : Safe_Str__LLM__Message__System
            fallback_prompt  : Safe_Str__LLM__Message__System

        with Schema__System__Config() as original:
            original.primary_prompt  = 'You are an AI assistant.'
            original.fallback_prompt = 'Answer questions helpfully.'

            json_data = original.json()
            assert json_data == {
                'primary_prompt': 'You are an AI assistant.',
                'fallback_prompt': 'Answer questions helpfully.'
            }

            with Schema__System__Config.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.primary_prompt) is Safe_Str__LLM__Message__System

    def test_realistic_system_prompts(self):                                        # Test real-world examples
        # Code assistant
        code_system = """You are a senior software engineer assistant.
Guidelines:
- Write clean, maintainable code
- Follow PEP-8 for Python
- Include error handling
- Add comments for complex logic"""

        result = Safe_Str__LLM__Message__System(code_system)
        assert 'senior software engineer' in result
        assert '\n' in result                                       # Newlines kept

        # JSON response system
        json_system = 'Always respond with valid JSON. Format: {"response": "text", "confidence": 0.0-1.0}'
        assert Safe_Str__LLM__Message__System(json_system) == json_system