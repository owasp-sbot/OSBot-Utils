import re
import pytest
from unittest                                                                      import TestCase
from osbot_utils.testing.__                                                        import __
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                    import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_float.Safe_Float                        import Safe_Float
from osbot_utils.type_safe.primitives.safe_float.llm.Safe_Float__LLM__Temperature  import Safe_Float__LLM__Temperature
from osbot_utils.utils.Objects                                                     import base_classes


class test_Safe_Float__LLM__Temperature(TestCase):

    def test__init__(self):                                                             # Test class initialization
        with Safe_Float__LLM__Temperature() as _:
            assert type(_)         is Safe_Float__LLM__Temperature
            assert base_classes(_) == [Safe_Float, Type_Safe__Primitive, float, object, object]
            assert _.obj()         == __(min_value      = 0.0   ,
                                         max_value      = 2.0   ,
                                         allow_bool     = False ,
                                         allow_int      = True  ,
                                         allow_inf      = False ,
                                         allow_none     = True  ,
                                         allow_str      = True  ,
                                         strict_type    = False ,
                                         decimal_places = 2     ,
                                         use_decimal    = True  ,
                                         epsilon        = 1e-09 ,
                                         round_output   = True  ,
                                         clamp_to_range = True  )
            assert _               == 0.0                                              # Default to 0.0
            assert _.min_value     == 0.0                                              # Minimum temperature
            assert _.max_value     == 2.0                                              # Maximum temperature  
            assert _.decimal_places == 2                                               # Two decimal precision
            assert _.use_decimal   is True                                             # Use Decimal for exactness
            assert _.clamp_to_range is True                                            # Auto-clamp to valid range

    def test_valid_temperatures(self):                                                 # Test valid temperature values
        # Common temperatures
        assert Safe_Float__LLM__Temperature(0.0)  == 0.0                                # Deterministic
        assert Safe_Float__LLM__Temperature(0.5)  == 0.5                                # Balanced
        assert Safe_Float__LLM__Temperature(0.7)  == 0.7                                # Default for many models
        assert Safe_Float__LLM__Temperature(1.0)  == 1.0                                # Creative
        assert Safe_Float__LLM__Temperature(1.5)  == 1.5                                # Very creative
        assert Safe_Float__LLM__Temperature(2.0)  == 2.0                                # Maximum creativity

        # Precision handling
        assert Safe_Float__LLM__Temperature(0.73) == 0.73                               # Two decimal places
        assert Safe_Float__LLM__Temperature(0.99) == 0.99
        assert Safe_Float__LLM__Temperature(1.23) == 1.23

        # String conversion
        assert Safe_Float__LLM__Temperature('0.7')  == 0.7                              # String to float
        assert Safe_Float__LLM__Temperature('1.0')  == 1.0
        assert Safe_Float__LLM__Temperature('0.25') == 0.25

    def test_clamping_behavior(self):                                                  # Test auto-clamping to valid range
        # Values below minimum get clamped to 0.0
        assert Safe_Float__LLM__Temperature(-0.5) == 0.0                                # Negative clamped to 0
        assert Safe_Float__LLM__Temperature(-1.0) == 0.0
        assert Safe_Float__LLM__Temperature(-100) == 0.0

        # Values above maximum get clamped to 2.0  
        assert Safe_Float__LLM__Temperature(2.1)  == 2.0                                # Over 2.0 clamped to 2.0
        assert Safe_Float__LLM__Temperature(3.0)  == 2.0
        assert Safe_Float__LLM__Temperature(10.0) == 2.0
        assert Safe_Float__LLM__Temperature(999)  == 2.0

    def test_decimal_precision(self):                                                  # Test Decimal arithmetic precision


        temp1 = Safe_Float__LLM__Temperature(0.1)                                   # check No floating point errors
        temp2 = Safe_Float__LLM__Temperature(0.2)                                   # since In regular float: 0.1 + 0.2 = 0.30000000000000004

        assert temp1 + temp2              == 0.3                                    # With Decimal: exact arithmetic (i.e. 0.3)
        assert temp1 + 0.2                == 0.3                                    # sum doesn't lose the type safe
        assert 0.1 + temp2                == 0.3                                    # sum doesn't lose the type safe
        assert type(0.1 + temp2 )         is Safe_Float__LLM__Temperature
        assert type(0.1 - temp2 )         is Safe_Float__LLM__Temperature
        assert temp1 - 0.05               == 0.05                                   # subtraction also doesn't lose the type safe
        assert temp2 - 0.05               == 0.15
        assert temp2 - 0.05               == 0.15000000000000001                    # so these work, because of the epsilon = 1e-09
        assert temp2 - 0.05               == 0.1500000000000001                     # so all these
        assert temp2 - 0.05               == 0.15000000000001
        assert temp2 - 0.05               == 0.1500000000001
        assert temp2 - 0.05               == 0.150000000001
        assert temp2 - 0.05               == 0.15000000001
        assert temp2 - 0.05               == 0.150000001
        assert temp2 - 0.05               != 0.15000001                             # up to here
        assert type(temp2 - 0.05)         is Safe_Float__LLM__Temperature           # good news is that we still have a Safe_Float__LLM__Temperature
        assert (str(temp2 - 0.05))        == "0.15"                                 # which is behaving ok in string operations
        assert (str(temp1 - 0.05))        == "0.05"
        assert float(temp1 + temp2)       == 0.3                                    # With Decimal: exact arithmetic (i.e. 0.3)
        assert type(temp1 + temp2)        == Safe_Float__LLM__Temperature
        assert type(float(temp1 + temp2)) == float

        assert 0.1 + 0.2 != 0.30000000000000001                                     # WTF: so this one doesn't work
        assert 0.1 + 0.2 != 0.3                                                     # WTF: so this one doesn't work
        assert 0.1 + 0.2 == 0.30000000000000002                                     # WTF: and this one does?
        assert 0.1 + 0.2 == 0.30000000000000003                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000004                                     # WTF: this is a reall
        assert 0.1 + 0.2 == 0.30000000000000005                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000006                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000007                                     # WTF: and this
        assert 0.1 + 0.2 != 0.30000000000000009                                     # WTF: and somehow the .9 doesn't
        assert str(0.2 - 0.05) == "0.15000000000000002"                             # WTF: this is bound to cause some bugs
        assert str(0.1 + 0.2 ) == "0.30000000000000004"                             # WTF: and this
        assert f'{0.1 + 0.2}'  == '0.30000000000000004'                             # WTF: this
        assert f'{0.2 - 0.05}' == '0.15000000000000002'                             # WTF: and this

    def test_rounding_behavior(self):                                                  # Test decimal places rounding
        # More than 2 decimal places get rounded
        assert Safe_Float__LLM__Temperature(0.777)    == 0.78                          # Rounds to 2 decimals
        assert Safe_Float__LLM__Temperature(0.774)    == 0.77                          # Standard rounding
        assert Safe_Float__LLM__Temperature(1.2345)   == 1.23                          # Truncates extra decimals
        assert Safe_Float__LLM__Temperature(1.999)    == 2.00                          # Rounds up to max

    def test_type_conversions(self):                                                   # Test various type conversions
        # Integer conversion
        assert Safe_Float__LLM__Temperature(0)   == 0.0
        assert Safe_Float__LLM__Temperature(1)   == 1.0
        assert Safe_Float__LLM__Temperature(2)   == 2.0

        # None defaults to 0.0
        assert Safe_Float__LLM__Temperature(None) == 0.0

        # Boolean (though unusual)
        with pytest.raises(TypeError, match=re.escape("Safe_Float__LLM__Temperature does not allow boolean values")):
            Safe_Float__LLM__Temperature(True)
        with pytest.raises(TypeError, match=re.escape("Safe_Float__LLM__Temperature does not allow boolean values")):
            Safe_Float__LLM__Temperature(False)

    def test_invalid_conversions(self):                                                # Test what can't be converted
        # Non-numeric strings
        with pytest.raises(ValueError):
            Safe_Float__LLM__Temperature('high')
            
        with pytest.raises(ValueError):
            Safe_Float__LLM__Temperature('0.7a')
            
        # Complex types
        with pytest.raises(TypeError):
            Safe_Float__LLM__Temperature([0.7])
            
        with pytest.raises(TypeError):
            Safe_Float__LLM__Temperature({'temp': 0.7})

    def test_comparison_operations(self):                                              # Test comparison with other values
        temp1 = Safe_Float__LLM__Temperature(0.7)
        temp2 = Safe_Float__LLM__Temperature(0.7)
        temp3 = Safe_Float__LLM__Temperature(1.0)

        # Equality
        assert temp1 == temp2
        assert temp1 == 0.7                                                           # Compare with float
        assert temp1 != temp3
        assert temp1 != 1.0

        # Ordering
        assert temp1 < temp3
        assert temp3 > temp1
        assert temp1 <= 0.7
        assert temp3 >= 1.0

    def test_arithmetic_operations(self):                                              # Test arithmetic with temperatures
        temp = Safe_Float__LLM__Temperature(0.5)

        # Addition returns regular Safe_Float__LLM__Temperature
        assert temp + 0.2 == 0.7
        assert type(temp + 0.2) is Safe_Float__LLM__Temperature

        # Subtraction
        assert temp - 0.2 == 0.3

        # Multiplication
        assert temp * 2 == 1.0

        # Division
        assert temp / 2 == 0.25

    def test_usage_in_type_safe(self):                                                # Test integration with Type_Safe
        class Schema__LLM__Config(Type_Safe):
            temperature     : Safe_Float__LLM__Temperature
            top_p          : float = 0.9
            model          : str = 'gpt-4'

        with Schema__LLM__Config() as _:
            assert type(_.temperature) is Safe_Float__LLM__Temperature
            assert _.temperature == 0.0                                               # Default initialization

            # Assignment with auto-conversion
            _.temperature = 0.7
            assert _.temperature == 0.7
            assert type(_.temperature) is Safe_Float__LLM__Temperature

            # String conversion
            _.temperature = '1.5'
            assert _.temperature == 1.5

            # Clamping on assignment
            _.temperature = 3.0                                                       # Gets clamped
            assert _.temperature == 2.0                                               # Clamped to max

    def test_json_serialization(self):                                                # Test JSON round-trip
        class Schema__Generation__Config(Type_Safe):
            temperature : Safe_Float__LLM__Temperature
            max_tokens  : int = 100

        with Schema__Generation__Config() as original:
            original.temperature = 0.7
            original.max_tokens = 500

            # Serialize
            json_data = original.json()
            assert json_data == {'temperature': 0.7, 'max_tokens': 500}
            assert type(json_data['temperature']) is float                            # Serializes as float

            # Deserialize
            with Schema__Generation__Config.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.temperature) is Safe_Float__LLM__Temperature
                assert restored.temperature == 0.7

    def test_string_representation(self):                                            # Test string formatting
        temp = Safe_Float__LLM__Temperature(0.70)

        # String representation
        assert str(temp) == '0.70'                                                    # Two decimal places
        assert f"Temperature: {temp}" == "Temperature: 0.70"

        # Repr
        assert repr(temp) == "Safe_Float__LLM__Temperature(0.70)"

        # Format with different precisions
        temp2 = Safe_Float__LLM__Temperature(1.0)
        assert str(temp2) == '1.00'                                                   # Always shows 2 decimals

    def test_common_llm_temperatures(self):                                           # Test common LLM temperature settings
        # GPT models typically use 0.7 default
        gpt_default = Safe_Float__LLM__Temperature(0.7)
        assert gpt_default == 0.7

        # Claude often uses 0.0 for deterministic responses
        claude_deterministic = Safe_Float__LLM__Temperature(0.0)
        assert claude_deterministic == 0.0

        # Creative writing often uses higher temps
        creative = Safe_Float__LLM__Temperature(1.2)
        assert creative == 1.2

        # Code generation often uses lower temps
        code_gen = Safe_Float__LLM__Temperature(0.2)
        assert code_gen == 0.2

    def test_temperature_validation_messages(self):                                   # Test validation edge cases
        # Test that clamping happens silently (no errors)
        temp = Safe_Float__LLM__Temperature(-10)
        assert temp == 0.0                                                            # Clamped, no error

        temp = Safe_Float__LLM__Temperature(100)
        assert temp == 2.0                                                            # Clamped, no error

        # Test with very small positive values
        temp = Safe_Float__LLM__Temperature(0.0001)
        assert temp == 0.00                                                           # Rounds to 0.00

        # Test with values very close to max
        temp = Safe_Float__LLM__Temperature(1.999)
        assert temp == 2.00                                                           # Rounds to 2.00

    def test_integration_with_llm_request(self):                                     # Test realistic LLM request scenario
        class Schema__OpenAI__Request(Type_Safe):
            model       : str
            temperature : Safe_Float__LLM__Temperature
            max_tokens  : int
            messages    : list

        with Schema__OpenAI__Request() as request:
            request.model = 'gpt-4'
            request.temperature = 0.7
            request.max_tokens = 1000
            request.messages = [
                {'role': 'system', 'content': 'You are helpful.'},
                {'role': 'user', 'content': 'Hello!'}
            ]

            # Verify temperature is properly typed and valued
            assert type(request.temperature) is Safe_Float__LLM__Temperature
            assert request.temperature == 0.7

            # Simulate API call payload
            api_payload = request.json()
            assert api_payload['temperature'] == 0.7
            assert type(api_payload['temperature']) is float

    def test_temperature_presets(self):                                               # Test common temperature presets
        # Define temperature presets as Safe_Float__LLM__Temperature
        TEMP_DETERMINISTIC = Safe_Float__LLM__Temperature(0.0)
        TEMP_FOCUSED       = Safe_Float__LLM__Temperature(0.3)
        TEMP_BALANCED      = Safe_Float__LLM__Temperature(0.7)
        TEMP_CREATIVE      = Safe_Float__LLM__Temperature(1.0)
        TEMP_RANDOM        = Safe_Float__LLM__Temperature(1.5)

        assert TEMP_DETERMINISTIC == 0.0
        assert TEMP_FOCUSED       == 0.3
        assert TEMP_BALANCED      == 0.7
        assert TEMP_CREATIVE      == 1.0
        assert TEMP_RANDOM        == 1.5

        # All are proper type
        assert type(TEMP_DETERMINISTIC) is Safe_Float__LLM__Temperature
        assert type(TEMP_CREATIVE) is Safe_Float__LLM__Temperature