# ═══════════════════════════════════════════════════════════════════════════════
# test_Safe_Str__Benchmark__Section - Tests for section identifier primitive
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section


class test_Safe_Str__Benchmark__Section(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Safe_Str__Benchmark__Section('A') as _:
            assert type(_)    is Safe_Str__Benchmark__Section
            assert str(_)     == 'A'
            assert isinstance(_, Safe_Str)

    def test__init____single_char(self):                                         # Test single character
        with Safe_Str__Benchmark__Section('B') as _:
            assert str(_) == 'B'

    def test__init____word(self):                                                # Test word section
        with Safe_Str__Benchmark__Section('Python') as _:
            assert str(_) == 'Python'

    def test__init____empty(self):                                               # Test empty string
        with Safe_Str__Benchmark__Section('') as _:
            assert str(_) == ''

    def test_max_length(self):                                                   # Test max_length attribute
        assert Safe_Str__Benchmark__Section.max_length == 50

    def test_inheritance(self):                                                  # Test inheritance chain
        with Safe_Str__Benchmark__Section('test') as _:
            assert isinstance(_, Safe_Str)
            assert isinstance(_, str)

    def test_comparison(self):                                                   # Test equality comparison
        sec_1 = Safe_Str__Benchmark__Section('A')
        sec_2 = Safe_Str__Benchmark__Section('A')
        sec_3 = Safe_Str__Benchmark__Section('B')

        assert sec_1 == sec_2
        assert sec_1 != sec_3
        assert sec_1 == 'A'                                                      # Compare with plain string

    def test_hash(self):                                                         # Test hashability for dict keys
        sec_1 = Safe_Str__Benchmark__Section('A')
        sec_2 = Safe_Str__Benchmark__Section('A')

        test_dict = {sec_1: 'Python Baselines'}
        assert test_dict[sec_2] == 'Python Baselines'
