# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Perf_Benchmark__Hypothesis__Config - Configuration for hypothesis testing
# Controls reporting, measurement mode, and timing settings
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Measure_Mode                      import Enum__Measure_Mode
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe


class Schema__Perf__Benchmark__Hypothesis__Config(Type_Safe):                     # Hypothesis configuration
    use_raw_scores   : bool                                  = True              # Use raw_score vs final_score in reports
    measure_mode     : Enum__Measure_Mode                    = Enum__Measure_Mode.QUICK  # Measurement accuracy
    timing_config    : Schema__Perf_Benchmark__Timing__Config                    # Base timing config (optional, created if None)