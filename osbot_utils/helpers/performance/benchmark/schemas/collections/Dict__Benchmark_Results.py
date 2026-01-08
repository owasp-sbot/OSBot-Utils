# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Benchmark_Results - Type-safe collection of benchmark results
# Maps benchmark IDs to their result schemas
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id            import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result  import Schema__Perf__Benchmark__Result
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                             import Type_Safe__Dict


class Dict__Benchmark_Results(Type_Safe__Dict):                                  # {benchmark_id → result}
    expected_key_type   = Safe_Str__Benchmark_Id
    expected_value_type = Schema__Perf__Benchmark__Result
