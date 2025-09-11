import pytest
import math
from decimal                                                 import Decimal
from unittest                                                import TestCase
from osbot_utils.type_safe.primitives.safe_float.Safe_Float  import Safe_Float
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Financial import Safe_Float__Financial
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Scientific import Safe_Float__Scientific


class test_Safe_Float(TestCase):

    def test_Safe_Float_class(self):
        # Valid cases - basic floats
        assert float(Safe_Float(123.45))    == 123.45
        assert float(Safe_Float(0.0))       == 0.0
        assert float(Safe_Float(-456.78))   == -456.78
        assert float(Safe_Float(3.14159))   == 3.14159

        # Integer conversion (allowed by default)
        assert float(Safe_Float(123))       == 123.0
        assert float(Safe_Float(0))         == 0.0
        assert float(Safe_Float(-456))      == -456.0

        # String conversion (allowed by default)
        assert float(Safe_Float('123.45'))  == 123.45
        assert float(Safe_Float('0.0'))     == 0.0
        assert float(Safe_Float('-456.78')) == -456.78
        assert float(Safe_Float('3.14159')) == 3.14159

        # Scientific notation
        assert float(Safe_Float(1e10))      == 1e10
        assert float(Safe_Float('1e10'))    == 1e10
        assert float(Safe_Float(1.23e-4))   == 1.23e-4

        # allow empty values
        assert Safe_Float(    ) == 0
        assert Safe_Float(None) == 0  # allow None

        # Boolean values (not allowed by default)
        with pytest.raises(TypeError, match="Safe_Float does not allow boolean values"):
            Safe_Float(True)
        with pytest.raises(TypeError, match="Safe_Float does not allow boolean values"):
            Safe_Float(False)

        # Invalid string conversions
        with pytest.raises(ValueError, match="Cannot convert 'abc' to float"):
            Safe_Float('abc')
        with pytest.raises(ValueError, match="Safe_Float does not allow NaN values"):
            Safe_Float('NaN123')

        # Other invalid types
        with pytest.raises(TypeError, match="Safe_Float requires a float value, got list"):
            Safe_Float([1.0, 2.0, 3.0])
        with pytest.raises(TypeError, match="Safe_Float requires a float value, got dict"):
            Safe_Float({'value': 123.45})

    def test_precision_handling(self):
        # Test decimal places rounding
        class Float_Two_Decimals(Safe_Float):
            decimal_places = 2
            round_output = True

        assert float(Float_Two_Decimals(3.14159))    == 3.14
        assert float(Float_Two_Decimals(3.145))      == 3.15  # Rounds up
        assert float(Float_Two_Decimals(3.144))      == 3.14  # Rounds down
        assert float(Float_Two_Decimals(123.456789)) == 123.46

        # Test floating point error cleanup
        class Float_Clean(Safe_Float):
            decimal_places = 2
            round_output = True

        # These would normally have floating point errors
        assert float(Float_Clean(157.95000000000002)) == 157.95
        assert float(Float_Clean(2.9999999999999996)) == 3.0
        assert float(Float_Clean(0.1 + 0.2))          == 0.3  # Classic example

    def test_decimal_arithmetic(self):
        # Test use_decimal for exact arithmetic
        class Float_Exact(Safe_Float):
            use_decimal = True
            decimal_places = 2
            round_output = True

        # Division that normally has precision issues
        val1 = Float_Exact(4.8)
        result = val1 / 1.6
        assert float(result) == 3.0  # Exactly 3.0, not 2.9999999999996

        # Multiplication that normally has precision issues
        val2 = Float_Exact(243)
        result = val2 * 0.65
        assert float(result) == 157.95  # Exactly 157.95, not 157.95000000000002

        # Chain of operations
        val3 = Float_Exact(100)
        result = (val3 * 0.1) * 0.1
        assert float(result) == 1.0  # Exactly 1.0

    def test_range_validation(self):
        class Float_Ranged(Safe_Float):
            min_value = -100.0
            max_value = 100.0

        # Valid range
        assert float(Float_Ranged(50.0))   == 50.0
        assert float(Float_Ranged(-50.0))  == -50.0
        assert float(Float_Ranged(100.0))  == 100.0
        assert float(Float_Ranged(-100.0)) == -100.0

        # Out of range
        with pytest.raises(ValueError, match="Float_Ranged must be >= -100.0, got -101.0"):
            Float_Ranged(-101.0)
        with pytest.raises(ValueError, match="Float_Ranged must be <= 100.0, got 101.0"):
            Float_Ranged(101.0)

    def test_clamping_behavior(self):
        class Float_Clamped(Safe_Float):
            min_value = 0.0
            max_value = 1.0
            clamp_to_range = True

        # Values get clamped instead of raising errors
        assert float(Float_Clamped(-0.5)) == 0.0   # Clamped to min
        assert float(Float_Clamped(1.5))  == 1.0   # Clamped to max
        assert float(Float_Clamped(0.5))  == 0.5   # Within range

    def test_inf_nan_handling(self):
        class Float_Inf_To_Max(Safe_Float):
            max_value = 1000.0

        # Infinity gets converted to max_value
        with pytest.raises(ValueError, match="Float_Inf_To_Max does not allow infinite values"):
            assert float(Float_Inf_To_Max(float('inf')))  == 1000.0
        with pytest.raises(ValueError, match="Float_Inf_To_Max does not allow infinite values"):
            assert float(Float_Inf_To_Max(float('-inf'))) == -1000.0


        with pytest.raises(ValueError, match="Float_Inf_To_Max does not allow NaN values"):
            assert float(Float_Inf_To_Max(float('nan'))) == 0.0

    def test_epsilon_equality(self):
        class Float_With_Epsilon(Safe_Float):
            epsilon = 1e-9

        val1 = Float_With_Epsilon(1.0)
        val2 = 1.0 + 1e-10  # Very small difference

        # These should be considered equal within epsilon
        assert val1 == val2
        assert val1 == 1.0

        # This should not be equal (difference > epsilon)
        assert not (val1 == 1.001)

    def test_arithmetic_operations(self):
        # Test that arithmetic operations maintain type and precision
        class Float_Arithmetic(Safe_Float):
            decimal_places = 2
            round_output   = True
            use_decimal    = True

        a = Float_Arithmetic(10.0)
        b = Float_Arithmetic(3.0)

        # Division with precision handling
        result = a / b
        assert type(result) is Float_Arithmetic
        assert float(result) == 3.33  # Rounded to 2 decimal places

        # Multiplication
        result = a * 0.15
        assert type(result) is Float_Arithmetic
        assert float(result) == 1.50

        # Complex calculation
        result = (a * 2.5) / 4.0
        assert type(result) is Float_Arithmetic
        assert float(result) == 6.25

    def test_usage_in_Type_Safe(self):
        class Product(Type_Safe):
            price      : Safe_Float
            tax_rate   : Safe_Float = Safe_Float(0.08)
            discount   : Safe_Float = Safe_Float(0.0)

        product = Product(price=Safe_Float(99.99))
        assert type(product.price) is Safe_Float
        assert float(product.price) == 99.99
        assert float(product.tax_rate) == 0.08
        assert float(product.discount) == 0.0

        # Calculate total with tax
        total = product.price * (1 + product.tax_rate)
        assert abs(float(total) - 107.9892) < 0.0001  # Close to expected value

        # Serialization round trip
        product_json = product.json()
        assert product_json == {
            'price': 99.99,
            'tax_rate': 0.08,
            'discount': 0.0
        }

        product_restored = Product.from_json(product_json)
        assert type(product_restored.price) is Safe_Float
        assert float(product_restored.price) == 99.99

    def test_custom_subclasses(self):

        # Test financial precision
        price = Safe_Float__Financial(19.99)
        quantity = 3
        subtotal = price * quantity
        assert float(subtotal) == 59.97  # Exactly 59.97, not 59.970000000000006

        # Can handle special values
        sci_val = Safe_Float__Scientific(1e308)

        result = sci_val * 10  # Would overflow
        assert math.isinf(result)

        # Percentage with clamping
        class Safe_Float__Percentage(Safe_Float):
            min_value = 0.0
            max_value = 100.0
            decimal_places = 2
            clamp_to_range = True

        pct = Safe_Float__Percentage(150.0)  # Over 100%
        assert float(pct) == 100.0  # Clamped to max

    def test_special_float_values(self):
        # Test that infinity is always rejected
        with pytest.raises(ValueError, match="Safe_Float does not allow infinite values"):
            Safe_Float(float('inf'))
        with pytest.raises(ValueError, match="Safe_Float does not allow infinite values"):
            Safe_Float(float('-inf'))

        # Test that NaN is always rejected
        with pytest.raises(ValueError, match="Safe_Float does not allow NaN values"):
            Safe_Float(float('nan'))

    def test_division_edge_cases(self):
        val = Safe_Float(10.0)

        # Division by zero always raises
        with pytest.raises(ZeroDivisionError):
            val / 0

        # Division by underflow value raises
        with pytest.raises(ZeroDivisionError):
            val / 1e-400

        # Division that would overflow raises
        big_val = Safe_Float(1e308)
        with pytest.raises(OverflowError):
            big_val / 1e-300

    def test_string_parsing_precision(self):
        # Test that string parsing maintains precision
        class Float_From_String(Safe_Float):
            use_decimal = True
            decimal_places = 10

        # These strings represent exact decimal values
        assert float(Float_From_String('0.1'))  == 0.1
        assert float(Float_From_String('0.01')) == 0.01
        assert float(Float_From_String('123.456789012345')) == 123.4567890123

    def test_combined_constraints(self):
        class Constrained_Float(Safe_Float):
            min_value = -273.15  # Absolute zero in Celsius
            max_value = 1000.0
            decimal_places = 1
            allow_inf = False
            allow_nan = False
            round_output = True
            use_decimal = True

        # Valid temperatures
        assert float(Constrained_Float(20.0))    == 20.0
        assert float(Constrained_Float(-40.0))   == -40.0
        assert float(Constrained_Float(100.0))   == 100.0
        assert float(Constrained_Float(37.456))  == 37.5  # Rounded

        # Out of range
        with pytest.raises(ValueError, match="Constrained_Float must be >= -273.15"):
            Constrained_Float(-300.0)
        with pytest.raises(ValueError, match="Constrained_Float must be <= 1000.0"):
            Constrained_Float(1001.0)

    def test_decimal_conversion(self):
        # Test conversion from Decimal
        class Float_From_Decimal(Safe_Float):
            decimal_places = 4

        decimal_val = Decimal('123.456789')
        result = Float_From_Decimal(decimal_val)
        assert float(result) == 123.4568  # Rounded to 4 places

    def test__safe_float__basic_arithmetic(self):
        # Basic Safe_Float
        float1 = Safe_Float(10.5)
        float2 = Safe_Float(20.3)

        result = float1 + float2
        assert type(result) is Safe_Float
        assert result == 30.8

        # With plain float
        result = float1 + 5.5
        assert type(result) is Safe_Float
        assert result == 16.0

    def test__safe_float__string_representation(self):
        # Basic Safe_Float
        value = Safe_Float(123.456)
        assert str(value) == "123.456"
        assert f"{value}" == "123.456"
        assert repr(value) == "Safe_Float(123.456)"

        # Scientific notation
        large = Safe_Float(1.23e10)
        assert str(large) == "12300000000.0"
        assert f"Value: {large}" == "Value: 12300000000.0"

        # Small numbers
        small = Safe_Float(0.000123)
        assert str(small) == "0.000123"
        assert f"{small:.6f}" == "0.000123"

    def test__safe_float__edge_cases(self):
        # Zero
        zero = Safe_Float(0.0)
        assert str(zero) == "0.0"
        assert f"{zero}" == "0.0"

        # Negative
        negative = Safe_Float(-123.45)
        assert str(negative) == "-123.45"
        assert f"Balance: {negative}" == "Balance: -123.45"

        # Very small (might use scientific notation)
        tiny = Safe_Float(0.00000001)
        assert "e" in str(tiny) or "E" in str(tiny) or str(tiny) == "0.00000001"

        # Integer-like float
        int_like = Safe_Float(42.0)
        assert str(int_like) == "42.0"

    def test__safe_float__addition_with_decimal(self):
        # Test addition with use_decimal=True for exact arithmetic
        class Float_Decimal(Safe_Float):
            use_decimal    = True
            decimal_places = 2
            round_output   = True

        # Classic floating point error: 0.1 + 0.2 != 0.3
        val1 = Float_Decimal(0.1)
        val2 = Float_Decimal(0.2)

        # Test Safe_Float + Safe_Float
        result = val1 + val2
        assert type(result) is Float_Decimal
        assert float(result) == 0.3  # Exactly 0.3, not 0.30000000000000004

        # Test Safe_Float + float
        result = val1 + 0.2
        assert type(result) is Float_Decimal
        assert float(result) == 0.3

        # Test float + Safe_Float (reverse addition)
        result = 0.1 + val2
        assert type(result) is Float_Decimal
        assert float(result) == 0.3

        # Chain of additions
        val3 = Float_Decimal(0.1)
        result = val1 + val2 + val3
        assert float(result) == 0.4

    def test__safe_float__subtraction_with_decimal(self):
        # Test subtraction with use_decimal=True
        class Float_Decimal(Safe_Float):
            use_decimal    = True
            decimal_places = 2
            round_output   = True

        val1 = Float_Decimal(0.3)
        val2 = Float_Decimal(0.1)

        # Test Safe_Float - Safe_Float
        result = val1 - val2
        assert type(result) is Float_Decimal
        assert float(result) == 0.2  # Exactly 0.2, not 0.19999999999999998

        # Test Safe_Float - float
        val3 = Float_Decimal(0.2)
        result = val3 - 0.05
        assert type(result) is Float_Decimal
        assert float(result) == 0.15  # Exactly 0.15, not 0.15000000000000002

        # Test float - Safe_Float (reverse subtraction)
        result = 0.3 - val2
        assert type(result) is Float_Decimal
        assert float(result) == 0.2

        # Complex subtraction chain
        val4 = Float_Decimal(1.0)
        result = val4 - 0.1 - 0.1 - 0.1
        assert float(result) == 0.7  # Exactly 0.7

    def test__safe_float__mixed_arithmetic_operations(self):
        # Test all arithmetic operations together
        class Float_Precise(Safe_Float):
            use_decimal    = True
            decimal_places = 4
            round_output   = True

        val = Float_Precise(10.0)

        # Addition
        assert float(val + 0.1) == 10.1
        assert float(0.1 + val) == 10.1

        # Subtraction
        assert float(val - 0.1) == 9.9
        assert float(10.1 - val) == 0.1

        # Multiplication (already implemented)
        assert float(val * 0.1) == 1.0
        assert float(0.1 * val) == 1.0

        # Division (already implemented)
        assert float(val / 3) == 3.3333

        # Complex expression
        result = (val + 5) * 2 - 10
        assert float(result) == 20.0

    def test__safe_float__arithmetic_without_decimal(self):
        # Test that regular float arithmetic still works without use_decimal
        class Float_Regular(Safe_Float):
            use_decimal = False  # Regular float arithmetic

        val1 = Float_Regular(0.1)
        val2 = Float_Regular(0.2)

        # This will have floating point error
        result = val1 + val2
        assert type(result) is Float_Regular
        assert float(result) == pytest.approx(0.30000000000000004)

        # Subtraction will also have precision issues
        val3 = Float_Regular(0.3)
        result = val3 - val1
        assert float(result) != 0.2  # Not exactly 0.2 due to float precision

    def test__safe_float__arithmetic_type_preservation(self):
        # Test that arithmetic operations preserve the Safe_Float subclass
        class Temperature(Safe_Float):
            min_value      = -273.15
            max_value      = 1000.0
            decimal_places = 1
            use_decimal    = True

        temp1 = Temperature(20.0)
        temp2 = Temperature(5.0)

        # All operations should return Temperature instances
        assert type(temp1 + temp2) is Temperature
        assert type(temp1 - temp2) is Temperature
        assert type(temp1 * 2) is Temperature
        assert type(temp1 / 2) is Temperature

        # Even with plain floats
        assert type(temp1 + 10.0) is Temperature
        assert type(30.0 - temp1) is Temperature

    def test__safe_float__arithmetic_with_constraints(self):
        # Test arithmetic with min/max constraints
        class Percentage(Safe_Float):
            min_value      = 0.0
            max_value      = 100.0
            decimal_places = 2
            use_decimal    = True

        pct1 = Percentage(50.0)
        pct2 = Percentage(30.0)

        # Valid operations
        result = pct1 + pct2
        assert float(result) == 80.0

        result = pct1 - pct2
        assert float(result) == 20.0

        # Operations that violate constraints return raw float
        result = pct1 + pct1 + pct1  # Would be 150.0
        assert type(result) is float  # Falls back to float
        assert result == 150.0

        result = pct2 - pct1  # Would be -20.0
        assert type(result) is float  # Falls back to float
        assert result == -20.0

    def test__safe_float__arithmetic_with_none_handling(self):
        # Test None handling in arithmetic
        class Float_Allow_None(Safe_Float):
            allow_none = True

        class Float_No_None(Safe_Float):
            allow_none = False

        # With allow_none=True
        val1 = Float_Allow_None(None)
        assert float(val1) == 0.0
        assert float(val1 + 10) == 10.0

        # With allow_none=False
        with pytest.raises(ValueError, match="Float_No_None does not allow None values"):
            Float_No_None(None)

    def test__safe_float__arithmetic_with_cleaning(self):
        # Test __clean_float method for fixing precision errors
        class Float_Clean(Safe_Float):
            decimal_places = 2
            round_output   = True
            use_decimal    = False  # Use regular float to test cleaning

        val = Float_Clean(10.0)

        # Operations that create "almost round" numbers
        result = val * 1.111111
        assert float(result) == 11.11  # Cleaned to exactly 11.11

        result = val / 3
        assert float(result) == 3.33  # Cleaned to exactly 3.33

    def test__bug__safe_float__arithmetic_overflow_handling(self):
        # Test overflow/underflow handling
        big_val = Safe_Float(1e308)

        # Multiplication overflow
        with pytest.raises(OverflowError, match="Multiplication resulted in inf"):
            big_val * 1e10

        # Division overflow
        with pytest.raises(OverflowError, match="Division resulted in inf"):
            big_val / 1e-300        # bug?? this works

        small_val = Safe_Float(1e-300)

        # Division underflow (approaches zero)
        result = small_val / 1e10
        assert float(result) == 0.0 or float(result) < 1e-309

    def test__safe_float__repr_and_str(self):
        # Test string representations for different Safe_Float subclasses

        # Basic Safe_Float
        basic = Safe_Float(123.45)
        assert str(basic) == "123.45"
        assert repr(basic) == "Safe_Float(123.45)"

        # Custom subclass
        class Money(Safe_Float):
            decimal_places = 2
            use_decimal    = True

        money = Money(19.99)
        assert str(money) == "19.99"
        assert repr(money) == "Money(19.99)"

        # With very small numbers
        tiny = Safe_Float(0.0000001)
        assert "e" in str(tiny).lower() or str(tiny) == "0.0000001"

        # Zero values
        zero = Safe_Float(0.0)
        assert str(zero) == "0.0"
        assert repr(zero) == "Safe_Float(0.0)"

    def test__decimal_precision(self):                                                  # Test Decimal arithmetic precision


        temp1 = Safe_Float(0.1)                                   # check No floating point errors
        temp2 = Safe_Float(0.2)                                   # since In regular float: 0.1 + 0.2 = 0.30000000000000004

        assert temp1 + temp2              == 0.3                                    # With Decimal: exact arithmetic (i.e. 0.3)
        assert temp1 + 0.2                == 0.3                                    # sum doesn't lose the type safe
        assert 0.1 + temp2                == 0.3                                    # sum doesn't lose the type safe
        assert temp1 - 0.05               == 0.05                                   # subtraction also doesn't lose the type safe
        assert temp2 - 0.05               == 0.15                    # BUG
        assert float(temp1 + temp2)       == 0.3                    # BUG
        assert type(temp1 + temp2)        == Safe_Float
        assert type(float(temp1 + temp2)) == float

        assert 0.1 + 0.2 != 0.30000000000000001                                     # WTF: so this one doesn't work
        assert 0.1 + 0.2 == 0.30000000000000002                                     # WTF: and this one does?
        assert 0.1 + 0.2 == 0.30000000000000003                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000004                                     # WTF: this is a reall
        assert 0.1 + 0.2 == 0.30000000000000005                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000006                                     # WTF: and this
        assert 0.1 + 0.2 == 0.30000000000000007                                     # WTF: and this
        assert 0.1 + 0.2 != 0.30000000000000009                                     # WTF: and somehow the .9 doesn't
        assert str(0.1 + 0.2) == "0.30000000000000004"
