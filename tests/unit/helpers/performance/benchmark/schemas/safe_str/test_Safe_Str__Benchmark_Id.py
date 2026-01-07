# ═══════════════════════════════════════════════════════════════════════════════
# test_Safe_Str__Benchmark_Id - Tests for benchmark ID primitive
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id


class test_Safe_Str__Benchmark_Id(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__Benchmark_Id('A_01__python__nop') as _:
            assert type(_)    is Safe_Str__Benchmark_Id
            assert str(_)     == 'A_01__python__nop'
            assert isinstance(_, Safe_Str)

    def test__init____empty(self):                                               # Test empty string
        with Safe_Str__Benchmark_Id('') as _:
            assert str(_) == ''

    def test__init____complex_id(self):                                          # Test complex benchmark ID
        with Safe_Str__Benchmark_Id('B_02__type_safe__with_primitives') as _:
            assert str(_) == 'B_02__type_safe__with_primitives'

    def test_max_length(self):                                                   # Test max_length attribute
        assert Safe_Str__Benchmark_Id.max_length == 100

    def test_inheritance(self):                                                  # Test inheritance chain
        with Safe_Str__Benchmark_Id('test') as _:
            assert isinstance(_, Safe_Str)
            assert isinstance(_, str)

    def test_comparison(self):                                                   # Test equality comparison
        id_1 = Safe_Str__Benchmark_Id('A_01__test')
        id_2 = Safe_Str__Benchmark_Id('A_01__test')
        id_3 = Safe_Str__Benchmark_Id('B_01__test')

        assert id_1 == id_2
        assert id_1 != id_3
        assert id_1 == 'A_01__test'                                              # Compare with plain string

    def test_hash(self):                                                         # Test hashability for dict keys
        id_1 = Safe_Str__Benchmark_Id('A_01__test')
        id_2 = Safe_Str__Benchmark_Id('A_01__test')

        test_dict = {id_1: 'value'}
        assert test_dict[id_2] == 'value'                                        # Same hash for equal values
