# ═══════════════════════════════════════════════════════════════════════════════
# List__Benchmark_Sessions - Type-safe list of benchmark sessions
# Used by Diff tool to track multiple sessions for comparison
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session import Schema__Perf__Benchmark__Session
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                             import Type_Safe__List


class List__Benchmark_Sessions(Type_Safe__List):                                 # [session, session, ...]
    expected_type = Schema__Perf__Benchmark__Session
