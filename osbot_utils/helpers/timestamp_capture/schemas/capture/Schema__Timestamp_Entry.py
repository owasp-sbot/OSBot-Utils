from dataclasses import dataclass
from typing      import Dict, Any

@dataclass(slots=True)
class Schema__Timestamp_Entry:
    name         : str              = ''
    event        : str              = ''                    # 'enter' | 'exit'
    timestamp_ns : int              = 0                     # perf_counter_ns (monotonic)
    clock_ns     : int              = 0                     # time_ns (wall clock)
    thread_id    : int              = 0
    depth        : int              = 0
    extra        : Dict[str, Any]   = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False