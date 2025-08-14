from unittest                                                   import TestCase
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt__Byte import Safe_UInt__Byte


class test_Safe_Int__Byte(TestCase):
    def test__safe_int__byte_overflow(self):
        # Byte (0-255)
        byte = Safe_UInt__Byte(250)

        result = byte + 5
        assert type(result) is Safe_UInt__Byte
        assert result == 255

        # Should fall back when exceeding byte range
        result = byte + 10  # Would be 260
        assert type(result) is int
        assert result == 260


    def test__safe_int_byte__string_representation(self):
        # Byte value
        byte = Safe_UInt__Byte(255)
        assert str(byte) == "255"
        assert f"0x{byte:02X}" == "0xFF"  # Hex formatting
        assert repr(byte) == "Safe_UInt__Byte(255)"

        # Zero byte
        zero = Safe_UInt__Byte(0)
        assert str(zero) == "0"
        assert f"{zero:08b}" == "00000000"  # Binary formatting