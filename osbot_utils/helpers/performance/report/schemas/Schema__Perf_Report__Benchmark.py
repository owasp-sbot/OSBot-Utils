# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Report__Benchmark - Single benchmark result
# Contains benchmark ID, timing in nanoseconds, category, and percentage
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id           import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section     import Safe_Str__Benchmark__Section
from osbot_utils.type_safe.primitives.core.Safe_UInt                                             import Safe_UInt
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Change import Safe_Float__Percentage_Change


class Schema__Perf_Report__Benchmark(Type_Safe):                    # Single benchmark result
    benchmark_id : Safe_Str__Benchmark_Id                           # Benchmark identifier (e.g., A_01__name)
    time_ns      : Safe_UInt                                        # Execution time in nanoseconds
    category_id  : Safe_Str__Benchmark__Section                     # Category letter (e.g., A, B, C)
    pct_of_total : Safe_Float__Percentage_Change                    # Percentage of total time
