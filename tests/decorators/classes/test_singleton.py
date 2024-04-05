import builtins
import types
from unittest import TestCase

from osbot_utils.decorators.classes.singleton import singleton
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_string
from osbot_utils.utils.Objects import type_full_name


class test_singleton(TestCase):

    def test_singleton(self):
        @singleton
        class An_Class:
            def __init__(self):
                self.an_value = random_string(prefix='an_value')

        an_class_1 = An_Class()
        an_class_2 = An_Class()
        assert an_class_1.an_value.startswith('an_value')
        assert an_class_1 == an_class_2
        assert an_class_1.an_value == an_class_2.an_value

        assert isinstance(An_Class, types.FunctionType) is True                         # todo: see if there is a way to access the type directly
        assert type(an_class_1)                         is not An_Class                 # todo: check if there is a way to make this check
        assert type_full_name(an_class_1)               == 'test_singleton.An_Class'
