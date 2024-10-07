import os
import sys
import types
import pytest
import unittest

from typing         import Optional, Union
from unittest       import TestCase
from unittest.mock  import patch, call




from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc import random_int, list_set
from osbot_utils.utils.Objects import class_name, get_field, get_value, obj_get_value, obj_values, obj_keys, obj_items, \
    obj_dict, default_value, value_type_matches_obj_annotation_for_attr, base_classes, \
    class_functions_names, class_functions, dict_remove, class_full_name, get_missing_fields, \
    print_object_methods, print_obj_data_aligned, obj_info, obj_data, print_obj_data_as_dict, print_object_members, \
    obj_base_classes, obj_base_classes_names, are_types_compatible_for_assigment, type_mro, \
    obj_is_type_union_compatible, value_type_matches_obj_annotation_for_union_attr, pickle_save_to_bytes, \
    pickle_load_from_bytes, convert_dict_to_value_from_obj_annotation, dict_to_obj, obj_to_dict


class test_Objects(TestCase):

    def test_are_types_compatible_for_assigment(self):
        assert are_types_compatible_for_assigment(source_type=int      , target_type=int      ) is True
        assert are_types_compatible_for_assigment(source_type=str      , target_type=str      ) is True
        assert are_types_compatible_for_assigment(source_type=float    , target_type=float    ) is True
        assert are_types_compatible_for_assigment(source_type=TestCase , target_type=TestCase ) is True
        assert are_types_compatible_for_assigment(source_type=int      , target_type=float    ) is True

        assert are_types_compatible_for_assigment(source_type=float    , target_type=int      ) is False
        assert are_types_compatible_for_assigment(source_type=int      , target_type=str      ) is False
        assert are_types_compatible_for_assigment(source_type=str      , target_type=int      ) is False

    def test_base_classes(self):
        assert base_classes(self) == [TestCase, object]
        assert base_classes(type(self)) == [TestCase, object]

    def test_class_functions_names(self):
        assert 'assertEqual' in class_functions_names(self)

    def test_class_functions(self):
        functions = class_functions(self)
        assert len(functions) > 90
        assert 'assertEqual' in functions
        assert functions['assertEqual'].__class__ == types.FunctionType

    def test_class_full_name(self):
        assert class_full_name(self       ) == 'test_Objects.test_Objects'
        assert class_full_name(TestCase   ) == 'builtins.type'

    def test_class_name(self):
        assert class_name(TestCase)   == "type"
        assert class_name(TestCase()) == "TestCase"

    def test_convert_dict_to_value_from_obj_annotation(self):

        # test case of using dicts (where if the target is a dict, it just should return the value provided)
        class An_Class(Type_Safe):
            an_dict : dict

        an_dict = {'a': 1, 'b': 2, 'c': 3}
        an_class_json = dict(an_dict=an_dict)
        an_class_1 = An_Class(**an_class_json)
        assert an_class_1.json() == an_class_json

        an_class_2 = An_Class()
        result = convert_dict_to_value_from_obj_annotation(an_class_2, 'an_dict', an_dict)

        assert result == an_dict

        # test case of nested classes
        class Class_A(Type_Safe):
            an_int: int
            an_str: str

        class Class_B(Type_Safe):
            an_bool: bool
            an_bytes: bytes

        class Class_C(Type_Safe):
            an_class_a: Class_A
            an_class_b: Class_B

        an_class_C = Class_C()
        an_class_c_json = { 'an_class_a': {'an_int' : 0    , 'an_str'  : '' },
                            'an_class_b': {'an_bool': False, 'an_bytes': b''}}
        assert an_class_C.json() == an_class_c_json

        an_class_a_json = an_class_c_json.get('an_class_a')
        an_class_b_json = an_class_c_json.get('an_class_b')
        assert an_class_a_json == {'an_int': 0, 'an_str': ''}

        result_a = convert_dict_to_value_from_obj_annotation(an_class_C, 'an_class_a', an_class_a_json)
        assert type(result_a) is Class_A
        result_b = convert_dict_to_value_from_obj_annotation(an_class_C, 'an_class_b', an_class_b_json)
        assert type(result_b) is Class_B

        assert Class_C(**an_class_c_json).json() == an_class_c_json


    def test_default_value(self):
        from decimal     import Decimal
        from datetime    import date, datetime
        from collections import defaultdict, Counter
        from fractions   import Fraction
        from queue       import Queue


        assert default_value(int      ) == 0
        assert default_value(bool     ) is False
        assert default_value(float    ) == 0.0
        assert default_value(str      ) == ''
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

        assert type(default_value(TestCase)) is unittest.case.TestCase
        assert type(default_value(Queue   )) is Queue

    def test_dict_remove(self):
        dict_1 = {'a': 1, 'b': 2, 'c': 3}
        assert dict_remove(dict_1, 'a') == {'b': 2, 'c': 3}
        assert dict_1 == {'b': 2, 'c': 3}
        assert dict_remove(dict_1, ['a','b']) == {'c': 3}
        assert dict_1 == { 'c': 3}

    def test_dict_to_obj(self):
        # variation #1: simple usage
        dict_1 =  {'an_bytes': b'the answer is...'    ,
                   'an_int'  : 42                     ,
                   'an_dict' : {'a': 1, 'b': 2, 'c': 3},
                   'an_str'  : 'string_1'             }

        assert dict_to_obj(dict_1).an_bytes     == b'the answer is...'
        assert dict_to_obj(dict_1).an_int       == 42
        assert dict_to_obj(dict_1).an_dict.a    == 1
        assert dict_to_obj(dict_1).an_dict.b    == 2
        assert dict_to_obj(dict_1).an_dict.c    == 3
        assert dict_to_obj(dict_1).an_str       == 'string_1'
        assert obj_to_dict(dict_to_obj(dict_1)) == dict_1

        # variation #2:  test_dict_to_obj_nested(self):
        dict_2 = {
            'level_1': {
                'level_2': {
                    'level_3': {
                        'an_int': 100,
                        'a_list': [1, 2, 3],
                    },
                    'another_str': 'string_2'
                },
                'an_float': 3.14
            }
        }

        obj = dict_to_obj(dict_2)
        assert obj.level_1.level_2.level_3.an_int == 100
        assert obj.level_1.level_2.level_3.a_list == [1, 2, 3]
        assert obj.level_1.level_2.another_str == 'string_2'
        assert obj.level_1.an_float == 3.14
        assert obj_to_dict(obj) == dict_2

        # variation #3: test_dict_to_obj_with_list_and_tuple
        dict_3 = {
            'a_list': [1, 'string', {'key': 'value'}],
            'a_tuple': (1, 2, {'nested_key': 'nested_value'}),
        }

        obj = dict_to_obj(dict_3)
        assert obj.a_list[0] == 1
        assert obj.a_list[1] == 'string'
        assert obj.a_tuple[0] == 1
        assert obj.a_tuple[1] == 2
        assert obj.a_tuple[2].nested_key == 'nested_value'
        assert obj_to_dict(obj) == dict_3

        # variation #4:  test_dict_to_obj_empty_input
        dict_4 = {}
        obj = dict_to_obj(dict_4)
        assert obj_to_dict(obj) == dict_4

        #test_dict_to_obj__special_types
        dict_5 = {
            'a_bool': True,
            'a_none': None,
            'a_float': 9.81,
            'a_set': {1, 2, 3},
        }

        obj = dict_to_obj(dict_5)
        assert obj.a_bool       is True
        assert obj.a_none       is None
        assert obj.a_float      == 9.81
        assert obj.a_set        == {1, 2, 3}
        assert obj_to_dict(obj) == dict_5

        # variation #5: test_dict_to_obj__abuse_case_non_dict
        assert dict_to_obj(42) == 42                                            # Passing non-dict types to dict_to_obj should return them unchanged
        assert dict_to_obj('string') == 'string'
        assert dict_to_obj([1, 2, 3]) == [1, 2, 3]

        # variation #6: test_dict_to_obj__abuse_case_circular_reference
        dict_6 = {}
        dict_6['self'] = dict_6  # Circular reference

        with pytest.raises(RecursionError):
            dict_to_obj(dict_6)

        # variation #7: test_obj_to_dict__with_incorrect_type
        assert obj_to_dict(42) == 42                                        # Trying to convert a non-SimpleNamespace object should just return it unchanged
        assert obj_to_dict('string') == 'string'
        assert obj_to_dict([1, 2, 3]) == [1, 2, 3]

        # variation #8: test_obj_to_dict__on_custom_class
        class CustomClass:                                                  # Test obj_to_dict on a custom object that isn't a SimpleNamespace
            def __init__(self):
                self.a = 10
                self.b = 'test'

        custom_obj = CustomClass()
        assert obj_to_dict(custom_obj) == custom_obj

        # variation #8: test_dict_to_obj__with_unusual_keys
        dict_7 = {
            'a_normal_key': 'value',
            'key_with space': 123,
            'key-with-dash': [1, 2, 3],
            'key.with.dot': {'nested_key': 'nested_value'}
        }

        obj = dict_to_obj(dict_7)

        assert obj.a_normal_key                          == 'value'         # this one we can get directly
        assert getattr(obj, 'a_normal_key')              == 'value'         # or like this

        assert getattr(obj, 'key_with space')            == 123             # but these can only be resolved using getattr
        assert getattr(obj, 'key-with-dash' )            == [1, 2, 3]
        assert getattr(obj, 'key.with.dot'  ).nested_key == 'nested_value'
        assert obj_to_dict(obj) == dict_7

    def test_get_field(self):
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

        if sys.version_info > (3, 12):
            pytest.skip("Skipping test that doesn't work on 3.13 or higher")
        if sys.version_info < (3, 11):
            pytest.skip("Skipping test that does't work on 3.11 or lower")

        class Target:
            def __init__(self):
                self.var_1 = 'the answer'
                self.var_2 = 'is'
                self.var_3 = 42
                self.__aa = "here"
        target = Target()



        expected_vars__show_internals = sorted([ '_Target__aa', 'var_1', 'var_2', 'var_3', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'])
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


    def test_pickle_save_to_bytes__pickle_load_from_bytes(self):
        an_object     = {"answer" : 42 }
        pickled_data  = pickle_save_to_bytes(an_object)
        pickle_data   = pickle_load_from_bytes(pickled_data)

        assert type(pickled_data)  is bytes
        assert pickle_data         == an_object

    def test_value_type_matches_obj_annotation_for_union_attr(self):

        an_str  : str   = ''
        an_int  :  int  = 1
        an_float: float = 1.0
        an_bool : bool  = True
        an_bytes: bytes = b"aaaa"

        class Direct_Type_Cases:
            var_1: str   = ''
            var_2: int   = 1
            var_3: float = 1.0
            var_4: bool  = True

        class With_Union_Types:
            str_int        : Union[str, int         ]
            int_float_bytes: Union[int, float, bytes]

        direct_type_cases = Direct_Type_Cases()
        with_union_types  = With_Union_Types()

        _ = value_type_matches_obj_annotation_for_union_attr

        assert _(target=direct_type_cases, attr_name='var_1'         , value=an_str  ) is None          # any not Union type will return None
        assert _(target=direct_type_cases, attr_name='var_1'         , value=an_int  ) is None
        assert _(target=direct_type_cases, attr_name='var_2'         , value=an_int  ) is None

        assert _(target=with_union_types, attr_name='str_int'        , value=an_str  ) is True
        assert _(target=with_union_types, attr_name='str_int'        , value=an_int  ) is True
        assert _(target=with_union_types, attr_name='str_int'        , value=an_bool ) is False
        assert _(target=with_union_types, attr_name='AAAAA'          , value=an_bool ) is None          # any not Union type will return None


        assert _(target=with_union_types, attr_name='int_float_bytes', value=an_int  ) is True
        assert _(target=with_union_types, attr_name='int_float_bytes', value=an_float) is True
        assert _(target=with_union_types, attr_name='int_float_bytes', value=an_bytes) is True
        assert _(target=with_union_types, attr_name='int_float_bytes', value=an_str  ) is False
        assert _(target=with_union_types, attr_name='int_float_bytes', value=an_bool ) is False
        assert _(target=with_union_types, attr_name='AAAAA'          , value=an_bool ) is None          # any not Union type will return None



    def test_obj_is_type_union_compatible(self):
        compatible_types = (int, float, bool, str)

        # Direct type cases
        var_1: str = ''
        var_2: int = 1
        var_3: float = 1.0
        var_4: bool = True

        assert obj_is_type_union_compatible(type(var_1), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_2), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_3), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_4), compatible_types) is True

        # Union types
        var_5: Union[str, int         ] = 2
        var_6: Union[int, float, bytes] = 3.14    # will work - type bytes is not in the compatible list, but var_6 is not assigned to it
        var_7: Union[int, float, bytes] = b'aaa'  # will fail - type bytes is not in the compatible list, and var_7 is assigned to it
        var_8: Union[str, int         ] = None
        var_9: Union[str, int         ] = None

        assert obj_is_type_union_compatible(Union[str, int]         , compatible_types) is True
        assert obj_is_type_union_compatible(type(var_5)             , compatible_types) is True
        assert obj_is_type_union_compatible(type(var_8)             , compatible_types) is True
        assert obj_is_type_union_compatible(type(var_9)             , compatible_types) is True
        assert obj_is_type_union_compatible(Union[int, float, bytes], compatible_types) is False  # Because bytes is not compatible
        assert obj_is_type_union_compatible(type(var_6)             , compatible_types) is True   # bytes could be one of the values, but it is not
        assert obj_is_type_union_compatible(type(var_7)             , compatible_types) is False  # now that bytes is one of the values, it fails

        # Optional types (which are essentially Union[type, NoneType])
        var_10: Optional[str  ] = None
        var_11: Optional[bytes] = None  # bytes is not in the compatible list, , but var_11 is not assigned to it
        var_12: Optional[str  ] = 'a'
        var_13: Optional[bytes] = 'a'
        var_14: Optional[bytes] = b'aaa'

        assert obj_is_type_union_compatible(type(var_10), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_11), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_12), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_13), compatible_types) is True   # todo: BUG type safe should had picked this up
        assert obj_is_type_union_compatible(type(var_14), compatible_types) is False  # Because bytes is not compatible

        # Complex case with nested Unions and Optionals
        var_15: Optional[Union[int, str, None ]] = None
        var_16: Optional[Union[int, str, bytes]] = None
        var_17: Optional[Union[int, str, bytes]] = 'a'
        var_18: Optional[Union[int, str, bytes]] = b'aaa'

        assert obj_is_type_union_compatible(type(var_15), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_16), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_17), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_18), compatible_types) is False

    def test_bug__obj_is_type_union_compatible(self):
        compatible_types = (int, float, str)        # bool not here
        var_1: Optional[bytes] = 'a'                # str
        var_2: Optional[bytes] = 1                  # int
        var_3: Optional[bytes] = 1.1                # float
        var_4: Optional[bytes] = False              # bool
        var_5: Optional[bytes] = b'aaa'             # bytes
        assert type(var_1) is str
        assert type(var_2) is int
        assert type(var_3) is float
        assert type(var_4) is bool
        assert type(var_5) is bytes
        assert obj_is_type_union_compatible(type(var_1), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_2), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_3), compatible_types) is True
        assert obj_is_type_union_compatible(type(var_4), compatible_types) is False
        assert obj_is_type_union_compatible(type(var_5), compatible_types) is False

    def test_print_object_members(self):
        if sys.version_info < (3, 11):
            pytest.skip("Skipping test that does't work on 3.11 or lower")

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
                                        call("Members for object:\n\t test_print_object_members (test_Objects.test_Objects.test_print_object_members) of type:<class 'test_Objects.test_Objects'>"),
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


    def test__regression__value_type_matches_obj_annotation__false_positive_on_compatible_types(self):
        class An_Class:
            an_str   : str
            an_int   : int
            an_float : float

        an_int   = 1
        an_float = 1.0
        an_class = An_Class()
        _ = value_type_matches_obj_annotation_for_attr
        assert _(target=an_class, attr_name='an_str'  , value=an_int  ) is False      # expected behaviour, a string can't be assigned to an int
        assert _(target=an_class, attr_name='an_int'  , value=an_int  ) is True       # expected behaviour, an int can be assigned to an int
        assert _(target=an_class, attr_name='an_float', value=an_float) is True       # expected behaviour, a float can be assigned to a float
        assert _(target=an_class, attr_name='an_int'  , value=an_float) is False      # expected behaviour, a float can't be assigned to an int
        assert _(target=an_class, attr_name='an_float', value=an_int  ) is True       # FIXED: was false    BUG: this should be True, an int can be assigned to a float


    def test_type_mro(self):
        assert type_mro(TestCase  ) == [TestCase, object]
        assert type_mro(TestCase()) == [TestCase, object]

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

