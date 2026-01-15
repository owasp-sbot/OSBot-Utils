# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Report__Metadata - Metadata for performance reports
# Contains timestamp, version, title, description, and benchmark count
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                    import Timestamp_Now
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                     import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description    import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title          import Safe_Str__Benchmark__Title
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                import Safe_UInt



class Schema__Perf_Report__Metadata(Type_Safe):                     # Metadata for performance report
    timestamp      : Timestamp_Now                                  # When report was generated
    version        : Safe_Str__Benchmark__Title                     # Version of code being tested
    title          : Safe_Str__Benchmark__Title                     # Report title
    description    : Safe_Str__Benchmark__Description               # Report description
    test_input     : Safe_Str__Benchmark__Description               # Description of test input
    measure_mode   : Enum__Measure_Mode                             # QUICK, FAST, or DEFAULT
    benchmark_count: Safe_UInt                                      # Number of benchmarks in report
