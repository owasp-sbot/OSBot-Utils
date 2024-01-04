import types
import unittest

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.testing.Catch                  import Catch
from osbot_utils.utils.Dev                      import pprint
from osbot_utils.utils.Misc                     import random_string
from osbot_utils.utils.Objects                  import obj_info, obj_data


class Test_Kwargs_To_Self(unittest.TestCase):

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
        assert self.Config_Class.__cls_kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': print }
        assert self.Extra_Config.__cls_kwargs__() == {'attribute3': 'another_value',                     'callable_attr_2': print }

        assert self.Config_Class.__cls_kwargs__() == self.Config_Class().__cls_kwargs__()
        assert self.Extra_Config.__cls_kwargs__() == self.Extra_Config().__cls_kwargs__()

    def test___default_kwargs__(self):
        class An_Class(Kwargs_To_Self):
            attribute1 = 'default_value'
            attribute2 = True

        assert An_Class.__default_kwargs__() == {'attribute1': 'default_value', 'attribute2': True}


    def test_default_kwargs_inheritance(self):
        """ Test that _default_kwargs handles inheritance correctly (i.e. only shows all defaults for all inherited classes). """
        expected_defaults = {'attribute1'     : 'default_value'  ,
                             'attribute2'     : True             ,
                             'attribute3'     : 'another_value'  ,
                             'callable_attr_1': print            ,
                             'callable_attr_2': print            }
        self.assertEqual(self.Extra_Config.__default_kwargs__(), expected_defaults)


    def test_default_kwargs_no_leakage(self):
        """ Test that instance attributes do not affect class-level defaults. """
        instance = self.Config_Class(attribute1='changed_value')
        expected_defaults = {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': self.Config_Class.__default_kwargs__()['callable_attr_1']}
        self.assertEqual(self.Config_Class.__default_kwargs__(), expected_defaults)
        self.assertNotEqual(instance.attribute1, self.Config_Class.__default_kwargs__()['attribute1'])

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
        default_kwargs   = self.Config_Class.__default_kwargs__()
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
        default_kwargs  = self.Extra_Config.__default_kwargs__()
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

