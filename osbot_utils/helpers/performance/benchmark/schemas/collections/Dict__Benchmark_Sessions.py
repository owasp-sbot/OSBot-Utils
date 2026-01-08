# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Benchmark_Sessions - Type-safe collection of benchmark sessions
# Maps benchmark IDs to their sessions
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.Performance_Measure__Session                       import Performance_Measure__Session
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id  import Safe_Str__Benchmark_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                   import Type_Safe__Dict


class Dict__Benchmark_Sessions(Type_Safe__Dict):                                  # {benchmark_id → result}
    expected_key_type   = Safe_Str__Benchmark_Id
    expected_value_type = Performance_Measure__Session
