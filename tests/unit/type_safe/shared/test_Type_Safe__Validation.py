from unittest import TestCase
from typing import Type
from osbot_utils.type_safe.Type_Safe import Type_Safe

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