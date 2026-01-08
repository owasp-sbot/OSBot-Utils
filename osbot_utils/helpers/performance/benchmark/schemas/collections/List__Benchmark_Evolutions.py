# ═══════════════════════════════════════════════════════════════════════════════
# List__Benchmark_Evolutions - List of benchmark evolution records
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Evolution import Schema__Perf__Benchmark__Evolution
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                               import Type_Safe__List

class List__Benchmark_Evolutions(Type_Safe__List):                               # [evolution, ...]
    expected_type = Schema__Perf__Benchmark__Evolution
