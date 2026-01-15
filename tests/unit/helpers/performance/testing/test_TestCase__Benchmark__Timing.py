# ═══════════════════════════════════════════════════════════════════════════════
# test_TestCase__Benchmark__Timing - Tests for benchmark TestCase base class
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.helpers.performance.benchmark.testing.TestCase__Benchmark__Timing                        import TestCase__Benchmark__Timing

class test_TestCase__Benchmark__Timing(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test_class_attributes(self):                                             # Test class attributes
        assert hasattr(TestCase__Benchmark__Timing, 'config')
        assert hasattr(TestCase__Benchmark__Timing, 'timing')

    def test_threshold_constants(self):                                          # Test threshold constants
        assert TestCase__Benchmark__Timing.time_100_ns  == 100
        assert TestCase__Benchmark__Timing.time_500_ns  == 500
        assert TestCase__Benchmark__Timing.time_1_kns   == 1_000
        assert TestCase__Benchmark__Timing.time_2_kns   == 2_000
        assert TestCase__Benchmark__Timing.time_5_kns   == 5_000
        assert TestCase__Benchmark__Timing.time_10_kns  == 10_000
        assert TestCase__Benchmark__Timing.time_20_kns  == 20_000
        assert TestCase__Benchmark__Timing.time_50_kns  == 50_000
        assert TestCase__Benchmark__Timing.time_100_kns == 100_000

    def test_inheritance(self):                                                  # Test inheritance
        assert issubclass(TestCase__Benchmark__Timing, TestCase)