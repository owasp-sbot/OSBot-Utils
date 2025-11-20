import os
import sys
import types
import pytest
import unittest
from collections.abc                                                    import Mapping
from enum                                                               import Enum
from typing                                                             import Optional, Union, List, Any, Dict, Set
from unittest                                                           import TestCase
from unittest.mock                                                      import patch, call
from osbot_utils.testing.Stdout                                         import Stdout
from osbot_utils.testing.__                                             import __
from osbot_utils.testing.__helpers                                      import dict_to_obj, obj_to_dict
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.llm.enums.Enum__LLM__Role import Enum__LLM__Role
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict   import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List   import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Convert     import type_safe_convert
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Validation  import type_safe_validation
from osbot_utils.utils.Misc                                             import random_int, list_set
from osbot_utils.utils.Objects                                          import class_name, get_field, get_value, obj_get_value, obj_values, obj_keys, obj_items, obj_dict, default_value, base_classes, \
                                                                               class_functions_names, class_functions, dict_remove, class_full_name, get_missing_fields, \
                                                                               print_object_methods, print_obj_data_aligned, obj_data, print_obj_data_as_dict, print_object_members, \
                                                                               obj_base_classes, obj_base_classes_names, type_mro, pickle_save_to_bytes, pickle_load_from_bytes, serialize_to_dict


