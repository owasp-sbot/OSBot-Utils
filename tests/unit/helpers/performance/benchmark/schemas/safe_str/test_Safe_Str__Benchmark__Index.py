# ═══════════════════════════════════════════════════════════════════════════════
# test_Safe_Str__Benchmark__Index - Tests for index identifier primitive
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Index                import Safe_Str__Benchmark__Index


class test_Safe_Str__Benchmark__Index(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__Benchmark__Index('01') as _:
            assert type(_)    is Safe_Str__Benchmark__Index
            assert str(_)     == '01'
            assert isinstance(_, Safe_Str)

    def test__init____single_digit(self):                                        # Test single digit
        with Safe_Str__Benchmark__Index('1') as _:
            assert str(_) == '1'

    def test__init____two_digits(self):                                          # Test two digit index
        with Safe_Str__Benchmark__Index('02') as _:
            assert str(_) == '02'

    def test__init____three_digits(self):                                        # Test three digit index
        with Safe_Str__Benchmark__Index('123') as _:
            assert str(_) == '123'

    def test__init____empty(self):                                               # Test empty string
        with Safe_Str__Benchmark__Index('') as _:
            assert str(_) == ''

    def test_max_length(self):                                                   # Test max_length attribute
        assert Safe_Str__Benchmark__Index.max_length == 10

    def test_inheritance(self):                                                  # Test inheritance chain
        with Safe_Str__Benchmark__Index('01') as _:
            assert isinstance(_, Safe_Str)
            assert isinstance(_, str)

    def test_comparison(self):                                                   # Test equality comparison
        idx_1 = Safe_Str__Benchmark__Index('01')
        idx_2 = Safe_Str__Benchmark__Index('01')
        idx_3 = Safe_Str__Benchmark__Index('02')

        assert idx_1 == idx_2
        assert idx_1 != idx_3
        assert idx_1 == '01'                                                     # Compare with plain string

    def test_hash(self):                                                         # Test hashability
        idx_1 = Safe_Str__Benchmark__Index('01')
        idx_2 = Safe_Str__Benchmark__Index('01')

        test_dict = {idx_1: 'first'}
        assert test_dict[idx_2] == 'first'
