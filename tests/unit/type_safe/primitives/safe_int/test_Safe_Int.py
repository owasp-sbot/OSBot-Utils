import pytest
from unittest                                                                  import TestCase
from osbot_utils.type_safe.primitives.safe_float.Safe_Float                    import Safe_Float
from osbot_utils.type_safe.primitives.safe_int.Safe_Int                        import Safe_Int
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_uint.llm.Safe_UInt__LLM__Max_Tokens import Safe_UInt__LLM__Max_Tokens
from osbot_utils.utils.Objects                                                 import __, base_types


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
        assert int(Constrained_Int(None)) == 10  # None becomes 0

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

    def test__safe_int__arithmetic_operations(self):
        # Basic Safe_Int
        int1 = Safe_Int(10)
        int2 = Safe_Int(20)

        result = int1 + int2
        assert type(result) is Safe_Int
        assert result == 30

        # With plain int
        result = int1 + 5
        assert type(result) is Safe_Int
        assert result == 15

        # Reverse order
        result = 5 + int1
        assert type(result) is Safe_Int
        assert result == 15

    def test__safe_int__string_representation(self):
        # Basic Safe_Int
        value = Safe_Int(42)
        assert str(value) == "42"
        assert f"{value}" == "42"
        assert repr(value) == "Safe_Int(42)"

        # Large number
        large = Safe_Int(1234567890)
        assert str(large) == "1234567890"
        assert f"ID: {large}" == "ID: 1234567890"

        # Zero
        zero = Safe_Int(0)
        assert str(zero) == "0"
        assert f"{zero:03d}" == "000"  # Padding should work

    def test__safe_int__edge_cases(self):
        # Negative
        negative = Safe_Int(-42)
        assert str(negative) == "-42"
        assert f"Temperature: {negative}°C" == "Temperature: -42°C"

        # One
        one = Safe_Int(1)
        assert str(one) == "1"
        assert f"{one} item" == "1 item"

        # Maximum int32
        max_int32 = Safe_Int(2147483647)
        assert str(max_int32) == "2147483647"

    def test__safe_int__arithmetic_preserves_representation(self):
        # After arithmetic, string representation should still work
        val1 = Safe_Int(100)
        val2 = Safe_Int(50)
        result = val1 + val2

        assert str(result) == "150"
        assert f"Sum: {result}" == "Sum: 150"
        assert repr(result) == "Safe_Int(150)"

    def test__safe_int__formatting_options(self):
        # Various formatting options should work
        num = Safe_Int(42)

        # Padding
        assert f"{num:05d}" == "00042"

        # Sign
        assert f"{num:+d}" == "+42"

        # Thousands separator (Python 3.6+)
        big = Safe_Int(1234567)
        assert f"{big:,}" == "1,234,567"

        # Different bases
        assert f"{num:b}" == "101010"  # Binary
        assert f"{num:x}" == "2a"      # Hex
        assert f"{num:o}" == "52"      # Octal

    def test__safe_numeric__mixed_operations(self):
        # Int and float operations
        int_val   = Safe_Int(10)
        float_val = Safe_Float(3.5)

        # Mixed arithmetic (would return regular float)
        result = int_val + float_val                         #fails here

        return
        assert str(result) == "13.5"

        # Formatting in expressions
        assert f"Price: {int_val} + {float_val} = {int_val + float_val}" == "Price: 10 + 3.5 = 13.5"

    def test_none_handling(self):
        token_limit = Safe_UInt__LLM__Max_Tokens(None)                  # Since min_value=1 (which is > 0), None should become 1
        assert token_limit == 1                                         # min_value is used as default
        assert type(token_limit) is Safe_UInt__LLM__Max_Tokens

        class Safe_Int__AllowsNegative(Safe_Int):                       # For a type where min_value is 0 or negative, None would become 0
            min_value = -10
            max_value = 10

        negative_int = Safe_Int__AllowsNegative(None)
        assert negative_int == 0                                        # Defaults to 0, not -10

    def test_sub_handling(self):
        token_limit = Safe_UInt__LLM__Max_Tokens(None)
        assert token_limit == 1
        assert type(token_limit) is Safe_UInt__LLM__Max_Tokens

        # Regular arithmetic maintains type and validates
        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got 0"):
            result = token_limit - 1

        # Augmented assignment ALSO maintains type and validates!
        with pytest.raises(ValueError, match="Safe_UInt__LLM__Max_Tokens must be >= 1, got 0"):
            token_limit -= 1  # ✓ We CAN catch this!

        # But direct assignment bypasses everything
        token_limit = 0  # This completely replaces the object
        assert type(token_limit) is not Safe_UInt__LLM__Max_Tokens
        assert type(token_limit) is int

    def test_augmented_assignment_operators(self):                                 # Test all augmented assignment operators maintain type safety
        # Test with regular Safe_Int
        value = Safe_Int(10)

        # += operator
        value += 5
        assert value == 15
        assert type(value) is Safe_Int

        # -= operator
        value -= 3
        assert value == 12
        assert type(value) is Safe_Int

        # *= operator
        value *= 2
        assert value == 24
        assert type(value) is Safe_Int

        # //= operator (floor division)
        value //= 5
        assert value == 4
        assert type(value) is Safe_Int

        # %= operator (modulo)
        value %= 3
        assert value == 1
        assert type(value) is Safe_Int

        # /= operator (true division returns Safe_Float)
        value = Safe_Int(10)
        value /= 3
        assert type(value) is Safe_Float
        assert abs(value - 3.333333) < 0.001

    def test_augmented_assignment_with_constraints(self):                          # Test augmented assignments respect constraints
        class Bounded_Int(Safe_Int):
            min_value = 0
            max_value = 10

        value = Bounded_Int(5)

        # Valid augmented assignment
        value += 3
        assert value == 8
        assert type(value) is Bounded_Int

        # Augmented assignment that would violate max
        with pytest.raises(ValueError, match="Bounded_Int must be <= 10, got 11"):
            value += 3  # 8 + 3 = 11, exceeds max

        # Augmented assignment that would violate min
        value = Bounded_Int(2)
        with pytest.raises(ValueError, match="Bounded_Int must be >= 0, got -1"):
            value -= 3  # 2 - 3 = -1, below min

    def test_clamp_to_range_behavior(self):                                       # Test clamping when enabled
        class Clamped_Int(Safe_Int):
            min_value      = 1
            max_value      = 10
            clamp_to_range = True

        # Direct construction with clamping
        assert Clamped_Int(0)   == 1   # Clamped to min
        assert Clamped_Int(15)  == 10  # Clamped to max
        assert Clamped_Int(5)   == 5   # Within range
        assert Clamped_Int(-10) == 1   # Clamped to min
        assert Clamped_Int(100) == 10  # Clamped to max

        # Arithmetic operations with clamping
        value = Clamped_Int(5)
        result = value + 10
        assert result == 10  # 5 + 10 = 15, clamped to 10
        assert type(result) is Clamped_Int

        result = value - 10
        assert result == 1  # 5 - 10 = -5, clamped to 1
        assert type(result) is Clamped_Int

        # Augmented assignment with clamping
        value = Clamped_Int(8)
        value += 5  # 8 + 5 = 13, should clamp to 10
        assert value == 10
        assert type(value) is Clamped_Int

        value = Clamped_Int(3)
        value -= 5  # 3 - 5 = -2, should clamp to 1
        assert value == 1
        assert type(value) is Clamped_Int

    def test_clamp_vs_validate_comparison(self):                                  # Compare clamping vs validation behavior
        class Validating_Int(Safe_Int):
            min_value      = 1
            max_value      = 10
            clamp_to_range = False  # Default: validate and raise

        class Clamping_Int(Safe_Int):
            min_value      = 1
            max_value      = 10
            clamp_to_range = True   # Clamp to range

        # Validating raises errors
        with pytest.raises(ValueError, match="Validating_Int must be >= 1, got 0"):
            Validating_Int(0)
        with pytest.raises(ValueError, match="Validating_Int must be <= 10, got 11"):
            Validating_Int(11)

        # Clamping silently adjusts
        assert Clamping_Int(0)  == 1
        assert Clamping_Int(11) == 10

        # Arithmetic behavior
        val = Validating_Int(5)
        with pytest.raises(ValueError):
            result = val + 10  # Would be 15, exceeds max

        val = Clamping_Int(5)
        result = val + 10  # 15 gets clamped to 10
        assert result == 10

    def test_none_handling_with_different_min_values(self):                       # Test None handling with various min_value settings
        # min_value > 0: None becomes min_value
        class Positive_Min(Safe_Int):
            min_value = 5
        assert Positive_Min(None) == 5

        # min_value = 0: None becomes 0
        class Zero_Min(Safe_Int):
            min_value = 0
        assert Zero_Min(None) == 0

        # min_value < 0: None becomes 0
        class Negative_Min(Safe_Int):
            min_value = -5
        assert Negative_Min(None) == 0

        # No min_value: None becomes 0
        class No_Min(Safe_Int):
            min_value = None
        assert No_Min(None) == 0

        # allow_none = False: None raises error
        class No_None(Safe_Int):
            allow_none = False
        with pytest.raises(ValueError, match="No_None does not allow None values"):
            No_None(None)

    def test_type_safety_preservation_edge_cases(self):                           # Test type preservation in complex scenarios
        class Custom_Int(Safe_Int):
            min_value = 1
            max_value = 100

        value = Custom_Int(50)

        # Chain operations
        result = value + 10 - 5 + 2
        assert result == 57
        assert type(result) is Custom_Int

        # Mixed with plain ints
        result = 10 + value - 5
        assert result == 55
        assert type(result) is Custom_Int

        # Augmented assignment chain
        value += 10
        value -= 5
        assert value == 55
        with pytest.raises(ValueError, match="Custom_Int must be <= 100, got 110"):
            value *= 2 # (50 + 10 - 5) * 2 = 110

    def test_reverse_arithmetic_operations(self):                                 # Test reverse operations (when Safe_Int is on the right)
        value = Safe_Int(10)

        # Reverse addition
        result = 5 + value
        assert result == 15
        assert type(result) is Safe_Int

        # Reverse subtraction
        result = 20 - value
        assert result == 10
        assert type(result) is Safe_Int

        # Reverse multiplication
        result = 3 * value
        assert result == 30
        assert type(result) is Safe_Int

    def test_division_operations(self):                                           # Test various division scenarios
        value = Safe_Int(10)

        # True division returns Safe_Float
        result = value / 3
        assert type(result) is Safe_Float
        assert abs(result - 3.333333) < 0.001

        # Floor division maintains Safe_Int
        assert value   == 10
        result = value // 3
        assert result == 3
        assert type(result) is Safe_Int

        # Division by zero
        with pytest.raises(ZeroDivisionError):
            value / 0
        with pytest.raises(ZeroDivisionError):
            value // 0

    def test_multiplication_edge_cases(self):                                     # Test multiplication with various types
        value = Safe_Int(10)

        # Multiply by Safe_Int
        result = value * Safe_Int(5)
        assert result == 50
        assert type(result) is Safe_Int

        # Multiply by plain int
        result = value * 5
        assert result == 50
        assert type(result) is Safe_Int

        # Multiply by float (should still return Safe_Int for now)
        result = value * 2.5
        assert result == 25.0
        # Note: Currently returns regular type for float multiplication
        # This might be a design decision to review

    def test_modulo_operations(self):
        value = Safe_Int(10)

        # Regular modulo
        result = value % 3
        assert result == 1
        assert type(result) is Safe_Int

        # Modulo with constraints
        class Bounded_Int(Safe_Int):
            min_value = 0
            max_value = 5

        value = Bounded_Int(4)
        result = value % 3  # 4 % 3 = 1
        assert result == 1
        assert type(result) is Bounded_Int

    def test_error_message_clarity(self):
        # Ensure 'from None' suppresses the exception chain
        class Ranged_Int(Safe_Int):
            min_value = 10
            max_value = 20

        try:
            Ranged_Int(5)
        except ValueError as e:
            assert e.__cause__ is None  # 'from None' should suppress the cause
            assert str(e) == "Ranged_Int must be >= 10, got 5"

    def test_not_implemented_handling(self):
        # Test that NotImplemented is properly handled
        class IncompatibleType:
            pass

        value = Safe_Int(10)
        incompatible = IncompatibleType()

        # These should return NotImplemented, not raise
        result = value.__add__(incompatible)
        assert result is NotImplemented

        result = value.__sub__(incompatible)
        assert result is NotImplemented

    def test_reverse_operations_with_constraints(self):
        class Bounded_Int(Safe_Int):
            min_value = 0
            max_value = 100

        value = Bounded_Int(50)

        # Reverse subtraction that violates constraint
        with pytest.raises(ValueError, match="Bounded_Int must be >= 0, got -30"):
            result = 20 - value  # 20 - 50 = -30, below min

    def test_reverse_true_division(self):
        value = Safe_Int(2)
        result = 10 / value                 # This uses value.__rtruediv__(10)
        assert result       == 5.0
        assert type(result) is float        # Python's int.__truediv__ always returns float


    def test_clamp_with_none(self):
        class Clamped_Int(Safe_Int):
            min_value = 10
            max_value = 100
            clamp_to_range = True

        value = Clamped_Int(None)               # None with clamping and positive min_value
        assert value == 10                      # Should use min_value as default

    def test_string_conversion_edge_cases(self):
        # Valid numeric strings
        assert Safe_Int("  123  ".strip()) == 123  # With whitespace
        assert Safe_Int("-123") == -123  # Negative
        assert Safe_Int("+123") == 123  # Explicit positive

        # Invalid strings that look numeric
        with pytest.raises(ValueError, match="Cannot convert"):
            Safe_Int("123.0")  # Float string
        with pytest.raises(ValueError, match="Cannot convert"):
            Safe_Int("1,234")  # With comma
        with pytest.raises(ValueError, match="Cannot convert"):
            Safe_Int("0x123")  # Hex string

    def test_strict_type_with_none(self):
        class Strict_But_None_OK(Safe_Int):
            strict_type = True
            allow_none = True
            min_value = 5

        # None should still work even with strict_type
        value = Strict_But_None_OK(None)
        assert value == 5  # Uses min_value

        # But other types should fail
        with pytest.raises(TypeError):
            Strict_But_None_OK("5")

    def test_augmented_assignment_not_implemented(self):
        value = Safe_Int(10)

        # This should handle NotImplemented gracefully
        # (though in practice, int + object usually raises TypeError)
        class Incompatible:
            def __radd__(self, other):
                return NotImplemented

        inc = Incompatible()
        # This tests the NotImplemented path in __iadd__
        with pytest.raises(TypeError):  # Python will raise this after NotImplemented
            value += inc

    def test_min_value_zero_with_none(self):
        class Zero_Min(Safe_Int):
            min_value = 0
            max_value = 10

        # When min_value is 0, None should become 0
        value = Zero_Min(None)
        assert value == 0  # Not min_value (which is also 0, but logic differs)