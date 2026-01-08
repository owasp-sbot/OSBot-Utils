# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Benchmark__Trend - Performance trend indicators
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__Benchmark__Trend(Enum):                                              # Performance trend
    STRONG_IMPROVEMENT = 'strong_improvement'                                    # ▼▼▼ > 10%
    IMPROVEMENT        = 'improvement'                                           # ▼ 0-10%
    UNCHANGED          = 'unchanged'                                             # ─
    REGRESSION         = 'regression'                                            # ▲ 0-10%
    STRONG_REGRESSION  = 'strong_regression'                                     # ▲▲▲ > 10%
