# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Time_Unit - Time display unit for benchmark results
# Controls formatting of timing values in reports
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__Time_Unit(Enum):                                                     # Time display unit
    NANOSECONDS  = 'ns'                                                          # Default unit
    MICROSECONDS = 'µs'                                                          # 1,000 ns
    MILLISECONDS = 'ms'                                                          # 1,000,000 ns
    SECONDS      = 's'                                                           # 1,000,000,000 ns
