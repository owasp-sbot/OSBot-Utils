from inspect import BoundArguments

import pytest
from enum                                                               import Enum
from unittest                                                           import TestCase
from typing                                                             import Optional, Union, List, Dict, Any, Type, Callable

from osbot_utils.type_safe.primitives.safe_int import Safe_Int
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id      import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid  import Random_Guid
from osbot_utils.type_safe.type_safe_core.methods.Type_Safe__Method     import Type_Safe__Method
from osbot_utils.utils.Dev import pprint


class TestEnum(Enum):                                                                    # Test enum for conversion tests
    VALUE1    = "test-value-1"
    VALUE2    = "test-value-2"
    INT_VALUE = 42


class CustomType:                                                                        # Custom type for testing
    def __init__(self, value):
        self.value = value


class BaseClass: pass                                                                    # Base class for inheritance testing


class DerivedClass(BaseClass): pass                                                      # Derived class for inheritance testing


class test_Type_Safe__Method(TestCase):

    def setUp(self):                                                                     # Setup test environment
        def example(self, param_a : Safe_Id                    ,
                          param_b : Optional[Safe_Id]          ,
                          param_c : Union[Safe_Id, Random_Guid],
                          param_d : List[Safe_Id]              ,
                          param_e : Safe_Id            = None
                   ) -> bool:
            return True

        self.example_func = example
        self.type_checker = Type_Safe__Method(example)

    # Test check_for_any_use method
    def test_check_for_any_use__with_lowercase_any(self):                              # Test detection of lowercase 'any' usage
        def bad_func(param: any):                                                       # Using lowercase any
            pass

        checker = Type_Safe__Method(bad_func)

        with self.assertRaises(ValueError) as context:
            checker.check_for_any_use()

        assert "uses lowercase 'any' instead of 'Any'"      in str(context.exception)
        assert "Please use 'from typing import Any'"        in str(context.exception)

    def test_check_for_any_use__with_uppercase_Any(self):                              # Test that uppercase Any doesn't raise error
        def good_func(param: Any):
            pass

        checker = Type_Safe__Method(good_func)
        checker.check_for_any_use()                                                    # Should not raise

    # Test validate_immutable_parameter method
    def test_validate_immutable_parameter__with_mutable_default(self):
        def func_with_mutable_default(param_list: List[str]      = [],
                                      param_dict: Dict[str, int] = {}
                                 ) -> None:
            pass

        checker = Type_Safe__Method(func_with_mutable_default)
        bound_args = checker.bind_args((), {})  # This will use the default values

        # Get the actual default-bound arguments
        param_list_val = bound_args.arguments['param_list']
        param_dict_val = bound_args.arguments['param_dict']

        # These are the *default* values, so now your is-check will match
        with self.assertRaises(ValueError) as context:
            checker.validate_immutable_parameter('param_list', param_list_val)
        assert "mutable default value of type 'list'" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            checker.validate_immutable_parameter('param_dict', param_dict_val)
        assert "mutable default value of type 'dict'" in str(context.exception)

    def test_validate_immutable_parameter__with_immutable_defaults(self):               # Test validation passes for immutable defaults
        def func_with_immutable_defaults(param_str  : str               = "default",
                                        param_int  : int               = 42       ,
                                        param_none : Optional[str]     = None
                                       ) -> None:
            pass

        checker    = Type_Safe__Method(func_with_immutable_defaults)
        bound_args = checker.bind_args((), {})

        # These should not raise
        checker.validate_immutable_parameter('param_str' , "default")
        checker.validate_immutable_parameter('param_int' , 42       )
        checker.validate_immutable_parameter('param_none', None     )

    # Test Type[T] validation
    def test_validate_type_parameter__valid_cases(self):                                # Test Type[T] parameter validation with valid cases
        def func_with_type_params(base_type : Type[BaseClass],
                                 any_type  : type
                                ) -> None:
            pass

        checker = Type_Safe__Method(func_with_type_params)

        # Valid: exact type
        checker.validate_type_parameter('base_type', BaseClass   , Type[BaseClass])

        # Valid: derived type
        checker.validate_type_parameter('base_type', DerivedClass, Type[BaseClass])

        # Valid: any type when no constraint
        checker.validate_type_parameter('any_type' , str         , type          )

    def test_validate_type_parameter__invalid_cases(self):                              # Test Type[T] parameter validation with invalid cases
        def func_with_type_params(base_type: Type[BaseClass]) -> None:
            pass

        checker = Type_Safe__Method(func_with_type_params)

        # Invalid: not a type
        with self.assertRaises(ValueError) as context:
            checker.validate_type_parameter('base_type', "not a type", Type[BaseClass])
        assert "expected a type class but got" in str(context.exception)

        # Invalid: wrong type hierarchy
        with self.assertRaises(ValueError) as context:
            checker.validate_type_parameter('base_type', str, Type[BaseClass])
        assert "which is not a subclass of" in str(context.exception)

    # Test Dict validation
    def test_validate_direct_type__dict_validation(self):                               # Test Dict type validation
        def func_with_dict(data: Dict[str, int]) -> None:
            pass

        checker = Type_Safe__Method(func_with_dict)

        # Valid dict
        valid_dict = {"key1": 1, "key2": 2}
        result     = checker.validate_direct_type('data', valid_dict, Dict[str, int])
        assert result is True

        # Invalid: not a dict
        with self.assertRaises(ValueError) as context:
            checker.validate_direct_type('data', [1, 2, 3], Dict[str, int])
        assert "expected dict but got" in str(context.exception)

        # Invalid: wrong key type
        with self.assertRaises(ValueError) as context:
            checker.validate_direct_type('data', {1: 1}, Dict[str, int])
        assert "Dict key '1' expected type" in str(context.exception)

        # Invalid: wrong value type
        with self.assertRaises(ValueError) as context:
            checker.validate_direct_type('data', {"key": "value"}, Dict[str, int])
        assert "Dict value for key 'key' expected type" in str(context.exception)

    # Test Any type handling
    def test_validate_direct_type__any_type(self):                                      # Test that Any type accepts anything
        def func_with_any(param: Any) -> None:
            pass

        checker = Type_Safe__Method(func_with_any)

        # All these should pass
        assert checker.validate_direct_type('param', 42       , Any) is True
        assert checker.validate_direct_type('param', "string" , Any) is True
        assert checker.validate_direct_type('param', [1, 2, 3], Any) is True
        assert checker.validate_direct_type('param', None     , Any) is True

    # Test Optional with Type[T]
    def test_check_parameter_value__optional_type_parameter(self):                      # Test Optional[Type[T]] handling
        def func_with_optional_type(param: Optional[Type[BaseClass]]=None) -> None:
            pass

        checker    = Type_Safe__Method(func_with_optional_type)
        bound_args = checker.bind_args((), {})

        # Valid: None for optional
        checker.check_parameter_value('param', None        , Optional[Type[BaseClass]], bound_args)

        # Valid: actual type
        checker.check_parameter_value('param', BaseClass   , Optional[Type[BaseClass]], bound_args)

        # Valid: derived type
        checker.check_parameter_value('param', DerivedClass, Optional[Type[BaseClass]], bound_args)

    # Test complex Union validation
    def test_validate_union_type__complex_unions(self):                                 # Test validation of complex Union types
        def func_with_unions(simple  : Union[int, str]                       ,
                            complex : Union[List[int], Dict[str, str], None]
                           ) -> None:
            pass

        checker = Type_Safe__Method(func_with_unions)

        # Simple union - valid cases
        checker.validate_union_type('simple', 42    , Union[int, str])
        checker.validate_union_type('simple', "test", Union[int, str])

        # Simple union - invalid case
        with self.assertRaises(ValueError) as context:
            checker.validate_union_type('simple', 3.14, Union[int, str])
        assert "expected one of types" in str(context.exception)

    # Test enum conversion edge cases
    def test_try_basic_type_conversion__enum_edge_cases(self):                          # Test enum conversion edge cases
        bound_args = self.type_checker.bind_args(
            ('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None), {})

        # Test enum to string conversion
        result = self.type_checker.try_basic_type_conversion(
            TestEnum.VALUE1, str, 'param', bound_args)
        assert result                           is True
        assert bound_args.arguments['param']    == "test-value-1"

        # Test enum with non-string expected type
        result = self.type_checker.try_basic_type_conversion(
            TestEnum.INT_VALUE, int, 'param', bound_args)
        assert result is False                                                          # Should not convert

        # Test failed enum conversion
        class NonStringEnum(Enum):
            VALUE = 123

        # This should handle exception and return False
        result = self.type_checker.try_basic_type_conversion(
            NonStringEnum.VALUE, list, 'param', bound_args)
        assert result is False

    # Test edge cases in type conversion
    def test_try_basic_type_conversion__edge_cases(self):                               # Test edge cases in basic type conversion
        bound_args = self.type_checker.bind_args(
            ('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None), {})

        # Test int to str conversion
        result = self.type_checker.try_basic_type_conversion(
            42, str, 'param', bound_args)
        assert result                         is True
        assert bound_args.arguments['param']  == "42"

        # Test str to int conversion
        result = self.type_checker.try_basic_type_conversion(
            "123", int, 'param', bound_args)
        assert result                         is True
        assert bound_args.arguments['param']  == 123

        # Test failed conversion (exception handling)
        result = self.type_checker.try_basic_type_conversion(
            "not_a_number", int, 'param', bound_args)
        assert result is False

        # Test with non-convertible type
        result = self.type_checker.try_basic_type_conversion(
            3.14, Safe_Id, 'param', bound_args)
        assert result is False                                                          # float not in [int, str]

    # Test None handling in validate_direct_type
    def test_validate_direct_type__none_handling(self):                                 # Test None handling in direct type validation
        # Test with optional parameter
        def func_optional(param: Optional[str]=None) -> None:
            pass

        checker = Type_Safe__Method(func_optional)
        # Should handle None for optional
        checker.validate_direct_type('param', None, Optional[str])

        # Test with non-optional parameter that has default
        def func_with_default(param: str = "default") -> None:
            pass

        checker = Type_Safe__Method(func_with_default)
        # Should handle None when has default
        checker.validate_direct_type('param', None, str)

    # Test list validation edge cases
    def test_validate_list_type__empty_list(self):                                      # Test list validation with empty list
        empty_list = []
        # Should pass for empty list
        self.type_checker.validate_list_type('param_d', empty_list, List[Safe_Id])

    def test_validate_list_type__nested_validation_error(self):                         # Test detailed error reporting for list items
        mixed_list = [Safe_Id('valid'), 'invalid', Safe_Id('valid2')]

        with self.assertRaises(ValueError) as context:
            self.type_checker.validate_list_type('param_d', mixed_list, List[Safe_Id])

        # Should indicate which index failed
        assert "List item at index 1" in str(context.exception)

    # Test parameter validation without annotation
    def test_validate_parameter__no_annotation(self):                                   # Test parameter validation when no annotation exists
        def func_no_annotation(param):
            pass

        checker    = Type_Safe__Method(func_no_annotation)
        bound_args = checker.bind_args(("test",), {})

        # Should not raise when no annotation
        checker.validate_parameter('param', "any_value", bound_args)

    # Test complex nested types
    def test_check_parameter_value__nested_optional_lists__raises_not_implemented_error(self):                        # Test deeply nested optional types
        def func_nested(param: List[str]=None) -> None:
            pass

        checker    = Type_Safe__Method(func_nested)
        bound_args = checker.bind_args((), {})

        # Valid: None for outer optional
        checker.check_parameter_value('param', None, Optional[List[Optional[str]]], bound_args)

        # Not Valid: list with mixed None and strings should not work
        expected_error = "List item at index 1 expected type <class 'str'>, but got <class 'NoneType'>"
        with pytest.raises(ValueError, match=expected_error) as context:
            checker.check_parameter_value('param', ["test", None, "test2"],List[str], bound_args) # todo: document this edge case (and see if we need to add support for it)

    # Test Union return in validate_direct_type
    def test_validate_direct_type__union_early_return(self):                            # Test that Union types return early in validate_direct_type
        # This tests the branch where origin is Union
        result = self.type_checker.validate_direct_type('param', "test", Union[str, int])
        assert result is True

    # Test complete flow with all parameter types
    def test_handle_type_safety__comprehensive(self):                                   # Test complete type safety handling with various parameter types
        def comprehensive_func(required_str : str                               ,
                               optional_int : Optional[int]   = None            ,
                               union_param  : Union[str, int, float] = 0        ,
                               list_param   : List[str]              = None     ,
                               dict_param   : Dict[str, Any]         = None     ,
                               type_param   : Type[BaseClass]        = BaseClass,
                               any_param    : Any                    = "anything"
                          ) -> None:
            pass

        checker = Type_Safe__Method(comprehensive_func)

        # Test with all valid arguments
        args   = ("test",)
        kwargs = { 'optional_int': 42          ,
                   'union_param' : 3.14        ,
                   'list_param'  : ["a", "b"]  ,
                   'dict_param'  : {"key": "value"},
                   'type_param'  : DerivedClass,
                   'any_param'   : [1, 2, 3]   }

        bound_args = checker.handle_type_safety(args, kwargs)
        assert bound_args.arguments['required_str'] == "test"
        assert bound_args.arguments['optional_int'] == 42

    # Test error messages are descriptive
    def test_error_messages_clarity(self):                                              # Test that error messages provide clear information
        def func(param: List[int]) -> None:
            pass

        checker = Type_Safe__Method(func)

        # Test various error scenarios for message clarity
        with self.assertRaises(ValueError) as context:
            checker.validate_list_type('param', "not a list", List[int])
        assert "expected a list but got <class 'str'>" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            checker.validate_list_type('param', ["valid", 123, "invalid"], List[int])
        assert "List item at index 0 expected type <class 'int'>, but got <class 'str'>" in str(context.exception)

    # Additional edge case tests for 100% coverage
    def test_check_parameter_value__type_origin(self):                                  # Test check_parameter_value with Type origin
        def func_with_type(param: Type[str]=None) -> None:
            pass

        checker    = Type_Safe__Method(func_with_type)
        bound_args = checker.bind_args((), {})

        # This should trigger the Type origin branch
        checker.check_parameter_value('param', str, Type[str], bound_args)

        # Test with invalid type
        with self.assertRaises(ValueError):
            checker.check_parameter_value('param', "not a type", Type[str], bound_args)

    def test_validate_direct_type__generic_origin_fallthrough(self):                    # Test generic type with origin that's not dict/Dict
        from typing import Set

        def func_with_set(param: Set[int]) -> None:
            pass

        checker = Type_Safe__Method(func_with_set)

        # Valid set
        valid_set = {1, 2, 3}
        result    = checker.validate_direct_type('param', valid_set, Set[int])
        assert result is True

        # Invalid: not a set
        with self.assertRaises(ValueError) as context:
            checker.validate_direct_type('param', [1, 2, 3], Set[int])
        assert "expected type" in str(context.exception)

    def test_function_without_annotations(self):                                        # Test function with no annotations at all
        def no_annotations_func(a, b, c):
            pass

        checker    = Type_Safe__Method(no_annotations_func)
        args       = (1, "test", [1, 2, 3])

        # Should handle gracefully without annotations
        bound_args = checker.handle_type_safety(args, {})
        assert len(bound_args.arguments) == 3

    def test_validate_parameter__custom_object_not_used_as_default(self):               # Test immutable validation when custom object passed (not default)
        class CustomDefault:
            pass

        def func_with_custom(param: CustomDefault = None) -> None:
            pass

        checker    = Type_Safe__Method(func_with_custom)
        bound_args = checker.bind_args((CustomDefault(),), {})

        # Should not raise because it's not using the default
        custom_instance = CustomDefault()
        checker.validate_immutable_parameter('param', custom_instance)

    def test_optional_with_non_type_origin(self):                                       # Test Optional type that doesn't have Type as origin
        def func_optional_list(param: Optional[List[str]]=None) -> None:
            pass

        checker    = Type_Safe__Method(func_optional_list)
        bound_args = checker.bind_args((), {})

        # Should recursively check the list type
        checker.check_parameter_value('param', ["test"], Optional[List[str]], bound_args)

        # Invalid list content
        with self.assertRaises(ValueError):
            checker.check_parameter_value('param', [123], Optional[List[str]], bound_args)

    def test_validate_type_parameter__forward_ref_handling(self):                       # Test Type parameter with forward reference or special attributes
        from typing import ForwardRef

        # Create a type with __origin__ attribute
        class TypeWithOrigin:
            __origin__ = str

        # This should handle types with __origin__ attribute
        checker = Type_Safe__Method(lambda x: Type[TypeWithOrigin])

        # Test the branch where required_base has __origin__
        with self.assertRaises(ValueError):
            checker.validate_type_parameter('param', int, Type[TypeWithOrigin])

    def test_kwargs_only_function(self):                                                # Test function with keyword-only arguments
        def kwargs_func(*, required : str         ,
                           optional : int = 10
                       ) -> None:
            pass

        checker = Type_Safe__Method(kwargs_func)

        # Valid kwargs
        bound_args = checker.handle_type_safety((), {'required': 'test', 'optional': 20})
        assert bound_args.arguments['required'] == 'test'
        assert bound_args.arguments['optional'] == 20

        # Invalid type for required
        with self.assertRaises(ValueError):
            checker.handle_type_safety((), {'required': 123})

    def test_mixed_args_kwargs(self):                                                   # Test function with mix of positional and keyword arguments
        def mixed_func(pos1 : str       ,
                      pos2 : int       ,
                      *                ,
                      kw1  : float     ,
                      kw2  : bool = True
                     ) -> None:
            pass

        checker = Type_Safe__Method(mixed_func)

        # Valid mixed arguments
        bound_args = checker.handle_type_safety(
            ("test", 42),
            {'kw1': 3.14, 'kw2': False}
        )
        assert bound_args.arguments['pos1'] == "test"
        assert bound_args.arguments['kw1']  == 3.14

    def test_varargs_and_kwargs(self):                                                  # Test function with *args and **kwargs
        def varargs_func(normal : str     ,
                         *args  : int     ,
                         **kwargs : str
                    ) -> None:
            pass

        checker = Type_Safe__Method(varargs_func)

        expected_error = "Parameter 'args' expected type <class 'int'>, but got <class 'tuple'>"
        with pytest.raises(ValueError, match=expected_error):
            checker.handle_type_safety(("test", 1, 2, 3), {'key': 'value'})


    def test_recursive_optional_handling(self):                                         # Test deeply nested Optional handling
        def func_deep_optional(param: Optional[Optional[str]]=None) -> None:
            # Note: Optional[Optional[T]] is equivalent to Optional[T]
            pass

        checker    = Type_Safe__Method(func_deep_optional)
        bound_args = checker.bind_args((), {})

        # All these should be valid
        checker.check_parameter_value('param', None  , Optional[Optional[str]], bound_args)
        checker.check_parameter_value('param', "test", Optional[Optional[str]], bound_args)

    def test_empty_union(self):                                                         # Test edge case with empty Union (if possible)
        # Union requires at least 2 types, so we test minimum case
        def func_min_union(param: Union[str, int]) -> None:
            pass

        checker = Type_Safe__Method(func_min_union)

        # Should validate both types
        checker.validate_union_type('param', "test", Union[str, int])
        checker.validate_union_type('param', 42    , Union[str, int])

    def test_validate_direct_type__type_error_chain(self):                              # Test that ValueError is raised without a chain
        def func(param: str) -> None:
            pass

        checker = Type_Safe__Method(func)

        # The 'from None' in the code suppresses exception chaining
        with self.assertRaises(ValueError) as context:
            checker.validate_direct_type('param', 123, str)

        # Verify no exception chain
        assert context.exception.__cause__ is None

    def test_class_method_validation(self):                                             # Test validation with class methods
        class MyClass:
            @classmethod
            def class_method(cls, param: str) -> None:
                pass

            @staticmethod
            def static_method(param: int) -> None:
                pass

        # Test class method
        checker    = Type_Safe__Method(MyClass.class_method)
        bound_args = checker.handle_type_safety(("test",), {})
        assert bound_args.arguments['param'] == "test"

        # Test static method
        checker    = Type_Safe__Method(MyClass.static_method)
        bound_args = checker.handle_type_safety((42,), {})
        assert bound_args.arguments['param'] == 42

    def test_regression__data_processing_pipeline__checks_not_implemented_error(self):                                             # Test validation for data processing functions
        def process_data(data            : List[Dict[str, Union[str, int, float]]],
                         transformations : List[Callable[[Any], Any]]        ,
                         options         : Dict[str, Any]                    ,
                         output_format   : str                        = "json"
                    ) -> List[Dict[str, Any]]:                                        # Process data through transformation pipeline
            result = data
            for transform in transformations:
                result = [transform(item) for item in result]
            return result

        checker = Type_Safe__Method(process_data)

        # Define transformations
        def uppercase_strings(item):
            return {k: v.upper() if isinstance(v, str) else v
                   for k, v in item.items()}

        def multiply_numbers(item):
            return {k: v * 2 if isinstance(v, (int, float)) else v
                   for k, v in item.items()}

        # Valid pipeline
        test_data = [ {"name": "alice", "score": 10, "rate": 0.5},
                      {"name": "bob"  , "score": 20, "rate": 0.8}]

        # expected_error = "Validation for list items with subscripted type 'typing.Callable[[typing.Any], typing.Any]' is not yet supported in parameter 'transformations'."
        # with pytest.raises(NotImplementedError, match=re.escape(expected_error)):
        #     checker.handle_type_safety((test_data, [uppercase_strings, multiply_numbers], {"debug": True}),{})      # BUG: should be handled
        bound_args = checker.handle_type_safety((test_data, [uppercase_strings, multiply_numbers], {"debug": True}), {})         # FIXED: doesn't raise exception

        result = process_data(**bound_args.arguments)
        assert result == [{'name': 'ALICE', 'rate': 1.0, 'score': 20},
                          {'name': 'BOB'  , 'rate': 1.6, 'score': 40}]


    def test_convert_primitive_parameters(self):

        def test_func(path       : Safe_Str__File__Path,                    # Create a real function with Type_Safe__Primitive parameters
                      count      : Safe_Int            ,
                      name       : Safe_Str            ,
                      regular_str: str                 ,
                      regular_int: int                 ):
            return path, count, name, regular_str, regular_int

        method = Type_Safe__Method(test_func)

        # Create real bound_args using the actual binding
        bound_args = method.bind_args(args   = ()                       ,
                                      kwargs = { 'path': '/tmp/test.txt',        # str that should convert to Safe_Str__File__Path
                                                 'count': '42'          ,        # str that should convert to Safe_Int
                                                 'name': 'test_name'    ,        # str that should convert to Safe_Str
                                                 'regular_str': 'normal',        # str that should stay str
                                                 'regular_int': 100     })       # int that should stay int


        assert type(bound_args) is BoundArguments
        assert bound_args.arguments == { 'count'      : '42'            ,
                                         'name'       : 'test_name'     ,
                                         'path'       : '/tmp/test.txt' ,
                                         'regular_int': 100             ,
                                         'regular_str': 'normal'        }

        assert type(bound_args.arguments['path']) is str                                    # Store original types for comparison
        assert type(bound_args.arguments['count']) is str
        assert type(bound_args.arguments['name']) is str


        method.convert_primitive_parameters(bound_args)                                     # Run conversion


        assert type(bound_args.arguments['path']) is Safe_Str__File__Path                   # Check conversions happened
        assert bound_args.arguments['path'] == '/tmp/test.txt'


        assert type(bound_args.arguments['count']) is Safe_Int
        assert bound_args.arguments['count']       == 42

        assert type(bound_args.arguments['name']) is Safe_Str
        assert bound_args.arguments['name'] == 'test_name'

        # Regular types should not be converted
        assert type(bound_args.arguments['regular_str']) is str
        assert bound_args.arguments['regular_str'] == 'normal'

        assert type(bound_args.arguments['regular_int']) is int
        assert bound_args.arguments['regular_int'] == 100

        # Test with invalid conversion (should silently fail and let validation handle it)
        def test_func_invalid(value: Safe_Int):
            return value

        method_invalid = Type_Safe__Method(test_func_invalid)
        bound_args_invalid = method_invalid.bind_args(args=(), kwargs={'value': 'not_a_number'})

        # This should not raise during conversion
        method_invalid.convert_primitive_parameters(bound_args_invalid)

        # Value should remain unchanged since conversion failed
        assert bound_args_invalid.arguments['value'] == 'not_a_number'
        assert type(bound_args_invalid.arguments['value']) is str

    def test_handle_type_safety(self):

        # Test successful conversion and validation
        def good_func(path: Safe_Str__File__Path, count: Safe_Int):
            return path, count

        method = Type_Safe__Method(good_func)

        # Test with valid inputs that need conversion
        bound_args = method.handle_type_safety(
            args=(),
            kwargs={'path': '/tmp/file.txt', 'count': '100'}
        )

        # Check conversions happened
        assert type(bound_args.arguments['path']) is Safe_Str__File__Path
        assert bound_args.arguments['path'] == '/tmp/file.txt'
        assert type(bound_args.arguments['count']) is Safe_Int
        assert bound_args.arguments['count'] == 100

        # Test with invalid type that can't be converted
        def strict_func(value: Safe_Int):
            return value

        method_strict = Type_Safe__Method(strict_func)

        # This should raise because dict can't convert to Safe_Int
        with pytest.raises(ValueError, match="Parameter 'value' expected type"):
            method_strict.handle_type_safety(args=(), kwargs={'value': {'key': 'value'}})

        # Test with optional parameters
        def optional_func(value: Safe_Int = 10):
            return value

        method_optional = Type_Safe__Method(optional_func)

        # Should use default when not provided
        bound_args = method_optional.handle_type_safety(args=(), kwargs={})
        assert bound_args.arguments['value'] == 10

        # Should convert when provided
        bound_args = method_optional.handle_type_safety(args=(), kwargs={'value': '20'})
        assert type(bound_args.arguments['value']) is Safe_Int
        assert bound_args.arguments['value'] == 20

        # Test with mixed types
        def mixed_func(safe_path: Safe_Str__File__Path, regular_str: str, safe_int: Safe_Int, regular_int: int):
            return safe_path, regular_str, safe_int, regular_int

        method_mixed = Type_Safe__Method(mixed_func)
        bound_args = method_mixed.handle_type_safety(
            args=(),
            kwargs={
                'safe_path': 'path.txt',     # Should convert
                'regular_str': 'text',        # Should stay str
                'safe_int': '42',            # Should convert
                'regular_int': 99            # Should stay int
            }
        )

        assert type(bound_args.arguments['safe_path']) is Safe_Str__File__Path
        assert type(bound_args.arguments['regular_str']) is str
        assert type(bound_args.arguments['safe_int']) is Safe_Int
        assert type(bound_args.arguments['regular_int']) is int