import re
from unittest                                                                       import TestCase
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                     import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Float                               import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_Int                                 import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_Str                                 import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode         import Enum__Safe_Str__Regex_Mode
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                   import Safe_Id
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__IP_Address import Safe_Str__IP_Address
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Username       import Safe_Str__Username


class test_Type_Safe__Primitive(TestCase):

    def test____primitive_base__(self):
        class An_Safe_Int(Type_Safe__Primitive, int): pass

        an_safe_int = An_Safe_Int(1)
        assert an_safe_int                                   == 1
        assert type(an_safe_int)                             is An_Safe_Int
        assert issubclass(An_Safe_Int, Type_Safe__Primitive) is True
        assert issubclass(An_Safe_Int, int                 ) is True

        assert hasattr(an_safe_int, "__primitive_base__")    is True
        assert getattr(an_safe_int, "__primitive_base__")    is int
        assert an_safe_int.__primitive_base__                is int

    def test__type_safe_primitive_default_values(self): # Test that primitive default values are automatically converted

        class Schema(Type_Safe):
            safe_str: Safe_Str             = 'default/value'
            safe_int: Safe_Int             = 42
            safe_id : Safe_Id              = 'default-id'
            safe_ip : Safe_Str__IP_Address = '192.168.1.1'

        # Should work with default values
        instance = Schema()
        assert isinstance(instance.safe_str, Safe_Str            )
        assert isinstance(instance.safe_int, Safe_Int            )
        assert isinstance(instance.safe_id , Safe_Id             )
        assert isinstance(instance.safe_ip , Safe_Str__IP_Address)

        assert instance.json() == { 'safe_str': 'default_value',
                                    'safe_int': 42             ,
                                    'safe_id' : 'default-id'   ,
                                    'safe_ip' : '192.168.1.1'  }

        # Should also work with override values
        instance2 = Schema(safe_str='override', safe_int=100)
        assert instance2.safe_str == 'override'
        assert instance2.safe_int == 100

    def test__to_primitive_method(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class An_Safe_Int(Type_Safe__Primitive, int):
            pass

        class An_Safe_Float(Type_Safe__Primitive, float):
            pass

        # Test string primitive
        safe_str = An_Safe_Str('hello')
        assert safe_str.__to_primitive__()       == 'hello'
        assert type(safe_str.__to_primitive__()) is str
        assert type(safe_str) is An_Safe_Str

        # Test int primitive
        safe_int = An_Safe_Int(42)
        assert safe_int.__to_primitive__() == 42
        assert type(safe_int.__to_primitive__()) is int
        assert type(safe_int) is An_Safe_Int

        # Test float primitive
        safe_float = An_Safe_Float(3.14)
        assert safe_float.__to_primitive__() == 3.14
        assert type(safe_float.__to_primitive__()) is float
        assert type(safe_float) is An_Safe_Float

        # Test with Safe_Id
        safe_id = Safe_Id('test-id')
        assert safe_id.__to_primitive__() == 'test-id'
        assert type(safe_id.__to_primitive__()) is str

    def test__primitive_in_collections(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        class Schema(Type_Safe):
            str_list: list[An_Safe_Str      ]
            str_dict: dict[An_Safe_Str, int ]
            str_set : set[An_Safe_Str       ]

        # Test with collections
        schema = Schema(str_list= ['a', 'b', 'c' ],
                        str_dict= {'x': 1, 'y': 2},
                        str_set = {'p', 'q', 'r' })

        # Verify types are converted
        assert all(isinstance (item, An_Safe_Str) for item in schema.str_list      )
        assert all(isinstance (key , An_Safe_Str) for key in schema.str_dict.keys())
        assert all(isinstance (item, An_Safe_Str) for item in schema.str_set       )

        # Test json serialization uses primitives
        json_data     = schema.json()
        expected_data = {'str_list': ['a', 'b', 'c' ],
                         'str_dict': {'x': 1, 'y': 2},
                         'str_set' : ['p', 'q', 'r']}
        json_data['str_set'] = sorted(json_data['str_set'])                 # we need to do this because the sets don't guarantee the same order
        assert json_data == expected_data # sets serialize as lists

    def test__primitive_edge_cases(self):
        class An_Safe_Str(Type_Safe__Primitive, str):
            pass

        # Test empty string
        empty = An_Safe_Str('')
        assert empty.__to_primitive__() == ''
        assert type(empty.__to_primitive__()) is str

        # Test with special characters
        special = An_Safe_Str('!@#$%^&*()')
        assert special.__to_primitive__() == '!@#$%^&*()'

        class Broken_Primitive(Type_Safe__Primitive, str):                  # Test primitive without __primitive_base__ set (edge case)
            __primitive_base__ = None                                       # Explicitly break it

        broken = Broken_Primitive('test')

        assert broken.__to_primitive__()       == 'test'                    # Should fallback to str
        assert type(broken.__to_primitive__()) is str

    def test__primitive_comparison_with_json(self):
        class An_Safe_Id(Type_Safe__Primitive, str):
            pass

        class Schema(Type_Safe):
            id_map: dict[An_Safe_Id, str]

        schema = Schema(id_map={'id1': 'value1', 'id2': 'value2'})

        # Before fix: keys would remain as An_Safe_Id in json
        # After fix: keys should be primitive strings
        json_data = schema.json()

        # Can access with primitive string keys
        assert json_data['id_map']['id1'] == 'value1'
        assert json_data['id_map']['id2'] == 'value2'

        # Round trip should work
        restored = Schema.from_json(json_data)
        assert isinstance(list(restored.id_map.keys())[0], An_Safe_Id)
        assert restored.id_map['id1'] == 'value1'

    def test_obj(self):
        assert Safe_Int().obj() == __(min_value        = None               ,
                                      max_value        = None               ,
                                      allow_none       = True               ,
                                      allow_bool       = False              ,
                                      allow_str        = True               ,
                                      strict_type      = False              ,
                                      clamp_to_range   = False              )

        assert Safe_Float().obj() == __(min_value       = None             ,
                                        max_value       = None             ,
                                        allow_none      = True             ,
                                        allow_bool      = False            ,
                                        allow_inf       = False            ,
                                        allow_str       = True             ,
                                        allow_int       = True             ,
                                        strict_type     = False            ,
                                        decimal_places  = None             ,
                                        use_decimal     = True             ,
                                        epsilon         = 1e-09            ,
                                        round_output    = True             ,
                                        clamp_to_range  = False            )

        assert Safe_Str().obj() == __(allow_all_replacement_char  =  True                                             ,
                                      allow_empty                 = True                                             ,
                                      exact_length                = False                                            ,
                                      max_length                  = 512                                              ,
                                      regex                       = re.compile('[^a-zA-Z0-9]')                       ,
                                      regex_mode                  = Enum__Safe_Str__Regex_Mode.REPLACE              ,
                                      replacement_char            = '_'                                              ,
                                      strict_validation           = False                                            ,
                                      to_lower_case               = False                                            ,
                                      trim_whitespace             = False                                            )

        assert Safe_Str__Username().obj() == __(allow_all_replacement_char  = True                                   ,
                                                allow_empty                 = True                                   ,
                                                exact_length                = False                                  ,
                                                max_length                  = 512                                    ,
                                                regex                       = re.compile('[^a-zA-Z0-9]')             ,
                                                regex_mode                  = Enum__Safe_Str__Regex_Mode.REPLACE    ,
                                                replacement_char            = '_'                                    ,
                                                strict_validation           = False                                  ,
                                                to_lower_case               = False                                  ,
                                                trim_whitespace             = False                                  )

        assert Safe_Str__IP_Address().obj() == __()
