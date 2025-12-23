from typing                          import Dict, Any
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Timestamp_Entry(Type_Safe):                   # Single timestamp capture entry
    name         : str              = ''
    event        : str              = ''                    # 'enter' | 'exit'
    timestamp_ns : int              = 0                     # perf_counter_ns (monotonic)
    clock_ns     : int              = 0                     # time_ns (wall clock)
    thread_id    : int              = 0
    depth        : int              = 0
    extra        : Dict[str, Any]   = None