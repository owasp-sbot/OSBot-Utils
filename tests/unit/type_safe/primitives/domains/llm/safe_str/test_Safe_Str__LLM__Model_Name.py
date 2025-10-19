import re
import pytest
from unittest                                                                        import TestCase
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                      import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Model_Name import Safe_Str__LLM__Model_Name


class test_Safe_Str__LLM__Model_Name(TestCase):

    def test__init__(self):                                                     # Test class initialization
        with Safe_Str__LLM__Model_Name() as _:
            assert type(_)         is Safe_Str__LLM__Model_Name
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 256

    def test_valid_model_names(self):                                          # Test human-readable model names
        # OpenAI names
        assert Safe_Str__LLM__Model_Name('GPT-4 Turbo')              == 'GPT-4 Turbo'
        assert Safe_Str__LLM__Model_Name('GPT-3.5 Turbo')            == 'GPT-3.5 Turbo'
        assert Safe_Str__LLM__Model_Name('DALL-E 3')                 == 'DALL-E 3'

        # Anthropic names with versions
        assert Safe_Str__LLM__Model_Name('Claude 3 Opus')            == 'Claude 3 Opus'
        assert Safe_Str__LLM__Model_Name('Claude 3 Sonnet (Latest)') == 'Claude 3 Sonnet (Latest)'
        assert Safe_Str__LLM__Model_Name('Claude 2.1')               == 'Claude 2.1'

        # Meta/Llama names
        assert Safe_Str__LLM__Model_Name('Llama 3.1: Instruct (70B)') == 'Llama 3.1: Instruct (70B)'
        assert Safe_Str__LLM__Model_Name('Llama 2 Chat (13B)')       == 'Llama 2 Chat (13B)'
        assert Safe_Str__LLM__Model_Name('Code Llama (34B)')         == 'Code Llama (34B)'

        # Google names
        assert Safe_Str__LLM__Model_Name('Gemini Pro 1.5')           == 'Gemini Pro 1.5'
        assert Safe_Str__LLM__Model_Name('PaLM 2')                   == 'PaLM 2'
        assert Safe_Str__LLM__Model_Name('Bard')                     == 'Bard'

        # Cohere names
        assert Safe_Str__LLM__Model_Name('Command R+')               == 'Command R+'
        assert Safe_Str__LLM__Model_Name('Command')                  == 'Command'
        assert Safe_Str__LLM__Model_Name('Embed v3')                 == 'Embed v3'

        # Names with special formatting
        assert Safe_Str__LLM__Model_Name('Mistral: Large')           == 'Mistral: Large'
        assert Safe_Str__LLM__Model_Name('Yi-34B Chat')              == 'Yi-34B Chat'
        assert Safe_Str__LLM__Model_Name('Falcon-180B')              == 'Falcon-180B'

        # With ampersand and comma
        assert Safe_Str__LLM__Model_Name('Fast, Accurate LLM')       == 'Fast, Accurate LLM'

    def test_character_sanitization(self):                                     # Test invalid character replacement
        # Invalid special characters
        assert Safe_Str__LLM__Model_Name('Model#1')                  == 'Model_1'
        assert Safe_Str__LLM__Model_Name('Test@Model')               == 'Test_Model'
        assert Safe_Str__LLM__Model_Name('Model$99')                 == 'Model_99'
        assert Safe_Str__LLM__Model_Name('Model{Test}')              == 'Model_Test_'
        assert Safe_Str__LLM__Model_Name('Model[v1]')                == 'Model_v1_'
        assert Safe_Str__LLM__Model_Name('Model<Pro>')               == 'Model_Pro_'

        # Mixed valid and invalid
        assert Safe_Str__LLM__Model_Name('GPT-4!Turbo#')             == 'GPT-4_Turbo_'
        assert Safe_Str__LLM__Model_Name('Claude@3$Opus')            == 'Claude_3_Opus'

        # Emoji and unicode (assuming not in allowed set)
        assert Safe_Str__LLM__Model_Name('Model 🚀 Fast')            == 'Model _ Fast'
        assert Safe_Str__LLM__Model_Name('AI™ Model')                == 'AI_ Model'

    def test_whitespace_handling(self):                                        # Test spaces are preserved
        # Multiple spaces preserved (part of allowed chars)
        assert Safe_Str__LLM__Model_Name('GPT  4')                   == 'GPT  4'
        assert Safe_Str__LLM__Model_Name('Model   Name')             == 'Model   Name'

        # Leading/trailing spaces preserved (no trim by default)
        assert Safe_Str__LLM__Model_Name('  Model  ')                == '  Model  '

        # Tabs and newlines get replaced
        assert Safe_Str__LLM__Model_Name('GPT\t4')                   == 'GPT_4'
        assert Safe_Str__LLM__Model_Name('GPT\n4')                   == 'GPT_4'
        assert Safe_Str__LLM__Model_Name('Model\nName')              == 'Model_Name'

    def test_auto_conversion(self):                                           # Test Type_Safe auto-conversion
        # Numbers
        assert Safe_Str__LLM__Model_Name(404)                        == '404'
        assert Safe_Str__LLM__Model_Name(3.5)                        == '3.5'

        # None and empty
        assert Safe_Str__LLM__Model_Name(None)                       == ''
        assert Safe_Str__LLM__Model_Name('')                         == ''

    def test_max_length_enforcement(self):                                    # Test 512 character limit
        # At max length
        long_name = 'A' * 256
        assert Safe_Str__LLM__Model_Name(long_name)                  == long_name

        # Exceeds max length
        too_long = 'A' * 257
        error_message = "in Safe_Str__LLM__Model_Name, value exceeds maximum length of 256"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Model_Name(too_long)

    def test_edge_cases(self):                                               # Test edge cases
        # Only special characters that get replaced
        assert Safe_Str__LLM__Model_Name('!@#&$%^*') == '________'

        # Single valid characters
        assert Safe_Str__LLM__Model_Name('A')                        == 'A'
        assert Safe_Str__LLM__Model_Name('.')                        == '.'
        assert Safe_Str__LLM__Model_Name('-')                        == '-'
        assert Safe_Str__LLM__Model_Name(':')                        == ':'
        assert Safe_Str__LLM__Model_Name('(')                        == '('
        assert Safe_Str__LLM__Model_Name(')')                        == ')'
        assert Safe_Str__LLM__Model_Name('+')                        == '+'
        assert Safe_Str__LLM__Model_Name(',')                        == ','

    def test_usage_in_type_safe(self):                                       # Test integration with Type_Safe
        class Schema__Model__Info(Type_Safe):
            display_name : Safe_Str__LLM__Model_Name
            short_name   : Safe_Str__LLM__Model_Name = Safe_Str__LLM__Model_Name('Default Model')

        with Schema__Model__Info() as _:
            assert type(_.display_name) is Safe_Str__LLM__Model_Name
            assert type(_.short_name)   is Safe_Str__LLM__Model_Name
            assert _.display_name        == ''
            assert _.short_name          == 'Default Model'

            # Test assignment with sanitization
            _.display_name = 'GPT-4: Turbo (Latest)'
            assert _.display_name == 'GPT-4: Turbo (Latest)'

            _.display_name = 'Model#123@Test'                         # Gets sanitized
            assert _.display_name == 'Model_123_Test'

    def test_json_serialization(self):                                       # Test JSON round-trip
        class Schema__Models(Type_Safe):
            primary   : Safe_Str__LLM__Model_Name
            secondary : Safe_Str__LLM__Model_Name

        with Schema__Models() as original:
            original.primary   = 'Claude 3 Opus (Latest)'
            original.secondary = 'GPT-4 Turbo'

            json_data = original.json()
            assert json_data == {'primary'   : 'Claude 3 Opus (Latest)',
                                'secondary' : 'GPT-4 Turbo'}

            with Schema__Models.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.primary)   is Safe_Str__LLM__Model_Name
                assert type(restored.secondary) is Safe_Str__LLM__Model_Name

    def test_complex_model_names(self):                                      # Test realistic complex names
        # Version numbers and dates
        assert Safe_Str__LLM__Model_Name('GPT-4 (March 2024 Update)') == 'GPT-4 (March 2024 Update)'
        assert Safe_Str__LLM__Model_Name('Claude 3.5 Sonnet')         == 'Claude 3.5 Sonnet'

        # Multiple parentheses
        assert Safe_Str__LLM__Model_Name('Llama 3 (70B) (Instruct)')  == 'Llama 3 (70B) (Instruct)'

        # Long descriptive names
        long_name = 'Super Advanced Language Model with Enhanced Reasoning and Multi-Modal Capabilities (Version 2.0)'
        assert Safe_Str__LLM__Model_Name(long_name) == long_name

        # With colons and hyphens
        assert Safe_Str__LLM__Model_Name('Meta-Llama: Code Generation Model') == 'Meta-Llama: Code Generation Model'