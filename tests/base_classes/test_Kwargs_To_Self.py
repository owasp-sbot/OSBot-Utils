import types
import unittest

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_string
from osbot_utils.utils.Objects import obj_info, obj_data


class Test_Kwargs_To_Self(unittest.TestCase):

    class Config_Class(Kwargs_To_Self):
        attribute1      = 'default_value'
        attribute2      = True
        callable_attr_1 = Kwargs_To_Self.__init__                       # make it a callable to make sure we also pick up on __default_kwargs__ and__kwargs__

    class Extra_Config(Config_Class):
        attribute3      = 'another_value'
        callable_attr_2 = print                                         # make it a callable to make sure we also pick up on __default_kwargs__ and__kwargs__#

        def __init__(self):
            super().__init__()
            self.local_attribute_4 = '123'                              # these locals should not be picked up by _kwargs or __kwargs__
            self.local_callable_attr_4 = print

    def test_default_kwargs(self):
        class ConfigClass(Kwargs_To_Self):
            attribute1 = 'default_value'
            attribute2 = True

        assert ConfigClass.__default_kwargs__() == {'attribute1': 'default_value', 'attribute2': True}


    def test_default_kwargs_inheritance(self):
        """ Test that _default_kwargs handles inheritance correctly (i.e. only shows all defaults for all inherited classes). """
        expected_defaults = {'attribute1'     : 'default_value'         ,
                             'attribute2'     : True                    ,
                             'attribute3'     : 'another_value'         ,
                             'callable_attr_1': Kwargs_To_Self.__init__ ,
                             'callable_attr_2': print                   }
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

        assert config_1.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': config_1.callable_attr_1}
        assert config_2.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'callable_attr_1': config_2.callable_attr_1}

        assert obj_data(config_1) == {'attribute1': 'default_value', 'attribute2': True}        # obj_doesn't pick up functions (unless explicity told to)
        assert obj_data(config_2) == {'attribute1': 'default_value', 'attribute2': True}

        new_value           = random_string(prefix='new_value_')
        config_1.attribute1 = new_value
        config_1.attribute2 = False

        assert config_1.__kwargs__() == {'attribute1': new_value      , 'attribute2': False, 'callable_attr_1': config_1.callable_attr_1}    # confirm that config_1 has the new values
        assert config_2.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True , 'callable_attr_1': config_2.callable_attr_1}    # confirm that config_2 has not been affected

    def test__kwargs_capture_doesnt_show_locals(self):
        extra_config = self.Extra_Config()
        assert extra_config.__kwargs__() == {'attribute1': 'default_value', 'attribute2': True, 'attribute3': 'another_value', 'callable_attr_1': extra_config.callable_attr_1, 'callable_attr_2': print}

    def test__kwargs__doesnt_pick_up_inherited_vars(self):
        extra_config = self.Extra_Config()
        assert extra_config.__kwargs__() == {'attribute1'      : 'default_value'              ,     # this list confirms that __kwargs__ only picks up the static variables
                                             'attribute2'      : True                         ,     # i.e. not the ones defined in the __init__ method
                                             'attribute3'      : 'another_value'              ,     # like the local_attribute_4 and local_callable_attr_4
                                             'callable_attr_1' : extra_config.callable_attr_1 ,
                                             'callable_attr_2' : print                        }
        assert callable(extra_config.callable_attr_1) is True                                       # confirm we are picking up callable (i.e. functions
        assert callable(extra_config.callable_attr_2) is True
        assert isinstance(extra_config.callable_attr_1, types.MethodType       ) is True            # confirm they are methods (this one local)
        assert isinstance(extra_config.callable_attr_2, types.BuiltinMethodType) is True            # this one from the builtins
        assert extra_config.callable_attr_1.__name__ == '__init__'                                  # confirm the name of the method of callable_attr_1
        assert extra_config.callable_attr_2.__name__ == 'print'                                     # confirm the name of the method of callable_attr_2

        assert extra_config.attribute1           == 'default_value'
        assert extra_config.attribute2           is True
        assert extra_config.attribute3           == 'another_value'
        assert extra_config.local_attribute_4    == '123'                    # this is a local var, that is available but not picked up by __kwargs__
        assert extra_config.local_callable_attr_4 == print                   # same for these methods


    def test__locals__(self):
        extra_config = self.Extra_Config()
        assert extra_config.__locals__() == {'local_attribute_4': '123', 'local_callable_attr_4': print}
