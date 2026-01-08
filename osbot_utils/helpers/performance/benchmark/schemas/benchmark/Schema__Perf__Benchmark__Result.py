# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Benchmark__Result - Single benchmark measurement result
# Pure data schema capturing timing and metadata for one benchmark
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Index                import Safe_Str__Benchmark__Index


class Schema__Perf__Benchmark__Result(Type_Safe):                                # Single benchmark result
    benchmark_id : Safe_Str__Benchmark_Id                                        # Full ID: "A_01__python__nop"
    section      : Safe_Str__Benchmark__Section                                  # Extracted: "A"
    index        : Safe_Str__Benchmark__Index                                    # Extracted: "01"
    name         : Safe_Str                                                      # Extracted: "python__nop"
    final_score  : Safe_UInt                                                     # Normalized score in ns
    raw_score    : Safe_UInt                                                     # Raw score in ns
