from unittest                                           import TestCase
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize   import Safe_UInt__FileSize


class test_Safe_UInt__FileSize(TestCase):
    def test__safe_int_file_size__string_representation(self):
        # File size
        size = Safe_UInt__FileSize(1024)
        assert str(size) == "1024"
        assert f"{size} bytes" == "1024 bytes"
        assert repr(size) == "Safe_UInt__FileSize(1024)"

        # Large file size
        large = Safe_UInt__FileSize(1048576)  # 1MB
        assert str(large) == "1048576"
        assert f"Size: {large/1024/1024:.1f}MB" == "Size: 1.0MB"