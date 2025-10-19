import re
import pytest
from unittest                                                                       import TestCase
from osbot_utils.utils.Objects                                                      import base_classes
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                 import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Id  import Safe_Str__LLM__Model_Id
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode         import Enum__Safe_Str__Regex_Mode

class test_Safe_Str__LLM__Model_Id(TestCase):

    def test__init__(self):                                                    # Test class initialization and defaults
        with Safe_Str__LLM__Model_Id() as _:
            assert type(_) is Safe_Str__LLM__Model_Id
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''                                       # Empty by default
            assert _.max_length    == 256
            assert _.regex_mode    == Enum__Safe_Str__Regex_Mode.REPLACE

    def test_valid_model_ids(self):                                           # Test various provider model ID formats
        # OpenRouter style
        assert Safe_Str__LLM__Model_Id('openai/gpt-4') == 'openai/gpt-4'
        assert Safe_Str__LLM__Model_Id('anthropic/claude-3-opus') == 'anthropic/claude-3-opus'
        assert Safe_Str__LLM__Model_Id('meta-llama/llama-3.1-70b') == 'meta-llama/llama-3.1-70b'

        # OpenAI style
        assert Safe_Str__LLM__Model_Id('gpt-4') == 'gpt-4'
        assert Safe_Str__LLM__Model_Id('gpt-3.5-turbo') == 'gpt-3.5-turbo'
        assert Safe_Str__LLM__Model_Id('text-davinci-003') == 'text-davinci-003'

        # Anthropic style with dates
        assert Safe_Str__LLM__Model_Id('claude-3-opus-20240229') == 'claude-3-opus-20240229'
        assert Safe_Str__LLM__Model_Id('claude-3-sonnet@20240229') == 'claude-3-sonnet@20240229'

        # Google style
        assert Safe_Str__LLM__Model_Id('models/gemini-pro') == 'models/gemini-pro'
        assert Safe_Str__LLM__Model_Id('gemini-1.5-pro') == 'gemini-1.5-pro'

        # Cohere style
        assert Safe_Str__LLM__Model_Id('command-r-plus') == 'command-r-plus'
        assert Safe_Str__LLM__Model_Id('command') == 'command'

        # With version numbers
        assert Safe_Str__LLM__Model_Id('llama-2-70b:v1.2.3') == 'llama-2-70b:v1.2.3'
        assert Safe_Str__LLM__Model_Id('model_v2.0') == 'model_v2.0'

    def test_character_sanitization(self):                                    # Test invalid character replacement
        # Spaces replaced with underscore
        assert Safe_Str__LLM__Model_Id('gpt 4 turbo') == 'gpt_4_turbo'
        assert Safe_Str__LLM__Model_Id('claude 3 opus') == 'claude_3_opus'

        # Special characters sanitized
        assert Safe_Str__LLM__Model_Id('gpt-4!turbo') == 'gpt-4_turbo'
        assert Safe_Str__LLM__Model_Id('model#123') == 'model_123'
        assert Safe_Str__LLM__Model_Id('test$model') == 'test_model'
        assert Safe_Str__LLM__Model_Id('model(v1)') == 'model_v1_'
        assert Safe_Str__LLM__Model_Id('model[test]') == 'model_test_'

        # Multiple special chars
        assert Safe_Str__LLM__Model_Id('test!#$%model') == 'test____model'
        assert Safe_Str__LLM__Model_Id('<<<model>>>') == '___model___'

    def test_auto_conversion(self):                                          # Test Type_Safe auto-conversion behavior
        # Integer conversion
        assert Safe_Str__LLM__Model_Id(123) == '123'
        assert Safe_Str__LLM__Model_Id(404) == '404'

        # Float conversion
        assert Safe_Str__LLM__Model_Id(3.14) == '3.14'
        assert Safe_Str__LLM__Model_Id(2.0) == '2.0'

        # None and empty
        assert Safe_Str__LLM__Model_Id(None) == ''
        assert Safe_Str__LLM__Model_Id('') == ''

    def test_max_length_enforcement(self):                                   # Test length validation
        # At max length
        model_id_max = 'a' * 256
        assert Safe_Str__LLM__Model_Id(model_id_max) == model_id_max

        # Exceeds max length
        model_id_too_long = 'a' * 257
        error_message = f"in Safe_Str__LLM__Model_Id, value exceeds maximum length of 256"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Model_Id(model_id_too_long)

    def test_edge_cases(self):                                              # Test edge cases and special scenarios
        # Only special characters
        assert Safe_Str__LLM__Model_Id('!#$%^&*()') == '_________'

        # Whitespace only (becomes empty after sanitization)
        assert Safe_Str__LLM__Model_Id('   ') == '___'

        # Single character
        assert Safe_Str__LLM__Model_Id('a') == 'a'
        assert Safe_Str__LLM__Model_Id('/') == '/'
        assert Safe_Str__LLM__Model_Id('-') == '-'
        assert Safe_Str__LLM__Model_Id('.') == '.'
        assert Safe_Str__LLM__Model_Id(':') == ':'
        assert Safe_Str__LLM__Model_Id('_') == '_'
        assert Safe_Str__LLM__Model_Id('@') == '@'

    def test_usage_in_type_safe(self):                                      # Test integration with Type_Safe classes
        class Schema__LLM__Request(Type_Safe):
            model_id     : Safe_Str__LLM__Model_Id
            backup_model : Safe_Str__LLM__Model_Id = Safe_Str__LLM__Model_Id('gpt-3.5-turbo')

        with Schema__LLM__Request() as _:
            assert type(_.model_id) is Safe_Str__LLM__Model_Id
            assert type(_.backup_model) is Safe_Str__LLM__Model_Id
            assert _.model_id           == ''
            assert _.backup_model       == 'gpt-3.5-turbo'

            # Test assignment with auto-conversion
            _.model_id = 'claude-3-opus'                            # Raw string auto-converts
            assert type(_.model_id) is Safe_Str__LLM__Model_Id
            assert _.model_id == 'claude-3-opus'

            # Test with sanitization
            _.model_id = 'gpt 4 turbo!'                            # Sanitizes on assignment
            assert _.model_id == 'gpt_4_turbo_'

    def test_json_serialization(self):                                      # Test JSON round-trip
        class Schema__Model(Type_Safe):
            primary_model   : Safe_Str__LLM__Model_Id
            fallback_model  : Safe_Str__LLM__Model_Id

        with Schema__Model() as original:
            original.primary_model  = 'openai/gpt-4'
            original.fallback_model = 'anthropic/claude-3-sonnet'

            # Serialize
            json_data = original.json()
            assert json_data == {'primary_model'  : 'openai/gpt-4',
                                 'fallback_model' : 'anthropic/claude-3-sonnet'}

            # Deserialize
            with Schema__Model.from_json(json_data) as restored:
                assert restored.obj()                == original.obj()
                assert type(restored.primary_model) is Safe_Str__LLM__Model_Id
                assert type(restored.fallback_model) is Safe_Str__LLM__Model_Id

    def test_string_operations(self):                                       # Test string operations preserve type
        model_id = Safe_Str__LLM__Model_Id('gpt-4')

        # Concatenation returns Safe_Str__LLM__Model_Id
        result = model_id + '-turbo'
        assert type(result) is Safe_Str__LLM__Model_Id
        assert result == 'gpt-4-turbo'

        # String methods return regular str
        assert type(model_id.upper()) is str
        assert model_id.upper() == 'GPT-4'

        assert type(model_id.replace('-', '_')) is str
        assert model_id.replace('-', '_') == 'gpt_4'

        # F-string formatting
        assert f"Model: {model_id}" == "Model: gpt-4"

        # Repr
        assert repr(model_id) == "Safe_Str__LLM__Model_Id('gpt-4')"