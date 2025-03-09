import pytest
from typing                                 import List, Dict, Set, Tuple
from unittest                               import TestCase
from osbot_utils.type_safe.Type_Safe        import Type_Safe
from osbot_utils.type_safe.Type_Safe__Dict  import Type_Safe__Dict
from osbot_utils.type_safe.Type_Safe__List  import Type_Safe__List
from osbot_utils.type_safe.Type_Safe__Set   import Type_Safe__Set
from osbot_utils.type_safe.Type_Safe__Tuple import Type_Safe__Tuple
from osbot_utils.utils.Objects              import __


class test_Type_Safe__List__regression(TestCase):

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