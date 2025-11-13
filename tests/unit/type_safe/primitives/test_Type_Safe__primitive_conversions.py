import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                               import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_Int                                 import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_Str                                 import Safe_Str
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__IP_Address import Safe_Str__IP_Address
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                      import type_safe


class test_Type_Safe__primitive_conversions(TestCase):
    """Comprehensive tests for Type_Safe__Primitive subclass conversions"""

    # ===== Safe_Float Conversions =====

    def test__safe_float__to__custom_safe_float__in_type_safe_init(self):
        """Test Safe_Float → Custom_Safe_Float conversion in Type_Safe.__init__"""

        class Custom_Safe_Float(Safe_Float):
            min_value = 0.0
            max_value = 1.0

        class An_Class(Type_Safe):
            value: Custom_Safe_Float

        # Test conversion from Safe_Float
        obj = An_Class(value=Safe_Float(0.5))
        assert type(obj.value) is Custom_Safe_Float
        assert obj.value == 0.5

        # Test conversion from primitive float
        obj = An_Class(value=0.7)
        assert type(obj.value) is Custom_Safe_Float
        assert obj.value == 0.7

        # Test conversion from primitive int
        obj = An_Class(value=1)
        assert type(obj.value) is Custom_Safe_Float
        assert obj.value == 1.0

    def test__safe_float__to__custom_safe_float__with_type_safe_decorator(self):
        """Test Safe_Float → Custom_Safe_Float conversion in @type_safe methods"""

        class Custom_Safe_Float(Safe_Float):
            min_value = 0.0
            max_value = 100.0

        @type_safe
        def process_value(value: Custom_Safe_Float) -> Custom_Safe_Float:
            return value

        # Test conversion from Safe_Float
        result = process_value(Safe_Float(50.0))
        assert type(result) is Custom_Safe_Float
        assert result == 50.0

        # Test conversion from primitive
        result = process_value(75.5)
        assert type(result) is Custom_Safe_Float
        assert result == 75.5

    def test__safe_float__to__custom_safe_float__validation_still_works(self):
        """Test that validation constraints are enforced during conversion"""

        class Bounded_Float(Safe_Float):
            min_value = 0.0
            max_value = 1.0

        class An_Class(Type_Safe):
            value: Bounded_Float

        # Should work within bounds
        obj = An_Class(value=Safe_Float(0.5))
        assert obj.value == 0.5

        # Should fail outside bounds
        with pytest.raises(ValueError, match="must be <= 1.0"):
            An_Class(value=Safe_Float(1.5))

        with pytest.raises(ValueError, match="must be >= 0.0"):
            An_Class(value=Safe_Float(-0.5))

    def test__safe_float__multiple_inheritance_levels(self):
        """Test conversion through multiple inheritance levels"""

        class Base_Float(Safe_Float):
            min_value = 0.0

        class Percentage_Float(Base_Float):
            max_value = 100.0

        class An_Class(Type_Safe):
            percentage: Percentage_Float

        # Test conversion from base Safe_Float
        obj = An_Class(percentage=Safe_Float(50.0))
        assert type(obj.percentage) is Percentage_Float
        assert obj.percentage == 50.0

        # Test conversion from intermediate class
        obj = An_Class(percentage=Base_Float(75.0))
        assert type(obj.percentage) is Percentage_Float
        assert obj.percentage == 75.0

    # ===== Safe_Int Conversions =====

    def test__safe_int__to__custom_safe_int__in_type_safe_init(self):
        """Test Safe_Int → Custom_Safe_Int conversion in Type_Safe.__init__"""

        class Custom_Safe_Int(Safe_Int):
            min_value = 0
            max_value = 100

        class An_Class(Type_Safe):
            count: Custom_Safe_Int

        # Test conversion from Safe_Int
        obj = An_Class(count=Safe_Int(42))
        assert type(obj.count) is Custom_Safe_Int
        assert obj.count == 42

        # Test conversion from primitive int
        obj = An_Class(count=75)
        assert type(obj.count) is Custom_Safe_Int
        assert obj.count == 75

    def test__safe_int__to__custom_safe_int__with_type_safe_decorator(self):
        """Test Safe_Int → Custom_Safe_Int conversion in @type_safe methods"""

        class Positive_Int(Safe_Int):
            min_value = 1

        @type_safe
        def increment(value: Positive_Int) -> Positive_Int:
            return Positive_Int(int(value) + 1)

        # Test conversion from Safe_Int
        result = increment(Safe_Int(5))
        assert type(result) is Positive_Int
        assert result == 6

        # Test conversion from primitive
        result = increment(10)
        assert type(result) is Positive_Int
        assert result == 11

    def test__safe_int__to__custom_safe_int__validation_still_works(self):
        """Test that validation constraints are enforced during conversion"""

        class Age_Int(Safe_Int):
            min_value = 0
            max_value = 150

        class Person(Type_Safe):
            age: Age_Int

        # Should work within bounds
        person = Person(age=Safe_Int(25))
        assert person.age == 25

        # Should fail outside bounds
        with pytest.raises(ValueError, match="must be <= 150"):
            Person(age=Safe_Int(200))

        with pytest.raises(ValueError, match="must be >= 0"):
            Person(age=Safe_Int(-5))

    # ===== Safe_Str Conversions =====

    def test__safe_str__to__custom_safe_str__in_type_safe_init(self):
        """Test Safe_Str → Custom_Safe_Str conversion in Type_Safe.__init__"""

        class Custom_Safe_Str(Safe_Str):
            max_length = 50

        class An_Class(Type_Safe):
            text: Custom_Safe_Str

        # Test conversion from Safe_Str
        obj = An_Class(text=Safe_Str("hello"))
        assert type(obj.text) is Custom_Safe_Str
        assert obj.text == "hello"

        # Test conversion from primitive str
        obj = An_Class(text="world")
        assert type(obj.text) is Custom_Safe_Str
        assert obj.text == "world"

    def test__safe_str__to__custom_safe_str__with_type_safe_decorator(self):
        """Test Safe_Str → Custom_Safe_Str conversion in @type_safe methods"""

        class Username(Safe_Str):
            max_length = 20
            to_lower_case = True

        @type_safe
        def format_username(name: Username) -> Username:
            return name

        # Test conversion from Safe_Str
        result = format_username(Safe_Str("Alice"))
        assert type(result) is Username
        assert result == "alice"  # lowercase transformation applied

        # Test conversion from primitive
        result = format_username("BOB")
        assert type(result) is Username
        assert result == "bob"

    def test__safe_str__to__custom_safe_str__validation_still_works(self):
        """Test that validation constraints are enforced during conversion"""

        class Short_Str(Safe_Str):
            max_length = 10

        class An_Class(Type_Safe):
            name: Short_Str

        # Should work within bounds
        obj = An_Class(name=Safe_Str("hello"))
        assert obj.name == "hello"

        # Should fail when too long
        with pytest.raises(ValueError, match="exceeds maximum length"):
            An_Class(name=Safe_Str("this_is_too_long"))

    # ===== Cross-Type Tests =====

    def test__multiple_primitive_types__in_same_class(self):
        """Test multiple different Type_Safe__Primitive conversions in one class"""

        class Custom_Float(Safe_Float):
            min_value = 0.0
            max_value = 1.0

        class Custom_Int(Safe_Int):
            min_value = 0
            max_value = 100

        class Custom_Str(Safe_Str):
            max_length = 20

        class Mixed_Class(Type_Safe):
            score: Custom_Float
            count: Custom_Int
            label: Custom_Str

        # Test all conversions work together
        obj = Mixed_Class(
            score=Safe_Float(0.85),
            count=Safe_Int(42),
            label=Safe_Str("test")
        )

        assert type(obj.score) is Custom_Float
        assert type(obj.count) is Custom_Int
        assert type(obj.label) is Custom_Str
        assert obj.score == 0.85
        assert obj.count == 42
        assert obj.label == "test"

    def test__incompatible_primitive_types__still_fail(self):
        """Test that incompatible conversions still raise errors"""

        class Float_Value(Safe_Float):
            pass

        class Int_Value(Safe_Int):
            pass

        class An_Class(Type_Safe):
            float_val: Float_Value
            int_val: Int_Value

        # Float → Int should fail (different primitive bases)
        error_message_1 = "Int_Value requires an integer value, got Safe_Float"
        with pytest.raises(TypeError, match=error_message_1):
            An_Class(int_val=Safe_Float(5.5))

        error_message_2 = "Cannot convert '0.0.0.0' to float"
        with pytest.raises(ValueError, match=error_message_2):
            An_Class(float_val=Safe_Str__IP_Address("0.0.0.0"))

    # ===== Type_Safe method parameter tests =====

    def test__type_safe_decorator__with_multiple_custom_primitives(self):
        """Test @type_safe with multiple custom primitive parameters"""

        class Score(Safe_Float):
            min_value = 0.0
            max_value = 100.0

        class Count(Safe_Int):
            min_value = 0

        class Label(Safe_Str):
            max_length = 50

        @type_safe
        def process_data(score: Score, count: Count, label: Label) -> dict:
            return {
                'score': float(score),
                'count': int(count),
                'label': str(label)
            }

        # Test all conversions work in decorated method
        result = process_data(
            score=Safe_Float(95.5),
            count=Safe_Int(10),
            label=Safe_Str("test_label")
        )

        assert result == {
            'score': 95.5,
            'count': 10,
            'label': 'test_label'
        }

    def test__type_safe_class_with_nested_custom_primitives(self):
        """Test nested Type_Safe classes with custom primitives"""

        class Temperature(Safe_Float):
            min_value = -273.15  # Absolute zero

        class Measurement(Type_Safe):
            temp: Temperature

        class Experiment(Type_Safe):
            measurement: Measurement

        # Test nested conversion
        exp = Experiment(measurement=Measurement(temp=Safe_Float(25.0)))
        assert type(exp.measurement.temp) is Temperature
        assert exp.measurement.temp == 25.0

    # ===== Edge Cases =====

    def test__none_values__preserved_correctly(self):
        """Test that None values are handled correctly in conversions"""

        class Custom_Float(Safe_Float):
            allow_none = True

        class An_Class(Type_Safe):
            value: Custom_Float = None

        # Test None is preserved
        obj = An_Class()
        assert obj.value is None

        # Test explicit None
        obj = An_Class(value=None)
        assert obj.value is None

        # Test conversion still works
        obj = An_Class(value=Safe_Float(5.0))
        assert type(obj.value) is Custom_Float
        assert obj.value == 5.0

    def test__decimal_precision__preserved_in_conversion(self):
        """Test that decimal precision is maintained during conversion"""

        class Precise_Float(Safe_Float):
            decimal_places = 3
            use_decimal = True

        class An_Class(Type_Safe):
            value: Precise_Float

        # Test precision from Safe_Float
        obj = An_Class(value=Safe_Float(0.12345))
        assert type(obj.value) is Precise_Float
        assert str(obj.value) == "0.123"  # Rounded to 3 decimal places

    def test__from_json__with_custom_primitives(self):
        """Test that from_json works with custom primitive conversions"""

        class Score(Safe_Float):
            min_value = 0.0
            max_value = 100.0

        class An_Class(Type_Safe):
            score: Score

        # Test from_json with primitive value
        obj = An_Class.from_json({'score': 85.5})
        assert type(obj.score) is Score
        assert obj.score == 85.5

        # Test round-trip
        json_data = obj.json()
        obj2 = An_Class.from_json(json_data)
        assert type(obj2.score) is Score
        assert obj2.score == 85.5

    def test__json_roundtrip__preserves_custom_primitive_types(self):
        """Test that json() → from_json() preserves custom primitive types"""

        class Custom_Float(Safe_Float):
            decimal_places = 2

        class Custom_Int(Safe_Int):
            min_value = 0

        class Custom_Str(Safe_Str):
            to_lower_case = True

        class An_Class(Type_Safe):
            f_val: Custom_Float
            i_val: Custom_Int
            s_val: Custom_Str

        # Create with primitive types
        obj1 = An_Class(
            f_val=Safe_Float(3.14159),
            i_val=Safe_Int(42),
            s_val=Safe_Str("HELLO")
        )

        # Round-trip through JSON
        json_data = obj1.json()
        obj2 = An_Class.from_json(json_data)

        # Verify types are preserved
        assert type(obj2.f_val) is Custom_Float
        assert type(obj2.i_val) is Custom_Int
        assert type(obj2.s_val) is Custom_Str

        # Verify values (with transformations applied)
        assert str(obj2.f_val) == "3.14"  # Rounded to 2 decimal places
        assert obj2.i_val == 42
        assert obj2.s_val == "hello"  # Lowercased