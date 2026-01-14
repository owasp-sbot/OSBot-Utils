# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Measure_Mode - Controls measurement accuracy vs speed tradeoff
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__Measure_Mode(Enum):
    QUICK   = 'quick'                                                            # ~100 iterations, fastest, highest variance
    FAST    = 'fast'                                                             # ~1,000 iterations, balanced
    DEFAULT = 'default'                                                          # ~10,000 iterations, most accurate, slowest
    ONLY_3  = 'only_3'          # todo: add only_3 support to execution engine