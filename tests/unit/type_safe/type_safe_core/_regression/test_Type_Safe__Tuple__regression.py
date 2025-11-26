import pytest
from typing                                                                     import Dict, Tuple, Type
from unittest                                                                   import TestCase
from osbot_utils.testing.__                                                     import __
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple          import Type_Safe__Tuple


class test_Type_Safe__Tuple__regression(TestCase):
    def test__regression__tuple__type_roundtrip(self):
        class An_Class(Type_Safe):
            an_tuple      : Tuple[Type,Type]
            an_dict_tuple : Dict[str, Tuple[Type,Type]]

        assert An_Class().json() == {'an_dict_tuple': {}, 'an_tuple': []}
        assert An_Class().obj () == __(an_tuple=[], an_dict_tuple=__())



        #assert An_Class(an_tuple=(str, int)).json() == {'an_dict_tuple': {}, 'an_tuple': [ str, int]}                   # BUG , it should be ['builtins.str', 'builtins.int']
        #assert An_Class(an_tuple=(str, int)).obj () == __(an_tuple=[str, int], an_dict_tuple=__())                       # BUG
        assert An_Class(an_tuple=(str, int)).json() == {'an_dict_tuple': {}, 'an_tuple': ['builtins.str', 'builtins.int']}
        assert An_Class(an_tuple=(str, int)).obj () == __(an_tuple=['builtins.str', 'builtins.int'], an_dict_tuple=__())

        # assert An_Class(an_dict_tuple={'an-id': (str, int)}).json() == { 'an_dict_tuple': {'an-id': (str, int)},        # BUG , it should be ('builtins.str', 'builtins.int')
        #                                                                  'an_tuple'     : []                   }
        #
        # assert An_Class(an_dict_tuple={'an-id': (Safe_Str__Id, Safe_Str__Id)}).json() == { 'an_dict_tuple': { 'an-id': ( Safe_Str__Id, Safe_Str__Id)},       # BUG
        #                                                                                    'an_tuple'     : []}

        assert An_Class(an_dict_tuple={'an-id': (str, int)}).json() == { 'an_dict_tuple': {'an-id': ('builtins.str', 'builtins.int')},        # BUG , it should be ('builtins.str', 'builtins.int')
                                                                         'an_tuple'     : []                   }

        assert An_Class(an_dict_tuple={'an-id': (Safe_Str__Id, Safe_Str__Id)}).json() == { 'an_dict_tuple': { 'an-id': ( 'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id',
                                                                                                                         'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id')},       # BUG
                                                                                           'an_tuple'     : []}

        # assert An_Class(an_dict_tuple={'an_id': (Safe_Str__Id, Safe_Str__Id)}).obj() == __(an_tuple      = [],
        #                                                                                    an_dict_tuple = __(an_id=(Safe_Str__Id,Safe_Str__Id)))  # BUG
        #
        # with An_Class() as _:
        #     _.an_tuple= (Safe_Str__Id, Safe_Str__Id)
        #     assert _.obj() == __( an_tuple     = [Safe_Str__Id,Safe_Str__Id],                                                                      # BUG
        #                           an_dict_tuple = __())

        assert An_Class(an_dict_tuple={'an_id': (Safe_Str__Id, Safe_Str__Id)}).obj() == __(an_tuple      = [],
                                                                                           an_dict_tuple = __(an_id=('osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id',
                                                                                                                     'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id')))

        with An_Class() as _:
            _.an_tuple= (Safe_Str__Id, Safe_Str__Id)
            assert _.obj() == __( an_tuple     = ['osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id',
                                                  'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id'],
                                  an_dict_tuple = __())


        #  check roundtrip
        assert An_Class.from_json(An_Class(                                       ).json()).json() ==  {'an_dict_tuple': {}, 'an_tuple': []}
        assert An_Class.from_json(An_Class(an_tuple=(str, int)                    ).json()).json() == {'an_dict_tuple': {}, 'an_tuple': ['builtins.str', 'builtins.int']}

        assert An_Class.from_json(An_Class(an_dict_tuple={'an-id': (str, int)    }).json()).json() == { 'an_dict_tuple': {'an-id': ('builtins.str', 'builtins.int')},        # BUG , it should be ('builtins.str', 'builtins.int')
                                                                                                    'an_tuple'     : []                   }
        assert An_Class.from_json(An_Class(an_dict_tuple={'an-id': (Safe_Str__Id,
                                                                    Safe_Str__Id)}).json()).json() == { 'an_dict_tuple': { 'an-id': ( 'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id',
                                                                                                                         'osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id.Safe_Str__Id')},       # BUG
                                                                                                        'an_tuple'     : []}


    def test__regression__type_safe_tuple__bypasses_on_add_mul(self):
        tuple1 = Type_Safe__Tuple(expected_types=(str, int), items=('hello', 42))

        # BUG 1: __add__ (tuple concatenation) returns plain tuple
        error_message_1 = "Cannot concatenate Type_Safe__Tuple with tuple. Use Type_Safe__Tuple for both operands to preserve type safety."
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            tuple1 + ('world',)
        #result = tuple1 + ('world',)
        #assert type(result) is tuple                         # BUG: should be Type_Safe__Tuple or raise error

        # BUG 2: __mul__ (tuple repetition) returns plain tuple
        result = tuple1 * 2
        #assert type(result) is tuple                         # BUG: should be Type_Safe__Tuple
        assert type(result) is Type_Safe__Tuple