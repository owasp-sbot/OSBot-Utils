from unittest                                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.python.safe_str.Safe_Str__Python__Package        import Safe_Str__Python__Package

class test_Safe_Str__Python__Package(TestCase):                                      # Test Python package name

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Python__Package('osbot_utils') as _:
            assert str(_) == 'osbot_utils'

    def test__lowercase_convention(self):                                            # Test lowercase enforced
        with Safe_Str__Python__Package('MyPackage') as _:
            assert str(_) == '_y_ackage'                                             # Uppercase fixed

    def test__allows_numbers(self):                                                  # Test numbers allowed
        with Safe_Str__Python__Package('package2') as _:
            assert str(_) == 'package2'

