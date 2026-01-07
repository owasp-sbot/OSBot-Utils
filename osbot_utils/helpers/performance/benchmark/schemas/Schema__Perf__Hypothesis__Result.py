# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Hypothesis__Result - Hypothesis evaluation outcome
# Captures before/after comparison and success/failure status
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Hypothesis__Status                     import Enum__Hypothesis__Status
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                          import Timestamp_Now


class Schema__Perf__Hypothesis__Result(Type_Safe):                               # Hypothesis outcome
    description        : Safe_Str__Benchmark__Description                        # What we're testing
    target_improvement : Safe_Float                                              # e.g., 0.5 for 50%
    actual_improvement : Safe_Float                                              # Calculated from results
    before_results     : Dict__Benchmark_Results                                 # Baseline measurements
    after_results      : Dict__Benchmark_Results                                 # Optimized measurements
    status             : Enum__Hypothesis__Status                                # SUCCESS, FAILURE, etc.
    timestamp          : Timestamp_Now                                           # When evaluated
    comments           : Safe_Str__Benchmark__Description                        # Optional notes