class test_Objects(TestCase):

    def test_are_types_compatible_for_assigment(self):
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=int      , target_type=int      ) is True
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=str      , target_type=str      ) is True
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=float    , target_type=float    ) is True
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=TestCase , target_type=TestCase ) is True
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=int      , target_type=float    ) is True

        assert type_safe_validation.are_types_compatible_for_assigment(source_type=float    , target_type=int      ) is False
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=int      , target_type=str      ) is False
        assert type_safe_validation.are_types_compatible_for_assigment(source_type=str      , target_type=int      ) is False

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
        assert class_full_name(TestCase   ) == 'unittest.case.TestCase'

        module_name = self.__module__
        class_name  = self.__class__.__name__

        assert class_full_name(self) == f'{module_name}.{class_name}'               # Tests class_full_name with current test class instance

        assert class_full_name(type(self)) == 'test_Objects.test_Objects'           # Tests class_full_name with type of current test class

        assert class_full_name(int)  == 'builtins.int'                              # Tests class_full_name with built-in types
        assert class_full_name(str)  == 'builtins.str'

        class Custom_Class: pass                                                    # Tests class_full_name with custom class
        instance = Custom_Class()
        assert class_full_name(instance)     == f'{module_name}.Custom_Class'
        assert class_full_name(Custom_Class) == f'{module_name}.Custom_Class'

        assert class_full_name(None) is None                                        # Tests class_full_name with edge cases
        assert class_full_name("")   is None

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
        result = type_safe_convert.convert_dict_to_value_from_obj_annotation(an_class_2, 'an_dict', an_dict)

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

        result_a = type_safe_convert.convert_dict_to_value_from_obj_annotation(an_class_C, 'an_class_a', an_class_a_json)
        assert type(result_a) is Class_A
        result_b = type_safe_convert.convert_dict_to_value_from_obj_annotation(an_class_C, 'an_class_b', an_class_b_json)
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
        if sys.version_info > (3, 10):      # in 3.10 the output of dict_to_obj are not sorted
            assert dict_to_obj(dict_1) == __(an_bytes=b'the answer is...',
                                             an_int=42,
                                             an_dict=__(a=1, b=2, c=3),
                                             an_str='string_1')
            with Stdout() as stdout:
                print(dict_to_obj(dict_1))
            assert stdout.value() == "__(an_bytes=b'the answer is...', an_int=42, an_dict=__(a=1, b=2, c=3), an_str='string_1')\n"

            with Stdout() as stdout:
                from osbot_utils.utils.Dev import pprint
                pprint(dict_to_obj(dict_1))
            assert stdout.value() == ('\n'
                                      "__(an_bytes=b'the answer is...',\n"
                                      '   an_int=42,\n'
                                      '   an_dict=__(a=1, b=2, c=3),\n'
                                      "   an_str='string_1')\n")


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
        if sys.version_info > (3, 10):  # in 3.10 the output of dict_to_obj are not sorted
            assert obj == __(level_1 =__(level_2=__(level_3=__(an_int      = 100, a_list=[1, 2, 3]),
                                                               another_str = 'string_2'           ),
                                                               an_float    = 3.14                 ))

        # variation #3: test_dict_to_obj_with_list_and_tuple
        dict_3 = {
            'a_list': [1, 'string', {'key': 'value'}],
            'a_tuple': (1, 2, {'nested_key': 'nested_value'}),
        }

        obj = dict_to_obj(dict_3)
        assert obj.a_list[0]             == 1
        assert obj.a_list[1]             == 'string'
        assert obj.a_tuple[0]            == 1
        assert obj.a_tuple[1]            == 2
        assert obj.a_tuple[2].nested_key == 'nested_value'
        assert obj_to_dict(obj)          == dict_3
        assert obj                       == __(a_list  = [1, 'string', __(key='value')],
                                               a_tuple = (1, 2, __(nested_key='nested_value')))

        # variation #4:  test_dict_to_obj_empty_input
        dict_4 = {}
        obj = dict_to_obj(dict_4)
        assert obj_to_dict(obj) == dict_4
        assert obj == __()  # this is the default value for an empty object

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
        if sys.version_info > (3, 10):  # in 3.10 the output of dict_to_obj are not sorted
            assert obj              == __(a_bool=True, a_none=None, a_float=9.81, a_set={1, 2, 3})

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

        #assert getattr(obj, 'key_with space')            == 123                                        # but these can only be resolved using getattr
        #assert getattr(obj, 'key-with-dash' )            == [1, 2, 3]
        #assert getattr(obj, 'key.with.dot'  ).nested_key == 'nested_value'
        assert getattr(obj, 'key_with_space')            == 123                                         # after fix, we now get a valid key names
        assert getattr(obj, 'key_with_dash' )            == [1, 2, 3]
        assert getattr(obj, 'key_with_dot'  ).nested_key == 'nested_value'
        assert obj_to_dict(obj)                         != dict_7                                       # these are now different
        assert obj                                       == __(a_normal_key='value',
                                                         key_with_space=123,
                                                         key_with_dash=[1, 2, 3],
                                                         key_with_dot=__(nested_key='nested_value'))    # but this now works :)

    def test_dict_to_obj__using_Type_Safe_classes(self):
        class An_Class_A(Type_Safe):
            an_str  : str   = "value_1"
            an_int  : int   = 42
            an_bytes: bytes = b"value_2"

        class An_Class_B(Type_Safe):
            an_class_a: An_Class_A
            another_str   : str
            another_int   : int
            another_bytes : bytes

        if sys.version_info > (3, 10):  # in 3.10 the output of dict_to_obj are not sorted
            assert An_Class_B().obj() == __(an_class_a    = __(an_str   = 'value_1'  ,
                                                               an_int   = 42         ,
                                                               an_bytes = b'value_2' ),
                                            another_str   = ''  ,
                                            another_int   = 0   ,
                                            another_bytes = b'' )

    def test_dict_to_obj__regression(self):
        # before fix dict_to_obj only recognized 'dict' as a valid type, where now it uses  collections.abc.Mapping
        regular_dict = {'apple': 2, 'banana': 3}
        proxy_dict   = types.MappingProxyType(regular_dict)
        assert isinstance(proxy_dict, dict)         is False
        assert isinstance(proxy_dict, Mapping)      is True
        assert(obj_to_dict(dict_to_obj(proxy_dict)) == regular_dict)

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
            pytest.skip("Skipping test that doesn't work on 3.12 or higher")
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

    def test_value_type_matches_obj_annotation_for_union_and_annotated(self):

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

        _ = type_safe_validation.check_if__type_matches__obj_annotation__for_union_and_annotated

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

        assert type_safe_validation.obj_is_type_union_compatible(type(var_1), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_2), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_3), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_4), compatible_types) is True

        # Union types
        var_5: Union[str, int         ] = 2
        var_6: Union[int, float, bytes] = 3.14    # will work - type bytes is not in the compatible list, but var_6 is not assigned to it
        var_7: Union[int, float, bytes] = b'aaa'  # will fail - type bytes is not in the compatible list, and var_7 is assigned to it
        var_8: Union[str, int         ] = None
        var_9: Union[str, int         ] = None

        assert type_safe_validation.obj_is_type_union_compatible(Union[str, int]         , compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_5)             , compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_8)             , compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_9)             , compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(Union[int, float, bytes], compatible_types) is False  # Because bytes is not compatible
        assert type_safe_validation.obj_is_type_union_compatible(type(var_6)             , compatible_types) is True   # bytes could be one of the values, but it is not
        assert type_safe_validation.obj_is_type_union_compatible(type(var_7)             , compatible_types) is False  # now that bytes is one of the values, it fails

        # Optional types (which are essentially Union[type, NoneType])
        var_10: Optional[str  ] = None
        var_11: Optional[bytes] = None  # bytes is not in the compatible list, , but var_11 is not assigned to it
        var_12: Optional[str  ] = 'a'
        var_13: Optional[bytes] = 'a'
        var_14: Optional[bytes] = b'aaa'

        assert type_safe_validation.obj_is_type_union_compatible(type(var_10), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_11), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_12), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_13), compatible_types) is True   # todo: BUG type safe should had picked this up
        assert type_safe_validation.obj_is_type_union_compatible(type(var_14), compatible_types) is False  # Because bytes is not compatible

        # Complex case with nested Unions and Optionals
        var_15: Optional[Union[int, str, None ]] = None
        var_16: Optional[Union[int, str, bytes]] = None
        var_17: Optional[Union[int, str, bytes]] = 'a'
        var_18: Optional[Union[int, str, bytes]] = b'aaa'

        assert type_safe_validation.obj_is_type_union_compatible(type(var_15), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_16), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_17), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_18), compatible_types) is False

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
        assert type_safe_validation.obj_is_type_union_compatible(type(var_1), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_2), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_3), compatible_types) is True
        assert type_safe_validation.obj_is_type_union_compatible(type(var_4), compatible_types) is False
        assert type_safe_validation.obj_is_type_union_compatible(type(var_5), compatible_types) is False

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
        _ = type_safe_validation.check_if__type_matches__obj_annotation__for_attr
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
        _ = type_safe_validation.check_if__type_matches__obj_annotation__for_attr
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


    def test_enum_with_string_values(self):                                # Test enums with string values
        # Direct serialization of enum
        assert serialize_to_dict(Enum__LLM__Role.SYSTEM)    == 'system'
        assert serialize_to_dict(Enum__LLM__Role.USER)      == 'user'
        assert serialize_to_dict(Enum__LLM__Role.ASSISTANT) == 'assistant'
        assert serialize_to_dict(Enum__LLM__Role.TOOL)      == 'tool'

        # Should return the value, not the name
        assert serialize_to_dict(Enum__LLM__Role.SYSTEM) != 'SYSTEM'

    def test_enum_with_numeric_values(self):                              # Test enums with numeric values
        class NumericEnum(Enum):
            FIRST  = 1
            SECOND = 2
            THIRD  = 3

        assert serialize_to_dict(NumericEnum.FIRST)  == 1
        assert serialize_to_dict(NumericEnum.SECOND) == 2
        assert serialize_to_dict(NumericEnum.THIRD)  == 3

        # Verify type is int, not enum
        result = serialize_to_dict(NumericEnum.FIRST)
        assert type(result) is int

    def test_enum_with_bool_and_none_values(self):                       # Test edge case enum values
        class EdgeCaseEnum(Enum):
            TRUE_VAL  = True
            FALSE_VAL = False
            NONE_VAL  = None

        assert serialize_to_dict(EdgeCaseEnum.TRUE_VAL)  is True
        assert serialize_to_dict(EdgeCaseEnum.FALSE_VAL) is False
        assert serialize_to_dict(EdgeCaseEnum.NONE_VAL)  is None

    def test_enum_with_complex_values(self):                              # Test enums with list/dict/tuple values
        class ComplexEnum(Enum):
            LIST_VAL = [1, 2, 3]
            DICT_VAL = {'key': 'value', 'count': 42}
            TUPLE_VAL = ('a', 'b', 'c')
            SET_VAL   = {'x', 'y', 'z'}

        assert type(ComplexEnum.LIST_VAL.value ) is list
        assert type(ComplexEnum.DICT_VAL.value ) is dict
        assert type(ComplexEnum.TUPLE_VAL.value) is tuple
        assert type(ComplexEnum.SET_VAL.value  ) is set

        # Should recursively serialize complex values
        assert serialize_to_dict(ComplexEnum.LIST_VAL )   == 'LIST_VAL'
        assert serialize_to_dict(ComplexEnum.DICT_VAL )   == 'DICT_VAL'
        assert serialize_to_dict(ComplexEnum.TUPLE_VAL)   == 'TUPLE_VAL'
        assert serialize_to_dict(ComplexEnum.SET_VAL  )   == 'SET_VAL'


    def test_from_json__Enum_tuple_support(self):
        class An_Enum(tuple, Enum):
            AB = ('a', 'b')
            CD = ('c', 'd')

        class An_Class(Type_Safe):
            an_enum : An_Enum  # ← Stores the ENUM itself

        # This is the real round-trip test:
        an_class = An_Class(an_enum='AB')
        assert an_class.json() == {'an_enum': 'AB'}  # ✅ Serializes to name

        restored = An_Class.from_json(an_class.json())
        assert restored.an_enum == An_Enum.AB  # ✅ Should deserialize back to enum
        assert restored.an_enum == ('a', 'b')  # ✅ Enum value comparison works

    def test_enum_with_nested_complex_values(self):                       # Test nested serialization
        class NestedEnum(Enum):
            NESTED_LIST = [1, [2, 3], {'inner': 'dict'}]
            NESTED_DICT = {'list': [1, 2], 'dict': {'a': 'b'}}

        result_list = serialize_to_dict(NestedEnum.NESTED_LIST)
        assert result_list == 'NESTED_LIST' #[1, [2, 3], {'inner': 'dict'}]

        result_dict = serialize_to_dict(NestedEnum.NESTED_DICT)
        assert result_dict == 'NESTED_DICT' # {'list': [1, 2], 'dict': {'a': 'b'}}

    def test_enum_with_unsupported_value_types(self):                    # Test fallback to .name
        class CustomClass:
            def __init__(self):
                self.value = "custom"

        class UnsupportedEnum(Enum):
            CUSTOM_OBJ = CustomClass()
            LAMBDA_VAL = lambda x: x + 1

        # Should fall back to returning the name for non-serializable values
        assert serialize_to_dict(UnsupportedEnum.CUSTOM_OBJ) == 'CUSTOM_OBJ'
        assert serialize_to_dict(UnsupportedEnum.LAMBDA_VAL) != 'LAMBDA_VAL'        # due to python limitations serialize_to_dict will get the function directly
        assert serialize_to_dict(UnsupportedEnum.LAMBDA_VAL) == '<lambda>'          # so the best we can do is to get the value of the callable


    def test_enum_in_type_safe_class(self):                              # Test enum in Type_Safe context
        class Schema__Message(Type_Safe):
            role    : Enum__LLM__Role
            content : str

        message = Schema__Message()
        message.role = Enum__LLM__Role.USER
        message.content = "Hello"

        # Get the JSON representation
        json_data = message.json()

        # The enum should be serialized to its string value
        assert json_data == {'role': 'user', 'content': 'Hello'}
        assert type(json_data['role']) is str
        assert json_data['role'] == 'user'

    def test_enum_in_nested_structures(self):                            # Test enum in lists/dicts
        # Enum in list
        data_list = [Enum__LLM__Role.SYSTEM, "text", 123]
        result = serialize_to_dict(data_list)
        assert result == ['system', 'text', 123]
        assert type(result[0]) is str

        # Enum in dict
        data_dict = {
            'role': Enum__LLM__Role.ASSISTANT,
            'count': 42,
            'active': True
        }
        result = serialize_to_dict(data_dict)
        assert result == {'role': 'assistant', 'count': 42, 'active': True}
        assert type(result['role']) is str

    def test_multiple_enum_types(self):                                  # Test different enum types together
        class Status(Enum):
            ACTIVE = 'active'
            INACTIVE = 'inactive'

        class Priority(Enum):
            HIGH = 1
            MEDIUM = 2
            LOW = 3

        data = {
            'role': Enum__LLM__Role.SYSTEM,
            'status': Status.ACTIVE,
            'priority': Priority.HIGH
        }

        result = serialize_to_dict(data)
        assert result == {
            'role': 'system',
            'status': 'active',
            'priority': 1
        }

        # Verify types
        assert type(result['role']) is str
        assert type(result['status']) is str
        assert type(result['priority']) is int

    def test_enum_round_trip_serialization(self):                       # Test full round-trip
        class Schema__Config(Type_Safe):
            role     : Enum__LLM__Role
            settings : dict

        # Create and populate
        original = Schema__Config()
        original.role = Enum__LLM__Role.ASSISTANT
        original.settings = {'temperature': 0.7}


        # Serialize
        json_data = original.json()
        assert json_data == {'role': 'assistant', 'settings': {'temperature': 0.7}}
        assert type(json_data['role']) is str

        restored = Schema__Config.from_json(json_data)
        assert type(restored.role)  is Enum__LLM__Role
        assert restored.role        == Enum__LLM__Role.ASSISTANT
        assert restored.role.value  == 'assistant'

    def test_serialize_callable_types(self):                                    # Test various callable serialization
        # Regular function
        def named_function():
            return "test"

        assert serialize_to_dict(named_function) == 'named_function'

        # Lambda
        lambda_func = lambda x: x * 2
        assert serialize_to_dict(lambda_func) == '<lambda>'

        # Built-in function
        assert serialize_to_dict(len) == 'len'
        assert serialize_to_dict(print) == 'print'

        # Method
        class MyClass:
            def my_method(self):
                pass

        obj = MyClass()
        assert serialize_to_dict(obj.my_method) == 'my_method'

        # Static method
        class WithStatic:
            @staticmethod
            def static_method():
                pass

        assert serialize_to_dict(WithStatic.static_method) == 'static_method'

    def test_serialize_class_vs_instance(self):                                # Test class handling
        class TestClass:
            value = "class_value"

            def __init__(self):
                self.instance_value = "instance"

        # Instance should serialize its __dict__
        instance = TestClass()
        assert serialize_to_dict(instance) == {'instance_value': 'instance'}

        # Class itself is callable, should return its name
        assert serialize_to_dict(TestClass) == 'test_Objects.TestClass'

        # Type objects
        assert serialize_to_dict(int) == 'builtins.int'
        assert serialize_to_dict(str) == 'builtins.str'
        assert serialize_to_dict(list) == 'builtins.list'

    def test_serialize_nested_callables(self):                                 # Test callables in structures
        def named_func(x):
            return x
        def named_validator(value):
            return True

        # Callable in list
        data_list = [lambda x: x, named_func, "text"]
        result = serialize_to_dict(data_list)
        assert result == ['<lambda>', 'named_func', 'text']

        # Callable in dict
        data_dict = {
            'processor': lambda x: x * 2,
            'validator': named_validator,
            'name': 'test'
        }
        result = serialize_to_dict(data_dict)
        assert result == {
            'processor': '<lambda>',
            'validator': 'named_validator',
            'name': 'test'
        }

        # Callable in tuple (becomes list)
        data_tuple = (lambda: None, print, "value")
        result = serialize_to_dict(data_tuple)
        assert result == ['<lambda>', 'print', 'value']

    def test_serialize_callable_edge_cases(self):                              # Test edge cases with callables
        # Partial function
        from functools import partial

        def add(a, b):
            return a + b

        add_five = partial(add, 5)
        assert serialize_to_dict(add_five) == 'partial'

        # Callable class instance
        class CallableClass:
            def __call__(self):
                return "called"

            def __init__(self):
                self.data = "test"

        callable_obj = CallableClass()
        result = serialize_to_dict(callable_obj)
        assert result == '__call__' or result == 'CallableClass'

    def test_serialize_enum_with_callable_workaround(self):                    # Test workaround for callable enum values
        class FunctionEnum(Enum):
            FUNC1 = lambda x: x + 1
            FUNC2 = lambda x: x * 2

        # Direct access gives us the lambda
        assert serialize_to_dict(FunctionEnum.FUNC1) == '<lambda>'
        assert serialize_to_dict(FunctionEnum.FUNC2) == '<lambda>'

    def test_serialize_set_types(self):                                        # Test set serialization
        # Basic set
        simple_set = {1, 2, 3}
        result = serialize_to_dict(simple_set)
        assert type(result) is list
        assert sorted(result) == [1, 2, 3]

        # String set
        string_set = {'apple', 'banana', 'cherry'}
        result = serialize_to_dict(string_set)
        assert type(result) is list
        assert sorted(result) == ['apple', 'banana', 'cherry']

        # Mixed type set
        mixed_set = {1, 'two', 3.0}
        result = serialize_to_dict(mixed_set)
        assert type(result) is list
        assert len(result) == 3
        assert 1 in result
        assert 'two' in result
        assert 3.0 in result

        # Empty set
        empty_set = set()
        result = serialize_to_dict(empty_set)
        assert result == []

    def test_serialize_nested_sets(self):                                      # Test sets in nested structures
        # Set in dict
        data_dict = {
            'tags': {'python', 'coding', 'test'},
            'count': 3
        }
        result = serialize_to_dict(data_dict)
        assert type(result['tags']) is list
        assert sorted(result['tags']) == ['coding', 'python', 'test']

        # Set in list
        data_list = [{'a', 'b'}, 'text', 123]
        result = serialize_to_dict(data_list)
        assert type(result[0]) is list
        assert sorted(result[0]) == ['a', 'b']

        # Set containing unhashable types gets filtered
        # (Can't actually create this in Python, but documenting the concept)

    def test_enum_round_trip_with_complex_values(self):                       # Test round-trip isn't preserved for complex types
        class ComplexEnum(Enum):
            LIST_VAL  = [1, 2, 3]
            DICT_VAL  = {'key': 'value', 'count': 42}
            TUPLE_VAL = ('a', 'b', 'c')
            SET_VAL   = {'x', 'y', 'z'}

        # Serialize each enum value
        serialized_list  = serialize_to_dict(ComplexEnum.LIST_VAL)
        serialized_dict  = serialize_to_dict(ComplexEnum.DICT_VAL)
        serialized_tuple = serialize_to_dict(ComplexEnum.TUPLE_VAL)
        serialized_set   = serialize_to_dict(ComplexEnum.SET_VAL)

        # Verify serialization results
        #assert serialized_list  == [1, 2, 3]
        #assert serialized_dict  == {'key': 'value', 'count': 42}
        #assert serialized_tuple == ['a', 'b', 'c']                            # Tuple becomes list
        #assert sorted(serialized_set) == ['x', 'y', 'z']                      # Set becomes list

        assert serialized_list        == 'LIST_VAL'
        assert serialized_dict        == 'DICT_VAL'
        assert serialized_tuple       == 'TUPLE_VAL'
        assert serialized_set         == 'SET_VAL'

        # Round-trip test - Type_Safe with enum
        class Schema__Config(Type_Safe):
            list_setting  : List[int]
            dict_setting  : Dict[str, Any]
            tuple_setting : List[str]                                         # Can't preserve tuple
            set_setting   : List[str]                                         # Can't preserve set

        config = Schema__Config()
        config.list_setting  = ComplexEnum.LIST_VAL.value
        config.dict_setting  = ComplexEnum.DICT_VAL.value
        config.tuple_setting = list(ComplexEnum.TUPLE_VAL.value)              # Must convert
        config.set_setting   = list(ComplexEnum.SET_VAL.value)                # Must convert

        # Serialize to JSON
        json_data = config.json()

        # Verify JSON structure
        assert type(json_data['set_setting']) is list
        json_data['set_setting'] = sorted(json_data['set_setting'])
        assert json_data == {
            'list_setting': [1, 2, 3],
            'dict_setting': {'key': 'value', 'count': 42},
            'tuple_setting': ['a', 'b', 'c'],
            'set_setting': sorted(list(ComplexEnum.SET_VAL.value))            # Order might vary
        }

        # Deserialize
        restored = Schema__Config.from_json(json_data)

        # Lists and dicts preserve type
        assert type(restored.list_setting) in [list, Type_Safe__List]
        assert type(restored.dict_setting) in [dict, Type_Safe__Dict]

        # Tuples and sets cannot be restored as original types
        assert type(restored.tuple_setting) in [list, Type_Safe__List]        # Not tuple
        assert type(restored.set_setting  ) in [list, Type_Safe__List]          # Not set

    def test_type_safe_with_set_attribute(self):                              # Test Type_Safe classes with set attributes
        class Schema__Tags(Type_Safe):
            tags: Set[str]
            ids : Set[int]

        schema = Schema__Tags()
        schema.tags = {'python', 'testing', 'code'}
        schema.ids = {1, 2, 3}

        # Serialize
        json_data = schema.json()

        # Sets become lists in JSON
        assert type(json_data['tags']) is list
        assert type(json_data['ids']) is list
        assert sorted(json_data['tags']) == ['code', 'python', 'testing']
        assert sorted(json_data['ids']) == [1, 2, 3]

        # Round-trip
        restored = Schema__Tags.from_json(json_data)

        # Check if Type_Safe restores them as sets or keeps as lists
        # (This depends on Type_Safe implementation)
        assert len(restored.tags) == 3
        assert len(restored.ids) == 3
        assert 'python' in restored.tags
        assert 1 in restored.ids

    def test_complex_enum_in_type_safe(self):                                # Test using complex enums in Type_Safe
        class DataEnum(Enum):
            DEFAULT_TAGS = {'tag1', 'tag2', 'tag3'}
            DEFAULT_MAP  = {'key1': 'val1', 'key2': 'val2'}
            DEFAULT_LIST = [1, 2, 3]
            DEFAULT_TUPLE = ('a', 'b', 'c')

        class Schema__Settings(Type_Safe):
            active_tags : List[str]
            config_map  : Dict[str, str]
            values      : List[int]
            sequence    : List[str]

        settings = Schema__Settings()

        # Assign enum values (sets/tuples must be converted)
        settings.active_tags = list(DataEnum.DEFAULT_TAGS.value)
        settings.config_map  = DataEnum.DEFAULT_MAP.value
        settings.values      = DataEnum.DEFAULT_LIST.value
        settings.sequence    = list(DataEnum.DEFAULT_TUPLE.value)

        # Serialize
        json_data = settings.json()

        # Verify all are in JSON-compatible format
        assert all(isinstance(v, (list, dict, str, int, float, bool, type(None)))
                   for v in json_data.values())

        # Round-trip
        restored = Schema__Settings.from_json(json_data)
        assert sorted(restored.active_tags) == sorted(list(DataEnum.DEFAULT_TAGS.value))
        assert restored.config_map == DataEnum.DEFAULT_MAP.value
        assert restored.values == DataEnum.DEFAULT_LIST.value
        assert restored.sequence == list(DataEnum.DEFAULT_TUPLE.value)

    def test__regression__from_json__enum_tuple_support(self):
        from enum import Enum

        class An_Enum(tuple, Enum):
            AB = ('a', 'b')
            CD = ('c', 'd')

        class An_Class(Type_Safe):
            an_enum : An_Enum

        assert An_Class().obj()  == __()                # is this a bug?
        assert An_Class().obj()  == __(an_enum = None)
        assert An_Class().json() == {'an_enum': None}
        assert An_Class(an_enum='AB'      ).an_enum == An_Enum.AB
        assert An_Class(an_enum=An_Enum.AB).an_enum == An_Enum.AB
        assert An_Class(an_enum=An_Enum.AB).an_enum == ('a', 'b')
        assert An_Class(an_enum='AB'      ).an_enum == ('a', 'b')
        assert An_Class(an_enum=An_Enum.AB).an_enum != An_Enum.CD

        assert An_Class.from_json(An_Class().json()).json() == {'an_enum': None}
        #error_message = "unhashable type: 'list'"
        #with pytest.raises(TypeError, match=error_message):
        #    An_Class.from_json(An_Class(an_enum='AB').json())            # BUG, this should have worked
        An_Class.from_json(An_Class(an_enum='AB').json())

        an_class = An_Class(an_enum=An_Enum.CD)
        # with pytest.raises(TypeError, match=error_message):
        #     An_Class.from_json(an_class.json())                         # BUG, this should have worked
        An_Class.from_json(an_class.json())
        #with pytest.raises(TypeError, match=error_message):
        #assert an_class.json() == {'an_enum': ['c', 'd']}               # BUG this be shoud be 'CD'?
        assert an_class.json() == {'an_enum': 'CD' }

        # error_message_2 = ("assert {'an_enum': ['c', 'd']} == {'an_enum': <An_Enum.CD: ('c', 'd')>}\n  \n  "
        #                    "Differing items:\n  {'an_enum': ['c', 'd']} != "
        #                    "{'an_enum': <An_Enum.CD: ('c', 'd')>}\n  \n  "
        #                    "Full diff:\n    {\n  -     'an_enum': <An_Enum.CD: ('c', 'd')>,\n  +    "
        #                    " 'an_enum': [\n  +         'c',\n  +         'd',\n  +     ],\n    }")
        # with pytest.raises(AssertionError, match=re.escape(error_message_2)):
        #     assert an_class.json() == {'an_enum': An_Enum.CD}               #
        assert an_class.json() == {'an_enum': 'CD'}
        assert An_Class.from_json({'an_enum': 'CD'}      ).an_enum == ('c', 'd')
        assert An_Class.from_json({'an_enum': An_Enum.CD}).an_enum == ('c', 'd')
        assert An_Class.from_json(An_Class(an_enum='AB').json()).json() == {'an_enum': 'AB'}