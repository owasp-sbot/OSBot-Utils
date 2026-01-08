# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Export - Base class for benchmark export formats
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two import Schema__Perf__Comparison__Two
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                 import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                import Schema__Perf__Statistics


class Perf_Benchmark__Export(Type_Safe):                                         # Base exporter


    def export_comparison(self, result: Schema__Perf__Comparison__Two) -> str:   # Export two-session comparison
        raise NotImplementedError()

    def export_evolution(self, result: Schema__Perf__Evolution) -> str:          # Export multi-session evolution
        raise NotImplementedError()

    def export_statistics(self, result: Schema__Perf__Statistics) -> str:        # Export statistics
        raise NotImplementedError()
