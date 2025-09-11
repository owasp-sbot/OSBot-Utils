import re

import pytest
from unittest                                   import TestCase
from osbot_utils.type_safe.primitives.safe_str.Safe_Str      import Safe_Str
from osbot_utils.type_safe.primitives.safe_float.Safe_Float  import Safe_Float
from osbot_utils.type_safe.primitives.safe_int.Safe_Int      import Safe_Int


class test_Safe_Str___mix_edge_cases(TestCase):
    def test__safe_primitives__edge_cases(self):
        # Negative numbers with Safe_Int
        int_val = Safe_Int(-10)
        result = int_val + (-5)
        assert type(result) is Safe_Int
        assert result == -15

        # Zero with Safe_Float
        float_val = Safe_Float(0.0)
        result = float_val + 10.5
        assert type(result) is Safe_Float
        assert result == 10.5

        # Empty string with Safe_Str
        str_val = Safe_Str('')
        result = str_val + 'hello'
        assert type(result) is Safe_Str
        assert result == 'hello'

    def test__safe_primitives__type_errors(self):
        # String + number should still raise TypeError
        str_val = Safe_Str('hello')
        with pytest.raises(TypeError):
            str_val + 123

        # Number + string should still raise TypeError
        int_val = Safe_Int(123)
        error_message_1 = "unsupported operand type(s) for +: 'Safe_Int' and 'str'"
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            int_val + 'hello'

        float_val = Safe_Float(12.3)
        error_message_2 = "could not convert string to float: 'hello'"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            float_val + 'hello'