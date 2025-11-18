import re
import pytest
from enum                                                                               import Enum
from typing                                                                             import Any, Dict, Optional, Type, List
from unittest                                                                           import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Int                                     import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                       import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now        import Timestamp_Now
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe

class test_decorator__type_safe__regression(TestCase):

    def test__regression__type_safe__method__failed_with_dict(self):
        @type_safe
        def an_method_1(html_dict: Dict): pass

        @type_safe
        def an_method_2(self, html_dict: Dict): pass

        @type_safe
        def an_method_3(html_dict: dict): pass

        @type_safe
        def an_method_4(self, html_dict: dict): pass

        an_dict_1     = {}
        an_dict_2     = dict()

        # BUG: with Dict fails
        # error_message = "not enough values to unpack (expected 2, got 0)"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     an_method_1({})                                                     # BUG
        #
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     an_method_2(None, {})                                 # BUG
        #
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     an_method_2(None, an_dict_1)                                   # BUG


        an_method_1({})                                                     # FIXED: BUG
        an_method_2(None, {})                                               # FIXED: BUG
        an_method_2(None, an_dict_1)                                        # FIXED: BUG

        # with dict it works
        an_method_3({})                                  # works with an_method_3(html_dict: dict)
        an_method_3(an_dict_1)                           # works with an_method_3(html_dict: dict)
        an_method_3(an_dict_2)                           # works with an_method_3(html_dict: dict)
        an_method_4(None, {})              # works with an_method_4(self, html_dict: dict)
        an_method_4(None, an_dict_1)                # works with an_method_4(self, html_dict: dict)
        an_method_4(None, an_dict_2)                # works with an_method_4(self, html_dict: dict)



    def test__regression__enum_doesnt_convert_str(self):
        class An_Enum(str, Enum):
            VALUE_A = 'value_a'
            VALUE_B = 'value_b'

            def __str__(self):
                return self.value

        @type_safe
        def an_method(an_enum: An_Enum):
            return f'{an_enum}'

        assert an_method(An_Enum.VALUE_A) == 'value_a'
        assert an_method(An_Enum.VALUE_B) == 'value_b'

        # error_message = "Parameter 'an_enum' expected type <enum 'An_Enum'>, but got <class 'str'>"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     an_method('value_a')                                                  # BUG

        assert an_method('value_a') == 'value_a'                                    # FIXED
        assert an_method('value_b') == 'value_b'


    def test__regression__type_safe__doesnt_check_return_value(self):
        @type_safe
        def return_int__1() -> int:    return 42

        @type_safe
        def return_int__2() -> int:    return "42"

        @type_safe
        def return_int__3() -> int:    return ['42']

        @type_safe
        def return_str__1() -> str:     return 42

        @type_safe
        def return_str__2() -> str:     return "42"

        @type_safe
        def return_str__3() -> str:     return ["42"]

        assert return_int__1() == 42                        # OK
        #assert return_int__2() == "42"                      # BUG
        #assert return_int__3() == ["42"]                    # BUG
        #assert return_str__1() == 42                        # BUG
        assert return_str__2() == "42"                      # OK
        #assert return_str__3() == ["42"]                    # BUG

        type_path = 'test_decorator__type_safe__regression.test__regression__type_safe__doesnt_check_return_value.<locals>'
        error_message_1 = f"Function '{type_path}.return_int__2' return type validation failed: Expected 'int', but got 'str'"
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            return_int__2()                                     # FIXED

        error_message_2 = f"Function '{type_path}.return_int__3' return type validation failed: Expected 'int', but got 'list'"
        with pytest.raises(TypeError, match=error_message_2):
            return_int__3()                                     # FIXED

        error_message_3 = f"Function '{type_path}.return_str__1' return type validation failed: Expected 'str', but got 'int'"
        with pytest.raises(TypeError, match=error_message_3):
            return_str__1()                                     # FIXED

        error_message_4 = f"Function '{type_path}.return_str__3' return type validation failed: Expected 'str', but got 'list'"
        with pytest.raises(TypeError, match=error_message_4):
            return_str__3()                                     # FIXED

    def test__regression__decorator__type_safe__casts_into_str_instead_if_safe_int(self):
        from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe
        @type_safe
        def an_method(an_int: Safe_Int):
            return an_int

        result = an_method('42')
        #assert type(result) is str                      # Fixed: BUG
        #assert type(result) is not Safe_Int             # Fixed: BUG
        #assert result == '42'                           # Fixed: BUG
        #assert result != 42                             # Fixed: BUG
        assert type(result) is Safe_Int
        assert result       == 42


    def test__regression__decorator__type_safe__str__to__str_safe_path(self):
        @type_safe
        def an_method(an_path: Safe_Str__File__Path):
            return an_path
        # error_message = "Parameter 'an_path' expected type <class 'osbot_utils.type_safe.primitives.domains.filesystem.safe_str.Safe_Str__File__Path.Safe_Str__File__Path'>, but got <class 'str'>"
        # with pytest.raises(ValueError, match=error_message):
        #     an_method('abc')                                      # BUG: should not rasie

        assert an_method('abc')       == 'abc'                      # FIXED :)
        assert type(an_method('abc')) == Safe_Str__File__Path
        assert type(an_method('abc')) is not str
        error_message = "Parameter 'an_path' expected type <class 'osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path.Safe_Str__File__Path'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=error_message):
            an_method(123)


    def test__regression__in_method_conversion(self):

        @type_safe
        def create_operation(parameters              : List[Dict[str, Any]] = None):
            pass

        create_operation()
        create_operation(parameters=None)
        create_operation(parameters=[]  )
        create_operation(parameters=[{}])
        #error_message = "typing.Any cannot be used with isinstance()"          # FIXED:  BUG
        # with pytest.raises(TypeError, match=re.escape(error_message)):        # FIXED:  BUG
        #     create_operation(parameters=[{'a':'b'}])                          # FIXED:  BUG
        # now that it is working we can double-check the typesafety checks

        create_operation(parameters=[{'a': 'b'      }])     # since it is Any
        create_operation(parameters=[{'a': None     }])     # the value can be anything
        create_operation(parameters=[{'a': 123      }])
        create_operation(parameters=[{'a': TestCase }])
        with pytest.raises(ValueError, match=re.escape("Parameter 'parameters' expected a list but got <class 'dict'>")):
            create_operation(parameters={})
        with pytest.raises(ValueError, match=re.escape("Parameter 'parameters' expected a list but got <class 'str'>")):
            create_operation(parameters="aaa")
        with pytest.raises(ValueError, match=re.escape("Parameter 'parameters' expected a list but got <class 'int'>")):
            create_operation(parameters=42   )
        with pytest.raises(ValueError, match=re.escape("List item at index 0 expected dict but got <class 'int'>")):
            create_operation(parameters=[42]   )
        with pytest.raises(ValueError, match=re.escape("List item at index 0 expected dict but got <class 'list'>")):
            create_operation(parameters=[[]])
        with pytest.raises(ValueError, match=re.escape("Dict key '42' at index 0 expected type <class 'str'>, but got <class 'int'>")):
            create_operation(parameters=[{ 42 : 'b'}]   )
        with pytest.raises(ValueError, match=re.escape("Dict key '111' at index 0 expected type <class 'str'>, but got <class 'int'>")):
            create_operation(parameters=[{ 'a': "b", 111 : 'b'}]   )

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
        expected_error_4 = "Parameter 'optional_type_str' expected type type[str], but got osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now.Timestamp_Now which is not a subclass of <class 'str'>"
        with pytest.raises(ValueError, match=re.escape(expected_error_4)):
            an_function(an_str="answer", an_int=42, optional_type_str=Timestamp_Now )  # BUG:should have raised exception, because Timestamp_Now(int)

        an_function(an_str="answer", an_int=42, optional_type_int=Timestamp_Now)  # OK because Timestamp_Now(int)
        expected_error_5 = "Parameter 'optional_type_int' expected type typing.Type[int], but got osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id.Safe_Id which is not a subclass of <class 'int'>"
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

        error_message = "Dict value for key 'aaa' in parameter 'attributes': Expected 'An_Attribute', but got 'str'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
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

    def test__regression__type_save_method__return_value_cast_to_safe_uint(self):
        @type_safe
        def an_method() -> Safe_UInt:
            return 42

        #error_message = "Function 'test__decorator__type_safe__bugs.test__bug__type_save_method__return_value_cast_to_safe_uint.<locals>.an_method' return type validation failed: Expected 'Safe_UInt', but got 'int'"
        # with pytest.raises(TypeError, match=re.escape(error_message)):
        #     an_method()             # BUG: we should handle transparently the conversion into Safe_UInt (and only raise an exeception if the data is bad)
        assert an_method()       == 42
        assert type(an_method()) is Safe_UInt

    def test_regression__type_safe_method__safe_float_conversion(self):

        from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe
        from osbot_utils.type_safe.primitives.core.Safe_Float          import Safe_Float

        class Safe_Float__Classification(Safe_Float):
            min_value = 0
            max_value = 1

        assert Safe_Float__Classification(0                     ) == 0.0
        assert Safe_Float__Classification(0.0                   ) == 0.0
        assert Safe_Float__Classification(0.5                   ) == 0.5
        assert Safe_Float__Classification(float(0.5)            ) == 0.5
        assert Safe_Float__Classification(Safe_Float(0.5)       ) == 0.5
        assert type( Safe_Float__Classification(0)              ) is Safe_Float__Classification
        assert type( Safe_Float__Classification(0.5)            ) is Safe_Float__Classification
        assert type( Safe_Float__Classification(Safe_Float(0.5))) is Safe_Float__Classification
        # Safe_Float__Classification(Safe_Int(0.5))                 # this fails, which makes sense

        @type_safe
        def an_method_2(an_float: Safe_Float__Classification):
            return an_float

        # return
        # error_message_1 = "Parameter 'an_float' expected type <class 'test__decorator__type_safe__bugs.test__decorator__type_safe__bugs.test_bug__type_safe_method__safe_float_conversion.<locals>.Safe_Float__Classification'>, but got <class 'int'>"
        # with pytest.raises(ValueError, match=re.escape(error_message_1)):
        #     an_method_2(0)                                                  # BUG should have worked
        assert an_method_2(0) == 0                                            # FIXED expected behaviour

        assert an_method_2(0.0) == 0
        assert an_method_2(0.0) == 0.0
        # error_message_2 = "Parameter 'an_float' expected type <class 'test__decorator__type_safe__bugs.test__decorator__type_safe__bugs.test_bug__type_safe_method__safe_float_conversion.<locals>.Safe_Float__Classification'>, but got <class 'float'>"
        # with pytest.raises(ValueError, match=re.escape(error_message_2)):
        #     an_method_2(0.2)                                                # BUG should have worked
        #     #assert an_method_2(0.2) == 0.2                                 # expected behaviour
        assert an_method_2(0.2) == 0.2                                        # FIXED

        # error_message_3 = "Parameter 'an_float' expected type <class 'test__decorator__type_safe__bugs.test__decorator__type_safe__bugs.test_bug__type_safe_method__safe_float_conversion.<locals>.Safe_Float__Classification'>, but got <class 'osbot_utils.type_safe.primitives.core.Safe_Float.Safe_Float'>"
        # with pytest.raises(ValueError, match=re.escape(error_message_3)):
        #     an_method_2(Safe_Float(4.2))                                    # BUG should have worked
        #     #assert an_method_2(Safe_Float(4.2)) == 4.2                      # expected behaviour

        assert an_method_2(Safe_Float(0.2)) == 0.2                              # FIXED

        error_message_4 = "Safe_Float__Classification must be <= 1, got 4.2"
        with pytest.raises(ValueError, match=re.escape(error_message_4)):
            assert an_method_2(Safe_Float__Classification(4.2)) == 4.2          # expected error message

        assert an_method_2(Safe_Float__Classification(0.2)) == 0.2              # expect behaviour


    def test_regression__type_safe_method__list_type_with_no_attribute(self):
        @type_safe
        def classify_topics(self, topics : List):
            return topics

        # error_message = "tuple index out of range"
        # with pytest.raises(IndexError, match=error_message):
        #     classify_topics(None, [])               # BUG

        classify_topics(None, [])       # FIXED

        assert classify_topics(None, [   ]) == [   ]
        assert classify_topics(None, ['a']) == ['a']

    def test__regression__type_safe__decorator__str_auto_conversion_on_dicts(self):

        @type_safe
        def an_method(texts : Dict[Safe_Str, Safe_UInt]):
            return texts

        texts_1 = { Safe_Str("aaa1234567"): Safe_UInt("42")}                # works
        texts_2 = {          "aaa1234567" : Safe_UInt("42")}                # FIXED: BUG , should also work
        texts_3 = { Safe_Str("aaa1234567"): "42"           }                # FIXED: BUG , should also work
        texts_4 = {          "aaa1234567" : "42"           }                # FIXED: BUG , should also work

        an_method(texts=texts_1)

        error_message_1 = "Dict key 'aaa1234567' expected type <class 'osbot_utils.type_safe.primitives.core.Safe_Str.Safe_Str'>, but got <class 'str'>"
        error_message_2 = "Dict value for key 'aaa1234567' in parameter 'texts': Expected 'Safe_UInt', but got 'str'"

        # with pytest.raises(ValueError, match=re.escape(error_message_1)):
        #     an_method(texts=texts_2)                                            # BUG , should also work
        #
        # with pytest.raises(ValueError, match=re.escape(error_message_2)):
        #     an_method(texts=texts_3)                                            # BUG , should also work
        #
        # with pytest.raises(ValueError, match=re.escape(error_message_1)):
        #     an_method(texts=texts_4)                                            # BUG , should also work

        assert an_method(texts=texts_2) == texts_2                                # FIXED
        assert an_method(texts=texts_3) == texts_3                                # FIXED
        assert an_method(texts=texts_4) == texts_4                                # FIXED

        assert an_method(texts=texts_1) == texts_1                                # these assert should also work
        assert an_method(texts=texts_1) == texts_2
        assert an_method(texts=texts_1) == texts_3
        assert an_method(texts=texts_1) == texts_4

    def test__regression__type_safe__return_value__not_works__with__bad__forward_refs(self):
        import re

        class An_Class(Type_Safe):
            @type_safe
            def an_method(self) -> 'An_Class2':
                return self

        error_message = ("Function 'test_decorator__type_safe__regression.test__regression__type_safe__return_value__not_works__with__bad__forward_refs."
                         "<locals>.An_Class.an_method' return type validation failed: "                         
                         "Expected type 'An_Class2' but got instance of 'An_Class'.")

        with pytest.raises(TypeError, match=re.escape(error_message)):
            An_Class().an_method()

    def test__regression__type_safe__return_value__not_works__with_differnt__forward_refs(self):
        class An_Class_2(Type_Safe):
            pass
        class An_Class_1(Type_Safe):
            @type_safe
            def an_method(self) -> 'An_Class_2':
                return An_Class_2()

        assert type(An_Class_1().an_method()) is An_Class_2         # FIXED: this used to fail before fix

    def test__regression__type_safe__return_value__not_works__with_forward_refs(self):
        class An_Class(Type_Safe):
            @type_safe
            def return_self(self) -> 'An_Class':
                return self
        # error_message = "Function 'test__decorator__type_safe__bugs.test__bug__type_safe__return_value__not_works__with_forward_refs.<locals>.An_Class.return_self' return type validation failed: isinstance() arg 2 must be a type, a tuple of types, or a union"
        # with pytest.raises(TypeError, match=re.escape(error_message)):
        #     An_Class().return_self()              # BUG
        assert type(An_Class().return_self()) is An_Class           # FIXED
