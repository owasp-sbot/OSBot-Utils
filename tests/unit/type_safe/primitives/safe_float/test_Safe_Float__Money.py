import pytest
from unittest                                           import TestCase
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money   import Safe_Float__Money
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class test_Safe_Float__Money(TestCase):

    def test_Safe_Float__Money_class(self):
        # Valid money values
        assert float(Safe_Float__Money(0.00))      == 0.00
        assert float(Safe_Float__Money(0.01))      == 0.01
        assert float(Safe_Float__Money(9.99))      == 9.99
        assert float(Safe_Float__Money(99.99))     == 99.99
        assert float(Safe_Float__Money(1000.00))   == 1000.00
        assert float(Safe_Float__Money(1234567.89)) == 1234567.89

        # String conversion with exact decimal handling
        assert float(Safe_Float__Money('19.99'))   == 19.99
        assert float(Safe_Float__Money('0.01'))    == 0.01
        assert float(Safe_Float__Money('1000.00')) == 1000.00

        # Integer conversion
        assert float(Safe_Float__Money(100))       == 100.00
        assert float(Safe_Float__Money(0))         == 0.00

        # Automatic rounding to 2 decimal places
        assert float(Safe_Float__Money(9.999))     == 10.00
        assert float(Safe_Float__Money(9.994))     == 9.99
        assert float(Safe_Float__Money(9.995))     == 10.00
        assert float(Safe_Float__Money(0.001))     == 0.00
        assert float(Safe_Float__Money(0.005))     == 0.01

        # Negative values not allowed (min_value = 0.0)
        with pytest.raises(ValueError, match="Safe_Float__Money must be >= 0.0, got -0.01"):
            Safe_Float__Money(-0.01)
        with pytest.raises(ValueError, match="Safe_Float__Money must be >= 0.0, got -100.0"):
            Safe_Float__Money(-100.00)

        # Special values not allowed
        with pytest.raises(ValueError, match="Safe_Float__Money does not allow infinite values"):
            Safe_Float__Money(float('inf'))
        with pytest.raises(ValueError, match="Safe_Float__Money does not allow NaN values"):
            Safe_Float__Money(float('nan'))

        # Invalid conversions
        with pytest.raises(ValueError, match="Cannot convert 'abc' to float"):
            Safe_Float__Money('abc')
        with pytest.raises(TypeError, match="Safe_Float__Money does not allow boolean values"):
            Safe_Float__Money(True)

    def test_exact_decimal_arithmetic(self):
        # Test that decimal arithmetic is exact (no floating point errors)

        # Classic floating point problem: 0.1 + 0.2 != 0.3
        val1 = Safe_Float__Money(0.1)
        val2 = Safe_Float__Money(0.2)
        result = Safe_Float__Money(float(val1) + float(val2))
        assert float(result) == 0.30  # Exactly 0.30, not 0.30000000000000004

        # Multiplication that typically has precision issues
        price = Safe_Float__Money(19.99)
        quantity = 3
        total = price * quantity
        assert float(total) == 59.97  # Exactly 59.97, not 59.970000000000006

        # Division with exact results
        total = Safe_Float__Money(100.00)
        result = total / 3
        assert float(result) == 33.33  # Rounded to 2 decimals

        # Chain of operations
        price = Safe_Float__Money(9.99)
        tax_rate = 0.0875  # 8.75%
        tax = price * tax_rate
        assert float(tax) == 0.87  # Rounded to 2 decimals

        total_with_tax = Safe_Float__Money(float(price) + float(tax))
        assert float(total_with_tax) == 10.86

    def test_common_money_calculations(self):
        # Shopping cart example
        item1 = Safe_Float__Money(29.99)
        item2 = Safe_Float__Money(15.50)
        item3 = Safe_Float__Money(7.25)

        subtotal = Safe_Float__Money(float(item1) + float(item2) + float(item3))
        assert float(subtotal) == 52.74

        # Discount calculation
        discount_percent = 0.15  # 15% off
        discount_amount = subtotal * discount_percent
        assert float(discount_amount) == 7.91

        # Tax calculation
        discounted_price = Safe_Float__Money(float(subtotal) - float(discount_amount))
        assert float(discounted_price) == 44.83

        tax_rate = 0.08  # 8% tax
        tax = discounted_price * tax_rate
        assert float(tax) == 3.59

        # Final total
        final_total = Safe_Float__Money(float(discounted_price) + float(tax))
        assert float(final_total) == 48.42

    def test_currency_edge_cases(self):
        # Very small amounts (penny splitting)
        total = Safe_Float__Money(10.00)
        split_three_ways = total / 3
        assert float(split_three_ways) == 3.33

        # Verify the remainder
        three_portions = Safe_Float__Money(float(split_three_ways) * 3)
        assert float(three_portions) == 9.99
        remainder = Safe_Float__Money(float(total) - float(three_portions))
        assert float(remainder) == 0.01

        # Large amounts
        million = Safe_Float__Money(1000000.00)
        assert float(million) == 1000000.00

        # Interest calculation
        principal = Safe_Float__Money(1000.00)
        rate = 0.035  # 3.5% annual
        interest = principal * rate
        assert float(interest) == 35.00

    def test_usage_in_Type_Safe(self):
        class Invoice_Line(Type_Safe):
            unit_price  : Safe_Float__Money
            quantity    : int
            tax_amount  : Safe_Float__Money = Safe_Float__Money(0.00)
            discount    : Safe_Float__Money = Safe_Float__Money(0.00)

        line = Invoice_Line(
            unit_price=Safe_Float__Money(24.99),
            quantity=2
        )

        # Calculate line total
        subtotal = Safe_Float__Money(float(line.unit_price) * line.quantity)
        assert float(subtotal) == 49.98

        # Apply discount
        line.discount = Safe_Float__Money(5.00)
        total_after_discount = Safe_Float__Money(float(subtotal) - float(line.discount))
        assert float(total_after_discount) == 44.98

        # Apply tax
        tax_rate = 0.07
        line.tax_amount = Safe_Float__Money(float(total_after_discount) * tax_rate)
        assert float(line.tax_amount) == 3.15

        # Serialization
        invoice_json = line.json()
        assert invoice_json == {
            'unit_price': 24.99,
            'quantity': 2,
            'tax_amount': 3.15,
            'discount': 5.00
        }

        # Deserialization
        restored = Invoice_Line.from_json(invoice_json)
        assert type(restored.unit_price) is Safe_Float__Money
        assert float(restored.unit_price) == 24.99

    def test_rounding_behavior(self):
        # Test banker's rounding (round half to even)
        assert float(Safe_Float__Money(2.225)) == 2.23  # Round up (ROUND_HALF_UP)
        assert float(Safe_Float__Money(2.215)) == 2.22  # Round up (ROUND_HALF_UP)
        assert float(Safe_Float__Money(2.2249)) == 2.22  # Round down
        assert float(Safe_Float__Money(2.2251)) == 2.23  # Round up

        # Edge cases at boundaries
        assert float(Safe_Float__Money(0.004)) == 0.00
        assert float(Safe_Float__Money(0.005)) == 0.01
        assert float(Safe_Float__Money(0.014)) == 0.01
        assert float(Safe_Float__Money(0.015)) == 0.02

    def test_money_formatting(self):
        # While Safe_Float__Money doesn't include formatting,
        # test that values are suitable for formatting
        price = Safe_Float__Money(1234.50)
        assert float(price) == 1234.50
        assert f"${float(price):,.2f}" == "$1,234.50"

        small = Safe_Float__Money(0.01)
        assert f"${float(small):.2f}" == "$0.01"

        large = Safe_Float__Money(1234567.89)
        assert f"${float(large):,.2f}" == "$1,234,567.89"

    def test__safe_float__money_precision(self):
        # Money with 2 decimal places
        price1 = Safe_Float__Money(10.99)
        price2 = Safe_Float__Money(5.50)

        result = price1 + price2
        assert type(result)           is Safe_Float__Money
        assert result                 == 16.49  # Should maintain precision
        assert type(str(result))      is str
        assert f"{result}"            == '16.49'             # Test that precision is maintained (Not 16.490000000000002)
        assert f"{float(result):.2f}" == '16.49'
        assert str(result)            == '16.49'

    def test__safe_float_money__string_representation(self):
        # Money with 2 decimal precision
        price = Safe_Float__Money(19.99)
        assert str(price) == "19.99"
        assert f"${price}" == "$19.99"
        assert repr(price) == "Safe_Float__Money(19.99)"

        # Money with rounding
        price_rounded = Safe_Float__Money(19.999)  # Should round to 19.99
        assert str(price_rounded) == "20.0"
        assert f"Total: ${price_rounded}" == "Total: $20.0"

        # Zero money
        zero = Safe_Float__Money(0.00)
        assert str(zero) == "0.0"
        assert f"${zero:.2f}" == "$0.00"


    def test__safe_float__arithmetic_preserves_representation(self):
        # After arithmetic, string representation should still work
        val1 = Safe_Float__Money(10.50)
        val2 = Safe_Float__Money(5.25)
        result = val1 + val2

        assert str(result) == "15.75"
        assert f"Total: ${result}" == "Total: $15.75"
        assert repr(result) == "Safe_Float__Money(15.75)"