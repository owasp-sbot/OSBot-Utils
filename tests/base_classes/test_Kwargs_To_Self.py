import types
from enum                                       import Enum, auto
from typing                                     import Union, Optional
from unittest                                   import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self, serialize_to_dict
from osbot_utils.base_classes.Type_Safe__List   import Type_Safe__List
from osbot_utils.testing.Catch                  import Catch
from osbot_utils.testing.Stdout                 import Stdout
from osbot_utils.utils.Json                     import json_dumps
from osbot_utils.utils.Misc                     import random_string, list_set
from osbot_utils.utils.Objects                  import obj_data


class Test_Kwargs_To_Self(TestCase):

    class Config_Class(Kwargs_To_Self):
        attribute1      = 'default_value'
        attribute2      = True
        callable_attr_1 = print                                             # make it a callable to make sure we also pick up on __default_kwargs__ and__kwargs__

        def an_method(self):
            pass

    class Extra_Config(Config_Class):
        attribute3      = 'another_value'
        callable_attr_2 = print                                            # make it a callable to make sure we also pick up on __default_kwargs__ and__kwargs__#

        def __init__(self):
            super().__init__()
            self.local_attribute_4 = '123'                                  # these locals should not be picked up by _kwargs or __kwargs__
            self.local_callable_attr_4 = print

        def an_extra_instance_method(self):
            pass

    def test___cls_kwargs__(self):
        assert self.Config_Class.__cls_kwargs__(include_base_classes=False) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert self.Config_Class.__cls_kwargs__(include_base_classes=True ) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert self.Extra_Config.__cls_kwargs__(include_base_classes=False) == {'attribute3': 'another_value',                     'callable_attr_2': print }
        assert self.Extra_Config.__cls_kwargs__(include_base_classes=True ) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print ,
                                                                                'attribute3': 'another_value',                     'callable_attr_2': print , }
        assert self.Config_Class.__cls_kwargs__(include_base_classes=True) == self.Config_Class.__cls_kwargs__()
        assert self.Extra_Config.__cls_kwargs__(include_base_classes=True) == self.Extra_Config.__cls_kwargs__()

        assert self.Config_Class.__cls_kwargs__() == self.Config_Class().__cls_kwargs__()
        assert self.Extra_Config.__cls_kwargs__() == self.Extra_Config().__cls_kwargs__()

        # handle current edge case for supporting the functools.cache decorator (in __cls_kwargs__)
        # todo: understand better this scenario and if there is a better way to handle
        from functools import cache

        class An_Class(Kwargs_To_Self):
            @cache
            def with_cache(self):
                pass

        an_class = An_Class()

        assert type(An_Class.with_cache).__name__ == '_lru_cache_wrapper'
        assert type(an_class.with_cache) == types.MethodType


    def test___cls_kwargs____with_multiple_levels_of_base_classes(self):
        class Base_Class                       :  pass                         # a base class
        class Implements_Base_Class(Base_Class): pass                          # is used as a base class here
        class An_Class(Kwargs_To_Self):                                        # now when a new class
            an_var: Base_Class                                                 # creates a var using the base class
        class Extends_An_Class(An_Class):                                      # and another class uses it has a base class
            an_var: Implements_Base_Class

        assert list_set(Extends_An_Class.__cls_kwargs__()) == ['an_var']

    def test___cls_kwargs__with_optional_attributes(self):
        if not hasattr(self, '__annotations__'):                    # can't do type safety checks if the class does not have annotations
            pytest.skip('Skipping test that requires __annotations__')

        class Immutable_Types_Class(Kwargs_To_Self):
            a_int       : int       = 1
            a_float     : float     = 1.0
            a_str       : str       = "string"
            a_tuple     : tuple     = (1, 2)
            a_frozenset : frozenset = frozenset([1, 2])
            a_bytes     : bytes     = b"byte"

        class With_Optional_And_Union(Kwargs_To_Self):
            optional_int    : Optional[int            ] = None
            union_str_float : Union   [str, float     ] = "string_or_float"
            union_with_none : Optional[Union[int, str]] = None

        immutable_types_class   = Immutable_Types_Class()
        with_optional_and_union = With_Optional_And_Union()
        assert immutable_types_class  .__locals__() == {'a_int': 1, 'a_float': 1.0, 'a_str': 'string', 'a_tuple': (1, 2), 'a_frozenset': frozenset({1, 2}), 'a_bytes': b'byte'}
        assert with_optional_and_union.__locals__() == {'optional_int': None, 'union_str_float': 'string_or_float', 'union_with_none': None}

    def test___default_kwargs__(self):
        class An_Class(Kwargs_To_Self):
            attribute1 = 'default_value'
            attribute2 = True

        assert An_Class().__default_kwargs__() == {'attribute1': 'default_value', 'attribute2': True}


    def test_default_kwargs_inheritance(self):
        """ Test that _default_kwargs handles inheritance correctly (i.e. only shows all defaults for all inherited classes). """
        expected_defaults = {'attribute1'     : 'default_value'  ,
                             'attribute2'     : True             ,
                             'attribute3'     : 'another_value'  ,
                             'callable_attr_1': print            ,
                             'callable_attr_2': print            }
        self.assertEqual(self.Extra_Config().__default_kwargs__(), expected_defaults)


    def test_default_kwargs_no_leakage(self):
        """ Test that instance attributes do not affect class-level defaults. """
        instance = self.Config_Class(attribute1='changed_value')
        expected_defaults = {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': self.Config_Class().__default_kwargs__()['callable_attr_1']}
        self.assertEqual(self.Config_Class().__default_kwargs__(), expected_defaults)
        self.assertNotEqual(instance.attribute1, self.Config_Class().__default_kwargs__()['attribute1'])

    # def test_locked(self):
    #     class An_Class(Kwargs_To_Self):
    #         an_str  : str = '42'
    #
    #     an_class = An_Class()
    #     an_class.before_lock = 42
    #     assert an_class.__lock_attributes__ == False
    #     assert an_class.__locals__() == {'an_str': '42', 'before_lock': 42}
    #     an_class.locked()
    #     assert an_class.__lock_attributes__ == True
    #     with self.assertRaises(Exception) as context:
    #         an_class.after_lock = 43
    #     assert context.exception.args[0] == ("'[Object Locked] Current object is locked (with __lock_attributes__=True) "
    #                                           'which prevents new attributes allocations (i.e. setattr calls). In this '
    #                                           "case  An_Class' object has no attribute 'after_lock'")
    #     assert an_class.__locals__() == {'an_str': '42', 'before_lock': 42}
    #     an_class.locked(False)
    #     assert an_class.__lock_attributes__ == False
    #     an_class.after_lock = 43
    #
    #     assert an_class.__locals__() == {'after_lock': 43, 'an_str': '42', 'before_lock': 42}

    def test_serialize_to_dict(self):
        if not hasattr(self, '__annotations__'):                    # can't do type safety checks if the class does not have annotations
            pytest.skip('Skipping test that requires __annotations__')

        class An_Enum_A(Enum):
            an_value = 1

        class An_Class_A(Kwargs_To_Self):
            an_str : str = '42'
            an_int : int = 42
            an_list : list
            an_dict : dict
            an_enum : An_Enum_A = An_Enum_A.an_value

        an_class_dict = {'an_dict': {}, 'an_enum': 'an_value', 'an_int': 42, 'an_list': [], 'an_str': '42'}
        an_class_a      = An_Class_A()
        assert an_class_a.serialize_to_dict() == an_class_dict
        obj_to_serialize = 3 + 4j  # A complex number which will not serialise
        with self.assertRaises(TypeError) as context:
            serialize_to_dict(obj_to_serialize)
        assert context.exception.args[0] == "Type <class 'complex'> not serializable"

        with self.assertRaises(TypeError) as context:
            serialize_to_dict(TestCase)
        assert context.exception.args[0] == "Type <class 'builtin_function_or_method'> not serializable"

    def test_serialize_to_dict__enum(self):
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Kwargs_To_Self):
            an_str  : str
            an_enum : An_Enum

        an_str_value  = 'an value'
        an_enum_value = An_Enum.value_1

        an_class = An_Class()

        assert an_class.serialize_to_dict() == {'an_enum': None, 'an_str': ''}
        an_class.an_str  = an_str_value
        an_class.an_enum = an_enum_value
        an_class_dict    = an_class.serialize_to_dict()
        assert an_enum_value.name == 'value_1'
        assert an_class_dict      == {'an_enum': an_enum_value.name, 'an_str': an_str_value}
        assert an_class.json()    == an_class.serialize_to_dict()

        an_class_2 = An_Class()
        an_class_2.deserialize_from_dict(an_class_dict)
        assert an_class_2.an_str  == an_class.an_str
        assert an_class_2.an_enum == an_class.an_enum
        assert an_class_2.json()  == an_class_dict


    def test_deserialize_from_dict(self):
        #check handing of enums
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Kwargs_To_Self):
            an_str  : str
            an_enum : An_Enum

        an_class_dict = {'an_enum': 'value_2', 'an_str': ''}
        an_class      = An_Class()

        an_class.deserialize_from_dict(an_class_dict)
        assert an_class.json() == an_class_dict


        #check handing of base classes
        class An_Base_Class(Kwargs_To_Self):
            in_base  : str

        class An_Parent_Class(An_Base_Class):
           in_parent : str

        an_parent_dict  = {'in_base': 'base', 'in_parent': 'parent'}
        an_parent_class = An_Parent_Class()
        an_parent_class.deserialize_from_dict(an_parent_dict)
        assert an_parent_class.json() == an_parent_dict

        # check nested objects
        class An_Class_1(Kwargs_To_Self):
            in_class_1 : str

        class An_Class_2(Kwargs_To_Self):
            an_class_1 : An_Class_1
            in_class_2 : str

        an_class_1_dict = {'an_class_1': {'in_class_1': 'data_1'}, 'in_class_2': 'data_2'}
        an_class_2 = An_Class_2()
        an_class_2.deserialize_from_dict(an_class_1_dict)
        assert an_class_2.json() == an_class_1_dict

        with Stdout() as stdout:
            an_class_2.print()
        assert stdout.value() == "\n{'an_class_1': {'in_class_1': 'data_1'}, 'in_class_2': 'data_2'}\n"

    def test_from_json(self):
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Kwargs_To_Self):
            an_str  : str
            an_enum : An_Enum

        an_class           = An_Class(an_str='an_str_value', an_enum=An_Enum.value_2)
        an_class_json      = an_class.json()
        an_class_str       = json_dumps(an_class_json)
        an_class_from_json = An_Class.from_json(an_class_json)
        an_class_from_str  = An_Class.from_json(an_class_str )

        assert type(an_class_from_json)   == An_Class
        assert an_class_json              == {'an_enum': 'value_2', 'an_str': 'an_str_value'}
        assert an_class_from_json.an_enum == An_Enum.value_2
        assert an_class_from_json.an_str  == 'an_str_value'
        assert an_class_from_json.json()  == an_class_json
        assert an_class_from_str .json()  == an_class_json

    def test___attr_names__(self):
        assert self.Config_Class().__attr_names__() == ['attribute1', 'attribute2', 'callable_attr_1']

    def test___default__value__(self):
        _ = Kwargs_To_Self.__default__value__
        assert      _(str      )  == ''
        assert      _(int      )  == 0
        assert      _(list     )  == []
        assert      _(list[str])  == []                 # although we get Type_Safe__List, the value when empty will always be []
        assert      _(list[int])  == []                 # although we get Type_Safe__List, the value when empty will always be []
        assert type(_(str      )) is str
        assert type(_(int      )) is int
        assert type(_(list     )) is list               # here (because list      was used) we get a normal list
        assert type(_(list[str])) is Type_Safe__List    # here (because list[str] was used) we get the special type Type_Safe__List
        assert type(_(list[int])) is Type_Safe__List
        assert repr(_(list[str])) == 'list[str] with 0 elements'        # Type_Safe__List will return a representation of the original list[str]
        assert repr(_(list[int])) == 'list[int] with 0 elements'

        assert _(list[str]).expected_type is str        # confirm that .expected_type is set to the correct expected type (in this case str)
        assert _(list[int]).expected_type is int        # confirm that .expected_type is set to the correct expected type (in this case int)

        _(list).append('aa')                            # if we don't define the type it is possible to do this
        _(list).append(42)                              # have a list with a str and an int
        _(list[str]).append('aaaa')                     # but if we define the type, it is ok to append a value of typed defined
        with self.assertRaises(Exception) as context:   # but if we append a value of a different type
            _(list[str]).append(42)                     # like an int, we will get a Type Safety exception :)
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'str', but got 'int'"

    def test___kwargs__(self):
        assert self.Config_Class().__kwargs__() == { 'attribute1'     : 'default_value',
                                                     'attribute2'     : True           ,
                                                     'callable_attr_1': print          }


    # test multiple scenarios

    def test__correct_attributes(self):
        """ Test that correct attributes are set from kwargs. """
        config = self.Config_Class(attribute1='new_value', attribute2=False)
        self.assertEqual(config.attribute1, 'new_value')
        self.assertFalse(config.attribute2)

    def test__undefined_attribute(self):
        """ Test that an exception is raised for undefined attributes. """
        with self.assertRaises(Exception) as context:
            self.Config_Class(attribute3='invalid')
        self.assertIn("Config_Class has no attribute 'attribute3'", str(context.exception))

    def test__no_kwargs(self):
        """ Test that default values are used when no kwargs are provided. """
        config = self.Config_Class()
        self.assertEqual(config.attribute1, 'default_value')
        self.assertTrue(config.attribute2)

    def test__check_type_safety_assignments__on_obj__union(self):
        an_bool_value  = True
        an_int_value   = 42
        an_str_value   = 'an_str_value'

        class An_Class(Kwargs_To_Self):
            an_bool    : Optional[bool            ]
            an_int     : Optional[int             ]
            an_str     : Optional[str             ]
            an_bool_int: Optional[Union[bool, int]]
            an_bool_str: Optional[Union[bool, str]]

        an_class = An_Class()
        assert an_class.an_bool     is None                                                             # note that when using Optional
        assert an_class.an_int      is None                                                             # values not explicitly set are mapped to None
        assert an_class.an_int      is None
        assert an_class.an_bool_int is None
        assert an_class.an_bool_str is None
        assert an_class.__locals__() == {'an_bool': None, 'an_bool_int': None, 'an_bool_str': None,
                                         'an_int' : None, 'an_str'     : None                     }     # confirm default values assignment

        an_class.an_bool     = an_bool_value                                                            # these should all work
        an_class.an_int      = an_int_value                                                             # since we are doing the correct type assigment
        an_class.an_str      = an_str_value
        an_class.an_bool_int = an_bool_value
        an_class.an_bool_str = an_bool_value
        an_class.an_bool_int = an_int_value
        an_class.an_bool_str = an_str_value

    def test__test_leakage_between_two_instances(self):
        config_1 = self.Config_Class()
        config_2 = self.Config_Class()

        assert config_1.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert config_2.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print}

        assert obj_data(config_1) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': f"{print}" }        # obj doesn't pick up functions (unless explicitly told to)
        assert obj_data(config_2) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': f"{print}"}

        new_value           = random_string(prefix='new_value_')
        config_1.attribute1 = new_value
        config_1.attribute2 = False

        assert config_1.__kwargs__() == {'attribute1': new_value      , 'attribute2': False, 'callable_attr_1': print }    # confirm that config_1 has the new values
        assert config_2.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True , 'callable_attr_1': print }    # confirm that config_2 has not been affected

    def test__kwargs_capture_doesnt_show_locals(self):
        extra_config = self.Extra_Config()
        assert extra_config.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'attribute3': 'another_value', 'callable_attr_1': print, 'callable_attr_2': extra_config.callable_attr_2}

    def test__kwargs__doesnt_pick_up_inherited_vars(self):
        extra_config = self.Extra_Config()
        assert extra_config.__kwargs__() == {'attribute1'      : 'default_value'              ,     # this list confirms that __kwargs__ only picks up the static variables
                                             'attribute2'      : True                         ,     # i.e. not the ones defined in the __init__ method
                                             'attribute3'      : 'another_value'              ,     # like the local_attribute_4 and local_callable_attr_4
                                             'callable_attr_1' : print                        ,
                                             'callable_attr_2' : print                        }
        assert callable(extra_config.callable_attr_1) is True                                       # confirm we are picking up callable (i.e. functions
        assert callable(extra_config.callable_attr_2) is True
        assert isinstance(extra_config.callable_attr_1, types.BuiltinMethodType) is True            # confirm they are methods (this one local)
        assert isinstance(extra_config.callable_attr_2, types.BuiltinMethodType) is True            # this one from the builtins
        assert extra_config.callable_attr_1.__name__ == 'print'                                     # confirm the name of the method of callable_attr_1
        assert extra_config.callable_attr_2.__name__ == 'print'                                     # confirm the name of the method of callable_attr_2

        assert extra_config.attribute1           == 'default_value'
        assert extra_config.attribute2           is True
        assert extra_config.attribute3           == 'another_value'
        assert extra_config.local_attribute_4    == '123'                    # this is a local var, that is available but not picked up by __kwargs__
        assert extra_config.local_callable_attr_4 == print                   # same for these methods

    def test__kwargs__picks_up_vars_defined_in__init__(self):
        random_value     = random_string()
        default_kwargs   = self.Config_Class().__default_kwargs__()
        config_2_kwargs  = {**default_kwargs, 'attribute1': random_value}

        assert default_kwargs == {  'attribute1'    : 'default_value',
                                    'attribute2'     : True          ,
                                    'callable_attr_1': print         }


        assert config_2_kwargs == {  'attribute1'    : random_value  ,         # fails
                                     'attribute2'     : True         ,
                                     'callable_attr_1': print        }


        config_1 = self.Config_Class()
        config_2 = self.Config_Class(attribute1=random_value)

        assert config_1.__default_kwargs__() == default_kwargs
        assert config_2.__default_kwargs__() == default_kwargs  # __default_kwargs__ should not been affected
        assert config_2.__kwargs__()         == config_2_kwargs

        # confirm that we can't set variables that are not defined in __kwargs__
        expected_error = ("Catch: <class 'Exception'> : Config_Class has no attribute 'extra_var' and "
                          "cannot be assigned the value 'aaa'. "
                          "Use Config_Class.__default_kwargs__() see what attributes are available")
        with Catch(expected_error=expected_error):
            self.Config_Class(extra_var="aaa")


    def test__locals__(self):
        default_kwargs  = self.Extra_Config().__default_kwargs__()
        extra_config_1  = self.Extra_Config()
        default_locals  = {**default_kwargs, 'callable_attr_2': extra_config_1.callable_attr_2, 'local_attribute_4': '123', 'local_callable_attr_4': print}

        assert extra_config_1.__locals__() == default_locals

        extra_config_1.local_attribute_4 = '___changed__'
        assert extra_config_1.__locals__() == {**default_locals, 'local_attribute_4': '___changed__'}

        extra_config_1.attribute1 = '__also_changed__'
        assert extra_config_1.__locals__() == {**default_locals, 'attribute1': '__also_changed__', 'local_attribute_4': '___changed__'}

        assert obj_data(extra_config_1) == { 'attribute1'           : '__also_changed__'            ,
                                             'attribute2'           : True                          ,
                                             'attribute3'           : 'another_value'               ,
                                             'callable_attr_1'      : '<built-in function print>'   ,
                                             'callable_attr_2'      : '<built-in function print>'   ,
                                             'local_attribute_4'    : '___changed__'                ,
                                             'local_callable_attr_4': '<built-in function print>'   }

        # confirm we can't add new vars
        with Catch(expect_exception=True):
            self.Config_Class(extra_var='123')

    def test__default_kwargs__picks_up_mutable__vars(self):

        class Class_With_Types(Kwargs_To_Self):
            value_1 = None
            value_2 = 'a'
            value_3 = 1
            type_01 : list
            type_02 : dict
            type_03 : int
            type_04 : float
            type_05 : str
            type_06 : bool
            type_07 : tuple
            type_08 : set
            type_09 : frozenset
            type_10 : bytes
            type_11 : complex
            type_value_1 : int = 1
            type_value_2 : str = "aaa"

        expected_values = { 'type_01': []         ,
                            'type_02': {}         ,
                            'type_03': 0          ,
                            'type_04': 0.0        ,
                            'type_05': ''         ,
                            'type_06': False      ,
                            'type_07': ()         ,
                            'type_08': set()      ,
                            'type_09': frozenset(),
                            'type_10': b''        ,
                            'type_11': 0j         ,
                            'value_1': None       ,
                            'value_2': 'a'        ,
                            'value_3': 1          ,
                            'type_value_1': 1     ,
                            'type_value_2': 'aaa' }

        assert Class_With_Types().__default_kwargs__() == expected_values
        assert Class_With_Types().__kwargs__      () == expected_values
        assert Class_With_Types().__locals__      () == expected_values

    def test__default_kwargs__picks_up_bad_types(self):

        class An_Bad_Type(Kwargs_To_Self):
            not_an_int: int = "an str"

        expected_error= "Catch: <class 'Exception'> : variable 'not_an_int' is defined as type '<class 'int'>' but has value 'an str' of type '<class 'str'>'"
        with Catch(expect_exception=True, expected_error=expected_error):
            An_Bad_Type().__default_kwargs__()

        expected_error = "Catch: <class 'Exception'> : variable 'not_an_int' is defined as type '<class 'int'>' but has value 'an str' of type '<class 'str'>'"
        with Catch(expect_exception=True, expected_error=expected_error):
            An_Bad_Type().__default_kwargs__()

    # def test___init___disable_type_safety(self):
    #     assert self.Config_Class(                         ).__type_safety__ is True
    #     assert self.Config_Class(disable_type_safety=True ).__type_safety__ is False
    #     assert self.Config_Class(disable_type_safety=False).__type_safety__ is True


    def test___init___pics_up_types_with_values(self):

        class An_Class(Kwargs_To_Self):
            attribute_1 = 'default_value'
            attribute_2 = True
            attribute_3 : bool = True
            attribute_4 : bool = False
            attribute_5 : str = 'abc'
            attribute_6 : str
            attribute_7 : list
            attribute_8 : int = 42

        expected_values =  {'attribute_1': 'default_value', 'attribute_2': True, 'attribute_3': True, 'attribute_4': False, 'attribute_5': 'abc', 'attribute_6': '', 'attribute_7': [], 'attribute_8': 42}
        an_class        = An_Class()

        assert an_class.attribute_1 == 'default_value'
        assert an_class.attribute_2 is True
        assert an_class.attribute_3 is True
        assert an_class.attribute_4 is False
        assert an_class.attribute_5 == 'abc'
        assert an_class.attribute_6 == ''
        assert an_class.attribute_7 == []
        assert an_class.attribute_8 == 42

        assert An_Class().__default_kwargs__() == expected_values
        assert An_Class().__kwargs__() == expected_values
        assert An_Class().__locals__() == expected_values

    def test___init__pics_up_types_mutable_types(self):
        if not hasattr(self, '__annotations__'):                    # can't do type safety checks if the class does not have annotations
            pytest.skip('Skipping test that requires __annotations__')

        class An_Class(Kwargs_To_Self):
            attribute_1 = 'default_value'
            attribute_2 = True
            attribute_3 : str            # ok
            attribute_4 : list           # ok
            attribute_5 : dict           # ok
            attribute_6 : str  = 'a'     # ok

            attribute_7 : list = []      # should fail

        expected_error=("Catch: <class 'Exception'> : variable 'attribute_7' is defined "
                        "as type '<class 'list'>' which is not supported by Kwargs_To_Self, "
                        "with only the following immutable types being supported: "
                        "'(<class 'bool'>, <class 'int'>, <class 'float'>, <class 'complex'>, <class 'str'>, "
                        "<class 'tuple'>, <class 'frozenset'>, <class 'bytes'>, <class 'NoneType'>, <class 'enum.EnumType'>)'")
        with Catch(expect_exception=True, expected_error = expected_error):
            An_Class()

        class An_Class_2(Kwargs_To_Self):
            attribute_8 : dict = {}

        expected_error=("Catch: <class 'Exception'> : variable 'attribute_8' is defined "
                        "as type '<class 'dict'>' which is not supported by Kwargs_To_Self, "
                        "with only the following immutable types being supported: "
                        "'(<class 'bool'>, <class 'int'>, <class 'float'>, <class 'complex'>, <class 'str'>, "
                        "<class 'tuple'>, <class 'frozenset'>, <class 'bytes'>, <class 'NoneType'>, <class 'enum.EnumType'>)'")
        with Catch(expect_exception=True, expected_error=expected_error):
            An_Class_2()

    def test___init___prevents_new_attributes(self):
        with self.assertRaises(Exception) as context:
            self.Config_Class(aaaa=123)
        assert context.exception.args[0] == ("Config_Class has no attribute 'aaaa' and cannot be assigned the value '123'. "
                                             'Use Config_Class.__default_kwargs__() see what attributes are available')

    def test___set__attr__(self):
        class An_Class(Kwargs_To_Self):
            an_str : str
        an_class = An_Class()
        assert an_class.json() == {'an_str': ''}
        expected_message = "Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'int'>'"
        with self.assertRaises(Exception) as context_1:
            an_class.an_str = 42
        assert context_1.exception.args[0] == expected_message

        expected_message_2 = "Can't set None, to a variable that is already set. Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'NoneType'>'"
        with self.assertRaises(Exception) as context_2:
            an_class.an_str = None
        assert context_2.exception.args[0] == expected_message_2



    def test_merge_with(self):
        class Base_Class(Kwargs_To_Self):
            an_int : int

        class Target_Class(Base_Class):
            an_str : str

        base_class   = Base_Class()
        target_class = Target_Class()
        assert list_set(base_class  .__kwargs__()) == ['an_int']
        assert list_set(target_class.__kwargs__()) == ['an_int', 'an_str']
        base_class.an_int = 42
        merged_class = target_class.merge_with(base_class)
        assert merged_class.an_int == 42
        base_class.an_int = 123                                                  # confirm that change in base_class
        assert merged_class.an_int == 123                                        # impacts merged_class
        merged_class.an_int= 456                                                 # confirm that change in merged_class
        assert base_class.an_int == 456                                          # impacts base_class