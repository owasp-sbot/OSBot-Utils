import builtins
import os
import types
import unittest
from unittest import TestCase
from unittest.mock import patch, call

from dotenv import load_dotenv
from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Lists import env_vars_list
from osbot_utils.utils.Misc import random_int, list_set
from osbot_utils.utils.Objects import class_name, get_field, get_value, obj_get_value, obj_values, obj_keys, obj_items, \
    obj_dict, env_value, env_vars, default_value, value_type_matches_obj_annotation_for_attr, base_classes, \
    class_functions_names, class_functions, dict_insert_field, dict_remove, class_full_name, get_missing_fields, \
    print_object_methods, print_obj_data_aligned, obj_info, obj_data, print_obj_data_as_dict, print_object_members, \
    obj_base_classes, obj_base_classes_names


class test_Objects(TestCase):

    def setUp(self):
        load_dotenv()                                       # todo: replace this with equivalent load_dotenv funcionality (since it is an extra import and all we currenty use of it is to load the .env file into memory)

    def test_base_classes(self):
        assert base_classes(self) == [TestCase, object]
        assert base_classes(type(self)) == [TestCase, object]

    def test_class_functions_names(self):
        assert 'assertEquals' in class_functions_names(self)

    def test_class_functions(self):
        functions = class_functions(self)
        assert len(functions) > 90
        assert 'assertEquals' in functions
        assert functions['assertEquals'].__class__ == types.FunctionType

    def test_class_full_name(self):
        assert class_full_name(self       ) == 'test_Objects.test_Objects'
        assert class_full_name(TestCase   ) == 'builtins.type'
        assert class_full_name(load_dotenv) == 'builtins.function'

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

    def test_dict_insert_field(self):
        dict_1 = {'a': 1, 'b': 2, 'c': 3}
        assert dict_insert_field(dict_1, new_key='x',insert_at=0) == {'x': None, 'a': 1, 'b': 2, 'c': 3}

    def test_dict_remove(self):
        dict_1 = {'a': 1, 'b': 2, 'c': 3}
        assert dict_remove(dict_1, 'a') == {'b': 2, 'c': 3}
        assert dict_1 == {'b': 2, 'c': 3}
        assert dict_remove(dict_1, ['a','b']) == {'c': 3}
        assert dict_1 == { 'c': 3}

    def test_env_value(self):
        assert env_value("ENV_VAR_1") == "ENV_VAR_1_VALUE"

    def test_env_vars(self):
        os.environ.__setitem__("ENV_VAR_FROM_CODE", "ENV_VAR_FROM_CODE_VALUE")
        loaded_env_vars = env_vars(reload_vars=True)
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

    def test_get_missing_fields(self):
        assert get_missing_fields({}  , ['a','b']) == ['a','b']
        assert get_missing_fields({}  , ['a'    ]) == ['a'    ]
        assert get_missing_fields({}  , []       ) == []

        assert get_missing_fields({}  , None     ) == []
        assert get_missing_fields(None, None     ) == []
        assert get_missing_fields(None, ['a'    ]) == ['a']
        assert get_missing_fields(None, []       ) == []
        assert get_missing_fields(self, ['a'   ]) == ['a']

    def test_get_value(self):
        assert get_value({}, 'a'           ) is None
        assert get_value({}, 'a', 'default') == 'default'
        assert get_value({}, None , 'd'    ) == 'd'
        assert get_value({}, None          ) is None
        assert get_value({'a': 42}, 'a'    ) == 42
        assert get_value(None, 'a'         ) == None

    def test_obj_data(self):

        class Target:
            def __init__(self):
                self.var_1 = 'the answer'
                self.var_2 = 'is'
                self.var_3 = 42
                self.__aa = "here"
        target = Target()



        expected_vars__show_internals = sorted([ '_Target__aa', 'var_1', 'var_2', 'var_3', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'])
        expected_vars__show_private   = sorted([ '_Target__aa', 'var_1', 'var_2', 'var_3'])

        assert obj_data(target) == {'var_1': 'the answer', 'var_2': 'is', 'var_3': 42}
        assert obj_data(target         , show_private=True                        ) == {'_Target__aa': 'here', 'var_1': 'the answer', 'var_2': 'is', 'var_3': 42}
        assert list_set(obj_data(target, show_private=True , show_internals=False)) == expected_vars__show_private
        assert list_set(obj_data(target, show_private=False, show_internals=True )) == expected_vars__show_internals
        assert list_set(obj_data(target, show_private=True , show_internals=True )) == expected_vars__show_internals



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

    def test_print_object_members(self):
        class An_Class:
            an_str   : str = 'the answer'
            an_int   : str = 42
            an_function = test_Objects.test_print_object_members
        an_class = An_Class()

        with patch('builtins.print') as _:
            print_object_members(an_class)
            print_object_members(self)
            assert _.call_args_list == [call(),
                                        call(f"Members for object:\n\t {an_class} of type:{type(an_class)}"),
                                        call( 'Settings:\n\t name_width: 30 | value_width: 100 | show_private: False | show_internals: False'),
                                        call(),
                                        call( 'field                          | value'),
                                        call( '----------------------------------------------------------------------------------------------------------------------------------'),
                                        call( 'an_int                         | 42'),
                                        call( 'an_str                         | the answer'),
                                        call(),
                                        call("Members for object:\n\t test_print_object_members (test_Objects.test_Objects) of type:<class 'test_Objects.test_Objects'>"),
                                        call('Settings:\n\t name_width: 30 | value_width: 100 | show_private: False | show_internals: False'),
                                        call(),
                                        call('field                          | value'),
                                        call('----------------------------------------------------------------------------------------------------------------------------------'),
                                        call("failureException               | <class 'AssertionError'>"),
                                        call('longMessage                    | True'),
                                        call('maxDiff                        | 640')]

        with patch('builtins.print') as _:
            print_object_members(an_class, only_show_methods=True)
            assert _.call_args_list == [call(),
                                        call(f"Members for object:\n\t {an_class} of type:{type(an_class)}"),
                                        call( 'Settings:\n\t name_width: 30 | value_width: 100 | show_private: False | show_internals: False'),
                                        call(),
                                        call( 'method                         (params)'),
                                        call( '----------------------------------------------------------------------------------------------------------------------------------'),
                                        call( 'an_function                    ()')]

        with patch('builtins.print') as _:
            print_object_members(an_class, show_value_class=True)
            assert _.call_args_list == [call(),
                                        call(f"Members for object:\n\t {an_class} of type:{type(an_class)}"),
                                        call('Settings:\n\t name_width: 30 | value_width: 100 | show_private: False | show_internals: False'),
                                        call(),
                                        call('field                          | type                           |value'),
                                        call('----------------------------------------------------------------------------------------------------------------------------------'),
                                        call('an_int                         | builtins.int                   | 42'),
                                        call('an_str                         | builtins.str                   | the answer')] != []


    def test_print_object_methods(self):
        with patch('osbot_utils.utils.Objects.print_object_members') as mock_print_object_members:
            name_width      = random_int()
            value_width     = random_int()
            show_private    = random_int()
            show_internals  = random_int()
            print_object_methods(self, name_width=name_width, value_width=value_width, show_private=show_private, show_internals=show_internals)
            mock_print_object_members.assert_called()
            assert mock_print_object_members.call_args_list == [call(self, name_width=name_width, value_width=value_width,
                                                                     show_private=show_private, show_internals=show_internals,
                                                                     only_show_methods=True)]
    def test_print_obj_data_aligned(self):
        with patch('builtins.print') as _:
            print_obj_data_aligned({'a': 1, 'b': 2, 'c': 3})
            print_obj_data_aligned(obj_data(self))
            assert _.call_args_list == [call('a = 1     ,\n'
                                             'b = 2     ,\n'
                                             'c = 3    '),
                                        call('failureException = "<class \'AssertionError\'>",\n'
                                             'longMessage      = True  ,\n'
                                             'maxDiff          = 640  ')]
    def test_print_obj_data_as_dict(self):
        with patch('builtins.print') as _:
            print_obj_data_as_dict(self)
            assert _.call_args_list == [call('dict(failureException = "<class \'AssertionError\'>",\n'
                                             '     longMessage      = True  ,\n'
                                             '     maxDiff          = 640   )')]


    def test_obj_base_classes(self):
        assert obj_base_classes(self) == [TestCase, object]

    def test_obj_base_classes_names(self):
        assert obj_base_classes_names(self                   ) == ['TestCase', 'object']
        assert obj_base_classes_names(self, show_module= True) == ['unittest.case.TestCase', 'builtins.object']

    def test_value_type_matches_obj_annotation(self):
        class An_Class:
            an_str  : str
            an_int  : int
            an_case : TestCase

        an_class = An_Class()
        _ = value_type_matches_obj_annotation_for_attr
        assert _(target=None    , attr_name=None      , value=None      ) is None
        assert _(target=None    , attr_name=None      , value=''        ) is None
        assert _(target=''      , attr_name=None      , value=''        ) is None
        assert _(target=an_class, attr_name=''        , value=''        ) is None
        assert _(target=an_class, attr_name='an_str__', value=''        ) is None               # an_class.an_str__ = ''   | can't make a decision
        assert _(target=an_class, attr_name='an_str'  , value=''        ) is True               # an_class.an_str   = ''   | should work
        assert _(target=an_class, attr_name='an_str'  , value=None      ) is False              # an_class.an_str   = None | should fail
        assert _(target=an_class, attr_name='an_str'  , value=1         ) is False              # an_class.an_str   = 1    | should fail
        assert _(target=an_class, attr_name='an_int__', value=''        ) is None               # an_class.an_int__ = ''   | can't make a decision
        assert _(target=an_class, attr_name='an_int'  , value=''        ) is False              # an_class.an_int   = ''   | should fail
        assert _(target=an_class, attr_name='an_int'  , value=None      ) is False              # an_class.an_int   = None | should fail
        assert _(target=an_class, attr_name='an_int'  , value=1         ) is True               # an_class.an_int   = 1    | should work
        assert _(target=an_class, attr_name='an_str'  , value=str       ) is False
        assert _(target=an_class, attr_name='an_int'  , value=int       ) is False
        assert _(target=an_class, attr_name='an_case' , value=TestCase  ) is False              # should fail since we assiging the type TestCase
        assert _(target=an_class, attr_name='an_case' , value=TestCase()) is True               # should work since we are assigning an instance of TestCase

        #assert _(target=an_class, attr_name=None, value='') is None
        #assert _(target=an_class, attr_name=None, value='') is None



    def test__pyhton_name_mangling(self):
        class Target:
            def __init__(self):
                self.var_1 = 'the answer'
                self.var_2 = 'is'
                self.var_3 = 42
                self.__aa = "????"                          #
        target = Target()
        assert hasattr(target, 'var_1'      ) is True
        assert hasattr(target, 'var_2'      ) is True
        assert hasattr(target, 'var_3'      ) is True
        assert hasattr(target, '__aa'       ) is False      # Name mangling
        assert hasattr(target, '_Target__aa') is True       # Name mangling
        assert target.var_1         == 'the answer'
        assert target.var_2         == 'is'
        assert target.var_3         == 42
        assert target._Target__aa   == '????'               # Name mangling

