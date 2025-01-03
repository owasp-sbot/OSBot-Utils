import sys

import pytest
from unittest                                   import TestCase
from typing                                     import Union, Optional, List
from dataclasses                                import dataclass
from osbot_utils.type_safe.Type_Safe         import Type_Safe
from osbot_utils.decorators.methods.type_safe   import type_safe
from osbot_utils.helpers.Safe_Id                import Safe_Id
from osbot_utils.helpers.Random_Guid            import Random_Guid

class test_type_safe(TestCase):

    def setUp(self):
        self.test_instance = TypeSafeTestClass()

    # Basic Type Safety Tests
    def test_basic_type_safety(self):
        # Valid cases
        assert self.test_instance.basic_method(Safe_Id("test"), 42) == "test-42"
        assert self.test_instance.basic_method("an_safe_id"   , 42) == "an_safe_id-42"
        assert self.test_instance.basic_method("made../..safe", 42) == "made_____safe-42"

        # Invalid cases
        with pytest.raises(ValueError, match="Parameter 'param' expected type <class 'osbot_utils.helpers.Safe_Id.Safe_Id'>, but got <class 'bytes'>"):
            self.test_instance.basic_method(b"not_safe_id", 42)
        with pytest.raises(ValueError, match="Parameter 'number' expected type <class 'int'>, but got <class 'str'>"):
            self.test_instance.basic_method(Safe_Id("test"), "not_int")


    # None Value Tests
    def test_none_value_handling(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
        # Test with optional parameters
        assert self.test_instance.optional_method(None) == "None"
        assert self.test_instance.optional_method(Safe_Id("test")) == "test"

        # Test with non-optional parameters
        with pytest.raises(ValueError, match="Parameter 'param' is not optional but got None"):
            self.test_instance.basic_method(None, 42)

    # Type Conversion Tests
    def test_type_conversion(self):
        # Test conversion from string to Safe_Id
        result = self.test_instance.convertible_method("valid_id")
        assert isinstance(result, Safe_Id)
        assert str(result) == "valid_id"

        # Test conversion from int to str
        assert self.test_instance.string_method     (42) == "42"
        assert self.test_instance.convertible_method(42) == "42"      # ints can be converted to strings and to Safe_Id
        # Test failed conversion
        with self.assertRaises(ValueError) as context:
            self.test_instance.convertible_method(b"123")  # Can't convert bytes to Safe_Id
        assert "expected type" in str(context.exception).lower()

    # Union Type Tests
    def test_union_types(self):
        # Test with Safe_Id
        assert self.test_instance.union_method(Safe_Id("test")) == "Safe_Id: test"

        # Test with Random_Guid
        guid = Random_Guid()
        assert self.test_instance.union_method(guid) == f"Random_Guid: {guid}"

        # Test with invalid type
        with self.assertRaises(ValueError) as context:
            self.test_instance.union_method(42)
        assert "expected one of types" in str(context.exception).lower()

    # Complex Type Tests
    def test_complex_types(self):
        # Test with valid complex type
        complex_obj = ComplexType(id="test", value=42)
        result = self.test_instance.complex_method(complex_obj)
        assert result == "test-42"

        # Test with invalid type
        with self.assertRaises(ValueError) as context:
            self.test_instance.complex_method({"id": "test", "value": 42})
        assert "expected type" in str(context.exception).lower()

    # Multiple Parameter Tests
    def test_multiple_parameters(self):
        # Test with all valid parameters
        result = self.test_instance.multi_param_method(
            Safe_Id("test"),
            42,
            Random_Guid(),
            "string"
        )
        assert result == "success"

        # Test with one invalid parameter
        with self.assertRaises(ValueError) as context:
            self.test_instance.multi_param_method(
                Safe_Id("test"),
                "not_int",
                Random_Guid(),
                "string"
            )
        assert "expected type" in str(context.exception).lower()

    # List Type Tests
    def test_list_types(self):
        # Test with valid list
        result = self.test_instance.list_method([Safe_Id("test1"), Safe_Id("test2")])
        assert len(result) == 2
        assert all(isinstance(x, Safe_Id) for x in result)

        # Test with invalid list contents
        with self.assertRaises(ValueError) as context:
            self.test_instance.list_method([Safe_Id("test"), "not_safe_id"])
        assert "expected type" in str(context.exception).lower()

    # Default Value Tests
    def test_default_values(self):
        # Test with default value
        assert self.test_instance.default_method() == "default"

        # Test with provided value
        assert self.test_instance.default_method(Safe_Id("custom")) == "custom"

    # Method Documentation Tests
    def test_method_documentation(self):
        # Verify that the decorator preserves docstrings
        assert "test method" in self.test_instance.documented_method.__doc__

        # Verify that the decorator preserves function signature
        import inspect
        sig = inspect.signature(self.test_instance.documented_method)
        assert 'param' in sig.parameters

# Test Support Classes

@dataclass
class ComplexType(Type_Safe):
    id: str
    value: int

class TypeSafeTestClass:
    @type_safe
    def basic_method(self, param: Safe_Id, number: int):
        #assert type(param) is Safe_Id
        return f"{param}-{number}"

    @type_safe
    def optional_method(self, param: Optional[Safe_Id]):
        return str(param)

    @type_safe
    def convertible_method(self, param: Safe_Id):
        return param

    @type_safe
    def string_method(self, param: str):
        return param

    @type_safe
    def union_method(self, param: Union[Safe_Id, Random_Guid]):
        if isinstance(param, Safe_Id):
            return f"Safe_Id: {param}"
        return f"Random_Guid: {param}"

    @type_safe
    def complex_method(self, param: ComplexType):
        return f"{param.id}-{param.value}"

    @type_safe
    def multi_param_method(self,
                          id: Safe_Id,
                          number: int,
                          guid: Random_Guid,
                          text: str):
        return "success"

    @type_safe
    def list_method(self, params: List[Safe_Id]):
        return params

    @type_safe
    def default_method(self, param: Safe_Id = Safe_Id("default")):
        return str(param)

    @type_safe
    def documented_method(self, param: Safe_Id):
        """A test method with documentation"""
        return str(param)