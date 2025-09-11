import pytest
from unittest                                             import TestCase
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt import Safe_UInt


class test_Safe_UInt(TestCase):

    def test_Safe_UInt_class(self):
        # Valid unsigned integers
        assert int(Safe_UInt(0)) == 0
        assert int(Safe_UInt(1)) == 1
        assert int(Safe_UInt(123)) == 123
        assert int(Safe_UInt(999999)) == 999999
        assert int(Safe_UInt(2 ** 32 - 1)) == 4294967295  # Max 32-bit unsigned

        # String conversion
        assert int(Safe_UInt('0')) == 0
        assert int(Safe_UInt('123')) == 123
        assert int(Safe_UInt('999999')) == 999999

        assert Safe_UInt(None) == 0
        assert Safe_UInt() == 0
        assert Safe_UInt(0) == 0
        # Negative values not allowed
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -1"):
            Safe_UInt(-1)
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -100"):
            Safe_UInt(-100)
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -999999"):
            Safe_UInt(-999999)

        # Negative string values
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -1"):
            Safe_UInt('-1')
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -100"):
            Safe_UInt('-100')

        # Boolean not allowed
        with pytest.raises(TypeError, match="Safe_UInt does not allow boolean values"):
            Safe_UInt(True)
        with pytest.raises(TypeError, match="Safe_UInt does not allow boolean values"):
            Safe_UInt(False)

        # Invalid types
        with pytest.raises(TypeError, match="Safe_UInt requires an integer value, got float"):
            Safe_UInt(3.14)
        with pytest.raises(ValueError, match="Cannot convert 'abc' to integer"):
            Safe_UInt('abc')


    def test_arithmetic_operations(self):
        a = Safe_UInt(10)
        b = Safe_UInt(5)

        # Addition maintains type
        result = a + b
        assert type(result) is Safe_UInt
        assert int(result) == 15

        # Subtraction that results in negative keeps type safety
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -5"):
            result = b - a

        # Subtraction that stays positive maintains type
        result = a - b
        assert type(result) is Safe_UInt
        assert int(result) == 5

        # Multiplication maintains type
        result = a * b
        assert type(result) is Safe_UInt
        assert int(result) == 50

    def test_usage_in_Type_Safe(self):
        class File_Info(Type_Safe):
            size       : Safe_UInt
            block_size : Safe_UInt = Safe_UInt(4096)
            inode      : Safe_UInt = Safe_UInt(0)

        file_info = File_Info(size=Safe_UInt(1024))
        assert int(file_info.size) == 1024
        assert int(file_info.block_size) == 4096
        assert int(file_info.inode) == 0

        # Update values
        file_info.size = Safe_UInt(2048)
        assert int(file_info.size) == 2048

        # Cannot set negative
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -100"):
            file_info.size = Safe_UInt(-100)

        # Serialization round trip
        file_info_json = file_info.json()
        assert file_info_json == {
            'size': 2048,
            'block_size': 4096,
            'inode': 0
        }

        file_info_restored = File_Info.from_json(file_info_json)
        assert type(file_info_restored.size) is Safe_UInt
        assert int(file_info_restored.size) == 2048

    def test_edge_cases(self):
        # Zero is valid
        assert int(Safe_UInt(0)) == 0
        assert int(Safe_UInt('0')) == 0

        # Large values
        assert int(Safe_UInt(2 ** 63 - 1)) == 9223372036854775807

        # Arithmetic at boundaries
        zero = Safe_UInt(0)
        one = Safe_UInt(1)

        # Subtraction at zero boundary
        result = zero - zero
        assert type(result) is Safe_UInt
        assert int(result) == 0
        with pytest.raises(ValueError, match="Safe_UInt must be >= 0, got -1"):
            result = zero - one  # Goes negative