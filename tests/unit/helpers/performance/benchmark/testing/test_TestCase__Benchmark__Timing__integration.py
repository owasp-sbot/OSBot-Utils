from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.testing.TestCase__Benchmark__Timing                        import TestCase__Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                     import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing__Reporter                           import Perf_Benchmark__Timing__Reporter
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id


class test_TestCase__Benchmark__Timing__integration(TestCase__Benchmark__Timing):               # Integration test using actual TestCase__Benchmark__Timing

    config = Schema__Perf_Benchmark__Timing__Config(title            = 'TestCase Integration',
                                                    print_to_console = False)

    def test_setUpClass_creates_timing(self):                                    # Test timing created
        assert self.timing is not None
        assert type(self.timing) is Perf_Benchmark__Timing

    def test_config_is_set(self):                                                # Test config set
        assert self.config is not None
        assert str(self.config.title) == 'TestCase Integration'

    def test_benchmark_method(self):                                             # Test benchmark method
        result = self.benchmark(Safe_Str__Benchmark_Id('A_01__test'),
                                lambda: None                          )

        assert type(result)            is Schema__Perf__Benchmark__Result
        assert str(result.benchmark_id) == 'A_01__test'
        assert int(result.final_score) >= 0

    def test_benchmark_multiple(self):                                           # Test multiple benchmarks
        self.benchmark(Safe_Str__Benchmark_Id('B_01__test1'), lambda: None)
        self.benchmark(Safe_Str__Benchmark_Id('B_02__test2'), lambda: 1 + 1)

        assert len(self.timing.results) >= 2

    def test_reporter_method(self):                                              # Test reporter method
        self.benchmark(Safe_Str__Benchmark_Id('C_01__test'), lambda: None)

        reporter = self.reporter()

        assert type(reporter) is Perf_Benchmark__Timing__Reporter
        assert len(reporter.results) >= 1

    def test_thresholds_accessible(self):                                        # Test thresholds accessible
        assert self.time_100_ns  == 100
        assert self.time_1_kns   == 1_000
        assert self.time_10_kns  == 10_000

    def test_benchmark_with_threshold(self):                                     # Test with threshold
        result = self.benchmark(Safe_Str__Benchmark_Id('D_01__test')            ,
                                lambda: None                                    ,
                                assert_less_than = self.time_100_kns            )  # 100µs threshold

        assert result is not None