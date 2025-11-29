import pytest
from unittest                                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                                 import Type_Safe__Primitive
from osbot_utils.utils.Objects                                                                  import base_classes
from osbot_utils.type_safe.primitives.core.Safe_Int                                             import Safe_Int
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int__Positive             import Safe_Int__Positive
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int__Positive             import TYPE_SAFE_INT__POSITIVE__MIN_VALUE


class test_Safe_Int__Positive(TestCase):

    def test__init__(self):                                                                     # Test Safe_Int__Positive initialization and inheritance
        with Safe_Int__Positive(1) as _:
            assert type(_)         is Safe_Int__Positive
            assert base_classes(_) == [Safe_Int, Type_Safe__Primitive, int, object, object]
            assert _               == 1
            assert _.min_value     == TYPE_SAFE_INT__POSITIVE__MIN_VALUE
            assert _.min_value     == 1                                                         # Strictly greater than zero

    def test__init____with_positive_values(self):                                               # Various positive integers are valid
        assert Safe_Int__Positive(1)          == 1
        assert Safe_Int__Positive(2)          == 2
        assert Safe_Int__Positive(100)        == 100
        assert Safe_Int__Positive(999999999)  == 999999999

    def test__init____with_string_conversion(self):                                             # Safe_Int allows string conversion by default
        assert Safe_Int__Positive("1")   == 1
        assert Safe_Int__Positive("42")  == 42
        assert Safe_Int__Positive("100") == 100

    def test__init____with_zero__raises_error(self):                                            # Zero is NOT valid (min_value = 1)
        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got 0"):
            Safe_Int__Positive(0)

    def test__init____with_negative__raises_error(self):                                        # Negative values are invalid
        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got -1"):
            Safe_Int__Positive(-1)

        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got -100"):
            Safe_Int__Positive(-100)

    def test__init____with_invalid_string__raises_error(self):                                  # Non-numeric strings raise error
        with pytest.raises(ValueError):
            Safe_Int__Positive("abc")

        with pytest.raises(ValueError):
            Safe_Int__Positive("")

    def test__init____with_float__raises_error(self):                                           # Float values are not allowed
        with pytest.raises(TypeError):
            Safe_Int__Positive(1.5)

    def test__init____with_bool__raises_error(self):                                            # Bool values not allowed by default
        with pytest.raises(TypeError):
            Safe_Int__Positive(True)

        with pytest.raises(TypeError):
            Safe_Int__Positive(False)

    def test__arithmetic__addition(self):                                                       # Arithmetic maintains type safety
        result = Safe_Int__Positive(5) + 3
        assert result        == 8
        assert type(result)  is Safe_Int__Positive

    def test__arithmetic__subtraction(self):                                                    # Subtraction that stays positive
        result = Safe_Int__Positive(10) - 5
        assert result        == 5
        assert type(result)  is Safe_Int__Positive

    def test__arithmetic__subtraction__to_invalid__raises_error(self):                          # Subtraction resulting in invalid value
        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got 0"):
            Safe_Int__Positive(5) - 5                                                           # Result would be 0

        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got -5"):
            Safe_Int__Positive(5) - 10                                                          # Result would be negative

    def test__arithmetic__multiplication(self):                                                 # Multiplication
        result = Safe_Int__Positive(3) * 4
        assert result        == 12
        assert type(result)  is Safe_Int__Positive

    def test__arithmetic__floor_division(self):                                                 # Floor division staying positive
        result = Safe_Int__Positive(10) // 3
        assert result        == 3
        assert type(result)  is Safe_Int__Positive

    def test__arithmetic__floor_division__to_invalid__raises_error(self):                       # Floor division resulting in zero
        with pytest.raises(ValueError, match="Safe_Int__Positive must be >= 1, got 0"):
            Safe_Int__Positive(1) // 2                                                          # Result would be 0