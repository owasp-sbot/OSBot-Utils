"""
Timestamp Capture - @timestamp decorator
==========================================

  Usage:
        @timestamp
        def my_method(self):
            ...

        @timestamp(name="custom.name")
        def another(self):
            ...
"""

from functools                                                                     import wraps
from typing                                                                        import Callable, Optional
from osbot_utils.helpers.timestamp_capture.static_methods.find_timestamp_collector import find_timestamp_collector


def timestamp(func: Callable = None, *, name: str = None):          #  Decorator to capture method timestamps.

    def decorator(fn: Callable) -> Callable:
        method_name = name or fn.__qualname__

        @wraps(fn)
        def wrapper(*args, **kwargs):
            collector = find_timestamp_collector()

            if collector is None:
                return fn(*args, **kwargs)

            collector.enter(method_name)
            try:
                return fn(*args, **kwargs)
            finally:
                collector.exit(method_name)

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


