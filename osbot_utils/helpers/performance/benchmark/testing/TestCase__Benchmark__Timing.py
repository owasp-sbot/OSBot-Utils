# ═══════════════════════════════════════════════════════════════════════════════
# TestCase__Benchmark__Timing - TestCase subclass for benchmark test files
# Provides minimal boilerplate for writing performance benchmark tests
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                               import Callable, Optional
from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                     import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing__Reporter                           import Perf_Benchmark__Timing__Reporter
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id


class TestCase__Benchmark__Timing(TestCase):                                     # Base for benchmark tests
    config : Schema__Perf_Benchmark__Timing__Config = None                               # Override in subclass
    timing : Perf_Benchmark__Timing         = None                               # Set in setUpClass

    # Standard thresholds (nanoseconds) - for convenience
    time_100_ns  = 100
    time_500_ns  = 500
    time_1_kns   = 1_000
    time_2_kns   = 2_000
    time_5_kns   = 5_000
    time_10_kns  = 10_000
    time_20_kns  = 20_000
    time_50_kns  = 50_000
    time_100_kns = 100_000


    # ═══════════════════════════════════════════════════════════════════════════════
    # Test Lifecycle
    # ═══════════════════════════════════════════════════════════════════════════════

    @classmethod
    def setUpClass(cls) -> None:                                                 # Initialize timing
        if cls.config is None:
            cls.config = Schema__Perf_Benchmark__Timing__Config()
        cls.timing = Perf_Benchmark__Timing(config=cls.config)
        cls.timing.start()

    @classmethod
    def tearDownClass(cls) -> None:                                              # Finalize and report
        cls.timing.stop()
        if cls.config.print_to_console:
            cls.timing.reporter().print_summary()


    # ═══════════════════════════════════════════════════════════════════════════════
    # Benchmark Method
    # ═══════════════════════════════════════════════════════════════════════════════

    def benchmark(self                                          ,                # Run single benchmark
                  benchmark_id    : Safe_Str__Benchmark_Id      ,                # Benchmark identifier
                  target          : Callable                    ,                # Function to measure
                  assert_less_than: Optional[Safe_UInt] = None                   # Optional threshold
             ) -> Schema__Perf__Benchmark__Result:
        return self.timing.benchmark(benchmark_id, target, assert_less_than)


    # ═══════════════════════════════════════════════════════════════════════════════
    # Reporter Access
    # ═══════════════════════════════════════════════════════════════════════════════

    @classmethod
    def reporter(cls) -> Perf_Benchmark__Timing__Reporter:                       # Get reporter instance
        return cls.timing.reporter()
