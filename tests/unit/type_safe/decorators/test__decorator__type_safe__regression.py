import re
import pytest
from typing                                     import Any, Dict, Optional, Type
from unittest                                   import TestCase
from osbot_utils.helpers.Safe_Id                import Safe_Id
from osbot_utils.helpers.Timestamp_Now          import Timestamp_Now
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe import type_safe

class test_decorator__type_safe__regression(TestCase):

    def test__regression__type_safe__not_detecting_mutable_assignment(self):
        @type_safe
        def an_method(an_list: list = ['a', 'b', 'c']):         # FIXED: BUG should detect
            return an_list
        expected_error = ("Parameter 'an_list' has a mutable default value of type 'list'. "
                          "Only immutable types are allowed as default values in type_safe functions.")
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            an_method()                                                     # FIXED: this now raises the exception

        ### the commended code below, shows the test before the fix, which is also a good example of the problems
        ###     (and subtle bugs) that can occur when allowing mutable values to be assigned in methods parameters
        #
        # result_1 = an_method()                                  # BUG: first call an_list is created
        # assert result_1 == ['a', 'b', 'c']                      # confirmed here
        # result_1.append('d')                                    # BUG: but adding a value to the returned list
        # result_2 = an_method()                                  # BUG: will exist in the an_list value inside the an_method
        # assert result_2 == ['a', 'b', 'c', 'd']                 # BUG: confirmed here
        #
        # result_3 = an_method(['f'])                             # assigning a new list object
        # assert result_3 == ['f']                                # is the one now used

    def test_regression__on_type_safe__decorator_check(self):
        @type_safe
        def an_function(target:Type[Type_Safe]):
            pass

        @type_safe
        def an_function_lowercase_type(target: type[Type_Safe]):
            pass

        class An_Class(Type_Safe):
            an_str: str

        an_function(An_Class)  # OK
        expected_error_1 = "Parameter 'target' expected type typing.Type[osbot_utils.type_safe.Type_Safe.Type_Safe], but got builtins.str which is not a subclass of <class 'osbot_utils.type_safe.Type_Safe.Type_Safe'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_1)):
            an_function(str)  # FIXED: BUG should have raised exception since str is not a subclass of Type_Safe

        expected_error_2 = "Parameter 'target' expected a type class but got <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            an_function("an str")

        an_function_lowercase_type(An_Class)                # OK

        expected_error_3 = "Parameter 'target' expected type type[osbot_utils.type_safe.Type_Safe.Type_Safe], but got builtins.str which is not a subclass of <class 'osbot_utils.type_safe.Type_Safe.Type_Safe'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_3)):
            an_function_lowercase_type(str     )                # FIXED: BUG should had raise exceptions
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            an_function_lowercase_type("an str")                # FIXED: BUG should had raise exceptions

    def test__regression__type_safe_decorator_not_validating_type_parameter(self):
        # Test that identifies a bug in @type_safe decorator when validating
        # Type[Type_Safe] parameters. The decorator should reject any type that
        # is not a subclass of Type_Safe, but it currently allows any type.
        # Define test classes
        class Base_Type_Safe(Type_Safe):
            name: str

        class Schema_Class(Type_Safe):
            @type_safe
            def process_schema(self, target_class: Type[Type_Safe]) -> Dict[str, Any]:
                """Method that should only accept Type_Safe classes"""
                return {"class_name": target_class.__name__}

        # Create test instances
        schema = Schema_Class()

        # Test valid case - should accept Type_Safe subclass
        result = schema.process_schema(Base_Type_Safe)
        assert result["class_name"] == "Base_Type_Safe"


        expected_error_1 = "Parameter 'target_class' expected type typing.Type[osbot_utils.type_safe.Type_Safe.Type_Safe], but got builtins.str which is not a subclass of <class 'osbot_utils.type_safe.Type_Safe.Type_Safe'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_1)):
            result = schema.process_schema(str)     # BUG: The following should fail but doesn't - str is not a Type_Safe subclass
            #assert result["class_name"] == "str"  # BUG This should not execute, but it does

        # The decorator does correctly catch non-type values
        expected_error_2 = "Parameter 'target_class' expected a type class but got <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            schema.process_schema("not a class")

        # Create a more complex example with nested Type parameters
        class Complex_Schema(Type_Safe):
            @type_safe
            def validate_schema(self,
                               primary_class  : Type[Type_Safe],
                               secondary_class: Type[Type_Safe] = None) -> bool:
                """Method with multiple Type parameters"""
                return issubclass(primary_class, Type_Safe)

        complex_schema = Complex_Schema()

        expected_error_3 = "Parameter 'secondary_class' expected type typing.Type[osbot_utils.type_safe.Type_Safe.Type_Safe], but got builtins.dict which is not a subclass of <class 'osbot_utils.type_safe.Type_Safe.Type_Safe'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_3)):
            assert complex_schema.validate_schema(Base_Type_Safe, dict) is True # BUG: Should fail but doesn't - dict is not a Type_Safe subclass

        expected_error_4 = "Parameter 'primary_class' expected type typing.Type[osbot_utils.type_safe.Type_Safe.Type_Safe], but got builtins.int which is not a subclass of <class 'osbot_utils.type_safe.Type_Safe.Type_Safe'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_4)):
            assert complex_schema.validate_schema(int) is False  # BUG: Should fail but doesn't - int is not a Type_Safe subclass,  Returns False instead of raising error


    def test__regression__type_safe_decorator__using_optional(self):
        @type_safe
        def an_function(an_str           : str,
                        an_int           : int,
                        optional_str     : Optional[str      ]=None,
                        optional_type    : Optional[type     ]=None,
                        optional_type_str: Optional[type[str]]=None,
                        optional_type_int: Optional[Type[int]]=None):
            pass

        an_function("answer", 42)           # OK
        an_function( an_str="answer", an_int=42)         # OK
        expected_error_1 = "Parameter 'an_int' expected type <class 'int'>, but got <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_1)):
            an_function(an_str="answer", an_int="aaaa") # OK

        an_function(an_str="answer", an_int=42, optional_str="aaa")         # OK

        expected_error_2 = "Parameter 'optional_str' expected type <class 'str'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_2)):
            an_function(an_str="answer", an_int=42, optional_str=42   )         # BUG:should have raised exception

        an_function(an_str="answer", an_int=42, optional_type=TestCase)     # OK
        expected_error_3 = "Parameter 'optional_type' expected type <class 'type'>, but got <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_3)):
            an_function(an_str="answer", an_int=42, optional_type="aaa"   )     # BUG:should have raised exception

        an_function(an_str="answer", an_int=42, optional_type_str=Safe_Id       )  # OK because Safe_Id(str)
        expected_error_4 = "Parameter 'optional_type_str' expected type type[str], but got osbot_utils.helpers.Timestamp_Now.Timestamp_Now which is not a subclass of <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_4)):
            an_function(an_str="answer", an_int=42, optional_type_str=Timestamp_Now )  # BUG:should have raised exception, because Timestamp_Now(int)

        an_function(an_str="answer", an_int=42, optional_type_int=Timestamp_Now)  # OK because Timestamp_Now(int)
        expected_error_5 = "Parameter 'optional_type_int' expected type typing.Type[int], but got osbot_utils.helpers.Safe_Id.Safe_Id which is not a subclass of <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_5)):
            an_function(an_str="answer", an_int=42, optional_type_int=Safe_Id      )  # BUG:should have raised exception, because Safe_Id(str)


    def test__regression__dict_attribute_fail(self):
        class An_Attribute(Type_Safe):
            an_str: str

        class An_Class(Type_Safe):
            @type_safe
            def an_method__instance(self, attributes: Dict[str, An_Attribute]):
                return attributes

        @type_safe
        def an_method__static(attributes: Dict[str, An_Attribute]):
            return attributes

        an_attribute = An_Attribute()
        attributes   = {'aaa': an_attribute}
        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     an_method__static(attributes)                                                 # Fixed: BUG   : should have not raised TypeError error
        assert an_method__static(attributes           ) == attributes                        # Fixed: now it works :)
        assert an_method__static({'aaa': an_attribute}) == attributes

        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     an_method__static({'aaa': 'abc'       })                                      # Fixed: BUG: should have failed with type safe check

        with pytest.raises(ValueError, match=re.escape("Dict value for key 'aaa' expected type <class 'test__decorator__type_safe__regression.test_decorator__type_safe__regression.test__regression__dict_attribute_fail.<locals>.An_Attribute'>, but got <class 'str'>")):
            an_method__static({'aaa': 'abc'       })                                        # Fixed: BUG: should have failed with type safe check
        #
        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     An_Class().an_method__instance({'aaa': an_attribute})                         # Fixed: BUG   : should have not raised TypeError error

        assert An_Class().an_method__instance(attributes           ) == attributes          # Fixed: expected behaviour
        assert An_Class().an_method__instance({'aaa': an_attribute}) == attributes


    def test__regression__kwargs_any_is_converted_into_bool(self):

        class An_Class(Type_Safe):

            @type_safe
            def method_1(self, value: any, node_type: type = None):
                return dict(value=value, node_type=node_type)

            @type_safe
            def method_2(self, value: Any, node_type: type = None):
                return dict(value=value, node_type=node_type)

        expected_error = "Parameter 'value' uses lowercase 'any' instead of 'Any' from typing module. Please use 'from typing import Any' and annotate as 'value: Any'"
        with pytest.raises(ValueError, match=expected_error):
            assert An_Class().method_1('a', int) # Fixed was:  == {'value': True, 'node_type': int}  # BUG, value should be 'a'

        assert An_Class().method_2('a', int) == {'node_type': int, 'value': 'a'}            # Fixed