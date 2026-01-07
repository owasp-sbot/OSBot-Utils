# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Export - Tests for base exporter class
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two            import Schema__Perf__Comparison__Two
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                              import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                            import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                           import Schema__Perf__Statistics


class test_Perf_Benchmark__Export(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Perf_Benchmark__Export() as _:
            assert type(_)         is Perf_Benchmark__Export
            assert isinstance(_, Type_Safe)

    def test_export_comparison__not_implemented(self):                           # Test abstract method
        with Perf_Benchmark__Export() as _:
            with self.assertRaises(NotImplementedError):
                _.export_comparison(Schema__Perf__Comparison__Two())

    def test_export_evolution__not_implemented(self):                            # Test abstract method
        with Perf_Benchmark__Export() as _:
            with self.assertRaises(NotImplementedError):
                _.export_evolution(Schema__Perf__Evolution())

    def test_export_statistics__not_implemented(self):                           # Test abstract method
        with Perf_Benchmark__Export() as _:
            with self.assertRaises(NotImplementedError):
                _.export_statistics(Schema__Perf__Statistics())

    def test_inheritance(self):                                                  # Test Type_Safe inheritance
        assert issubclass(Perf_Benchmark__Export, Type_Safe)
