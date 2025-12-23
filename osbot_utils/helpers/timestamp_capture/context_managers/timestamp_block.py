"""
Context manager to timestamp a code block.

Usage:
    with timestamp_block("my_phase"):
        # code to measure
        ...
"""
from contextlib                                                                    import contextmanager
from osbot_utils.helpers.timestamp_capture.static_methods.find_timestamp_collector import find_timestamp_collector


@contextmanager
def timestamp_block(name: str):

    collector = find_timestamp_collector()
    if collector:
        collector.enter(name)
    try:
        yield
    finally:
        if collector:
            collector.exit(name)