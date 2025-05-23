import pytest
from unittest                                         import TestCase
from osbot_utils.helpers.safe_int.Safe_Int__UInt      import Safe_Int__UInt
from osbot_utils.type_safe.Type_Safe                  import Type_Safe


class test_Safe_Int__UInt(TestCase):

    def test_Safe_Int__UInt_class(self):
        # Valid unsigned integers
        assert int(Safe_Int__UInt(0))       == 0
        assert int(Safe_Int__UInt(1))       == 1
        assert int(Safe_Int__UInt(123))     == 123
        assert int(Safe_Int__UInt(999999))  == 999999
        assert int(Safe_Int__UInt(2**32-1)) == 4294967295  # Max 32-bit unsigned

        # String conversion
        assert int(Safe_Int__UInt('0'))      == 0
        assert int(Safe_Int__UInt('123'))    == 123
        assert int(Safe_Int__UInt('999999')) == 999999

        assert Safe_Int__UInt(None) == 0
        assert Safe_Int__UInt(    ) == 0
        assert Safe_Int__UInt(0   ) == 0
        # Negative values not allowed
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -1"):
            Safe_Int__UInt(-1)
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -100"):
            Safe_Int__UInt(-100)
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -999999"):
            Safe_Int__UInt(-999999)

        # Negative string values
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -1"):
            Safe_Int__UInt('-1')
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -100"):
            Safe_Int__UInt('-100')

        # Boolean not allowed
        with pytest.raises(TypeError, match="Safe_Int__UInt does not allow boolean values"):
            Safe_Int__UInt(True)
        with pytest.raises(TypeError, match="Safe_Int__UInt does not allow boolean values"):
            Safe_Int__UInt(False)

        # Invalid types
        with pytest.raises(TypeError, match="Safe_Int__UInt requires an integer value, got float"):
            Safe_Int__UInt(3.14)
        with pytest.raises(ValueError, match="Cannot convert 'abc' to integer"):
            Safe_Int__UInt('abc')


    def test_arithmetic_operations(self):
        a = Safe_Int__UInt(10)
        b = Safe_Int__UInt(5)

        # Addition maintains type
        result = a + b
        assert type(result) is Safe_Int__UInt
        assert int(result) == 15

        # Subtraction that results in negative returns plain int
        result = b - a
        assert type(result) is int  # Not Safe_Int__UInt because it's negative
        assert result == -5

        # Subtraction that stays positive maintains type
        result = a - b
        assert type(result) is Safe_Int__UInt
        assert int(result) == 5

        # Multiplication maintains type
        result = a * b
        assert type(result) is Safe_Int__UInt
        assert int(result) == 50

    def test_usage_in_Type_Safe(self):
        class File_Info(Type_Safe):
            size       : Safe_Int__UInt
            block_size : Safe_Int__UInt = Safe_Int__UInt(4096)
            inode      : Safe_Int__UInt = Safe_Int__UInt(0)

        file_info = File_Info(size=Safe_Int__UInt(1024))
        assert int(file_info.size) == 1024
        assert int(file_info.block_size) == 4096
        assert int(file_info.inode) == 0

        # Update values
        file_info.size = Safe_Int__UInt(2048)
        assert int(file_info.size) == 2048

        # Cannot set negative
        with pytest.raises(ValueError, match="Safe_Int__UInt must be >= 0, got -100"):
            file_info.size = Safe_Int__UInt(-100)

        # Serialization round trip
        file_info_json = file_info.json()
        assert file_info_json == {
            'size': 2048,
            'block_size': 4096,
            'inode': 0
        }

        file_info_restored = File_Info.from_json(file_info_json)
        assert type(file_info_restored.size) is Safe_Int__UInt
        assert int(file_info_restored.size) == 2048

    def test_edge_cases(self):
        # Zero is valid
        assert int(Safe_Int__UInt(0)) == 0
        assert int(Safe_Int__UInt('0')) == 0

        # Large values
        assert int(Safe_Int__UInt(2**63-1)) == 9223372036854775807

        # Arithmetic at boundaries
        zero = Safe_Int__UInt(0)
        one = Safe_Int__UInt(1)

        # Subtraction at zero boundary
        result = zero - zero
        assert type(result) is Safe_Int__UInt
        assert int(result) == 0

        result = zero - one  # Goes negative
        assert type(result) is int  # Falls back to regular int
        assert result == -1