from unittest                                                                                  import TestCase
from osbot_utils.type_safe.primitives.domains.python.safe_str.Safe_Str__Python__Method         import Safe_Str__Python__Method

class test_Safe_Str__Python__Method(TestCase):                                       # Test Python method name

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Python__Method('process_data') as _:
            assert str(_) == 'process_data'

    def test__allows_dunder(self):                                                   # Test dunder methods
        with Safe_Str__Python__Method('__init__') as _:
            assert str(_) == '__init__'

        with Safe_Str__Python__Method('__str__') as _:
            assert str(_) == '__str__'

    def test__allows_private(self):                                                  # Test private methods
        with Safe_Str__Python__Method('_private_helper') as _:
            assert str(_) == '_private_helper'

    def test__comparison(self):                                                      # Test string comparison
        method = Safe_Str__Python__Method('my_method')
        assert method == 'my_method'