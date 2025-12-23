from osbot_utils.helpers.timestamp_capture.schemas.Schema__Method_Timing   import Schema__Method_Timing
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry import Schema__Timestamp_Entry
from osbot_utils.helpers.timestamp_capture.timestamp_collector__config     import NS_TO_MS


def timestamp_entry__to_ms(entry: Schema__Timestamp_Entry) -> float:            # Convert entry timestamp to milliseconds
    return entry.timestamp_ns / NS_TO_MS

def method_timing__total_ms(timing: Schema__Method_Timing) -> float:            # Total time in milliseconds
    return timing.total_ns / NS_TO_MS

def method_timing__avg_ms(timing: Schema__Method_Timing) -> float:              # Average time per call in milliseconds
    if timing.call_count > 0:
        return timing.total_ns / timing.call_count / NS_TO_MS
    return 0.0

def method_timing__self_ms(timing: Schema__Method_Timing) -> float:             # Self time (exclusive) in milliseconds
    return timing.self_ns / NS_TO_MS

def method_timing__min_ms(timing: Schema__Method_Timing) -> float:              # Minimum call time in milliseconds
    return timing.min_ns / NS_TO_MS

def method_timing__max_ms(timing: Schema__Method_Timing) -> float:              # Maximum call time in milliseconds
    return timing.max_ns / NS_TO_MS