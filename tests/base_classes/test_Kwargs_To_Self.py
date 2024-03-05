import types
import unittest
from enum import Enum, auto
from unittest import TestCase
from unittest.mock import patch, MagicMock

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.testing.Catch                  import Catch
from osbot_utils.utils.Dev                      import pprint
from osbot_utils.utils.Misc import random_string, list_set
from osbot_utils.utils.Objects import obj_info, obj_data, default_value


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

    def test_serialize_to_dict(self):
        class An_Enum(Enum):
            value_1 = auto()
            value_2 = auto()

        class An_Class(Kwargs_To_Self):
            an_str  : str
            an_enum : An_Enum

        an_class = An_Class()
        assert an_class.serialize_to_dict() == {'an_enum': None, 'an_str': ''}
        an_class.an_enum = An_Enum.value_1
        assert an_class.serialize_to_dict() == {'an_enum': 'value_1', 'an_str': ''}

    def test__correct_attributes(self):
        """ Test that correct attributes are set from kwargs. """
        config = self.Config_Class(attribute1='new_value', attribute2=False)
        self.assertEqual(config.attribute1, 'new_value')
        self.assertFalse(config.attribute2)

    def test__kwargs__(self):
        assert self.Config_Class().__kwargs__() == { 'attribute1'     : 'default_value',
                                                     'attribute2'     : True           ,
                                                     'callable_attr_1': print          }

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




    def test__test_leakage_between_two_instances(self):
        config_1 = self.Config_Class()
        config_2 = self.Config_Class()

        assert config_1.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert config_2.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print}

        assert obj_data(config_1) == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': f"{print}" }        # obj_doesn't pick up functions (unless explicity told to)
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
        assert config_2.__default_kwargs__() == default_kwargs  # __default_kwargs__ should not been affeced
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

        # this is bug since locals should have all vars
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
        with Catch(expect_exception=True, expected_error=expected_error) as catch:
            An_Bad_Type().__default_kwargs__()

        expected_error = "Catch: <class 'Exception'> : variable 'not_an_int' is defined as type '<class 'int'>' but has value 'an str' of type '<class 'str'>'"
        with Catch(expect_exception=True, expected_error=expected_error):
            An_Bad_Type().__default_kwargs__()

    def test___init__pics_up_types_with_values(self):

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
                        "with only the following imumutable types being supported: "
                        "'(<class 'bool'>, <class 'int'>, <class 'float'>, <class 'complex'>, <class 'str'>, "
                        "<class 'tuple'>, <class 'frozenset'>, <class 'bytes'>, <class 'NoneType'>, <class 'enum.EnumType'>)'")
        with Catch(expect_exception=True, expected_error = expected_error) as catch:
            An_Class()

        class An_Class_2(Kwargs_To_Self):
            attribute_8 : dict = {}

        expected_error=("Catch: <class 'Exception'> : variable 'attribute_8' is defined "
                        "as type '<class 'dict'>' which is not supported by Kwargs_To_Self, "
                        "with only the following imumutable types being supported: "
                        "'(<class 'bool'>, <class 'int'>, <class 'float'>, <class 'complex'>, <class 'str'>, "
                        "<class 'tuple'>, <class 'frozenset'>, <class 'bytes'>, <class 'NoneType'>, <class 'enum.EnumType'>)'")
        with Catch(expect_exception=True, expected_error=expected_error):
            An_Class_2()


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






    # test BUGS and REGRESSION TESTS


    def test__regression__default_value_is_not_cached(self):                    # FIXED: this is a test that confirms a BUG the currently exists in the default_value method

        class An_Class(Kwargs_To_Self):
            test_case : TestCase
        with patch('osbot_utils.base_classes.Kwargs_To_Self.default_value') as patched_default_value:
            patched_default_value.side_effect = default_value                   # make sure that the main code uses the original method (i.e. not the patched one)
                                                                                #       since all we need is the ability to count how many times the method was called
            an_class = An_Class()                                               # create instance of class (which will call default_value via __default__kwargs__)
            assert patched_default_value.call_count == 1                        # expected result, since we used the default_value to create an instance of TestCase
            test_case = an_class.__locals__().get('test_case')                  # get a reference of that object (which (BUG) will also call default_value)
            assert test_case                         is not None                # make sure var that is set
            assert type(test_case)                   == TestCase                #       and that is the correct type
            assert patched_default_value.call_count  == 1 # was 2               # FIXED - BUG: we shouldn't see another call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # confirm that although there was a call to default_value, it's value was not used
            assert patched_default_value.call_count  == 1 # was 3               # FIXED -BUG: again we should not see a call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # just to double-check the behaviour/bug we are seeing
            assert patched_default_value.call_count  == 1 # was 4               # FIXED -BUG: this should be 1 (since we should only create the object once via default_value)
            assert default_value(TestCase).__class__ is TestCase                # confirm that a direct call to default_value does create an instance of TestCase
            assert default_value(TestCase)           is not test_case           # confirm that default_value object doesn't match the one we got originally
            assert TestCase()                        is not TestCase()          # double check that TestCase() creates a new object every time
            assert test_case                         is test_case               # confirm that the 'is' operator is the one correct one to check equality
            assert test_case                         == test_case               # confirm that we can't use == (i.e. __eq__) for equality
            assert TestCase()                        == TestCase()              #       since this should be False (i.e. two new instances of TestCase)

    def test__regression__type_safety_race_condition_on_overloaded_vars(self):

        class Base_Class                       :  pass                         # a base class
        class Implements_Base_Class(Base_Class): pass                          # is used as a base class here
        class An_Class(Kwargs_To_Self):                                        # now when a new class
            an_var: Base_Class                                                 # creates a var using the base class
        class Extends_An_Class(An_Class):                                      # and another class uses it has a base class
            an_var: Implements_Base_Class                                      # and changes the type to a compatible type
                                                                               #   we will get an exception, because Kwargs_To_Self creates
                                                                               #   a new object of type Base_Class when it should create
                                                                               #   a new object of type Implements_Base_Class

        Base_Class()                                                           # this works ok
        Implements_Base_Class()                                                # this works ok
        An_Class()                                                             # this works ok (with an_var = Base_Class() )
        Extends_An_Class()                                                     # FIXED: this works now (with an_var = Implements_Base_Class() )

        assert type(An_Class()        .an_var) is Base_Class                  # just confirming an_var is Base_Class
        assert type(Extends_An_Class().an_var) is Implements_Base_Class       # just confirming an_var is now Implements_Base_Class

        # with self.assertRaises(Exception) as context:                       # BUG: this now will fail
        #     Extends_An_Class()                                              # BUG: due to a bug in type safety logic Kwargs_To_Self
        #
        # assert str(context.exception) == ("Invalid type for attribute 'an_var'. Expected '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Implements_Base_Class'>' "
        #                                  "but got '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Base_Class'>'")

    def test__regression__type_safety_bug__in___cls_kwargs__(self):
        class Base_Class                           : pass                                  # set of classes that replicate the bug
        class Implements_Base_Class(Base_Class    ): pass                                  # which happens when we have a base class
        class An_Class             (Kwargs_To_Self): an_var: Base_Class                    # and a class that uses it as a var
        class Extends_An_Class     (An_Class      ):an_var: Implements_Base_Class          # and another class that extends it and changes the type

        an_class__cls_kwargs__         = An_Class        .__cls_kwargs__()                 # the bug in __cls_kwargs__() so lets get its output for both
        extends_an_class__cls_kwargs__ = Extends_An_Class.__cls_kwargs__()                 # An_Class and Extends_An_Class
        assert list_set(an_class__cls_kwargs__        )           == ['an_var']            # confirm that the only var created and assigned
        assert list_set(extends_an_class__cls_kwargs__)           == ['an_var']            # the 'an_var' one
        assert type(an_class__cls_kwargs__        .get('an_var')) == Base_Class            # this is ok since the an_var in An_Class should be Base_Class
        assert type(extends_an_class__cls_kwargs__.get('an_var')) == Implements_Base_Class # FIXED: BUG: since an_var in Extends_An_Class should be Implements_Base_Class



    def test__regression__cast_issue_with_base_class_mode_a(self):                   # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_A(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                self.__dict__ = target.__dict__
                return self

        base_class = Base_Class()                                                    # create an object of Base_Class base class
        assert list_set(base_class.__kwargs__())  == ['an_int']                      # confirm that it has the expected vars
        assert base_class.an_int                  == 42                              # confirm that an_int was correct set via Kwargs_To_Self
        cast_mode_a = Cast_Mode_A()                                                  # create an object of Cast_Mode_A class
        assert list_set(cast_mode_a.__kwargs__()) == ['an_int', 'an_str']            # confirm that it has the vars from Base_Class and Cast_Mode_A
        assert cast_mode_a.an_int                 == 42                              # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_a.an_str                 == 'abc'                           # confirm that an_str was correctly set via Kwargs_To_Self

        base_class.an_int                          = 123                             # now change the value of base_class.an_int
        assert base_class.an_int                  == 123                             # confirm it has been changed correctly
        cast_mode_a_from_base_class                = Cast_Mode_A().cast(base_class)  # now create a new object of Cast_Mode_A and cast it from base_class
        assert cast_mode_a_from_base_class.an_int == 123                             # confirm that an_int was the new object picked up the new value (via cast)

        cast_mode_a_from_base_class.an_int         = 456                             # now change the an_int on the new class
        assert cast_mode_a_from_base_class.an_int == 456                             # and confirm that the value has been changed correctly in the 'casted' object
        assert base_class.an_int                  == 456                             # and confirm that it also was changed in the original object (i.e. base_class)

        # the example above is the exact behaviour which replicates the 'cast' operation in other languages (i.e. C#), where
        #       cast_mode_a_from_base_class = Cast_Mode_A().cast(base_class)
        # is equivalent to
        #       cast_mode_a_from_base_class = (Cast_Mode_A) base_class
        assert cast_mode_a_from_base_class.an_str  == 'abc'
        cast_mode_a_from_base_class.new_str         = 'new_str'
        assert cast_mode_a_from_base_class.new_str == 'new_str'                      # confirm that the new var is set correctly
        assert base_class.new_str                  == 'new_str'                      # confirm that the new var is set correctly
        assert cast_mode_a_from_base_class.__dict__ == base_class.__dict__

        base_class_2  = Base_Class()                                                 # create a clean instance of Base_Class
        cast_mode_a_2 = Cast_Mode_A()                                                # create a clean instance of Cast_Mode_A
        assert list_set(base_class_2 .__dict__) == ['an_int']                        # confirm that it has the expected vars
        assert list_set(cast_mode_a_2.__dict__) == ['an_int', 'an_str']              # confirm that it has the vars from Base_Class and Cast_Mode_A
        cast_mode_a_2.cast(base_class_2)                                             # cast it from base_class_2
        assert list_set(base_class_2.__dict__ ) == ['an_int']                        # re-config that base_class_2 only has the one var
        assert list_set(cast_mode_a_2.__dict__) == ['an_int']                        # BUG: but now cast_mode_a_2 lost the an_str var
        assert cast_mode_a_2.an_str             == 'abc'                             # works because an_str is defined in the Cast_Mode_A class, it's still accessible by instances of that class, even if it's not in their instance __dict__.

        cast_mode_a_3 = Cast_Mode_A()
        cast_mode_a_3.an_str = 'changed'
        assert cast_mode_a_3.an_str == 'changed'
        cast_mode_a_3.cast(base_class_2)
        assert cast_mode_a_3.an_str == 'abc'

    def test__regression__cast_issue_with_base_class_mode_b(self):                         # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_B(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                for key, value in target.__dict__.items():
                    setattr(self, key, value)
                return self

        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_b = Cast_Mode_B().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_b.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_b.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_b.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_b.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 222                            # BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_b.an_int                 == 123                            # BUG: but the value in the Cast_Mode_B object was not changed!

        # the current hypothesis is that the current cast code
        #                  for key, value in target.__dict__.items():
        #                     setattr(self, key, value)
        # is actually creating a copy of the an_int object, instead of a reference to it (which is what we want)


    def test__regression__cast_issue_with_base_class_mode_c(self):                  # the cast version below is the one that has the correct behaviour
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_C(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}       # Store the original attributes of self that should be retained.
                self.__dict__ = target.__dict__                                                             # Set the target's __dict__ to self, now self and target share the same __dict__.
                self.__dict__.update(original_attrs)                                                        # Reassign the original attributes back to self.
                return self



        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_c = Cast_Mode_C().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_c.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_c.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_c.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_c.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 123                            # FIXED :BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_c.an_int                 == 456                            # FIXED: BUG: but the value in the Cast_Mode_B object was not changed!





    def test__bug__cast_issue_with_base_class__with_new_vars__in_mermaid(self):
        from osbot_utils.graphs.mermaid.Mermaid import Mermaid
        from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node
        from osbot_utils.graphs.mermaid.Mermaid__Graph import Mermaid__Graph
        new_node_1 = Mermaid().add_node(key='id')
        assert list_set(new_node_1.__kwargs__()) == ['attributes', 'config', 'key', 'label']
        assert type(new_node_1).__name__ == 'Mermaid__Node'

        new_node_2 = Mermaid().add_node(key='id')
        assert type(new_node_2).__name__ == 'Mermaid__Node'

        assert list_set(new_node_2.__dict__         ) == ['attributes', 'config', 'key', 'label']


        mermaid_node = Mermaid__Graph().add_node(key='id')
        assert type(mermaid_node).__name__ == 'Mermaid__Node'
        assert list_set(mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']   # BUG, should be ['attributes', 'key', 'label']

        mgraph_node = MGraph__Node(key='id')
        assert type(mgraph_node).__name__ == 'MGraph__Node'
        new_mermaid_node = Mermaid__Node()
        assert list_set(mgraph_node.__dict__     ) == ['attributes', 'key'   , 'label'       ]
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

        new_mermaid_node.merge_with(mgraph_node)
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label'          ]



