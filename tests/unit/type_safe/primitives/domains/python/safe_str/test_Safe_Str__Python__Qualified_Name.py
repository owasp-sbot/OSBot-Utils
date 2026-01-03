from unittest                                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.python.safe_str.Safe_Str__Python__Qualified_Name import Safe_Str__Python__Qualified_Name

class test_Safe_Str__Python__Qualified_Name(TestCase):                               # Test qualified name

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Python__Qualified_Name('module.Class.method') as _:
            assert str(_) == 'module.Class.method'

    def test__allows_dots(self):                                                     # Test dots allowed
        with Safe_Str__Python__Qualified_Name('osbot_utils.helpers.semantic_graphs') as _:
            assert str(_) == 'osbot_utils.helpers.semantic_graphs'

    def test__full_path(self):                                                       # Test full qualified path
        with Safe_Str__Python__Qualified_Name('package.subpackage.Module.Class.method') as _:
            assert str(_) == 'package.subpackage.Module.Class.method'

    def test__sanitizes_special_chars(self):                                         # Test special chars removed
        with Safe_Str__Python__Qualified_Name('module/Class') as _:
            assert str(_) == 'module_Class'                                           # Slash fixed