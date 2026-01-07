# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf__Statistics - Performance statistics summary
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                               import Optional
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison      import Schema__Perf__Benchmark__Comparison
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                          import Timestamp_Now


class Schema__Perf__Statistics(Type_Safe):                                       # Statistics summary
    status            : Enum__Comparison__Status                                 # Operation status
    error             : Safe_Str__Benchmark__Description                         # Empty if success
    session_count     : Safe_UInt                                                # Number of sessions
    benchmark_count   : Safe_UInt                                                # Benchmarks tracked
    improvement_count : Safe_UInt                                                # Improved benchmarks
    regression_count  : Safe_UInt                                                # Regressed benchmarks
    avg_improvement   : Safe_Float                                               # Average improvement %
    avg_regression    : Safe_Float                                               # Average regression %
    best_improvement  : Optional[Schema__Perf__Benchmark__Comparison]            # Best performing
    worst_regression  : Optional[Schema__Perf__Benchmark__Comparison]            # Worst performing
    timestamp         : Timestamp_Now                                            # When calculated
