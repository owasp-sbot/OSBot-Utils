from unittest                                                        import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                  import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_Int                  import Safe_Int
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id    import Safe_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set import Type_Safe__Set


class test_Type_Safe__Set(TestCase):

    def test__contains__with_type_safe_primitive(self):
        # Test with Safe_Str type
        safe_str_set = Type_Safe__Set(Safe_Str)
        safe_str_set.add(Safe_Str('hello'))
        safe_str_set.add(Safe_Str('world'))

        # Direct Safe_Str instance lookup
        assert Safe_Str('hello') in safe_str_set
        assert Safe_Str('world') in safe_str_set
        assert Safe_Str('foo')   not in safe_str_set

        # String primitive lookup (should be converted)
        assert 'hello' in safe_str_set
        assert 'world' in safe_str_set
        assert 'foo'   not in safe_str_set

    def test__contains__with_safe_int(self):
        # Test with Safe_Int type
        safe_int_set = Type_Safe__Set(Safe_Int)
        safe_int_set.add(Safe_Int(42))
        safe_int_set.add(Safe_Int(100))

        # Direct Safe_Int instance lookup
        assert Safe_Int(42)  in safe_int_set
        assert Safe_Int(100) in safe_int_set
        assert Safe_Int(999) not in safe_int_set

        # Integer primitive lookup (should be converted)
        assert 42  in safe_int_set
        assert 100 in safe_int_set
        assert 999 not in safe_int_set

        # String that can be converted to int
        assert '42'  in safe_int_set
        assert '100' in safe_int_set
        assert '999' not in safe_int_set

    def test__contains__with_safe_id(self):
        # Test with a more complex Safe_Id type
        safe_id_set = Type_Safe__Set(Safe_Id)
        safe_id_set.add(Safe_Id('user-123'))
        safe_id_set.add(Safe_Id('admin-456'))

        # Direct Safe_Id instance lookup
        assert Safe_Id('user-123')  in safe_id_set
        assert Safe_Id('admin-456') in safe_id_set
        assert Safe_Id('guest-789') not in safe_id_set

        # String primitive lookup (should be converted)
        assert 'user-123'  in safe_id_set
        assert 'admin-456' in safe_id_set
        assert 'guest-789' not in safe_id_set

    def test__contains__with_regular_types(self):
        # Test that regular types still work normally
        string_set = Type_Safe__Set(str)
        string_set.add('hello')
        string_set.add('world')

        assert 'hello' in string_set
        assert 'world' in string_set
        assert 'foo'   not in string_set

        # These should not be found (no conversion for regular types)
        assert 123 not in string_set