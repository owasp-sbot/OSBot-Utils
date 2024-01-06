import os
import unittest
from unittest import TestCase

from osbot_utils.utils.Lists import env_vars_list
from osbot_utils.utils.Objects import class_name, get_field, get_value, obj_get_value, obj_values, obj_keys, obj_items, \
    obj_dict, env_value, env_vars, default_value


class test_Objects(TestCase):

    def test_class_name(self):
        assert class_name(TestCase)   == "type"
        assert class_name(TestCase()) == "TestCase"

    def test_default_value(self):
        from decimal     import Decimal
        from datetime    import date, datetime
        from collections import defaultdict, Counter
        from fractions   import Fraction
        from queue       import Queue


        assert default_value(int      ) == 0
        assert default_value(bool     ) is False
        assert default_value(float    ) == 0.0
        assert default_value(str      ) is ''
        assert default_value(list     ) == []
        assert default_value(dict     ) == {}
        assert default_value(complex  ) == 0j
        assert default_value(tuple    ) == ()
        assert default_value(frozenset) == frozenset()
        assert default_value(bytes    ) == b''
        assert default_value(set      ) == set()

        assert default_value(Decimal    ) == Decimal('0')
        assert default_value(defaultdict) == defaultdict(None)
        assert default_value(Counter    ) == Counter()
        assert default_value(Fraction   ) == Fraction(0, 1)

        assert default_value(None    ) is None
        assert default_value(os      ) is None
        assert default_value(1       ) is None
        assert default_value('1'     ) is None
        assert default_value(False   ) is None
        assert default_value(date    ) is None
        assert default_value(datetime) is None

        assert type(default_value(self    )) is unittest.result.TestResult
        assert type(default_value(TestCase)) is unittest.case.TestCase
        assert type(default_value(Queue   )) is Queue


    def test_env_value(self):
        assert env_value("ENV_VAR_1") == "ENV_VAR_1_VALUE"

    def test_env_vars(self):
        os.environ.__setitem__("ENV_VAR_FROM_CODE", "ENV_VAR_FROM_CODE_VALUE")
        loaded_env_vars = env_vars()
        assert loaded_env_vars.get("ENV_VAR_1"        ) == 'ENV_VAR_1_VALUE'
        assert loaded_env_vars.get("ENV_VAR_2"        ) == 'ENV_VAR_2_VALUE'
        assert loaded_env_vars.get("ENV_VAR_FROM_CODE") == 'ENV_VAR_FROM_CODE_VALUE'

    def test_env_vars_list(self):
        assert env_vars_list().__contains__("ENV_VAR_1")
        assert env_vars_list().__contains__("ENV_VAR_2")
        assert env_vars_list() == sorted(set(env_vars()))

    def test_get_field(self):
        print()
        print(self.__module__)
        assert str(get_field(self, '__module__')) == "test_Objects"
        assert get_field({}, None               ) == None
        assert get_field({}, None, default=42   ) == 42

    def test_get_value(self):
        assert get_value({}, 'a'           ) is None
        assert get_value({}, 'a', 'default') == 'default'
        assert get_value({}, None , 'd'    ) == 'd'
        assert get_value({}, None          ) is None
        assert get_value({'a': 42}, 'a'    ) == 42
        assert get_value(None, 'a'         ) == None

    def test_obj_dict(self):
        class Target:
            def __init__(self):
                self.var_1 = 'the answer'
                self.var_2 = 'is'
                self.var_3 = 42
        assert obj_dict  (Target()) == {'var_1': 'the answer', 'var_2': 'is', 'var_3': 42}
        assert obj_items (Target()) == [('var_1', 'the answer'), ('var_2', 'is'), ('var_3', 42)]
        assert obj_keys  (Target()) == ['var_1', 'var_2', 'var_3']
        assert obj_values(Target()) == ['the answer', 'is', 42]
        target = Target()
        for key,value in obj_items(target):
            assert obj_get_value(target, key          ) == value
            assert obj_get_value(target, key    , 'aa') == value
            assert obj_get_value(target, key+'a', 'aa') == 'aa'

        # check cases when bad data is submitted
        assert obj_dict  ()   == {}
        assert obj_items ()   == []
        assert obj_keys  ()   == []
        assert obj_values()   == []
        assert obj_dict  (42) == {}
        assert obj_items (42) == []
        assert obj_keys  (42) == []
        assert obj_values({}) == []
        assert obj_dict  ({}) == {}
        assert obj_items ({}) == []
        assert obj_keys  ({}) == []
        assert obj_values({}) == []