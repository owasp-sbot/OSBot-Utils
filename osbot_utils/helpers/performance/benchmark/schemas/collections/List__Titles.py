# ═══════════════════════════════════════════════════════════════════════════════
# List__Titles - List of benchmark titles
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                           import Type_Safe__List
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title      import Safe_Str__Benchmark__Title


class List__Titles(Type_Safe__List):                                             # [title, title, ...]
    expected_type = Safe_Str__Benchmark__Title
