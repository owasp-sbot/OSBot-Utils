import sys
from typing                                                             import Optional
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector          import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.timestamp_collector__config  import MAX_STACK_DEPTH, COLLECTOR_VAR_NAME


def find_timestamp_collector(max_depth: int = MAX_STACK_DEPTH           # Walk call stack to find Timestamp_Collector
                            ) -> Optional[Timestamp_Collector]:         # Returns None if not found (instrumentation disabled)

    frame = sys._getframe(1)

    for _ in range(max_depth):
        if frame is None:
            break

        if COLLECTOR_VAR_NAME in frame.f_locals:                        # Looks for local variable named '_timestamp_collector_'
            obj = frame.f_locals[COLLECTOR_VAR_NAME]
            if isinstance(obj, Timestamp_Collector):
                return obj

        frame = frame.f_back

    return None