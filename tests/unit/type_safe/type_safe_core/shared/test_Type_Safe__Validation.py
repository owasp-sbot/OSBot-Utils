import re
from enum import Enum, EnumMeta
from unittest                        import TestCase
from typing import Type, Literal, Optional, Union, get_args

import pytest

from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Validation import type_safe_validation


class SimpleClass:
    pass

class AnotherClass:
    pass

class DerivedClass(SimpleClass):
    pass

class test_Type_Safe__Validation(TestCase):

    def test_generic_type_annotation(self):                             # Test annotation with Type (no type parameter)

        class TestClass(Type_Safe):
            any_type: Type                                              # Generic Type annotation - should accept any type

        test_obj = TestClass()

        # These should work - assigning various types
        test_obj.any_type = str
        test_obj.any_type = int
        test_obj.any_type = SimpleClass
        test_obj.any_type = DerivedClass

        # These should fail - not type objects
        with self.assertRaises(ValueError):
            test_obj.any_type = "not a type"

        with self.assertRaises(ValueError):
            test_obj.any_type = 42

        with self.assertRaises(ValueError):
            test_obj.any_type = SimpleClass()

    def test_specific_type_annotation(self):                            # Test annotation with Type[T] - constrained to specific type"""

        class TestClass(Type_Safe):
            specific_type: Type[SimpleClass]                            # Only accepts SimpleClass or its subclasses

        test_obj = TestClass()

        # These should work - SimpleClass and its subclasses
        test_obj.specific_type = SimpleClass
        test_obj.specific_type = DerivedClass

        # These should fail - not SimpleClass or subclass
        with self.assertRaises(ValueError):
            test_obj.specific_type = str

        with self.assertRaises(ValueError):
            test_obj.specific_type = AnotherClass

        with self.assertRaises(ValueError):
            test_obj.specific_type = SimpleClass()  # Instance, not type

    def test_type_none_handling(self):                                  # Test handling of None with Type annotations"""

        class TestClass(Type_Safe):
            any_type: Type

        test_obj = TestClass()

        # Initial state should be None
        self.assertIsNone(test_obj.any_type)

        # Set to a valid type
        test_obj.any_type = str

        # Should not be able to set back to None after setting a value
        with self.assertRaises(ValueError):
            test_obj.any_type = None

    def test_literal_type_validation(self):
        from typing import Literal

        class Schema__Response_Format(Type_Safe):
            response_type: Literal["text", "json_object"     ] = "text"
            status       : Literal[200, 404, 500             ] = 200
            mode         : Literal["read", "write", "execute"] = "read"

        schema = Schema__Response_Format()                  # Test default values
        assert schema.response_type == "text"
        assert schema.status        == 200
        assert schema.mode          == "read"


        schema.response_type = "json_object"                # Test valid assignments
        assert schema.response_type == "json_object"

        schema.status = 404
        assert schema.status == 404

        schema.mode = "write"
        assert schema.mode == "write"

        # Test invalid assignments
        error_message_1 = "Invalid value for 'response_type': must be one of ['text', 'json_object'], got 'xml'"
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            schema.response_type = "xml"

        error_message_2 = "Invalid value for 'status': must be one of [200, 404, 500], got 201"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            schema.status = 201

        error_message_3 = "Invalid value for 'mode': must be one of ['read', 'write', 'execute'], got 'delete'"
        with pytest.raises(ValueError, match=re.escape(error_message_3)):
            schema.mode = "delete"

    def test_literal_with_single_value(self):
        from typing import Literal

        class Single_Literal(Type_Safe):
            constant: Literal["fixed"] = "fixed"

        single = Single_Literal()
        assert single.constant == "fixed"

        # Can only be set to the single allowed value
        single.constant = "fixed"  # Should work

        with pytest.raises(ValueError):
            single.constant = "other"

    def test_literal_mixed_types(self):
        from typing import Literal

        class Mixed_Literals(Type_Safe):
            mixed: Literal["string", 42, True, None] = "string"

        mixed = Mixed_Literals()

        # Test all valid values
        mixed.mixed = "string"
        assert mixed.mixed == "string"

        mixed.mixed = 42
        assert mixed.mixed == 42

        mixed.mixed = True
        assert mixed.mixed is True

        error_message = "Can't set None, to a variable that is already set. Invalid type for attribute 'mixed'. Expected 'typing.Literal['string', 42, True, None]' but got '<class 'NoneType'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            mixed.mixed = None
        assert mixed.mixed is True                      # value was not changed

        # Test invalid values
        with pytest.raises(ValueError):
            mixed.mixed = "other"

        with pytest.raises(ValueError):
            mixed.mixed = 43

        with pytest.raises(ValueError):
            mixed.mixed = False

    def test_literal_with_optional(self):

        class Optional_Literal(Type_Safe):
            maybe_format: Optional[Literal["json", "xml"]] = None

        opt = Optional_Literal()
        assert opt.maybe_format is None
        error_message = "Invalid type for attribute 'maybe_format'. Expected 'typing.Optional[typing.Literal['json', 'xml']]' but got '<class 'str'>"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            opt.maybe_format = "json"
        #assert opt.maybe_format == "json"

        opt.maybe_format = None  # Should be allowed
        assert opt.maybe_format is None

        with pytest.raises(ValueError):
            opt.maybe_format = "yaml"

    def test_literal_json_serialization(self):
        from typing import Literal

        class Literal_Schema(Type_Safe):
            format_type: Literal["text", "json"] = "text"
            code: Literal[200, 404] = 200

        schema = Literal_Schema(format_type="json", code=404)

        # Test serialization
        json_data = schema.json()
        assert json_data == {"format_type": "json", "code": 404}

        # Test deserialization
        restored = Literal_Schema.from_json(json_data)
        assert restored.format_type == "json"
        assert restored.code == 404

        # Test invalid deserialization
        invalid_json = {"format_type": "xml", "code": 200}
        with pytest.raises(ValueError):
            Literal_Schema.from_json(invalid_json)

    def test_literal_in_nested_structures(self):
        from typing import Literal, List, Dict

        class Nested_Literals(Type_Safe):
            items  : List[Literal["a", "b", "c"]]
            mapping: Dict[str, Literal[1, 2, 3]]

        nested = Nested_Literals()

        # Valid list operations
        nested.items.append("a")
        nested.items.append("b")
        assert nested.items == ["a", "b"]

        # Invalid list append
        error_message_1 = "Literal value must be one of 'a', 'b', 'c', got 'd'"
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            nested.items.append("d")

        # Valid dict operations
        nested.mapping["key1"] = 1
        nested.mapping["key2"] = 3
        assert nested.mapping == {"key1": 1, "key2": 3}

        # Invalid dict assignment
        error_message_2 = "Literal value must be one of 1, 2, 3, got 4"
        with pytest.raises(ValueError, match=error_message_2):
            nested.mapping["key3"] = 4


    def test_validate_type_immutability_comprehensive(self):

        # Test 1: Variables in IMMUTABLE_TYPES should pass
        type_safe_validation.validate_type_immutability("test_int"      , int)
        type_safe_validation.validate_type_immutability("test_str"      , str)
        type_safe_validation.validate_type_immutability("test_bool"     , bool)
        type_safe_validation.validate_type_immutability("test_float"    , float)
        type_safe_validation.validate_type_immutability("test_bytes"    , bytes)
        type_safe_validation.validate_type_immutability("test_complex"  , complex)
        type_safe_validation.validate_type_immutability("test_type"     , type)

        # Test 2: Variables starting with '__' should always pass
        type_safe_validation.validate_type_immutability("__private_list", list)  # mutable but allowed
        type_safe_validation.validate_type_immutability("__private_dict", dict)  # mutable but allowed

        # Test 3: Literal types with immutable values should pass
        type_safe_validation.validate_type_immutability("literal_str", Literal["a", "b"])
        type_safe_validation.validate_type_immutability("literal_int", Literal[1, 2, 3])
        type_safe_validation.validate_type_immutability("literal_mixed", Literal["text", 42, None, True])

        # Test 4: Literal types with mutable values should fail
        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("bad_literal", Literal[[1, 2]])                         # noqa

        # Test 5: Union/Optional types with immutable components should pass
        type_safe_validation.validate_type_immutability("optional_int", Optional[int])
        type_safe_validation.validate_type_immutability("optional_str", Optional[str])
        type_safe_validation.validate_type_immutability("union_immutable", Union[int, str])
        type_safe_validation.validate_type_immutability("union_with_none", Optional[Union[int, str]])

        # Test 6: Union types with mutable components should fail
        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("union_mutable", Union[list, dict])

        # Test 7: Enum types should pass
        class TestEnum(Enum):
            VALUE1 = "v1"
            VALUE2 = "v2"

        type_safe_validation.validate_type_immutability("enum_type", TestEnum)

        # Test 8: Subclasses of int, str, float should pass
        class CustomInt(int):
            pass

        class CustomStr(str):
            pass

        class CustomFloat(float):
            pass

        type_safe_validation.validate_type_immutability("custom_int", CustomInt)
        type_safe_validation.validate_type_immutability("custom_str", CustomStr)
        type_safe_validation.validate_type_immutability("custom_float", CustomFloat)

        # Test 9: Regular mutable types should fail
        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("list_type", list)

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("dict_type", dict)

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("set_type", set)

        # Test 10: Custom classes (not subclassing immutable types) should fail
        class CustomClass:
            pass

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("custom_class", CustomClass)

        # Test 11: type(var_type) in IMMUTABLE_TYPES check
        # This handles cases where the type of the type itself is immutable
        # For example, EnumMeta is in IMMUTABLE_TYPES
        assert type(TestEnum) is EnumMeta
        type_safe_validation.validate_type_immutability("enum_check", TestEnum)

        # Test 12: Edge case - None type
        import types
        type_safe_validation.validate_type_immutability("none_type", types.NoneType)

        # Test 13: Nested Union/Optional combinations
        type_safe_validation.validate_type_immutability("nested_union", Optional[Union[int, str, bool]])

        # Test 14: Variable names not starting with '__' but containing '__'
        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("has__double", list)  # should fail

    def test_python_literal_edge_cases_that_should_fail_but_dont(self):
        """
        Demonstrates problematic Python behavior where Literal accepts mutable values
        that IDEs correctly flag as errors but Python runtime allows.

        These are all INVALID uses of Literal that Python doesn't catch at runtime.
        """

        # Edge case 1: Lists in Literals (IDE shows error, Python allows it)
        BadLiteral1 = Literal[[1, 2, 3]]        # PyCharm: "Expected type 'None', got 'list[int]' instead"      # noqa
        literal_args = get_args(BadLiteral1)
        assert literal_args == ([1, 2, 3],)     # Python accepts this!
        assert type(literal_args[0]) is list    # It's actually a list

        # Edge case 2: Dictionaries in Literals (IDE error, Python allows)
        BadLiteral2 = Literal[{"key": "value"}]  # PyCharm shows error                                          # noqa
        literal_args = get_args(BadLiteral2)
        assert literal_args == ({"key": "value"},)
        assert type(literal_args[0]) is dict

        # Edge case 3: Sets in Literals (IDE error, Python allows)
        BadLiteral3 = Literal[{1, 2, 3}]  # PyCharm shows error                                                 # noqa
        literal_args = get_args(BadLiteral3)
        assert literal_args == ({1, 2, 3},)
        assert type(literal_args[0]) is set

        # Edge case 4: The comparison problem - each list is a different object
        BadLiteral4 = Literal[[1, 2]]                                                                           # noqa
        list1 = [1, 2]
        list2 = [1, 2]
        assert list1 == list2  # Values are equal
        assert list1 is not list2  # But they're different objects!
        # This means Literal[[1,2]] comparison would be unreliable

        # Edge case 5: Mutable objects can be modified after Literal creation
        mutable_list = [1, 2, 3]
        BadLiteral5 = Literal[mutable_list]  # IDE error, Python allows                                         # noqa
        mutable_list.append(4)  # We can modify the list!
        literal_args = get_args(BadLiteral5)
        assert literal_args[0] == [1, 2, 3, 4]  # The Literal's value changed!

        # Edge case 6: Custom objects in Literals
        class CustomClass:
            def __init__(self, value):
                self.value = value

        obj = CustomClass(42)
        BadLiteral6 = Literal[obj]  # IDE error, Python allows                                                  # noqa
        literal_args = get_args(BadLiteral6)
        assert literal_args == (obj,)
        assert isinstance(literal_args[0], CustomClass)

        # THIS IS WHY Type_Safe's validate_type_immutability is important!
        # It catches these at runtime, which Python doesn't do
        from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Validation import type_safe_validation

        # Type_Safe correctly rejects all these bad Literals
        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("bad1", BadLiteral1)

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("bad2", BadLiteral2)

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("bad3", BadLiteral3)

        with pytest.raises(ValueError, match="which is not supported by Type_Safe"):
            type_safe_validation.validate_type_immutability("bad6", BadLiteral6)

        # Demonstrate the right way with Type_Safe
        GoodLiteral = Literal["text", "json", 42, True, None]  # Only immutable values
        type_safe_validation.validate_type_immutability("good", GoodLiteral)  # This passes!

    def test__bug__type_safe__literal_optional_assignment(self):
        class An_Class_1(Type_Safe):
            an_optional_literal: Optional[Literal["allow", "deny"]] = None  # Data collection preference

        error_messsage__1 = "Invalid type for attribute 'an_optional_literal'. Expected 'typing.Optional[typing.Literal['allow', 'deny']]' but got '<class 'str'>"
        with pytest.raises(ValueError, match=re.escape(error_messsage__1)):
            An_Class_1(an_optional_literal='allow')                              # BUG

        class An_Class_2(Type_Safe):
            an_literal: Literal["allow", "deny"] = None  # Data collection preference

        An_Class_2(an_literal='allow')                                          # works as expected