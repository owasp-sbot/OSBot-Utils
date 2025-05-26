from unittest                                           import TestCase
from osbot_utils.type_safe.Type_Safe__Primitive         import Type_Safe__Primitive


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