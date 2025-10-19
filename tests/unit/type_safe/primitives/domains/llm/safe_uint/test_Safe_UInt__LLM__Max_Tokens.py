import pytest
from unittest                                                                          import TestCase
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                        import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Int                                    import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_UInt                                   import Safe_UInt
from osbot_utils.type_safe.primitives.domains.llm.safe_uint.Safe_UInt__LLM__Max_Tokens import Safe_UInt__LLM__Max_Tokens, DEFAULT__VALUE_UINT__LLM__MAX_TOKENS
from osbot_utils.utils.Objects                                                         import base_classes



class test_Safe_UInt__LLM__Max_Tokens(TestCase):

    def test__init__(self):                                                         # Test class initialization
        with Safe_UInt__LLM__Max_Tokens() as _:
            assert type(_)         is Safe_UInt__LLM__Max_Tokens
            assert base_classes(_) == [Safe_UInt, Safe_Int, Type_Safe__Primitive, int, object, object]
            assert _               == DEFAULT__VALUE_UINT__LLM__MAX_TOKENS           # Default to DEFAULT__VALUE_UINT__LLM__MAX_TOKENS
            assert _.min_value     == 1                                             # Minimum 1 token
            assert _.max_value     == 200000                                        # Maximum 200k tokens
            assert _.allow_none    is True                                          # None allowed for model defaults

    def test_valid_token_counts(self):                                             # Test common token limits
        # Small responses
        assert Safe_UInt__LLM__Max_Tokens(1)      == 1                            # Minimum valid
        assert Safe_UInt__LLM__Max_Tokens(10)     == 10                           # Very short
        assert Safe_UInt__LLM__Max_Tokens(100)    == 100                          # Short response
        assert Safe_UInt__LLM__Max_Tokens(256)    == 256                          # Common small limit

        # Standard responses
        assert Safe_UInt__LLM__Max_Tokens(500)    == 500                          # Medium response
        assert Safe_UInt__LLM__Max_Tokens(1000)   == 1000                         # Standard limit
        assert Safe_UInt__LLM__Max_Tokens(1024)   == 1024                         # Power of 2 limit
        assert Safe_UInt__LLM__Max_Tokens(2048)   == 2048                         # Common default

        # Large responses
        assert Safe_UInt__LLM__Max_Tokens(4000)   == 4000                         # GPT-3.5 common
        assert Safe_UInt__LLM__Max_Tokens(4096)   == 4096                         # GPT-4 common
        assert Safe_UInt__LLM__Max_Tokens(8192)   == 8192                         # Extended response
        assert Safe_UInt__LLM__Max_Tokens(16384)  == 16384                        # 16k context

        # Very large responses
        assert Safe_UInt__LLM__Max_Tokens(32768)  == 32768                        # 32k context
        assert Safe_UInt__LLM__Max_Tokens(65536)  == 65536                        # 64k context
        assert Safe_UInt__LLM__Max_Tokens(128000) == 128000                       # GPT-4 Turbo max
        assert Safe_UInt__LLM__Max_Tokens(200000) == 200000                       # Claude max

    def test_boundary_validation(self):                                            # Test min/max boundaries
        # Below minimum
        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got 0"):
            Safe_UInt__LLM__Max_Tokens(0)

        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got -1"):
            Safe_UInt__LLM__Max_Tokens(-1)

        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got -100"):
            Safe_UInt__LLM__Max_Tokens(-100)

        # Above maximum
        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be <= 200000, got 200001"):
            Safe_UInt__LLM__Max_Tokens(200001)

        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be <= 200000, got 250000"):
            Safe_UInt__LLM__Max_Tokens(250000)

        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be <= 200000, got 1000000"):
            Safe_UInt__LLM__Max_Tokens(1000000)

    def test_sub_handling(self):                                                  # Test None value support
        token_limit = Safe_UInt__LLM__Max_Tokens(None)                              # None is allowed (means use model default)
        assert token_limit == DEFAULT__VALUE_UINT__LLM__MAX_TOKENS
        assert type(token_limit) == Safe_UInt__LLM__Max_Tokens
        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got 0"):
            abc = token_limit - DEFAULT__VALUE_UINT__LLM__MAX_TOKENS
        assert type(token_limit+1  ) is Safe_UInt__LLM__Max_Tokens
        assert type(token_limit+1-1) is Safe_UInt__LLM__Max_Tokens

        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got 0"):
            token_limit -= DEFAULT__VALUE_UINT__LLM__MAX_TOKENS                     # at this stage we can still pickup this

        token_limit = 0                                                             # But since this completely replaces the object
        assert type(token_limit) is not Safe_UInt__LLM__Max_Tokens                  # we lose type safety
        assert type(token_limit) is int                                             # we are back to being an int
        assert token_limit == 0                                                     # and we end up in cases like this
        token_limit = -1                                                            # where invalid values can occur
        assert token_limit == -1
        token_limit += 1                                                            # like this
        assert token_limit == 0                                                     # and this

        return
        class Schema__Request(Type_Safe):
            max_tokens : Safe_UInt__LLM__Max_Tokens = None

        with Schema__Request() as _:
            assert _.max_tokens is None                                            # None as default

            _.max_tokens = 1000
            assert _.max_tokens == 1000

            _.max_tokens = None                                                    # Can set back to None
            assert _.max_tokens is None

    def test_string_conversion(self):                                              # Test string to int conversion
        # Valid string numbers
        assert Safe_UInt__LLM__Max_Tokens('100')   == 100
        assert Safe_UInt__LLM__Max_Tokens('1000')  == 1000
        assert Safe_UInt__LLM__Max_Tokens('4096')  == 4096
        assert Safe_UInt__LLM__Max_Tokens('32768') == 32768

        # Invalid strings
        with pytest.raises(ValueError):
            Safe_UInt__LLM__Max_Tokens('unlimited')

        with pytest.raises(ValueError):
            Safe_UInt__LLM__Max_Tokens('100.5')                                   # No floats

        with pytest.raises(ValueError):
            Safe_UInt__LLM__Max_Tokens('1e3')                                     # No scientific notation

    def test_float_conversion(self):                                               # Test float to int conversion
        # Floats can't be used
        with pytest.raises(TypeError, match="Safe_UInt__LLM__Max_Tokens requires an integer value, got float"):
            assert Safe_UInt__LLM__Max_Tokens(100.0)  == 100


        with pytest.raises(TypeError, match="Safe_UInt__LLM__Max_Tokens requires an integer value, got float"):
            assert Safe_UInt__LLM__Max_Tokens(100.7)  == 100

    def test_type_conversions(self):                                               # Test various type conversions
        with pytest.raises(TypeError, match="Safe_UInt__LLM__Max_Tokens does not allow boolean values"):
            assert Safe_UInt__LLM__Max_Tokens(True)  == 1                            # True -> 1
        with pytest.raises(TypeError):                                           # False -> 0, which is invalid
            Safe_UInt__LLM__Max_Tokens(False)

        # Invalid types
        with pytest.raises(TypeError):
            Safe_UInt__LLM__Max_Tokens([100])

        with pytest.raises(TypeError):
            Safe_UInt__LLM__Max_Tokens({'tokens': 100})

        with pytest.raises(TypeError):
            Safe_UInt__LLM__Max_Tokens(complex(100, 0))

    def test_comparison_operations(self):                                          # Test comparison with other values
        tokens1 = Safe_UInt__LLM__Max_Tokens(1000)
        tokens2 = Safe_UInt__LLM__Max_Tokens(1000)
        tokens3 = Safe_UInt__LLM__Max_Tokens(2000)

        # Equality
        assert tokens1 == tokens2
        assert tokens1 == 1000                                                    # Compare with int
        assert tokens1 != tokens3
        assert tokens1 != 2000

        # Ordering
        assert tokens1 < tokens3
        assert tokens3 > tokens1
        assert tokens1 <= 1000
        assert tokens3 >= 2000

        # Comparisons with None
        tokens_none = Safe_UInt__LLM__Max_Tokens(None)
        assert tokens_none == Safe_UInt__LLM__Max_Tokens(DEFAULT__VALUE_UINT__LLM__MAX_TOKENS)
        assert tokens_none == DEFAULT__VALUE_UINT__LLM__MAX_TOKENS
        assert tokens_none != tokens1

    def test_arithmetic_operations(self):                                          # Test arithmetic with token counts
        tokens = Safe_UInt__LLM__Max_Tokens(1000)

        # Addition returns Safe_UInt__LLM__Max_Tokens
        assert tokens + 500 == 1500
        assert type(tokens + 500) is Safe_UInt__LLM__Max_Tokens

        # Subtraction
        assert tokens - 500 == 500

        # Multiplication
        assert tokens * 2 == 2000

        # Division (integer division)
        assert tokens // 2 == 500
        assert tokens / 2 == 500.0                                                # Float division

    def test_usage_in_type_safe(self):                                            # Test integration with Type_Safe
        class Schema__LLM__Request(Type_Safe):
            model      : str
            max_tokens : Safe_UInt__LLM__Max_Tokens
            prompt     : str

        with Schema__LLM__Request() as _:
            assert type(_.max_tokens) is Safe_UInt__LLM__Max_Tokens
            assert _.max_tokens == DEFAULT__VALUE_UINT__LLM__MAX_TOKENS           # Default initialization

            # Assignment with auto-conversion
            _.model = 'gpt-4'
            _.max_tokens = 2048
            _.prompt = 'Hello, world!'

            assert _.max_tokens == 2048
            assert type(_.max_tokens) is Safe_UInt__LLM__Max_Tokens

            # String conversion
            _.max_tokens = '4096'
            assert _.max_tokens == 4096

            # Validation on assignment
            with pytest.raises(ValueError):
                _.max_tokens = 0                                                  # Below minimum

            with pytest.raises(ValueError):
                _.max_tokens = 300000                                             # Above maximum

    def test_json_serialization(self):                                            # Test JSON round-trip
        class Schema__Generation__Config(Type_Safe):
            max_tokens  : Safe_UInt__LLM__Max_Tokens
            temperature : float = 0.7

        with Schema__Generation__Config() as original:
            original.max_tokens = 4096
            original.temperature = 0.9

            # Serialize
            json_data = original.json()
            assert json_data == {'max_tokens': 4096, 'temperature': 0.9}
            assert type(json_data['max_tokens']) is int                          # Serializes as int

            # Deserialize
            with Schema__Generation__Config.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.max_tokens) is Safe_UInt__LLM__Max_Tokens
                assert restored.max_tokens == 4096

    def test_json_with_none(self):                                                # Test JSON serialization with None
        class Schema__Optional__Config(Type_Safe):
            max_tokens : Safe_UInt__LLM__Max_Tokens = None
            model      : str = 'gpt-4'

        with Schema__Optional__Config() as original:
            assert original.max_tokens is None

            # Serialize with None
            json_data = original.json()
            assert json_data == {'max_tokens': None, 'model': 'gpt-4'}

            # Deserialize preserves None
            with Schema__Optional__Config.from_json(json_data) as restored:
                assert restored.max_tokens is None
                assert restored.model == 'gpt-4'

    def test_string_representation(self):                                         # Test string formatting
        tokens = Safe_UInt__LLM__Max_Tokens(4096)

        # String representation
        assert str(tokens) == '4096'
        assert f"Max tokens: {tokens}" == "Max tokens: 4096"

        # Repr
        assert repr(tokens) == "Safe_UInt__LLM__Max_Tokens(4096)"

        # Different values
        tokens_small = Safe_UInt__LLM__Max_Tokens(100)
        assert str(tokens_small) == '100'

        tokens_large = Safe_UInt__LLM__Max_Tokens(128000)
        assert str(tokens_large) == '128000'

    def test_model_specific_limits(self):                                         # Test typical model-specific limits
        # GPT-3.5 Turbo
        gpt35_limit = Safe_UInt__LLM__Max_Tokens(4096)
        assert gpt35_limit == 4096

        # GPT-4 standard
        gpt4_limit = Safe_UInt__LLM__Max_Tokens(8192)
        assert gpt4_limit == 8192

        # GPT-4 Turbo
        gpt4_turbo_limit = Safe_UInt__LLM__Max_Tokens(128000)
        assert gpt4_turbo_limit == 128000

        # Claude 2
        claude2_limit = Safe_UInt__LLM__Max_Tokens(100000)
        assert claude2_limit == 100000

        # Claude 3 Opus
        claude3_limit = Safe_UInt__LLM__Max_Tokens(200000)
        assert claude3_limit == 200000

        # All are proper type
        assert type(gpt35_limit) is Safe_UInt__LLM__Max_Tokens
        assert type(claude3_limit) is Safe_UInt__LLM__Max_Tokens

    def test_token_budget_calculations(self):                                     # Test token budget scenarios
        # Typical prompt + response budget
        total_context = 4096
        prompt_tokens = 1000
        max_response = Safe_UInt__LLM__Max_Tokens(total_context - prompt_tokens)
        assert max_response == 3096

        # Multiple message context
        messages_tokens = [100, 200, 150, 300]  # Previous messages
        used_tokens = sum(messages_tokens)
        available = Safe_UInt__LLM__Max_Tokens(4096 - used_tokens)
        assert available == 3346

        # Safety margin
        context_window = 128000
        safety_margin = 1000
        prompt_estimate = 5000
        safe_max = Safe_UInt__LLM__Max_Tokens(context_window - safety_margin - prompt_estimate)
        assert safe_max == 122000

    def test_integration_with_api_request(self):                                 # Test realistic API request scenario
        class Schema__OpenAI__Request(Type_Safe):
            model       : str
            messages    : list
            max_tokens  : Safe_UInt__LLM__Max_Tokens = None                      # Optional
            temperature : float = 0.7

        with Schema__OpenAI__Request() as request:
            request.model = 'gpt-4-turbo'
            request.messages = [
                {'role': 'system', 'content': 'You are helpful.'},
                {'role': 'user', 'content': 'Write a story.'}
            ]
            request.max_tokens = 2000

            # Verify max_tokens is properly typed
            assert type(request.max_tokens) is Safe_UInt__LLM__Max_Tokens
            assert request.max_tokens == 2000

            # Simulate API payload
            api_payload = request.json()
            assert api_payload['max_tokens'] == 2000
            assert type(api_payload['max_tokens']) is int

        # Test with None (use model default)
        with Schema__OpenAI__Request() as request2:
            request2.model = 'gpt-4'
            request2.messages = [{'role': 'user', 'content': 'Hi'}]
            # max_tokens left as None

            api_payload2 = request2.json()
            assert api_payload2['max_tokens'] is None                            # None preserved

    def test_token_limit_presets(self):                                          # Test common token limit presets
        # Define presets as Safe_UInt__LLM__Max_Tokens
        TOKENS_TWEET        = Safe_UInt__LLM__Max_Tokens(50)                     # Tweet-length
        TOKENS_PARAGRAPH    = Safe_UInt__LLM__Max_Tokens(200)                    # Single paragraph
        TOKENS_SHORT        = Safe_UInt__LLM__Max_Tokens(500)                    # Short response
        TOKENS_STANDARD     = Safe_UInt__LLM__Max_Tokens(1000)                   # Standard response
        TOKENS_DETAILED     = Safe_UInt__LLM__Max_Tokens(2000)                   # Detailed response
        TOKENS_ESSAY        = Safe_UInt__LLM__Max_Tokens(4000)                   # Essay-length
        TOKENS_COMPREHENSIVE = Safe_UInt__LLM__Max_Tokens(8000)                  # Comprehensive

        assert TOKENS_TWEET == 50
        assert TOKENS_PARAGRAPH == 200
        assert TOKENS_STANDARD == 1000
        assert TOKENS_ESSAY == 4000

        # All are proper type
        assert type(TOKENS_TWEET) is Safe_UInt__LLM__Max_Tokens
        assert type(TOKENS_COMPREHENSIVE) is Safe_UInt__LLM__Max_Tokens

    def test_edge_cases(self):                                                   # Test edge cases
        # Minimum valid value
        min_tokens = Safe_UInt__LLM__Max_Tokens(1)
        assert min_tokens == 1

        # Maximum valid value
        max_tokens = Safe_UInt__LLM__Max_Tokens(200000)
        assert max_tokens == 200000

        # Common power of 2 values
        powers_of_2 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
        for value in powers_of_2:
            if value <= 200000:                                                  # Within max limit
                tokens = Safe_UInt__LLM__Max_Tokens(value)
                assert tokens == value