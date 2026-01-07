# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Comparison__Status - Status of comparison operations
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__Comparison__Status(Enum):                                            # Comparison operation status
    SUCCESS                     = 'success'
    ERROR_NO_SESSIONS           = 'no_sessions'
    ERROR_INSUFFICIENT_SESSIONS = 'insufficient_sessions'
    ERROR_NO_COMMON_BENCHMARKS  = 'no_common_benchmarks'
