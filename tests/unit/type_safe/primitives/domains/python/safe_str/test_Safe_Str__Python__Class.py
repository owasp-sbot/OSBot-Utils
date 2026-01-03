from unittest                                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.python.safe_str.Safe_Str__Python__Class          import Safe_Str__Python__Class

class test_Safe_Str__Python__Class(TestCase):                                        # Test Python class name

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Python__Class('MyClass') as _:
            assert str(_) == 'MyClass'

    def test__allows_pascal_case(self):                                              # Test PascalCase
        with Safe_Str__Python__Class('CallFlowAnalyzer') as _:
            assert str(_) == 'CallFlowAnalyzer'

    def test__allows_underscores(self):                                              # Test underscore naming
        with Safe_Str__Python__Class('Schema__Call_Graph') as _:
            assert str(_) == 'Schema__Call_Graph'

    def test__allows_numbers(self):                                                  # Test numbers in name
        with Safe_Str__Python__Class('Version2Handler') as _:
            assert str(_) == 'Version2Handler'

    def test__sanitizes_special_chars(self):                                         # Test special chars removed
        with Safe_Str__Python__Class('My-Class!') as _:
            assert str(_) == 'My_Class_'                                             # Dashes and special chars fixed

