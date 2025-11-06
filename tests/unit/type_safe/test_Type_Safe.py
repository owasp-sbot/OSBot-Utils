import re
import socket
import sys
import pytest
import types
import threading
from _thread                                                                        import RLock
from enum                                                                           import Enum, auto
from typing                                                                         import Union, Optional, Type, Set
from unittest                                                                       import TestCase
from osbot_utils.testing.__helpers                                                  import obj
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now    import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.Guid                      import Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid               import Random_Guid
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List
from osbot_utils.testing.Catch                                                      import Catch
from osbot_utils.testing.Stdout                                                     import Stdout
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__From_Json          import type_safe_step_from_json
from osbot_utils.utils.Json                                                         import json_dumps
from osbot_utils.utils.Misc                                                         import random_string, list_set
from osbot_utils.utils.Objects                                                      import obj_data, default_value, serialize_to_dict
from osbot_utils.testing.__ import __, __SKIP__


class test_Type_Safe(TestCase):

    class Config_Class(Type_Safe):
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

    def test__set_support(self):
        class An_Class(Type_Safe):
            an_set_1 : set[str]
            an_set_2 : Set[str]

        an_class = An_Class(an_set_1=set(['a', 'b']))
        an_class.an_set_1.remove('a')
        an_class.an_set_2.add   ('a')
        assert an_class.json() == {'an_set_1': ['b'], 'an_set_2': ['a']}
        assert an_class.obj () == __(an_set_1=['b'], an_set_2=['a'])



    def test___cls_kwargs__(self):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that doesn't work on 3.8 or lower")


        assert self.Config_Class.__cls_kwargs__( ) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert self.Extra_Config.__cls_kwargs__( ) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print ,
                                                       'attribute3': 'another_value',                     'callable_attr_2': print , }
        assert self.Config_Class.__cls_kwargs__() == self.Config_Class.__cls_kwargs__()
        assert self.Extra_Config.__cls_kwargs__() == self.Extra_Config.__cls_kwargs__()
        assert self.Config_Class.__cls_kwargs__() == self.Config_Class().__cls_kwargs__()
        assert self.Extra_Config.__cls_kwargs__() == self.Extra_Config().__cls_kwargs__()

        # handle current edge case for supporting the functools.cache decorator (in __cls_kwargs__)
        # todo: understand better this scenario and if there is a better way to handle
        from functools import cache

        class An_Class(Type_Safe):
            @cache
            def with_cache(self):
                pass

        an_class = An_Class()

        assert type(An_Class.with_cache).__name__ == '_lru_cache_wrapper'
        assert type(an_class.with_cache) == types.MethodType


    def test___cls_kwargs____with_multiple_levels_of_base_classes(self):
        class Base_Class                       :  pass                         # a base class
        class Implements_Base_Class(Base_Class): pass                          # is used as a base class here
        class An_Class(Type_Safe):                                        # now when a new class
            an_var: Base_Class                                                 # creates a var using the base class
        class Extends_An_Class(An_Class):                                      # and another class uses it has a base class
            an_var: Implements_Base_Class

        assert list_set(Extends_An_Class.__cls_kwargs__()) == ['an_var']

    def test___cls_kwargs__with_optional_attributes(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")

        class Immutable_Types_Class(Type_Safe):
            a_int       : int       = 1
            a_float     : float     = 1.0
            a_str       : str       = "string"
            #a_tuple     : tuple     = (1, 2)
            #a_frozenset : frozenset = frozenset([1, 2])
            a_bytes     : bytes     = b"byte"

        class With_Optional_And_Union(Type_Safe):
            optional_int    : Optional[int            ] = None
            union_str_float : Union   [str, float     ] = "string_or_float"
            union_with_none : Optional[Union[int, str]] = None

        immutable_types_class   = Immutable_Types_Class()
        with_optional_and_union = With_Optional_And_Union()
        assert immutable_types_class  .__locals__() == {'a_int': 1, 'a_float': 1.0, 'a_str': 'string', 'a_bytes': b'byte'}
        assert with_optional_and_union.__locals__() == {'optional_int': None, 'union_str_float': 'string_or_float', 'union_with_none': None}

    def test___default_kwargs__(self):
        class An_Class(Type_Safe):
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

    def test___setattr__(self):
        class An_Class(Type_Safe):
            an_str : str
        an_class = An_Class()
        assert an_class.json() == {'an_str': ''}
        expected_message = "On An_Class, invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'int'>'"
        with self.assertRaises(Exception) as context_1:
            an_class.an_str = 42
        assert context_1.exception.args[0] == expected_message

        expected_message_2 = "On An_Class, can't be set to None, to a variable that is already set. Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'NoneType'>'"
        with self.assertRaises(Exception) as context_2:
            an_class.an_str = None
        assert context_2.exception.args[0] == expected_message_2


    # todo: move this test to __bug__ capturing the fact that the classes are not locked
    # def test_locked(self):
    #     class An_Class(Type_Safe):
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
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")

        class An_Enum_A(Enum):
            an_value = 1

        class An_Class_A(Type_Safe):
            an_str : str = '42'
            an_int : int = 42
            an_list : list
            an_dict : dict
            an_enum : An_Enum_A = An_Enum_A.an_value

        an_class_dict = {'an_dict': {}, 'an_enum': 1, 'an_int': 42, 'an_list': [], 'an_str': '42'}
        an_class_a      = An_Class_A()
        assert an_class_a.serialize_to_dict() == an_class_dict

        obj_to_serialize = 3 + 4j                                   # A complex number which will not serialise
        # with self.assertRaises(TypeError) as context:
        #     serialize_to_dict(obj_to_serialize)
        # assert context.exception.args[0]  == "Type <class 'complex'> not serializable"            # Breaking change, we don't raise an exception any more in serialize_to_dict

        # NEW TEST: Complex numbers (unserializable) now return None instead of raising
        obj_to_serialize = 3 + 4j
        assert serialize_to_dict(obj_to_serialize) is None  # Graceful handling                     # now we just return None


        assert serialize_to_dict(TestCase) == 'unittest.case.TestCase'                  # types are supported

    def test_serialize_to_dict__enum(self):
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Type_Safe):
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
        assert an_class_dict      == {'an_enum': an_enum_value.value, 'an_str': an_str_value}
        assert an_class.json()    == an_class.serialize_to_dict()

        an_class_2 = An_Class()
        type_safe_step_from_json.deserialize_from_dict(an_class_2, an_class_dict)
        assert an_class_2.an_str  == an_class.an_str
        assert an_class_2.an_enum == an_class.an_enum
        assert an_class_2.json()  == an_class_dict


    def test_deserialize_from_dict(self):
        #check handing of enums
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Type_Safe):
            an_str  : str
            an_enum : An_Enum

        an_class_dict = {'an_enum': 2, 'an_str': ''}
        an_class      = An_Class()

        type_safe_step_from_json.deserialize_from_dict(an_class, an_class_dict)
        assert an_class.json() == an_class_dict

        #check handing of base classes
        class An_Base_Class(Type_Safe):
            in_base  : str

        class An_Parent_Class(An_Base_Class):
           in_parent : str

        an_parent_dict  = {'in_base': 'base', 'in_parent': 'parent'}
        an_parent_class = An_Parent_Class()
        type_safe_step_from_json.deserialize_from_dict(an_parent_class,an_parent_dict)
        assert an_parent_class.json() == an_parent_dict

        # check nested objects
        class An_Class_1(Type_Safe):
            in_class_1 : str

        class An_Class_2(Type_Safe):
            an_class_1 : An_Class_1
            in_class_2 : str

        an_class_1_dict = {'an_class_1': {'in_class_1': 'data_1'}, 'in_class_2': 'data_2'}
        an_class_2 = An_Class_2()
        type_safe_step_from_json.deserialize_from_dict(an_class_2, an_class_1_dict)
        assert an_class_2.json() == an_class_1_dict

        with Stdout() as stdout:
            an_class_2.print()
        assert stdout.value() == "\n{'an_class_1': {'in_class_1': 'data_1'}, 'in_class_2': 'data_2'}\n"

    def test_deserialize_from_dict__recursive(self):
        class An_Class_1(Type_Safe):
            in_class_1 : str        = 'data_1'

        class An_Class_2(Type_Safe):
            an_class_1 : An_Class_1
            in_class_2 : str        = 'data_2'

        class An_Class_3(Type_Safe):
            an_class_2 : An_Class_2
            in_class_3 : str        = 'data_3'

        class An_Class_4(Type_Safe):
            an_class_3 : An_Class_3
            in_class_4 : str        = 'data_4'

        an_class = An_Class_4()
        assert an_class.in_class_4                                  == 'data_4'
        assert an_class.an_class_3.in_class_3                       == 'data_3'
        assert an_class.an_class_3.an_class_2.in_class_2            == 'data_2'
        assert an_class.an_class_3.an_class_2.an_class_1.in_class_1 == 'data_1'

        assert an_class.json() == {'an_class_3': {'an_class_2': {'an_class_1': {'in_class_1': 'data_1'},
                                                                 'in_class_2': 'data_2'},
                                                  'in_class_3': 'data_3'},
                                   'in_class_4': 'data_4'}
        an_class__round_trip = An_Class_4.from_json(an_class.json())
        assert an_class__round_trip.in_class_4                                  == 'data_4'
        assert an_class__round_trip.an_class_3.in_class_3                       == 'data_3'
        assert an_class__round_trip.an_class_3.an_class_2.in_class_2            == 'data_2'
        assert an_class__round_trip.an_class_3.an_class_2.an_class_1.in_class_1 == 'data_1'
        assert an_class__round_trip.json()                                      == an_class.json()



    def test_from_json(self):
        class An_Enum(Enum):
            value_1 :str = 'value_1'
            value_2 :str = 'value_2'

        class An_Class(Type_Safe):
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
        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that needs FIXING on 3.8 or lower")

        _ = Type_Safe.__default__value__
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

        class An_Class(Type_Safe):
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
        expected_error = ("Catch: <class 'ValueError'> : Config_Class has no attribute 'extra_var' and "
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

        class Class_With_Types(Type_Safe):
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

        class An_Bad_Type(Type_Safe):
            not_an_int: int = "an str"

        expected_error= "On An_Bad_Type, invalid type for attribute 'not_an_int'. Expected '<class 'int'>' but got '<class 'str'>'"
        #with Catch(expect_exception=True, expected_error=expected_error):
        with pytest.raises(ValueError, match=expected_error ):
            An_Bad_Type().__default_kwargs__()

        expected_error = "On An_Bad_Type, invalid type for attribute 'not_an_int'. Expected '<class 'int'>' but got '<class 'str'>'"
        with pytest.raises(ValueError, match=expected_error ):
            An_Bad_Type().__default_kwargs__()

    # def test___init___disable_type_safety(self):
    #     assert self.Config_Class(                         ).__type_safety__ is True
    #     assert self.Config_Class(disable_type_safety=True ).__type_safety__ is False
    #     assert self.Config_Class(disable_type_safety=False).__type_safety__ is True


    def test___init___pics_up_types_with_values(self):

        class An_Class(Type_Safe):
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

    def test___init___prevents_new_attributes(self):
        with self.assertRaises(Exception) as context:
            self.Config_Class(aaaa=123)
        assert context.exception.args[0] == ("Config_Class has no attribute 'aaaa' and cannot be assigned the value '123'. "
                                             'Use Config_Class.__default_kwargs__() see what attributes are available')

    def test_merge_with(self):
        class Base_Class(Type_Safe):
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

    # not supported anymore (it was a good idea, but this is better done with set_as_property)
    # def test___supports_automatic_getters_and_setters_for_attributes(self):
    #     class An_Class(Type_Safe):
    #         an_str   : str
    #         an_int   : int
    #         an_list  : list
    #         _private : str  # Test private attribute behavior
    #
    #     an_class = An_Class()
    #
    #     # Test basic getter/setter functionality
    #     assert an_class.set_an_str('abc') == an_class
    #     assert an_class.get_an_str() == 'abc'
    #     assert an_class.json() == {'an_int': 0, 'an_list': [], 'an_str': 'abc', '_private': ''}
    #
    #     # Test method chaining
    #     assert an_class.set_an_int(123).set_an_str('def').get_an_str() == 'def'
    #     assert an_class.get_an_int() == 123
    #
    #     # Test list attribute
    #     test_list = [1, 2, 3]
    #     assert an_class.set_an_list(test_list) == an_class
    #     assert an_class.get_an_list() == test_list
    #
    #     # Test None assignments
    #     with pytest.raises(ValueError, match="Can't set None, to a variable that is already set. Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'NoneType'>'"):
    #         assert an_class.set_an_str(None) == an_class
    #     assert an_class.get_an_str() == 'def'                           # confirm value has not been changed
    #
    #     # Test private attribute access
    #     assert an_class.set__private("secret") == an_class
    #     assert an_class.get__private() == "secret"
    #
    #     # Test error cases
    #     with pytest.raises(AttributeError, match="'An_Class' object has no attribute 'set_an_aaa'"):
    #         an_class.set_an_aaa()
    #     with pytest.raises(AttributeError, match="'An_Class' object has no attribute 'get_an_aaa'"):
    #         an_class.get_an_aaa()
    #     with pytest.raises(AttributeError, match="'An_Class' object has no attribute 'aaaaaaaaaa'"):
    #         an_class.aaaaaaaaaa()
    #     with pytest.raises(ValueError, match="Invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'int'>"):
    #         an_class.set_an_str(123)
    #     with pytest.raises(ValueError, match="Invalid type for attribute 'an_int'. Expected '<class 'int'>' but got '<class 'str'>"):
    #         an_class.set_an_int('abc')
    #
    #     # Test edge cases
    #     with pytest.raises(AttributeError):
    #         an_class.get_()  # Empty attribute name
    #     with pytest.raises(AttributeError):
    #         an_class.set_()  # Empty attribute name

    def test__type_assignments_and_validation(self):        # Test simple type assignment with 'type' annotation
        class Simple_Type(Type_Safe):
            type_field: type = str                          # Now allowed

        simple = Simple_Type()
        assert simple.type_field == str
        simple.type_field = int                             # Can change to another type
        assert simple.type_field == int

        class Constrained_Type(Type_Safe):                  # Test Type[T] with specific type constraint
            str_type    : Type[str] = str                   # OK: str is instance of Type[str]
            number_type : Type[int] = int                   # OK: int is instance of Type[int]

        constrained = Constrained_Type()
        assert constrained.str_type == str
        assert constrained.number_type == int

        class Type_Safety(Type_Safe):                       # Test type safety with Type[T]
            str_type: Type[str]

        type_safety = Type_Safety()
        type_safety.str_type = str                          # OK: str matches Type[str]

        with pytest.raises(ValueError, match=re.escape("On Type_Safety, invalid type for attribute 'str_type'. Expected 'typing.Type[str]' but got '<class 'int'>'")):    # Should fail: int is not a subclass of str
            type_safety.str_type = int


        # Test nested types
        class Nested_Valid(Type_Safe):
            class Inner(Type_Safe):
                type_field: Type[str] = str          # Now valid
            nested: Inner

        nested = Nested_Valid()
        assert nested.nested.type_field == str

        # Test None assignments
        class Optional_Type(Type_Safe):
            type_field: Optional[Type[str]] = None   # None should be allowed for Optional

        optional = Optional_Type()
        assert optional.type_field is None
        optional.type_field = str                    # Can set to valid type
        assert optional.type_field == str

    def test__support_types_in_json(self):
        class An_Class(Type_Safe):
            an_type: type

        an_class = An_Class()
        an_class.an_type = str

        an_class.an_type = type(TestCase)
        an_class.an_type = int

        assert 0         == default_value(an_class.an_type)
        assert 123       == an_class.an_type(123)
        assert an_class.json() == {'an_type': 'builtins.int'}

        assert An_Class.from_json(an_class.json()).json() == an_class.json()


    def test_type_serialization(self):
        class Type_Test_Class(Type_Safe):
            builtin_type    : type
            custom_type     : type
            none_type       : type

        # Test serialization of built-in types
        test_obj              = Type_Test_Class()
        test_obj.builtin_type = str
        assert test_obj.json() == {'builtin_type'   : 'builtins.str',
                                   'custom_type'    : None          ,
                                   'none_type'      : None          }


        # Test deserialization of built-in types
        restored = Type_Test_Class.from_json(test_obj.json())
        assert restored.builtin_type == str
        assert restored.json()       == test_obj.json()

        # Test multiple built-in types
        builtin_types = [int, float, bool, list, dict, set, tuple]
        for type_to_test in builtin_types:
            test_obj.builtin_type = type_to_test
            json_data = test_obj.json()
            assert json_data['builtin_type'] == f'builtins.{type_to_test.__name__}'
            restored = Type_Test_Class.from_json(json_data)
            assert restored.builtin_type == type_to_test

        # Test custom class types (that don't inherit from Type_Safe)

        test_obj.custom_type = Custom_Class
        json_data = test_obj.json()

        assert json_data['custom_type'] == f'{Custom_Class.__module__}.Custom_Class'
        error_message = "Module 'test_Type_Safe' is not in allowed modules and 'Custom_Class' does not inherit from Type_Safe. Allowed modules: ['builtins', 'collections', 'collections.abc', 'datetime', 'decimal', 'enum', 'osbot_utils.type_safe', 'osbot_utils.type_safe.primitives', 'types', 'typing']"
        with pytest.raises(ValueError, match=re.escape(error_message)):
             Type_Test_Class.from_json(json_data)             # before security fix, this worked

        # Test custom class types (that inherit from Type_Safe)

        test_obj.custom_type = Custom_Class__Type_Safe
        json_data = test_obj.json()

        assert json_data['custom_type'] == f'{Custom_Class__Type_Safe.__module__}.Custom_Class__Type_Safe'

        restored = Type_Test_Class.from_json(json_data)
        assert restored.custom_type == Custom_Class__Type_Safe

    def test_type_serialization__lists(self):
        class Type_Test_Class(Type_Safe):
            builtin_type    : type
            collection_type : type

        test_obj = Type_Test_Class()

        from typing import List                                   # Test collection types from typing module
        test_obj.collection_type = List

        json_data = test_obj.json()

        assert json_data['collection_type'] == 'builtins.list'

        restored = Type_Test_Class.from_json(json_data)
        assert restored.collection_type == list                             # the roundtrip is list not List

        # Test type safety
        with self.assertRaises(ValueError):
            test_obj.builtin_type = "not a type"

        # Test None handling
        test_obj.builtin_type = None
        json_data = test_obj.json()
        assert json_data['builtin_type'] is None
        restored = Type_Test_Class.from_json(json_data)
        assert restored.builtin_type is None

    def test_nested_type_serialization(self):
        class Nested_Type_Class(Type_Safe):
            outer_type: type
            inner_type: type

        class Container_Class(Type_Safe):
            nested: Nested_Type_Class

        # Test nested type serialization
        nested = Nested_Type_Class()
        nested.outer_type = list
        nested.inner_type = str
        container = Container_Class(nested=nested)

        json_data = container.json()
        assert json_data == {
            'nested': {
                'outer_type': 'builtins.list',
                'inner_type': 'builtins.str'
            }
        }

        # Test nested type deserialization
        restored = Container_Class.from_json(json_data)
        assert restored.nested.outer_type == list
        assert restored.nested.inner_type == str
        assert restored.json() == json_data

    def test_type_edge_cases(self):
        if sys.version_info < (3, 10):
            pytest.skip("Skipping test that doesn't work on 3.9 or lower")
            
        class Edge_Cases(Type_Safe):
            type_field: type

        test_obj = Edge_Cases()

        # Test type of type
        test_obj.type_field = type
        json_data = test_obj.json()
        assert json_data['type_field'] == 'builtins.type'
        restored = Edge_Cases.from_json(json_data)
        assert restored.type_field == type

        test_obj.type_field = type(None)                                # Test type of None
        json_data = test_obj.json()
        # if sys.version_info >= (3, 10):
        #     expected_type = 'types.NoneType'
        # else:
        #     expected_type = 'builtins.NoneType'
        expected_type = 'builtins.NoneType'
        assert json_data['type_field'] == expected_type

        restored = Edge_Cases.from_json(json_data)
        assert restored.type_field == type(None)

        # Test with exception types
        test_obj.type_field = ValueError
        json_data = test_obj.json()
        assert json_data['type_field'] == 'builtins.ValueError'
        restored = Edge_Cases.from_json(json_data)
        assert restored.type_field == ValueError

        # Test with only a null value
        class An_Class(Type_Safe):
            an_type    : type

        an_class = An_Class()

        assert an_class.from_json(an_class.json()).json() == {'an_type': None}


    def test_error_cases(self):
        class Error_Test(Type_Safe):
            type_field: type

        Error_Test()

        invalid_json = {'type_field': 'nonexistent_module.SomeType'}                            # Test 1: Module not in allow listed (security check)
        error_message = "Could not import module 'nonexistent_module': No module named 'nonexistent_module'"
        with pytest.raises(ValueError, match=error_message):
            Error_Test.from_json(invalid_json)

        invalid_json = {'type_field': 'builtins.NonexistentType'}                               # Test 2: Invalid type in valid module (type doesn't exist)
        error_message = "Type 'NonexistentType' not found in module 'builtins'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Error_Test.from_json(invalid_json)

        invalid_json = {'type_field': 'not_a_valid_type_string'}                                # Test 3: Malformed type string (missing module)
        error_message = "Type reference must include module"
        with pytest.raises(ValueError, match=error_message):
            Error_Test.from_json(invalid_json)

        invalid_json = {'type_field': 'module..DoubleDotsType'}                                 # Test 4: Invalid format with special characters
        error_message = "Invalid type reference format"
        with pytest.raises(ValueError, match=error_message):
            Error_Test.from_json(invalid_json)

        invalid_json = {'type_field': 'builtins.eval'}                                          # Test 5: Dangerous/deny listed type
        error_message = "Type 'eval' is deny listed"
        with pytest.raises(ValueError, match=error_message):
            Error_Test.from_json(invalid_json)

    def test__type_serialization__typing_objects(self):
        class An_Class(Type_Safe):
            an_type : type

        an_class = An_Class()
        an_class.an_type = str                              # these work ok
        an_class.an_type = An_Class
        an_class.an_type = TestCase
        an_class.an_type = set
        an_class.an_type = list
        an_class.an_type = dict
        assert an_class.json()                            == {'an_type': 'builtins.dict'}
        assert An_Class.from_json(an_class.json()).json() == {'an_type': 'builtins.dict'}

        from typing import List, Dict, Set

        class An_Typing_Class(Type_Safe):
            an_dict: type
            an_list: type
            an_set : type

        with An_Typing_Class() as _:
            assert _.obj() == __(an_dict=None, an_list=None, an_set=None)
            _.an_dict = Dict
            _.an_list = List
            _.an_set  = Set
            assert _.json() == {'an_dict': 'builtins.dict', 'an_list': 'builtins.list', 'an_set': 'builtins.set'}
            assert An_Typing_Class.from_json(_.json()).json() == _.json()
            round_trip = An_Typing_Class.from_json(_.json())
            assert default_value(round_trip.an_dict) == {}
            assert default_value(round_trip.an_list) == []
            assert default_value(round_trip.an_set ) == set()

    def test__type__with_type__are_enforced__and_default_is_type(self):
        class An_Class(Type_Safe):
            an_type_str: Type[str]
            an_type_int: Type[int]

        class Random_Guid__Extra(Random_Guid):
            pass

        class Timestamp_Now__Extra(Timestamp_Now):
            pass

        an_class = An_Class()
        assert an_class.an_type_str is str
        assert an_class.an_type_int is int
        an_class.an_type_str = str
        an_class.an_type_int = int
        an_class.an_type_str = Guid
        an_class.an_type_str = Random_Guid
        an_class.an_type_str = Random_Guid__Extra
        an_class.an_type_int = Timestamp_Now
        an_class.an_type_int = Timestamp_Now__Extra

        class An_Class_1(Type_Safe):
            an_guid      : Type[Guid]
            an_time_stamp: Type[Timestamp_Now]

        assert An_Class_1().json() == {'an_guid'      : 'osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid'                            ,
                                       'an_time_stamp': 'osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now.Timestamp_Now' }

    def test_type_checks_on__forward_ref__works_on_multiple_levels(self):
        class An_Class(Type_Safe):
            node_type: Type['An_Class']

        class Child_Type_1(An_Class):
            pass

        class Child_Type_2(Child_Type_1):
            pass

        class Child_Type_3(Child_Type_2):
            pass

        class Child_Type_4(Child_Type_3):
            pass

        class Should_Fail(Type_Safe):
            pass

        An_Class(node_type=An_Class    )                                                   # works
        An_Class(node_type=Child_Type_1)                                                   # works
        An_Class(node_type=Child_Type_2)
        An_Class(node_type=Child_Type_3)
        An_Class(node_type=Child_Type_4)

        error_message = "On An_Class, invalid type for attribute 'node_type'. Expected 'typing.Type[ForwardRef('An_Class')]' but got '<class 'test_Type_Safe.test_Type_Safe.test_type_checks_on__forward_ref__works_on_multiple_levels.<locals>.Should_Fail'>'"
        with pytest.raises(ValueError,match=re.escape(error_message)):
            An_Class(node_type=Should_Fail)

        assert issubclass(Child_Type_1, An_Class)
        assert issubclass(Child_Type_2, An_Class)
        assert issubclass(Child_Type_3, An_Class)
        assert issubclass(Child_Type_4, An_Class)


    def test_property_descriptor_behaviour(self):                                           # Test that confirms that property descriptors work correctly in Type_Safe classes

        value_captured = None                                                               # Variable to capture setter values
        getter_calls   = 0                                                                  # Counter for getter calls
        setter_calls   = 0                                                                  # Counter for setter calls

        class Test_Class(Type_Safe):
            data: str = "base_data"                                                         # Normal Type_Safe attribute

            def __init__(self):
                super().__init__()
                self._label = "initial_value"                                               # Initialize backing field

            @property
            def label(self):
                nonlocal getter_calls
                getter_calls += 1
                return self._label

            @label.setter
            def label(self, value):
                nonlocal setter_calls, value_captured
                setter_calls += 1
                value_captured = value
                self._label = value

        test_class = Test_Class()
        assert getter_calls     == 0, "Getter should not be called during initialization"           # Test initialization
        assert setter_calls     == 0, "Setter should not be called during initialization"
        assert test_class.obj() == __(data='base_data', _label='initial_value')

        assert test_class.label == "initial_value"                                                  # Test getter
        assert getter_calls     == 1, "Getter should be called exactly once"

        test_class.label = "new_value"                                                              # Test setter
        assert setter_calls     == 1, "Setter should be called exactly once"
        assert value_captured   == "new_value"
        assert test_class.label == "new_value"
        assert getter_calls     == 2, "Getter should be called twice now"

        assert test_class.obj() == __(data='base_data', _label='new_value')

        assert isinstance(getattr(Test_Class, 'label'), property)                                   # Verify property descriptor remains intact

        test_class.label = "another_value"                                                          # Test that property still works with multiple updates
        assert setter_calls     == 2
        assert test_class.label == "another_value"
        assert getter_calls     == 3

        assert test_class.obj() == __(data='base_data', _label='another_value')

        with pytest.raises(ValueError, match="On Test_Class, invalid type for attribute 'data'. Expected '<class 'str'>' but got '<class 'int'>'"):
            test_class.data = 123                                                                   # confirm that type safety is still working on the main class

    def test_validate_type_immutability(self):                                        # Tests type immutability validation
        # class Simple_Type(Type_Safe):
        #     valid_int   : int        = 42                                            # valid immutable type
        #     valid_str   : str        = 'abc'                                         # valid immutable type
        #     valid_bool  : bool       = True                                          # valid immutable type
        #     valid_tuple : tuple      = (1,2)                                         # valid immutable type
        #
        # simple = Simple_Type()                                                       # Should work fine with valid types
        # assert simple.valid_int   == 42
        # assert simple.valid_str   == 'abc'
        # assert simple.valid_bool  == True
        # assert simple.valid_tuple == (1,2)

        with pytest.raises(ValueError, match= "variable 'invalid_list' is defined as type '<class 'list'>' which is not supported by Type_Safe" ):                                    # Test invalid mutable type
            class Invalid_Type(Type_Safe):
                invalid_list: list  = ['a', 'b']                                     # list is not in IMMUTABLE_TYPES
            Invalid_Type()

        class Union_Types(Type_Safe):                                                # Test union types compatibility
            optional_int : Optional[int] = None                                      # Should work as Optional is handled
            union_types  : Union[str, int] = "test"                                  # Should work as Union is handled

        union = Union_Types()
        assert union.optional_int is None
        assert union.union_types == "test"

    def test_validate_type_immutability_with_enums(self):                           # Tests enum validation in Type_Safe
        class An_Enum(Enum):
            VALUE_1 = "value_1"
            VALUE_2 = "value_2"

        class With_Enum(Type_Safe):
            enum_var     : An_Enum                                                  # enum without default
            enum_default : An_Enum = An_Enum.VALUE_1                               # enum with default

        test_obj = With_Enum()
        assert test_obj.enum_default == An_Enum.VALUE_1                            # check default assignment

        test_obj.enum_var = An_Enum.VALUE_2                                        # check assignment
        assert test_obj.enum_var == An_Enum.VALUE_2

        with pytest.raises(ValueError, match="On With_Enum, invalid type for attribute 'enum_var'. Expected '<enum 'An_Enum'>' but got '<class 'str'>'") as context:                    # validate type safety
            test_obj.enum_var = "VALUE_2"                                          # try to assign string instead of enum

        # Test with Optional enum
        class With_Optional_Enum(Type_Safe):
            optional_enum: Optional[An_Enum] = None                                # Optional enum should work

        optional_test = With_Optional_Enum()
        assert optional_test.optional_enum is None
        optional_test.optional_enum = An_Enum.VALUE_1                               # can assign enum value
        assert optional_test.optional_enum == An_Enum.VALUE_1

    def test_serialize_to_dict__unserializable_types_return_none(self):             #  Test that unserializable types return None instead of raising exceptions


        # Complex numbers - not serializable
        assert serialize_to_dict(3 + 4j) is None

        # Threading primitives - not serializable
        lock = threading.RLock()
        assert serialize_to_dict(lock) is None


        # File handles - also serializable :)
        import io
        file_obj = io.StringIO()
        assert serialize_to_dict(file_obj) == {}

        # Thread are also serializable now :)
        thread = threading.Thread(target=lambda: None)
        assert obj(serialize_to_dict(thread)) == __( _target = '<lambda>',
                                                     _name   = __SKIP__  ,          # this has a different value when running with all tests
                                                     _args=[],
                                                     _kwargs=__(),
                                                     _daemonic=False,
                                                     _ident=None,
                                                     _native_id=None,
                                                     _tstate_lock=None,
                                                     _started=__(_cond=__(_lock=None,
                                                                          acquire='acquire',
                                                                          release='release',
                                                                          _waiters=None),
                                                                 _flag=False),
                                                     _is_stopped=False,
                                                     _initialized=True,
                                                     _stderr=__(),
                                                     _invoke_excepthook='invoke_excepthook')


    def test_serialize_to_dict__mixed_serializable_and_unserializable(self):        # Test objects with both serializable and unserializable attributes
        import threading

        class MixedObject:
            def __init__(self):
                self.name = "test"
                self.count = 42
                self._lock = threading.RLock()  # Unserializable
                self.active = True

        mixed_obj = MixedObject()
        result = serialize_to_dict(mixed_obj)

        # Should contain serializable fields
        assert result['name'] == "test"
        assert result['count'] == 42
        assert result['active'] is True

        # Unserializable field should be None
        assert result['_lock'] is None

        assert obj(result) == __(name   = 'test',
                                 count  = 42    ,
                                 _lock  = None  ,  # None, because threading.RLock() is not serializable
                                 active = True  )

        # check with Type_Safe objects
        class Mixed_Object_2(Type_Safe):
            name  : str             = "test"
            count : int             = 42
            _lock : RLock           = None                          # threading.RLock() will return an _thread._lock object
            active: bool            = True

        assert Mixed_Object_2().obj()                                  == __(name='test', count=42, _lock=None, active=True)
        assert Mixed_Object_2(_lock= threading.RLock()).obj()          == __(name='test', count=42, _lock=None, active=True)
        assert Mixed_Object_2.from_json(Mixed_Object_2().json()).obj() == __(name='test', count=42, _lock=None, active=True)



    def test_serialize_to_dict__nested_unserializable(self):        # Test nested structures containing unserializable objects

        mixed_list = [1, "two", threading.RLock(), 3.14]            # List with mixed content
        result     = serialize_to_dict(mixed_list)

        assert result == [1, "two", None, 3.14]

        # Dict with unserializable values
        mixed_dict = { 'good': 123                  ,
                        'bad': threading.RLock()    ,
                        'ugly': 3 + 4j              }

        result = serialize_to_dict(mixed_dict)
        assert result['good'] == 123
        assert result['bad' ] is None
        assert result['ugly'] is None

    def test_type_safe_roundtrip_with_unserializable_infrastructure(self):      # Test that Type_Safe objects round-trip correctly even with unserializable __dict__ entries
        class ServiceClient(Type_Safe):
            base_url: str = "http://localhost"
            timeout: int = 30
            retries: int = 3

        # Create instance and add unserializable infrastructure
        client       = ServiceClient(base_url="http://api.example.com", timeout=60)
        client._lock = threading.RLock()  # Simulate infrastructure added by library
        client._pool = threading.Semaphore(5)  # More infrastructure

        # Serialize (should handle unserializable gracefully)
        json_data = client.json()

        assert json_data == {'_lock': None,
                             '_pool': {'_cond': {'_lock': None,
                                                 '_waiters': None,
                                                 'acquire': 'acquire',
                                                 'release': 'release'},
                                       '_value': 5},
                             'base_url': 'http://api.example.com',
                             'retries': 3,
                             'timeout': 60}

        # Round-trip should work perfectly
        client2 = ServiceClient.from_json(json_data)
        assert client2.base_url == "http://api.example.com"
        assert client2.timeout == 60
        assert client2.retries == 3

        assert ServiceClient.from_json(json_data).json() == {'base_url': 'http://api.example.com',      # round trip doesn't add _.pool or _lock because they are not in the ServiceClient class definition
                                                             'retries': 3,
                                                             'timeout': 60}

    def test_serialize_to_dict__deeply_nested_unserializable(self):                          # Test deeply nested structures with unserializable objects at various levels
        nested = {
            'level1': {
                'level2': {
                    'good_data': [1, 2, 3],
                    'bad_data': threading.RLock(),
                    'level3': {
                        'more_good': "hello",
                        'more_bad': 3 + 4j
                    }
                }
            }
        }

        result = serialize_to_dict(nested)

        # Verify structure is preserved
        assert result['level1']['level2']['good_data'] == [1, 2, 3]
        assert result['level1']['level2']['bad_data'] is None
        assert result['level1']['level2']['level3']['more_good'] == "hello"
        assert result['level1']['level2']['level3']['more_bad'] is None

    def test_type_safe_with_unserializable_in_list(self):                   # Test Type_Safe objects with lists containing unserializable items
        class TaskQueue(Type_Safe):
            name : str  = "default"
            tasks: list

        queue = TaskQueue(name="worker_queue")
        # Simulate adding tasks with some unserializable items
        queue.tasks = [ {'id': 1, 'data': 'task1'          },
                        {'id': 2, 'lock': threading.RLock()},  # Has unserializable field
                        {'id': 3, 'data': 'task3'          }]

        json_data = queue.json()

        # Should serialize with None for unserializable field
        assert json_data['name'] == 'worker_queue'
        assert json_data['tasks'][0] == {'id': 1, 'data': 'task1'}
        assert json_data['tasks'][1] == {'id': 2, 'lock': None}
        assert json_data['tasks'][2] == {'id': 3, 'data': 'task3'}

    def test_serialize_to_dict__unserializable_in_type_safe_dict(self):     # Test Type_Safe__Dict with unserializable values"""

        # Create a Type_Safe__Dict
        config_dict = Type_Safe__Dict(expected_key_type=str, expected_value_type=object)
        config_dict['host'] = 'localhost'
        config_dict['port'] = 8080
        config_dict['_internal_lock'] = threading.RLock()

        result = config_dict.json()

        # Serializable values should be present
        assert result['host'] == 'localhost'
        assert result['port'] == 8080
        # Unserializable value should be None
        # assert result['_internal_lock']       is not None                               # BUG this should be either be None of a valid json value (i.e. string, int, etc..)
        # assert type(result['_internal_lock']) is RLock                                  # BUG since .json() should not return an invalid json file
        # assert result['_internal_lock']       == config_dict['_internal_lock']          # BUG:
        # assert result == { '_internal_lock':config_dict['_internal_lock'],              # BUG
        #                    'host'          : 'localhost'                 ,
        #                    'port'          : 8080                        }
        assert result['_internal_lock']       is None                                     # FIXED: BUG this should be either be None of a valid json value (i.e. string, int, etc..)
        assert type(result['_internal_lock']) is types.NoneType                           # FIXED: BUG since .json() should not return an invalid json file
        assert result == { '_internal_lock': None                        ,                # FIXED: BUG
                           'host'          : 'localhost'                 ,
                           'port'          : 8080                        }


    def test_print_obj_with_unserializable_fields(self):                    # Test that print_obj() works even with unserializable fields
        class ClientWithInfrastructure(Type_Safe):
            url   : str = "http://localhost"
            active: bool = True

        client            = ClientWithInfrastructure()
        client._lock      = threading.RLock()
        client._semaphore = threading.Semaphore(3)

        # These should not raise exceptions

        with Stdout() as stdout:
            client.print_obj()
        assert stdout.value() == ('\n'
                                  "__(url='http://localhost',\n"
                                  '   active=True,\n'
                                  '   _lock=None,\n'
                                  '   _semaphore=__(_cond=__(_lock=None,\n'
                                  "                          acquire='acquire',\n"
                                  "                          release='release',\n"
                                  '                          _waiters=None),\n'
                                  '                 _value=3))\n')
        client.json()           # Should work
        client_obj = client.obj()  # Should work

        assert client_obj.url == "http://localhost"
        assert client_obj.active is True
        assert client_obj == __(url='http://localhost',
                                active=True,
                                _lock=None,                                             # _.lock doesn't serialise
                                _semaphore=__(_cond=__(_lock=None,
                                                       acquire='acquire',
                                                       release='release',
                                                       _waiters=None),
                                              _value=3))

    def test_serialize_to_dict__custom_objects_without_dict(self):                                      # Test objects that aren't serializable and don't have __dict__
        sock = socket.socket()                                                                          # Socket objects don't have __dict__ and aren't serializable
        assert serialize_to_dict(sock) is None
        sock.close()

    def test_type_safe_nested_with_unserializable(self):                                                # Test nested Type_Safe objects where some have unserializable infrastructure

        class Connection(Type_Safe):
            host: str = "localhost"
            port: int = 5432

        class Database(Type_Safe):
            name: str = "testdb"
            connection: Connection = None

        # Create instances with infrastructure
        conn = Connection(host="db.example.com", port=5432)
        conn._socket_lock = threading.RLock()

        db = Database(name="production", connection=conn)
        db._pool_lock = threading.RLock()

        # Should serialize and round-trip correctly
        json_data = db.json()
        assert json_data == { '_pool_lock': None,
                              'connection': {'_socket_lock': None, 'host': 'db.example.com', 'port': 5432},
                              'name'      : 'production'}

        # Round-trip
        db2 = Database.from_json(json_data)
        assert db2.name == "production"
        assert db2.connection.host == "db.example.com"
        assert db2.connection.port == 5432

class Custom_Class():         # used in test_type_serialization
    pass

class Custom_Class__Type_Safe(Type_Safe):         # used in test_type_serialization
    pass