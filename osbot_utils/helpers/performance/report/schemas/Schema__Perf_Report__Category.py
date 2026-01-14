# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Report__Category - Category summary with aggregated timing
# Contains category ID, name, description, total time, and benchmark count
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section     import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title       import Safe_Str__Benchmark__Title
from osbot_utils.type_safe.primitives.core.Safe_UInt                                             import Safe_UInt
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Change import Safe_Float__Percentage_Change


class Schema__Perf_Report__Category(Type_Safe):                     # Category summary
    category_id    : Safe_Str__Benchmark__Section                   # Category letter (e.g., A, B, C)
    name           : Safe_Str__Benchmark__Title                     # Display name from legend
    description    : Safe_Str__Benchmark__Description               # Description from legend
    total_ns       : Safe_UInt                                      # Sum of all benchmark times in category
    pct_of_total   : Safe_Float__Percentage_Change                  # Percentage of total report time
    benchmark_count: Safe_UInt                                      # Number of benchmarks in category
