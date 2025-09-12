import re
import pytest
from unittest                                                                        import TestCase
from osbot_utils.utils.Objects                                                       import __, base_classes
from osbot_utils.type_safe.Type_Safe__Primitive                                      import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__API__Parameter  import Safe_Str__API__Parameter


class test_Safe_Str__API__Parameter(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__API__Parameter() as _:
            assert type(_)         is Safe_Str__API__Parameter
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 64

    def test_valid_parameters(self):                                            # Test API parameter names
        # Common LLM parameters
        assert Safe_Str__API__Parameter('max_tokens')           == 'max_tokens'
        assert Safe_Str__API__Parameter('temperature')          == 'temperature'
        assert Safe_Str__API__Parameter('top_p')                == 'top_p'
        assert Safe_Str__API__Parameter('top_k')                == 'top_k'
        assert Safe_Str__API__Parameter('stream')               == 'stream'
        assert Safe_Str__API__Parameter('response_format')      == 'response_format'
        assert Safe_Str__API__Parameter('stop_sequences')       == 'stop_sequences'
        assert Safe_Str__API__Parameter('presence_penalty')     == 'presence_penalty'
        assert Safe_Str__API__Parameter('frequency_penalty')    == 'frequency_penalty'

        # With numbers
        assert Safe_Str__API__Parameter('param1')               == 'param1'
        assert Safe_Str__API__Parameter('value_2')              == 'value_2'
        assert Safe_Str__API__Parameter('test_123')             == 'test_123'

        # Invalid chars replaced
        assert Safe_Str__API__Parameter('param-name')           == 'param_name'
        assert Safe_Str__API__Parameter('param.name')           == 'param_name'
        assert Safe_Str__API__Parameter('param name')           == 'param_name'
        assert Safe_Str__API__Parameter('param@value')          == 'param_value'

    def test_edge_cases(self):                                                  # Test edge cases
        # Only underscores
        assert Safe_Str__API__Parameter('___')                  == '___'

        # Single character
        assert Safe_Str__API__Parameter('n')                    == 'n'
        assert Safe_Str__API__Parameter('_')                    == '_'

        # Numbers only
        assert Safe_Str__API__Parameter('123')                  == '123'

        # Max length
        long_param = 'a' * 64
        assert Safe_Str__API__Parameter(long_param)             == long_param

        # Exceeds max length
        too_long = 'a' * 65
        error_message = "in Safe_Str__API__Parameter, value exceeds maximum length of 64"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__API__Parameter(too_long)


