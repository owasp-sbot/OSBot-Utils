# ═══════════════════════════════════════════════════════════════════════════════
# List__Benchmark_Comparisons - List of benchmark comparison results
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison import Schema__Perf__Benchmark__Comparison
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                                import Type_Safe__List


class List__Benchmark_Comparisons(Type_Safe__List):                              # [comparison, ...]
    expected_type = Schema__Perf__Benchmark__Comparison
