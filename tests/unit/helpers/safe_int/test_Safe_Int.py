import pytest
from unittest                                    import TestCase
from osbot_utils.helpers.safe_float.Safe_Float   import Safe_Float
from osbot_utils.helpers.safe_int.Safe_Int       import Safe_Int
from osbot_utils.type_safe.Type_Safe             import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive  import Type_Safe__Primitive
from osbot_utils.utils.Objects                   import __, base_types


class test_Safe_Int(TestCase):

    def test_Safe_Int_class(self):
        # Valid cases - basic integers
        assert int(Safe_Int(123))      == 123
        assert int(Safe_Int(0))        == 0
        assert int(Safe_Int(-456))     == -456
        assert int(Safe_Int(999999))   == 999999

        # String conversion (allowed by default)
        assert int(Safe_Int('123'))    == 123
        assert int(Safe_Int('0'))      == 0
        assert int(Safe_Int('-456'))   == -456
        assert int(Safe_Int('999999')) == 999999

        # Edge values
        assert int(Safe_Int(2**31 - 1)) == 2147483647  # Max 32-bit int
        assert int(Safe_Int(-2**31))    == -2147483648  # Min 32-bit int

        # Boolean values (not allowed by default)
        with pytest.raises(TypeError, match="Safe_Int does not allow boolean values"):
            Safe_Int(True)
        with pytest.raises(TypeError, match="Safe_Int does not allow boolean values"):
            Safe_Int(False)

        # allow None and empty
        assert Safe_Int(None) == 0
        assert Safe_Int()     == 0
        assert Safe_Int(0)    == 0

        # Invalid string conversions
        with pytest.raises(ValueError, match="Cannot convert 'abc' to integer"):
            Safe_Int('abc')
        with pytest.raises(ValueError, match="Cannot convert '12.34' to integer"):
            Safe_Int('12.34')
        with pytest.raises(ValueError, match="Cannot convert '1e10' to integer"):
            Safe_Int('1e10')

        # Other invalid types
        with pytest.raises(TypeError, match="Safe_Int requires an integer value, got float"):
            Safe_Int(3.14)
        with pytest.raises(TypeError, match="Safe_Int requires an integer value, got list"):
            Safe_Int([1, 2, 3])
        with pytest.raises(TypeError, match="Safe_Int requires an integer value, got dict"):
            Safe_Int({'value': 123})

    def test_custom_subclass(self):
        # Create a subclass with custom settings
        class Custom_Safe_Int(Safe_Int):
            min_value  = -100
            max_value  = 100
            allow_none = True
            allow_bool = True

        # Test custom settings
        assert int(Custom_Safe_Int(50))   == 50
        assert int(Custom_Safe_Int(-50))  == -50
        assert int(Custom_Safe_Int(100))  == 100
        assert int(Custom_Safe_Int(-100)) == -100

        # None becomes 0
        assert int(Custom_Safe_Int(None)) == 0

        # Boolean conversion allowed
        assert int(Custom_Safe_Int(True))  == 1
        assert int(Custom_Safe_Int(False)) == 0

        # Range validation
        with pytest.raises(ValueError, match="Custom_Safe_Int must be >= -100, got -101"):
            Custom_Safe_Int(-101)
        with pytest.raises(ValueError, match="Custom_Safe_Int must be <= 100, got 101"):
            Custom_Safe_Int(101)

    def test_custom_subclass__in_Type_Safe(self):
        class Custom_Safe_Int(Safe_Int):
            min_value   = 0
            max_value   = 1000
            allow_str   = False
            strict_type = True

        class An_Class(Type_Safe):
            an_int: Custom_Safe_Int = Custom_Safe_Int(42)

        an_class = An_Class()
        assert type(an_class.an_int)       is Custom_Safe_Int
        assert base_types(an_class.an_int) == [Safe_Int, Type_Safe__Primitive, int, object, object]

        # Valid assignment
        an_class.an_int = Custom_Safe_Int(100)
        assert int(an_class.an_int) == 100

        # String conversion not allowed
        with pytest.raises(TypeError, match="Custom_Safe_Int requires int type, got str"):
            an_class.an_int = Custom_Safe_Int('100')

        # Out of range
        with pytest.raises(ValueError, match="Custom_Safe_Int must be <= 1000, got 1001"):
            an_class.an_int = Custom_Safe_Int(1001)

        # Round trip serialization
        an_class_round_trip = An_Class.from_json(an_class.json())
        assert an_class_round_trip.obj()      == an_class.obj()
        assert type(an_class_round_trip.an_int) is Custom_Safe_Int

    def test_usage_in_Type_Safe(self):
        class An_Class(Type_Safe):
            safe_int_1: Safe_Int = None
            safe_int_2: Safe_Int = Safe_Int(123)
            safe_int_3: Safe_Int = Safe_Int(-456)
            safe_int_4: Safe_Int = Safe_Int('789')

        an_class = An_Class()
        assert type(an_class.safe_int_1) is type(None)
        assert type(an_class.safe_int_2) is Safe_Int
        assert type(an_class.safe_int_3) is Safe_Int
        assert type(an_class.safe_int_4) is Safe_Int

        assert an_class.obj() == __(safe_int_1 = None,
                                    safe_int_2 = 123,
                                    safe_int_3 = -456,
                                    safe_int_4 = 789)

        assert an_class.json() == {'safe_int_1': None,
                                  'safe_int_2': 123,
                                  'safe_int_3': -456,
                                  'safe_int_4': 789}

        an_class__round_trip = An_Class.from_json(an_class.json())
        assert an_class__round_trip.obj() == an_class.obj()
        assert type(an_class__round_trip.safe_int_1) is type(None)

    def test_arithmetic_operations(self):
        # Test that arithmetic operations maintain type safety
        a = Safe_Int(10)
        b = Safe_Int(5)

        # Addition
        result = a + b
        assert type(result) is Safe_Int
        assert int(result) == 15

        # Subtraction
        result = a - b
        assert type(result) is Safe_Int
        assert int(result) == 5

        # Multiplication
        result = a * b
        assert type(result) is Safe_Int
        assert int(result) == 50

        # True division (returns float)
        result = a / b
        assert type(result) is Safe_Float
        assert result == 2.0

        # Integer division with no remainder
        result = Safe_Int(10).__truediv__(Safe_Int(5))
        assert type(result) is Safe_Float
        assert int(result) == 2

    def test_strict_type_validation(self):
        class Strict_Safe_Int(Safe_Int):
            strict_type = True
            allow_str   = False
            allow_bool  = False

        # Only pure integers allowed
        assert int(Strict_Safe_Int(123)) == 123
        assert int(Strict_Safe_Int(0))   == 0
        assert int(Strict_Safe_Int(-456)) == -456

        # No string conversion
        with pytest.raises(TypeError, match="Strict_Safe_Int requires int type, got str"):
            Strict_Safe_Int('123')

        # No boolean conversion
        with pytest.raises(TypeError, match="Strict_Safe_Int does not allow boolean values"):
            Strict_Safe_Int(True)

        # No float conversion
        with pytest.raises(TypeError, match="Strict_Safe_Int requires int type, got float"):
            Strict_Safe_Int(3.14)

    def test_combined_constraints(self):
        class Constrained_Int(Safe_Int):
            min_value   = 10
            max_value   = 100
            allow_str   = True
            allow_bool  = False
            allow_none  = True

        # Valid values
        assert int(Constrained_Int(50))  == 50
        assert int(Constrained_Int(10))  == 10
        assert int(Constrained_Int(100)) == 100
        assert int(Constrained_Int('75')) == 75
        assert int(Constrained_Int(None)) == 0  # None becomes 0

        # Out of range
        with pytest.raises(ValueError, match="Constrained_Int must be >= 10, got 9"):
            Constrained_Int(9)
        with pytest.raises(ValueError, match="Constrained_Int must be <= 100, got 101"):
            Constrained_Int(101)

        # Invalid string
        with pytest.raises(ValueError, match="Cannot convert 'abc' to integer"):
            Constrained_Int('abc')

        # Boolean not allowed
        with pytest.raises(TypeError, match="Constrained_Int does not allow boolean values"):
            Constrained_Int(True)