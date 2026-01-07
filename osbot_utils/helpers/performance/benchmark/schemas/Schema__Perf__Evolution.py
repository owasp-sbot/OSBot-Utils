# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Evolution - Multi-session evolution result
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Titles                           import List__Titles
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Evolutions             import List__Benchmark_Evolutions
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                          import Timestamp_Now


class Schema__Perf__Evolution(Type_Safe):                                        # compare_all result
    status        : Enum__Comparison__Status                                     # Operation status
    error         : Safe_Str__Benchmark__Description                             # Empty if success
    session_count : Safe_UInt                                                    # Number of sessions
    titles        : List__Titles                                                 # Session titles in order
    evolutions    : List__Benchmark_Evolutions                                   # Per-benchmark evolution
    timestamp     : Timestamp_Now                                                # When compared
