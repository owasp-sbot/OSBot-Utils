# ═══════════════════════════════════════════════════════════════════════════════
# List__Scores - List of benchmark scores (nanoseconds)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                           import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt


class List__Scores(Type_Safe__List):                                             # [score, score, ...]
    expected_type = Safe_UInt
