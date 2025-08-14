from unittest                                                                  import TestCase
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path import Safe_Str__File__Path


class test_Safe_Str__File__Path(TestCase):

    def test__safe_str_file_path__string_representation(self):      # Valid path
        path = Safe_Str__File__Path("/home/user/documents")
        assert str(path)        == "/home/user/documents"
        assert f"Path: {path}"  == "Path: /home/user/documents"
        assert repr(path)       == "Safe_Str__File__Path('/home/user/documents')"

        # Path with traversal attempt (should not be sanitized here, since this is a valid path)        # todo: add to the documentation of this class, this 'by design' behaviour
        path_sanitized = Safe_Str__File__Path("/home/../etc/passwd")
        assert "../" in str(path_sanitized)  # Traversal removed