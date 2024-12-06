from enum                                 import Enum
from unittest                             import TestCase
from typing                               import Optional, Union, List
from osbot_utils.helpers.Safe_Id          import Safe_Id
from osbot_utils.helpers.Random_Guid      import Random_Guid
from osbot_utils.helpers.Type_Safe_Method import Type_Safe_Method


class test_Type_Safe_Method(TestCase):

    def setUp(self):                                                                              # Setup test environment
        def example(self, param_a: Safe_Id,
                          param_b: Optional[Safe_Id],
                          param_c: Union[Safe_Id, Random_Guid],
                          param_d: List[Safe_Id],
                          param_e: Safe_Id = None):
            return True

        self.example_func    = example                                                           # Store test function
        self.type_checker    = Type_Safe_Method(example)                                         # Create type checker instance

    def test_handle_type_safety__valid_args(self):                                              # Test handling of valid arguments
        args     = ('self', Safe_Id('a'), None, Random_Guid(), [Safe_Id('d')], None)
        bound = self.type_checker.handle_type_safety(args=args, kwargs={})
        self.assertIsNotNone(bound)
        self.assertEqual(len(bound.arguments), 6)

    def test_handle_type_safety__invalid_args(self):                                            # Test handling of invalid arguments
        args = ('self', b'not_safe', None, Random_Guid(), [Safe_Id('d')], None)
        with self.assertRaises(ValueError) as context:
            self.type_checker.handle_type_safety(args=args, kwargs={})
        self.assertIn("expected type", str(context.exception))

    def test_bind_args(self):                                                                   # Test argument binding
        args   = ('self', Safe_Id('a'), None, Random_Guid(), [Safe_Id('d')], None)
        bound = self.type_checker.bind_args(args, {})
        self.assertTrue('self' in bound.arguments)
        self.assertEqual(len(bound.arguments), 6)

    def test_validate_parameter__valid(self):                                                   # Test valid parameter validation
        bound_args = self.type_checker.bind_args(
            ('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None), {})
        self.type_checker.validate_parameter('param_a', Safe_Id('test'), bound_args)            # Should not raise exception

    def test_validate_parameter__invalid(self):                                                 # Test invalid parameter validation
        bound_args = self.type_checker.bind_args(
            ('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None),
            {})
        with self.assertRaises(ValueError):
            self.type_checker.validate_parameter('param_a', b'invalid', bound_args)

    def test_check_parameter_value__valid_cases(self):                                             # Test parameter value checking
        cases = [('param_a', Safe_Id('test'), Safe_Id),                                            # Basic type
                 ('param_b', None, Optional[Safe_Id]),                                             # Optional type
                 ('param_c', Random_Guid(), Union[Safe_Id, Random_Guid]),                          # Union type
                 ('param_d', [Safe_Id('test')], List[Safe_Id]),                                    # List type
                 ('param_e', None, Safe_Id)                             ]                          # Default value type

        bound_args = self.type_checker.bind_args(('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None),{})
        for param_name, value, expected_type in cases:
            self.type_checker.check_parameter_value(param_name, value, expected_type, bound_args)

    def test_is_optional_type(self):                                                           # Test optional type detection
        self.assertTrue (self.type_checker.is_optional_type(Optional[Safe_Id]))                # Optional type
        self.assertFalse(self.type_checker.is_optional_type(Safe_Id))                         # Non-optional type

    def test_has_default_value(self):                                                          # Test default value detection
        self.assertTrue (self.type_checker.has_default_value('param_e'))                       # Has default
        self.assertFalse(self.type_checker.has_default_value('param_a'))                      # No default

    def test_validate_none_value(self):                                                        # Test None value validation
        self.type_checker.validate_none_value('param_b', True, False)                         # Optional parameter
        self.type_checker.validate_none_value('param_e', False, True)                         # Default value parameter

        with self.assertRaises(ValueError):                                                   # Non-optional parameter
            self.type_checker.validate_none_value('param_a', False, False)

    def test_is_list_type(self):                                                              # Test list type detection
        from typing import List
        self.assertTrue (self.type_checker.is_list_type(List))                                # List type
        self.assertTrue (self.type_checker.is_list_type(list))                                # Python list
        self.assertFalse(self.type_checker.is_list_type(Safe_Id))                            # Non-list type

    def test_validate_list_type(self):                                                        # Test list validation
        valid_list = [Safe_Id('test1'), Safe_Id('test2')]                                    # Valid list
        self.type_checker.validate_list_type('param_d', valid_list, List[Safe_Id])           # Should not raise

        invalid_list = [Safe_Id('test1'), 'not_safe']                                        # Invalid list
        with self.assertRaises(ValueError):
            self.type_checker.validate_list_type('param_d', invalid_list, List[Safe_Id])

        not_a_list = "not_a_list"                                                            # Not a list
        with self.assertRaises(ValueError):
            self.type_checker.validate_list_type('param_d', not_a_list, List[Safe_Id])

    def test_is_union_type(self):                                                            # Test union type detection
        self.assertTrue (self.type_checker.is_union_type(Union, False))                      # Union type
        self.assertFalse(self.type_checker.is_union_type(Union, True))                      # Optional type (Union with None)
        self.assertFalse(self.type_checker.is_union_type(Safe_Id, False))                   # Non-union type

    def test_validate_union_type(self):                                                      # Test union validation
        union_type = Union[Safe_Id, Random_Guid]
        self.type_checker.validate_union_type('param_c', Safe_Id('test'), union_type)       # Valid first type
        self.type_checker.validate_union_type('param_c', Random_Guid(), union_type)         # Valid second type

        with self.assertRaises(ValueError):
            self.type_checker.validate_union_type('param_c', 'invalid', union_type)         # Invalid type

    def test_try_basic_type_conversion(self):                                               # Test basic type conversion
        bound_args = self.type_checker.bind_args(('self', Safe_Id('test'), None, Random_Guid(), [Safe_Id('d')], None), {})

        # Try converting string to Safe_Id
        self.assertTrue(self.type_checker.try_basic_type_conversion(                        # Valid conversion
            'valid_id', Safe_Id, 'param_a', bound_args))

        self.assertFalse(self.type_checker.try_basic_type_conversion(                      # Invalid conversion
            [], Safe_Id, b'param_a', bound_args))

    def test_validate_direct_type(self):                                                   # Test direct type validation
        self.type_checker.validate_direct_type('param_a', Safe_Id('test'), Safe_Id)       # Valid type

        with self.assertRaises(ValueError):                                               # Invalid type
            self.type_checker.validate_direct_type('param_a', 'not_safe', Safe_Id)


    def test_try_basic_type_conversion_enum(self):                           # Test enum conversion
        class TestEnum(Enum):                                                # Define test enum
            TEST = 'test-value'                                             # With test value

        bound_args = self.type_checker.bind_args(                           # Create bound args
            ('self', Safe_Id('test'), None, Random_Guid(),
             [Safe_Id('d')], None), {})

        self.assertTrue(self.type_checker.try_basic_type_conversion(        # Test valid enum conversion
            TestEnum.TEST, Safe_Id, 'param_a', bound_args))

        self.assertEqual(                                                   # Verify converted value
            bound_args.arguments['param_a'],
            Safe_Id('test-value'))