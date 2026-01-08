# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Benchmark__Evolution - Single benchmark across multiple sessions
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend                       import Enum__Benchmark__Trend
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Scores                           import List__Scores
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Change          import Safe_Float__Percentage_Change


class Schema__Perf__Benchmark__Evolution(Type_Safe):                             # One benchmark over time
    benchmark_id   : Safe_Str__Benchmark_Id                                      # Full ID
    name           : Safe_Str__Benchmark__Title                                  # Display name
    scores         : List__Scores                                                # Score per session
    first_score    : Safe_UInt                                                   # First session score
    last_score     : Safe_UInt                                                   # Last session score
    change_percent : Safe_Float__Percentage_Change                               # Overall change
    trend          : Enum__Benchmark__Trend                                      # Trend indicator
