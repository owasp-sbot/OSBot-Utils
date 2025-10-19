import re
import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Description   import Safe_Str__LLM__Description


class test_Safe_Str__LLM__Description(TestCase):

    def test__init__(self):                                                        # Test class initialization
        with Safe_Str__LLM__Description() as _:
            assert type(_)         is Safe_Str__LLM__Description
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 4096

    def test_valid_descriptions(self):                                            # Test rich description content
        # Simple descriptions
        assert Safe_Str__LLM__Description('A powerful language model') == 'A powerful language model'
        assert Safe_Str__LLM__Description('Advanced AI system')        == 'Advanced AI system'

        # With punctuation
        desc1 = 'GPT-4 is OpenAI\'s most advanced system, producing safer and more useful responses.'
        assert Safe_Str__LLM__Description(desc1) == desc1

        # With quotes and emphasis
        desc2 = 'The "best" model for general-purpose tasks with \'excellent\' performance.'
        assert Safe_Str__LLM__Description(desc2) == desc2

        # Mathematical notation
        desc3 = 'Supports context windows up to 128k tokens (4× larger than previous version).'
        assert Safe_Str__LLM__Description(desc3) == desc3

        # With brackets and annotations
        desc4 = 'Claude 3 [Latest] supports multiple languages including English, Spanish, and French.'
        assert Safe_Str__LLM__Description(desc4) == desc4

        # Code-like descriptions
        desc5 = 'Optimized for code generation in Python, JavaScript, C++, and more.'
        assert Safe_Str__LLM__Description(desc5) == desc5

        # With special characters
        desc6 = 'Price: $0.01/1k tokens | Speed: ~50 tokens/sec | Quality: ★★★★★'
        assert Safe_Str__LLM__Description(desc6) == desc6.replace('★', '_')  # Black Stars not in allowed set , only *

        desc7 = 'Price: $0.01/1k tokens | Speed: ~50 tokens/sec | Quality: *****'       # these ones work
        assert Safe_Str__LLM__Description(desc6) != desc6
        # URLs and paths
        desc8 = 'Documentation available at https://docs.example.com/models'
        assert Safe_Str__LLM__Description(desc8) == desc8

    def test_multiline_descriptions(self):                                        # Test multiline support
        multiline = """This is a powerful language model.
Features include:
- Natural language understanding
- Code generation
- Multi-lingual support"""

        expected = """This is a powerful language model.
Features include:
- Natural language understanding
- Code generation
- Multi-lingual support"""

        assert Safe_Str__LLM__Description(multiline) == expected

    def test_technical_descriptions(self):                                        # Test technical content
        # With percentages and numbers
        tech1 = 'Achieves 95.2% accuracy on benchmark tests, 2× faster than v1.0'
        assert Safe_Str__LLM__Description(tech1) == tech1

        # Mathematical symbols
        tech2 = 'Performance = O(n log n), Memory ≤ 16GB, Latency < 100ms'
        assert Safe_Str__LLM__Description(tech2) == tech2.replace('≤', '_').replace('≈', '_')  # Some symbols not allowed

        # Version numbers and dates
        tech3 = 'Released on 2024-03-15, version 2.1.0-beta'
        assert Safe_Str__LLM__Description(tech3) == tech3

        # Complex formatting
        tech4 = 'Model size: 175B parameters; Training data: 1.5TB; Cost: $5M+'
        assert Safe_Str__LLM__Description(tech4) == tech4

    def test_character_sanitization(self):                                       # Test invalid character replacement
        # Emoji replacement
        assert Safe_Str__LLM__Description('Best model 🚀 ever!')    == 'Best model _ ever!'
        assert Safe_Str__LLM__Description('AI 🤖 assistant')        == 'AI _ assistant'

        # Control characters
        assert Safe_Str__LLM__Description('Line1\tLine2')           == 'Line1\tLine2'
        assert Safe_Str__LLM__Description('Text\rMore')             == 'Text\rMore'

        # Unicode symbols not in allowed set
        assert Safe_Str__LLM__Description('Model™ Professional©')    == 'Model_ Professional_'
        assert Safe_Str__LLM__Description('Rating: ★★★★☆')          == 'Rating: _____'

    def test_auto_conversion(self):                                             # Test Type_Safe auto-conversion
        # Numbers
        assert Safe_Str__LLM__Description(12345)                    == '12345'
        assert Safe_Str__LLM__Description(99.99)                    == '99.99'

        # None and empty
        assert Safe_Str__LLM__Description(None)                     == ''
        assert Safe_Str__LLM__Description('')                       == ''

    def test_max_length_enforcement(self):                                      # Test 4096 character limit
        # Near max length
        long_desc = 'A' * 4096
        assert Safe_Str__LLM__Description(long_desc)                == long_desc

        # Exceeds max length
        too_long = 'A' * 4097
        error_message = "in Safe_Str__LLM__Description, value exceeds maximum length of 4096"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Description(too_long)

    def test_edge_cases(self):                                                  # Test edge cases
        # Only invalid characters
        assert Safe_Str__LLM__Description('™©®℠')  == '____' # Only special unicode

        # Lots of special punctuation (all allowed)
        punct = '!@#$%^&*()_+-=[]{}|;:,.<>?/'
        assert Safe_Str__LLM__Description(punct) == punct.replace('^', '_')  # Most are allowed

        # Single characters
        assert Safe_Str__LLM__Description('.')                      == '.'
        assert Safe_Str__LLM__Description('!')                      == '!'
        assert Safe_Str__LLM__Description('$')                      == '$'
        assert Safe_Str__LLM__Description('\n')                     == '\n'

    def test_usage_in_type_safe(self):                                         # Test integration with Type_Safe
        class Schema__Model__Documentation(Type_Safe):
            short_description : Safe_Str__LLM__Description
            full_description  : Safe_Str__LLM__Description
            changelog         : Safe_Str__LLM__Description = Safe_Str__LLM__Description('Initial release')

        with Schema__Model__Documentation() as _:
            assert type(_.short_description) is Safe_Str__LLM__Description
            assert type(_.full_description)  is Safe_Str__LLM__Description
            assert type(_.changelog)         is Safe_Str__LLM__Description
            assert _.short_description       == ''
            assert _.full_description        == ''
            assert _.changelog               == 'Initial release'

            # Assignment with multiline
            _.full_description = """Advanced language model with:
- 175B parameters
- Multi-modal capabilities
- Support for 100+ languages"""

            assert '\n'   in _.full_description                         # Newlines preserved
            assert '175B' in _.full_description

    def test_json_serialization(self):                                         # Test JSON round-trip
        class Schema__Documentation(Type_Safe):
            description : Safe_Str__LLM__Description
            notes       : Safe_Str__LLM__Description

        with Schema__Documentation() as original:
            original.description = 'Model: GPT-4 | Context: 128k tokens | Price: $0.01/1k'
            original.notes = 'Best for complex tasks requiring advanced reasoning.'

            json_data = original.json()
            assert json_data == {
                'description': 'Model: GPT-4 | Context: 128k tokens | Price: $0.01/1k',
                'notes': 'Best for complex tasks requiring advanced reasoning.'
            }

            with Schema__Documentation.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.description) is Safe_Str__LLM__Description
                assert type(restored.notes)       is Safe_Str__LLM__Description

    def test_realistic_model_descriptions(self):                               # Test real-world descriptions
        # OpenAI style
        openai_desc = """GPT-4 Turbo with Vision
The latest GPT-4 Turbo model with vision capabilities. Vision requests can now use JSON mode and function calling.
Context window: 128,000 tokens
Training data: Up to Dec 2023"""

        result = Safe_Str__LLM__Description(openai_desc)
        assert 'GPT-4 Turbo' in result
        assert '128,000' in result
        assert 'Dec 2023' in result

        # Anthropic style
        anthropic_desc = """Claude 3 Opus - Our most intelligent model
Superior performance on highly complex tasks, such as math and coding.
• 200K context window
    • Multilingual capabilities
    - Advanced reasoning
Price: $15.00 / million input tokens"""

        result = Safe_Str__LLM__Description(anthropic_desc)
        assert result == anthropic_desc.replace('•', '_')
        assert 'Claude 3 Opus' in result
        assert '200K' in result
        assert '$15.00' in result
        assert '•' not in result  # Bullet point not preserved