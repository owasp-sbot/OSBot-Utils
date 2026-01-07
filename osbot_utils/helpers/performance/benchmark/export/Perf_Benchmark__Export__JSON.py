# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Export__JSON - JSON export format
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two import Schema__Perf__Comparison__Two
from osbot_utils.utils.Json                                                                    import json_dumps
from osbot_utils.helpers.performance.benchmark.export.Perf_Benchmark__Export                   import Perf_Benchmark__Export
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                 import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                import Schema__Perf__Statistics


class Perf_Benchmark__Export__JSON(Perf_Benchmark__Export):                      # JSON exporter


    # ═══════════════════════════════════════════════════════════════════════════════
    # Export Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_comparison(self, result: Schema__Perf__Comparison__Two) -> str:   # Export comparison
        return json_dumps(result.json(), indent=2)

    def export_evolution(self, result: Schema__Perf__Evolution) -> str:          # Export evolution
        return json_dumps(result.json(), indent=2)

    def export_statistics(self, result: Schema__Perf__Statistics) -> str:        # Export statistics
        return json_dumps(result.json(), indent=2)
