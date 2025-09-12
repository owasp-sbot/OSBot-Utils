import pytest
from unittest                                                                      import TestCase
from osbot_utils.utils.Objects                                                     import __, base_types
from osbot_utils.type_safe.primitives.core.Safe_Str                                import Safe_Str
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                    import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash, SIZE__VALUE_HASH


class test_Safe_Str__Hash(TestCase):

    def test_basic_usage(self):
        # Valid hexadecimal strings of length 10
        assert str(Safe_Str__Hash('0123456789')) == '0123456789'
        assert str(Safe_Str__Hash('abcdef0123')) == 'abcdef0123'
        assert str(Safe_Str__Hash('ABCDEF9876')) == 'ABCDEF9876'
        assert str(Safe_Str__Hash('01AbCdEf89')) == '01AbCdEf89'

        # Trimming works
        assert str(Safe_Str__Hash(' 0123456789 ')) == '0123456789'

        # Converting non-string values, as long as they're valid
        assert str(Safe_Str__Hash(1234567890)) == '1234567890'

    def test_invalid_values(self):
        # Invalid character (not hexadecimal)
        with pytest.raises(ValueError, match="in Safe_Str__Hash, value contains invalid characters") as exc_info:
            Safe_Str__Hash('012345678g')  # 'g' is not hex

        with pytest.raises(ValueError, match="in Safe_Str__Hash, value contains invalid characters") as exc_info:
            Safe_Str__Hash('ABCDEFGHIJ')  # G-J are not hex

        with pytest.raises(ValueError, match="in Safe_Str__Hash, value contains invalid characters") as exc_info:
            Safe_Str__Hash('1234-56789')  # '-' is not hex

        # Wrong length
        with pytest.raises(ValueError, match=f"in Safe_Str__Hash, value must be exactly {SIZE__VALUE_HASH} characters long") as exc_info:
            Safe_Str__Hash('12345')  # Too short

        with pytest.raises(ValueError, match=f"in Safe_Str__Hash, value must be exactly {SIZE__VALUE_HASH} characters long") as exc_info:
            Safe_Str__Hash('12345678901')  # Too long

        # Empty or None
        #with pytest.raises(ValueError, match="in Safe_Str__Hash, value cannot be None when allow_empty is Fals") as exc_info:
        assert Safe_Str__Hash(None) == ''

        #with pytest.raises(ValueError, match=f"in Safe_Str__Hash, value cannot be empty when allow_empty is False"):
        assert Safe_Str__Hash('') == ''

        # Whitespace only
        #with pytest.raises(ValueError, match=f"in Safe_Str__Hash, value cannot be empty when allow_empty is False") as exc_info:
        assert Safe_Str__Hash('   ') == ''

    def test_inheritance(self):
        hash_str = Safe_Str__Hash('abcdef1234')
        assert isinstance(hash_str, Safe_Str__Hash)
        assert isinstance(hash_str, Safe_Str)
        assert isinstance(hash_str, str)
        assert base_types(hash_str) == [Safe_Str, Type_Safe__Primitive, str, object, object]

    def test_usage_in_Type_Safe(self):
        class Hash_Container(Type_Safe):
            hash_value: Safe_Str__Hash = Safe_Str__Hash('0123456789')

        # Test instantiation with default
        container = Hash_Container()
        assert str(container.hash_value) == '0123456789'
        assert type(container.hash_value) is Safe_Str__Hash

        # Test updating with valid value
        container.hash_value = Safe_Str__Hash('abcdef0123')
        assert str(container.hash_value) == 'abcdef0123'

        # Test serialization and deserialization
        container_json = container.json()
        assert container_json == {'hash_value': 'abcdef0123'}

        # Round trip test
        container_round_trip = Hash_Container.from_json(container_json)
        assert container_round_trip.obj() == container.obj()
        assert type(container_round_trip.hash_value) is Safe_Str__Hash

    def test_md5_hash_compatibility(self):
        # Test compatibility with MD5 hash truncation scenario
        # These would be the results of truncated MD5 hashes as mentioned in requirements
        assert str(Safe_Str__Hash('4f705147de')) == '4f705147de'
        assert str(Safe_Str__Hash('b27d7492c0')) == 'b27d7492c0'

    def test__safe_str_hash__string_representation(self):
        # Hash value
        hash_val = Safe_Str__Hash("a1b2c3d4e5")
        assert str(hash_val) == "a1b2c3d4e5"
        assert f"Hash: {hash_val}" == "Hash: a1b2c3d4e5"
        assert repr(hash_val) == "Safe_Str__Hash('a1b2c3d4e5')"