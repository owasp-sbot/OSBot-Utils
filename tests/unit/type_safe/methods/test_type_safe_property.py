import re
import pytest
from unittest                                         import TestCase
from typing                                           import Optional, Dict
from osbot_utils.type_safe.Type_Safe                  import Type_Safe
from osbot_utils.type_safe.methods.type_safe_property import type_safe_property


class test_Type_Safe__Property(TestCase):

    def setUp(self):                                                                    # Initialize test data
        class NestedData(Type_Safe):
            name   : str
            age    : int
            active : bool
            tags   : Optional[Dict[str, str]]

        class InnerClass(Type_Safe):
            data: NestedData

        class TestClass(Type_Safe):
            inner: InnerClass

            name    = type_safe_property('inner.data', 'name'  , str )
            age     = type_safe_property('inner.data', 'age'   , int )
            active  = type_safe_property('inner.data', 'active', bool)
            tags    = type_safe_property('inner.data', 'tags'  , dict)

        self.NestedData = NestedData
        self.InnerClass = InnerClass
        self.TestClass = TestClass

    def test_basic_property_access(self):                                              # Tests basic getter and setter functionality
        test_obj = self.TestClass()
        test_obj.inner = self.InnerClass()
        test_obj.inner.data = self.NestedData()

        test_obj.name = "test"
        assert test_obj.name == "test"
        assert test_obj.inner.data.name == "test"

        test_obj.age = 25
        assert test_obj.age == 25
        assert test_obj.inner.data.age == 25

    def test_type_validation(self):                                                    # Tests type safety validation
        test_obj            = self.TestClass()
        test_obj.inner      = self.InnerClass()
        test_obj.inner.data = self.NestedData()

        # Test valid assignments
        test_obj.name   = "valid"
        test_obj.age    = 30
        test_obj.active = True
        test_obj.tags   = {"key": "value"}

        # Test invalid assignments
        with self.assertRaises(TypeError) as context:
            test_obj.name = 123
        assert "Cannot set property 'name' with value of type <class 'int'>, expected <class 'str'>" in str(context.exception)

        with self.assertRaises(TypeError) as context:
            test_obj.age = "not an int"
        assert "Cannot set property 'age' with value of type <class 'str'>, expected <class 'int'>" in str(context.exception)

        with self.assertRaises(TypeError) as context:
            test_obj.active = "not a bool"
        assert "Cannot set property 'active' with value of type <class 'str'>, expected <class 'bool'>" in str(context.exception)

    def test_none_values(self):                                                        # Tests handling of None values
        test_obj            = self.TestClass()
        test_obj.inner      = self.InnerClass()
        test_obj.inner.data = self.NestedData()

        # Test setting None on optional field
        test_obj.tags        = None
        assert test_obj.tags is None

        # Test setting None on required field
        with pytest.raises(ValueError, match=re.escape("Can't set None, to a variable that is already set. Invalid type for attribute 'name'. Expected '<class 'str'>' but got '<class 'NoneType'>'")):
            test_obj.name = None


    def test_invalid_paths(self):  # Tests error handling for invalid paths
        class Data_Class(Type_Safe):
            pass

        class Inner_Class(Type_Safe):
            data: Data_Class

        class Bad_Class(Type_Safe):
            inner: Inner_Class

            bad_path   = type_safe_property('wrong.path'    , 'name'   , str)            # property with non-existent path
            bad_start  = type_safe_property('missing.data'  , 'name'   , str)            # property with invalid first part
            bad_middle = type_safe_property('inner.missing' , 'name'   , str)            # property with invalid second part
            bad_end    = type_safe_property('inner.data'    , 'missing', str)            # property with invalid final attribute

        test_obj = Bad_Class()

        with pytest.raises(AttributeError, match="'Bad_Class' object has no attribute 'wrong'"):
            test_obj.bad_path = "test"

        with pytest.raises(AttributeError, match="'Bad_Class' object has no attribute 'missing'"):
            test_obj.bad_start = "test"

        with pytest.raises(AttributeError, match="'Inner_Class' object has no attribute 'missing'"):
            test_obj.bad_middle = "test"

        with pytest.raises(AttributeError, match="Target path 'inner.data' does not have an attribute 'missing'"):
            test_obj.bad_end = "test"


    def test_property_isolation(self):                                                 # Tests property isolation between instances
        obj1 = self.TestClass()
        obj1.inner = self.InnerClass()
        obj1.inner.data = self.NestedData()

        obj2 = self.TestClass()
        obj2.inner = self.InnerClass()
        obj2.inner.data = self.NestedData()

        obj1.name = "obj1"
        obj2.name = "obj2"

        assert obj1.name == "obj1"
        assert obj2.name == "obj2"

    def test_inheritance(self):                                                        # Tests inheritance behavior
        class ChildClass(self.TestClass):
            extra = type_safe_property('inner.data', 'tags', dict)

        child = ChildClass()
        child.inner = self.InnerClass()
        child.inner.data = self.NestedData()

        # Test inherited property
        child.name = "test"
        assert child.name == "test"

        # Test new property
        child.extra = {"new": "value"}
        assert child.extra == {"new": "value"}

        # Verify parent class properties still work
        parent = self.TestClass()
        parent.inner = self.InnerClass()
        parent.inner.data = self.NestedData()
        parent.name = "parent"
        assert parent.name == "parent"

    def test_edge_cases(self):                                                        # Tests edge cases and boundary conditions
        test_obj = self.TestClass()
        test_obj.inner = self.InnerClass()
        test_obj.inner.data = self.NestedData()

        # Test empty string
        test_obj.name = ""
        assert test_obj.name == ""

        # Test zero
        test_obj.age = 0
        assert test_obj.age == 0

        # Test empty dict
        test_obj.tags = {}
        assert test_obj.tags == {}