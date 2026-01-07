# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Timing - Core benchmark timing infrastructure
# Wraps Performance_Measure__Session with result capture and reporting
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                               import Callable, Optional, Tuple
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.Performance_Measure__Session                                         import Performance_Measure__Session as Perf
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing__Reporter                           import Perf_Benchmark__Timing__Reporter
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Sessions               import Dict__Benchmark_Sessions
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Index                import Safe_Str__Benchmark__Index

# Standard thresholds (nanoseconds)
time_100_ns  : Safe_UInt = 100
time_500_ns  : Safe_UInt = 500
time_1_kns   : Safe_UInt = 1_000
time_2_kns   : Safe_UInt = 2_000
time_5_kns   : Safe_UInt = 5_000
time_10_kns  : Safe_UInt = 10_000
time_20_kns  : Safe_UInt = 20_000
time_50_kns  : Safe_UInt = 50_000
time_100_kns : Safe_UInt = 100_000

class Perf_Benchmark__Timing(Type_Safe):                                         # Core benchmark class
    config   : Schema__Perf_Benchmark__Timing__Config                                    # Configuration
    results  : Dict__Benchmark_Results                                           # Lightweight summaries
    sessions : Dict__Benchmark_Sessions                                          # Full measurement data


    # ═══════════════════════════════════════════════════════════════════════════════
    # Lifecycle Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def start(self) -> 'Perf_Benchmark__Timing':                                 # Initialize
        self.results  = Dict__Benchmark_Results ()
        self.sessions = Dict__Benchmark_Sessions()
        return self

    def stop(self) -> 'Perf_Benchmark__Timing':                                  # Finalize
        if self.config.auto_save_on_completion and self.config.output_path:
            self.reporter().save_all()
        return self


    # ═══════════════════════════════════════════════════════════════════════════════
    # Context Manager
    # ═══════════════════════════════════════════════════════════════════════════════

    def __enter__(self) -> 'Perf_Benchmark__Timing':                             # Context enter
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:                       # Context exit
        self.stop()
        return False


    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Benchmark Method
    # ═══════════════════════════════════════════════════════════════════════════════

    def benchmark(self                                          ,                # Run single benchmark
                  benchmark_id    : Safe_Str__Benchmark_Id      ,                # Benchmark identifier
                  target          : Callable                    ,                # Function to measure
                  assert_less_than: Optional[Safe_UInt] = None                   # Optional threshold
             ) -> Schema__Perf__Benchmark__Result:

        session = Perf(assert_enabled=True)                                      # Fresh session per benchmark
        session.measure__quick(target)
        perf_result = session.result

        section, index, name = self.parse_benchmark_id(benchmark_id)

        result = Schema__Perf__Benchmark__Result(benchmark_id = benchmark_id                               ,
                                                 section      = section                                    ,
                                                 index        = index                                      ,
                                                 name         = name                                       ,
                                                 final_score  = Safe_UInt(int(perf_result.final_score))    ,
                                                 raw_score    = Safe_UInt(int(perf_result.raw_score  ))    )

        self.results[benchmark_id]  = result                                     # Store summary
        self.sessions[benchmark_id] = session                                    # Store full session

        if assert_less_than is not None:
            session.assert_time__less_than(int(assert_less_than))

        return result


    # ═══════════════════════════════════════════════════════════════════════════════
    # Reporter Access
    # ═══════════════════════════════════════════════════════════════════════════════

    def reporter(self) -> Perf_Benchmark__Timing__Reporter:                      # Create reporter
        return Perf_Benchmark__Timing__Reporter(results = self.results,
                                                config  = self.config )


    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def parse_benchmark_id(self                                 ,                # Parse ID components
                           benchmark_id: Safe_Str__Benchmark_Id
                      ) -> Tuple[Safe_Str__Benchmark__Section   ,
                                 Safe_Str__Benchmark__Index     ,
                                 Safe_Str                       ]:

        id_str = str(benchmark_id)
        parts  = id_str.split('_', 2)

        if len(parts) >= 3:
            section = Safe_Str__Benchmark__Section(parts[0])
            index   = Safe_Str__Benchmark__Index(parts[1])
            name    = Safe_Str(parts[2].lstrip('_'))
            return (section, index, name)

        return (Safe_Str__Benchmark__Section('')  ,
                Safe_Str__Benchmark__Index('')    ,
                Safe_Str(id_str)                  )