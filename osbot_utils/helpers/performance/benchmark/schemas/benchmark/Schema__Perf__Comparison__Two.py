# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Comparison__Two - Two-session comparison result
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Comparisons            import List__Benchmark_Comparisons
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                          import Timestamp_Now


class Schema__Perf__Comparison__Two(Type_Safe):                                  # compare_two result
    status      : Enum__Comparison__Status                                       # Operation status
    error       : Safe_Str__Benchmark__Description                               # Empty if success
    title_a     : Safe_Str__Benchmark__Title                                     # First session title
    title_b     : Safe_Str__Benchmark__Title                                     # Second session title
    comparisons : List__Benchmark_Comparisons                                    # Per-benchmark diffs
    timestamp   : Timestamp_Now                                                  # When compared
