import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Int                                 import Safe_Int
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int__Negative import Safe_Int__Negative
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int__Negative import TYPE_SAFE_INT__NEGATIVE__MAX_VALUE
from osbot_utils.utils.Objects                                                      import base_classes


class test_Safe_Int__Negative(TestCase):

    def test__init__(self):                                                                     # Test Safe_Int__Negative initialization and inheritance
        with Safe_Int__Negative(-1) as _:
            assert type(_)         is Safe_Int__Negative
            assert base_classes(_) == [Safe_Int, Type_Safe__Primitive, int, object, object]
            assert _               == -1
            assert _.max_value     == TYPE_SAFE_INT__NEGATIVE__MAX_VALUE
            assert _.max_value     == -1                                                        # Strictly less than zero

    def test__init____with_negative_values(self):                                               # Various negative integers are valid
        assert Safe_Int__Negative(-1)          == -1
        assert Safe_Int__Negative(-2)          == -2
        assert Safe_Int__Negative(-100)        == -100
        assert Safe_Int__Negative(-999999999)  == -999999999

    def test__init____with_string_conversion(self):                                             # Safe_Int allows string conversion by default
        assert Safe_Int__Negative("-1")   == -1
        assert Safe_Int__Negative("-42")  == -42
        assert Safe_Int__Negative("-100") == -100

    def test__init____with_zero__raises_error(self):                                            # Zero is NOT valid (max_value = -1)
        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 0"):
            Safe_Int__Negative(0)

    def test__init____with_positive__raises_error(self):                                        # Positive values are invalid
        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 1"):
            Safe_Int__Negative(1)

        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 100"):
            Safe_Int__Negative(100)

    def test__init____with_invalid_string__raises_error(self):                                  # Non-numeric strings raise error
        with pytest.raises(ValueError):
            Safe_Int__Negative("abc")

        with pytest.raises(ValueError):
            Safe_Int__Negative("")

    def test__init____with_float__raises_error(self):                                           # Float values are not allowed
        with pytest.raises(TypeError):
            Safe_Int__Negative(-1.5)

    def test__init____with_bool__raises_error(self):                                            # Bool values not allowed by default
        with pytest.raises(TypeError):
            Safe_Int__Negative(True)

        with pytest.raises(TypeError):
            Safe_Int__Negative(False)

    def test__arithmetic__addition__stays_negative(self):                                       # Addition that stays negative
        result = Safe_Int__Negative(-10) + 5
        assert result        == -5
        assert type(result)  is Safe_Int__Negative

    def test__arithmetic__addition__to_invalid__raises_error(self):                             # Addition resulting in invalid value
        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 0"):
            Safe_Int__Negative(-5) + 5                                                          # Result would be 0

        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 5"):
            Safe_Int__Negative(-5) + 10                                                         # Result would be positive

    def test__arithmetic__subtraction(self):                                                    # Subtraction (goes more negative)
        result = Safe_Int__Negative(-5) - 3
        assert result        == -8
        assert type(result)  is Safe_Int__Negative

    def test__arithmetic__multiplication__negative_result(self):                                # Multiplication with negative result
        result = Safe_Int__Negative(-3) * 4
        assert result        == -12
        assert type(result)  is Safe_Int__Negative

    def test__arithmetic__multiplication__to_invalid__raises_error(self):                       # Multiplication resulting in positive
        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 12"):
            Safe_Int__Negative(-3) * -4                                                         # Result would be positive 12

    def test__arithmetic__floor_division__stays_negative(self):                                 # Floor division staying negative
        result = Safe_Int__Negative(-10) // 3
        assert result        == -4                                                              # Python floor division rounds toward -inf
        assert type(result)  is Safe_Int__Negative

    def test__arithmetic__floor_division__to_invalid__raises_error(self):                       # Floor division resulting in zero or positive
        with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 5"):
            Safe_Int__Negative(-10) // -2                                                       # Result would be positive 5

    def test__bug__arithmetic__negation__doesnt__raises_error(self):                            # Negation would make it positive
        #with pytest.raises(ValueError, match="Safe_Int__Negative must be <= -1, got 0"):
        #    aa = -Safe_Int__Negative(-5)                                                       # BUG should have raised, but this could be a bug by design | Result would be positive 5
        now_an_int = - Safe_Int__Negative(-5)                                                   # Result is a positive 5
        assert type(now_an_int) is int                                                          # and an int
        assert now_an_int == 5