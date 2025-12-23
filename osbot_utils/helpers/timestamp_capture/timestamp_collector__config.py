# todo: see if this value is too high (explore performance implications)
MAX_STACK_DEPTH      : int = 50                             # Max frames to walk looking for collector
COLLECTOR_VAR_NAME   : str = '_timestamp_collector_'        # Magic variable name to search for
OVERHEAD_THRESHOLD_NS: int = 1000                           # 1μs - warn if overhead exceeds
NS_TO_MS             : int = 1_000_000                       # nanoseconds to milliseconds