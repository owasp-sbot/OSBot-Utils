import re
import sys
import pytest
from unittest                                                                           import TestCase
from typing                                                                             import Union, Optional, List, Type, Callable, Any
from dataclasses                                                                        import dataclass
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash      import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name       import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now        import Timestamp_Now
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                       import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                   import Random_Guid
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class test__decorator__type_safe(TestCase):

    def setUp(self):
        self.test_instance = TypeSafeTestClass()

    # Basic Type Safety Tests
    def test_basic_type_safety(self):
        # Valid cases
        assert self.test_instance.basic_method(Safe_Id("test"         ), 42) == "test-42"
        assert self.test_instance.basic_method(Safe_Id("an_safe_id"   ), 42) == "an_safe_id-42"
        assert self.test_instance.basic_method(Safe_Id("made../..safe"), 42) == "made_____safe-42"

        # Invalid cases
        with pytest.raises(ValueError, match="Parameter 'param' expected type <class 'osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id.Safe_Id'>, but got <class 'bytes'>"):
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
        return

        # Test with non-optional parameters
        with pytest.raises(ValueError, match="Parameter 'param' is not optional but got None"):
            self.test_instance.basic_method(None, 42)

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

    def test__multiple_kwargs_variations(self):
        @type_safe
        def example_1(param_a: str, param_b: int):
            return dict(param_a=param_a, param_b=param_b)

        @type_safe
        def example_2(value: Safe_Id):
            return dict(value=value)

        @type_safe
        def example_3(value: Safe_Id, an_str: str= None):
            return dict(value=value, an_str=an_str)

        assert example_1('a', 1)                == {'param_a': 'a', 'param_b': 1}
        assert example_1('a', param_b=1)                 == {'param_a': 'a', 'param_b': 1}

        assert example_2(Safe_Id('test_1'))                      == {'value': 'test_1'}
        assert type(example_2(Safe_Id('test_2'))['value'])       is Safe_Id
        assert example_2(Safe_Id('test_3'))                      == {'value': 'test_3'}
        assert type(example_2(Safe_Id('test_3'))['value'])       is Safe_Id
        assert type(example_2(value=Safe_Id('test_3'))['value']) is Safe_Id

        assert example_3(Safe_Id('test_3'))                      == {'an_str': None, 'value': 'test_3'}
        assert type(example_3(Safe_Id('test_3'))['value'])       is Safe_Id
        assert type(example_3(value=Safe_Id('test_3'))['value']) is Safe_Id


    def test__fixed__type_safe_decorator__using_optional(self):                 # Test to verify that @type_safe correctly handles Optional[Type[T]] parameters and properly validates the type constraints when a value is provided.

        class StringClass(Type_Safe):
            value: str

        class IntClass(Type_Safe):
            value: int

        @type_safe
        def test_function(an_str           : str,
                          an_int           : int,
                          optional_str     : Optional[str]       = None,
                          optional_type    : Optional[type]      = None,
                          optional_type_str: Optional[Type[str]] = None,
                          optional_type_int: Optional[Type[int]] = None):
            return {
                'an_str': an_str,
                'an_int': an_int,
                'optional_str': optional_str,
                'optional_type': optional_type,
                'optional_type_str': optional_type_str,
                'optional_type_int': optional_type_int
            }

        # Test basic cases work
        result = test_function("answer", 42)
        assert result['an_str'] == "answer"
        assert result['an_int'] == 42

        # Test with keyword arguments
        result = test_function(an_str="answer", an_int=42)
        assert result['an_str'] == "answer"
        assert result['an_int'] == 42

        # # Test required parameter validation
        expected_error_1 = "Parameter 'an_int' expected type <class 'int'>, but got <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_1)):
            test_function(an_str="answer", an_int="not_an_int")

        # Test Optional[str] validation
        result = test_function(an_str="answer", an_int=42, optional_str="valid_string")
        assert result['optional_str'] == "valid_string"

        # Should raise error for wrong type in Optional[str]
        expected_error_2 = "Parameter 'optional_str' expected type"
        with pytest.raises(ValueError, match=expected_error_2):
            test_function(an_str="answer", an_int=42, optional_str=42.12)

        # Test Optional[type] validation
        result = test_function(an_str="answer", an_int=42, optional_type=TestCase)
        assert result['optional_type'] == TestCase

        # Should raise error for non-type in Optional[type]
        expected_error_3 = "Parameter 'optional_type' expected type <class 'type'>, but got <class 'str'>"
        with pytest.raises(ValueError, match=expected_error_3):
            test_function(an_str="answer", an_int=42, optional_type="not_a_type")


        # Test Optional[Type[str]] validation
        result = test_function(an_str="answer", an_int=42, optional_type_str=str)
        assert result['optional_type_str'] == str

        result = test_function(an_str="answer", an_int=42, optional_type_str=Safe_Id)
        assert result['optional_type_str'] == Safe_Id  # Safe_Id is subclass of str

        # Should raise error for Type[int] in Optional[Type[str]]
        expected_error_4 = "not a subclass of"
        with pytest.raises(ValueError, match=expected_error_4):
            test_function(an_str="answer", an_int=42, optional_type_str=int)

        # Should raise error for Timestamp_Now in Optional[Type[str]]
        with pytest.raises(ValueError, match=expected_error_4):
            test_function(an_str="answer", an_int=42, optional_type_str=Timestamp_Now)

        # Test Optional[Type[int]] validation
        result = test_function(an_str="answer", an_int=42, optional_type_int=int)
        assert result['optional_type_int'] == int

        result = test_function(an_str="answer", an_int=42, optional_type_int=Timestamp_Now)
        assert result['optional_type_int'] == Timestamp_Now  # Timestamp_Now is subclass of int

        # Should raise error for Type[str] in Optional[Type[int]]
        with pytest.raises(ValueError, match=expected_error_4):
            test_function(an_str="answer", an_int=42, optional_type_int=str)

        # Should raise error for Safe_Id in Optional[Type[int]]
        with pytest.raises(ValueError, match=expected_error_4):
            test_function(an_str="answer", an_int=42, optional_type_int=Safe_Id)

    def test_type_safe__detects_value_types(self):
        def test_list_1(xyz: List[str]):
            return xyz

        @type_safe
        def test_list_2(xyz: List[str]):
            return xyz

        assert test_list_1(['a', 'b', 123]) == ['a', 'b', 123]                  # normal python code will not pick up the bug

        expected_error = ("List item at index 2 expected type <class 'str'>, "
                          "but got <class 'int'>")
        with pytest.raises(ValueError, match=expected_error):                   # but Type_Safe's @type_safe will
            test_list_2(['a', 'b', 123])



    def test_type_safe_only_allows_immutable_assignments(self):
        @type_safe
        def an_method__with_only_immutable_vars          (an_str:str, an_int:int, an_bytes:bytes): pass
        @type_safe
        def an_method__with_immutable_vars_and_values    (an_str: str='str', an_int: int=42, an_bytes: bytes=b"bytes"): pass
        @type_safe
        def an_method__with_mutable_vars                 (an_list:list, an_dict:dict, an_set: set, an_tuple: tuple): pass
        @type_safe
        def an_method__with_immutable_classes            (obj_id:Obj_Id, safe_id: Safe_Id, safe_str: Safe_Str): pass
        @type_safe
        def an_method__with_immutable_classes_and_values (obj_id: Obj_Id=Obj_Id(), safe_id: Safe_Id = Safe_Id(), safe_str: Safe_Str=Safe_Str()): pass
        @type_safe
        def an_method__with_immutable_safe_str_and_values(safe_str_1: Safe_Str = Safe_Str(),
                                                          safe_str_2: Safe_Str = Safe_Str__File__Name("a.txt"),
                                                          safe_str_3: Safe_Str = Safe_Str__Hash     ("1234567890")): pass

        an_method__with_only_immutable_vars         ("str", 42, b"bytes")
        an_method__with_immutable_vars_and_values   ()
        an_method__with_mutable_vars                ([], {}, set(), tuple())
        an_method__with_immutable_classes           (Obj_Id(), Safe_Id(), Safe_Str())
        an_method__with_immutable_classes_and_values()
        an_method__with_immutable_safe_str_and_values()

    def test__type_safe__list_callable_param__type_checking(self):
        from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

        @type_safe
        def process_with_transforms(transformations: List[Callable[[Any], Any]]):
            pass

        # Valid callables - should pass
        def func1(x): return x
        def func2(x): return x * 2
        lambda_func = lambda x: x + 1

        process_with_transforms(transformations=[func1, func2])                       # Functions work
        process_with_transforms(transformations=[lambda_func])                        # Lambda works
        process_with_transforms(transformations=[func1, lambda_func, func2])         # Mix of functions and lambdas
        process_with_transforms(transformations=[])                                   # Empty list is valid
        process_with_transforms(transformations=[str.upper, str.lower])              # Built-in methods work
        process_with_transforms(transformations=[len, abs, round])                   # Built-in functions work

        # Type checking validation - should fail
        with pytest.raises(ValueError, match="List item at index 0 expected callable but got <class 'str'>"):
            process_with_transforms(transformations=["not_a_function"])              # String is not callable

        with pytest.raises(ValueError, match="List item at index 1 expected callable but got <class 'int'>"):
            process_with_transforms(transformations=[func1, 123])                    # Int is not callable

        with pytest.raises(ValueError, match="List item at index 0 expected callable but got <class 'dict'>"):
            process_with_transforms(transformations=[{"key": "value"}])              # Dict is not callable

        with pytest.raises(ValueError, match="List item at index 2 expected callable but got <class 'NoneType'>"):
            process_with_transforms(transformations=[func1, func2, None])            # None is not callable

        with pytest.raises(ValueError, match="Parameter 'transformations' expected a list but got <class 'function'>"):
            process_with_transforms(transformations=func1)                           # Single function not in list

        with pytest.raises(ValueError, match="Parameter 'transformations' expected a list but got <class 'str'>"):
            process_with_transforms(transformations="not_a_list")                    # String instead of list

        with pytest.raises(ValueError, match="Parameter 'transformations' expected a list but got <class 'dict'>"):
            process_with_transforms(transformations={})                              # Dict instead of list

        with pytest.raises(ValueError, match="Parameter 'transformations' is not optional but got None"):
            process_with_transforms(transformations=None)                            # None for non-optional param

        # Mixed valid and invalid items
        with pytest.raises(ValueError, match="List item at index 1 expected callable but got <class 'bool'>"):
            process_with_transforms(transformations=[func1, True, func2])            # Boolean is not callable

        with pytest.raises(ValueError, match="List item at index 3 expected callable but got <class 'list'>"):
            process_with_transforms(transformations=[func1, func2, lambda x: x, []])  # Nested list is not callable

        # Class instances with __call__ method should work
        class CallableClass:
            def __call__(self, x):
                return x * 2

        callable_instance = CallableClass()
        process_with_transforms(transformations=[callable_instance])                 # Callable class instance works
        process_with_transforms(transformations=[func1, callable_instance, func2])   # Mixed with functions

        # But non-callable class instances should fail
        class NonCallableClass:
            pass

        non_callable_instance = NonCallableClass()
        with pytest.raises(ValueError, match="List item at index 0 expected callable but got <class '.*NonCallableClass'>"):
            process_with_transforms(transformations=[non_callable_instance])         # Non-callable class instance fails


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