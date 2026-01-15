# ═══════════════════════════════════════════════════════════════════════════════
# List__Perf_Report__Benchmarks - Typed list of benchmark results
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report__Benchmark import Schema__Perf_Report__Benchmark
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List              import Type_Safe__List


class List__Perf_Report__Benchmarks(Type_Safe__List):               # Collection of benchmark results
    expected_type = Schema__Perf_Report__Benchmark
