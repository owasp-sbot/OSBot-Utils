# ═══════════════════════════════════════════════════════════════════════════════
# Safe_Str__Benchmark_Id - Full benchmark identifier primitive
# e.g., "A_01__python__nop", "B_03__type_safe__empty"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Benchmark_Id(Safe_Str):                                          # Full benchmark ID
    max_length = 100
