from unittest                                           import TestCase

from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_int import Safe_Int
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__IP_Address import Safe_Str__IP_Address


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