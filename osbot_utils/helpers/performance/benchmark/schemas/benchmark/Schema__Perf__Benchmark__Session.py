# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Benchmark__Session - Full benchmark session for serialization
# Captures all data from a benchmark run for persistence and comparison
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description  import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title        import Safe_Str__Benchmark__Title
from osbot_utils.type_safe.Type_Safe                                                              import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results        import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend        import Dict__Benchmark__Legend
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                  import Timestamp_Now


class Schema__Perf__Benchmark__Session(Type_Safe):                               # Full session data
    title       : Safe_Str__Benchmark__Title                                                   # Session title
    description : Safe_Str__Benchmark__Description                               # Optional description
    timestamp   : Timestamp_Now                                                  # When session was run
    results     : Dict__Benchmark_Results                                        # All benchmark results
    legend      : Dict__Benchmark__Legend                                        # Section descriptions
