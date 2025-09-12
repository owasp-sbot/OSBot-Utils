import pytest
from typing                                                             import List, Dict, Set, Tuple
from unittest                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                import Safe_Str
from osbot_utils.utils.Objects                                          import __
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict   import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List   import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set    import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple  import Type_Safe__Tuple


class test_Type_Safe__List__regression(TestCase):

    def test__bug__in_type_safe__list__nested_conversion(self):
        class Schema__Model(Type_Safe):
            an_list : List[Safe_Str]

        class Schema__Models(Type_Safe):
            data: List[Schema__Model]

        model        = Schema__Model (an_list=[Safe_Str('abc')])
        models       = Schema__Models(data=[model])
        model__json  = model.json()
        models__json = models.json()

        assert model__json  == {'an_list': ['abc']}
        assert models__json == {'data': [{'an_list': ['abc']}]}

        model__roundtrip = Schema__Model.from_json(model__json)                     # roundtrip model directly
        assert model__roundtrip.json() == model__json                               # works

        # BUG
        # error_message_2 = "In Type_Safe__List: Invalid type for item: Expected 'Safe_Str', but got 'str'"
        # with pytest.raises(TypeError, match=error_message_2):
        #     Schema__Model (an_list=['abc'])                     # BUG this should support just 'abc'
        assert Schema__Model(an_list=['abc']).json() == {'an_list': ['abc']}                            # FIXED

        # error_message_2 = "In Type_Safe__List: Invalid type for item: Expected 'Safe_Str', but got 'str'"
        # with pytest.raises(TypeError, match=error_message_2):
        #     Schema__Models.from_json(models__json)              # BUG but roundtrip from list fails
        assert Schema__Models.from_json(models__json).json() == {'data': [{'an_list': ['abc']}]}        # FIXED


    def test__regression__list__forward_ref__fails_roundtrip(self):
        class An_Class(Type_Safe):
            an_str: str
            an_list: List['An_Class']
        an_class_1      = An_Class(an_str  = 'an_class_1')
        an_class_2      = An_Class(an_str  = 'an_class_2' ,
                                   an_list = [an_class_1])
        an_class_2_json = an_class_2.json()
        assert  an_class_2_json == {'an_list': [{'an_list': []            ,
                                                  'an_str' : 'an_class_1'}],
                                     'an_str' : 'an_class_2' }
        #with pytest.raises(TypeError, match="'ForwardRef' object is not callable"):
        #    An_Class.from_json(an_class_2_json)                                    # Fixed: BUG: ForwardRef not being handled
        assert  An_Class.from_json(an_class_2_json).json() == an_class_2_json

    def test__regression__list__type_safety__not_checked_on_assigment(self):
        class An_Class(Type_Safe):
            list__str : List[str]

        with An_Class() as _:
            assert type(_.list__str) is Type_Safe__List
            assert _.list__str.expected_type is str

            with pytest.raises(TypeError, match="In Type_Safe__List: Invalid type for item: Expected 'str', but got 'int'"):
                _.list__str = [123]
                #_.list__str = [123]                                 # Fixed: BUG: this breaks type safety (an exception should have been raised)
                #assert type(_.list__str) is list                    # Fixed: BUG: should be Type_Safe__List

            _.list__str = []                                        # this should be allowed, but not if we lost the Type_Safe__List and the expected_type
            #assert type(_.list__str) is list                       # FIXED: BUG: should be Type_Safe__List
            assert type(_.list__str) is Type_Safe__List             # confirm we didn't list the Type_Safe__List



    def test__regression__type_safe_list__on__init__with_values(self):
        class An_Class(Type_Safe):
            an_dict : Dict [str, str]
            an_list : List [str     ]
            an_set  : Set  [str     ]
            an_tuple: Tuple[str, str]

        kwargs = dict(an_dict  = dict (aaa="42" )   ,
                      an_list  = list (['aaa'])     ,
                      an_set   = set  ('aa'   )     ,
                      an_tuple = tuple(('aaa','42')))

        an_class = An_Class(**kwargs)
        assert type(an_class.an_list ) is Type_Safe__List   # FIXED: BUG
        assert type(an_class.an_dict ) is Type_Safe__Dict   # OK
        assert type(an_class.an_set  ) is Type_Safe__Set    # FIXED: BUG
        assert type(an_class.an_tuple) is Type_Safe__Tuple  # FIXED: BUG

        assert an_class.obj() == __(an_dict  = __(aaa='42' ),
                                    an_list  = ['aaa'      ],
                                    an_set   = ['a'        ],
                                    an_tuple = ['aaa', '42'])

    def test__regression__type_safe_list__on__init(self):
        class An_Class(Type_Safe):
            an_dict : Dict [str, str]
            an_list : List [str     ]
            an_set  : Set  [str     ]
            an_tuple: Tuple[str, str]

        an_class = An_Class()
        assert type(an_class.an_list ) is Type_Safe__List   # OK
        assert type(an_class.an_dict ) is Type_Safe__Dict   # OK
        assert type(an_class.an_set  ) is Type_Safe__Set    # OK
        assert type(an_class.an_tuple) is Type_Safe__Tuple  # OK

        kwargs = dict(an_dict  = dict()  ,
                      an_list  = []      ,
                      an_set   = set()   ,
                      an_tuple = tuple() )
        an_class_2 = An_Class(**kwargs)
        assert type(an_class_2.an_dict ) is Type_Safe__Dict                     # FIXED: BUG, should be Type_Safe__List
        assert type(an_class_2.an_list ) is Type_Safe__List
        assert type(an_class_2.an_set  ) is Type_Safe__Set
        assert type(an_class_2.an_tuple) is Type_Safe__Tuple
        assert an_class_2.an_dict  .expected_key_type   == str
        assert an_class_2.an_dict  .expected_value_type == str
        assert an_class_2.an_list  .expected_type       == str
        assert an_class_2.an_tuple .expected_types      == (str, str)
        assert an_class_2.an_set   .expected_type       == str
        assert an_class_2.an_set   .expected_type       == str

    def test__regression__nested_types__not_supported__in_list(self):
        class An_Class(Type_Safe):
            an_str  : str
            an_list : List['An_Class']

        an_class   = An_Class()
        assert type(an_class.an_list) is Type_Safe__List
        assert an_class.an_list       == []

        an_class_a = An_Class()
        an_class.an_list.append(an_class_a)
        with pytest.raises(TypeError, match="In Type_Safe__List: Invalid type for item: Expected 'An_Class', but got 'str'"):
            an_class.an_list.append('b'       )     # BUG: as above

    def test__regression__type_safe_list_with_forward_references(self):
        class An_Class(Type_Safe):
            an_list__self_reference: List['An_Class']

        an_class = An_Class()
        an_class.an_list__self_reference.append(An_Class())

        #an_class.an_list__self_reference.append(1)  # BUG , type safety not checked on forward references
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'int'"):
            an_class.an_list__self_reference.append(1)

    def test__regression__json_is_not_supported(self):
        class An_Class(Type_Safe):
            an_str  : str
            an_list : List['An_Class']

        an_class = An_Class()
        an_class.an_list.append(An_Class())
        assert an_class.json() == {'an_list': [{'an_list': [], 'an_str': ''}], 'an_str': ''}

        # with pytest.raises(AttributeError, match = "Type_Safe__List' object has no attribute 'json'"):
        #     assert an_class.an_list.json()

        assert an_class.an_list.json() == [{'an_list': [], 'an_str': ''}]