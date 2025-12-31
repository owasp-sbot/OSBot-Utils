from unittest                                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.python.safe_str.Safe_Str__Python__Function       import Safe_Str__Python__Function

class test_Safe_Str__Python__Function(TestCase):                                     # Test Python function name

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Python__Function('calculate_total') as _:
            assert str(_) == 'calculate_total'

    def test__allows_underscores(self):                                              # Test underscores
        with Safe_Str__Python__Function('helper_function_v2') as _:
            assert str(_) == 'helper_function_v2'
