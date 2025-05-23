import pytest
import math
from decimal                                    import Decimal
from unittest                                   import TestCase
from osbot_utils.helpers.safe_float.Safe_Float  import Safe_Float
from osbot_utils.type_safe.Type_Safe            import Type_Safe



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
        with pytest.raises(ValueError, match="Cannot convert 'NaN123' to float"):
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
        # Financial calculations
        class Safe_Float__Financial(Safe_Float):
            decimal_places = 2
            use_decimal = True
            allow_inf = False
            allow_nan = False
            round_output = True

        # Test financial precision
        price = Safe_Float__Financial(19.99)
        quantity = 3
        subtotal = price * quantity
        assert float(subtotal) == 59.97  # Exactly 59.97, not 59.970000000000006

        # Scientific calculations
        class Safe_Float__Scientific(Safe_Float):
            allow_inf = True
            allow_nan = True
            decimal_places = 15

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