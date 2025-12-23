"""
Timestamp Capture - @timestamp_args decorator
===============================================

Decorator for dynamic timestamp names using function argument interpolation.

Usage:
    @timestamp_args(name="process.{item_type}")
    def process(self, item_type: str, data):
        ...
    # Records as "process.json", "process.xml", etc.

    @timestamp_args(name="link_component({name})")
    def _link_component(self, name: str, root_id: int):
        ...
    # Records as "link_component(head)", "link_component(body)", etc.

For static names, use @timestamp instead (lower overhead).
"""

import inspect
from functools                                                                     import wraps
from typing                                                                        import Callable
from osbot_utils.helpers.timestamp_capture.static_methods.find_timestamp_collector import find_timestamp_collector


def timestamp_args(*, name: str):                                                  # Decorator with dynamic name from args
    if not name:
        raise ValueError("timestamp_args requires a name parameter")
    if '{' not in name:
        raise ValueError("timestamp_args name must contain {arg} placeholders. Use @timestamp for static names.")

    def decorator(fn: Callable) -> Callable:
        fn_signature = inspect.signature(fn)                                       # Cache signature at decoration time

        @wraps(fn)
        def wrapper(*args, **kwargs):
            collector = find_timestamp_collector()

            if collector is None:
                return fn(*args, **kwargs)

            try:                                                                   # Resolve dynamic name from arguments
                bound = fn_signature.bind(*args, **kwargs)
                bound.apply_defaults()
                method_name = name.format(**bound.arguments)
            except (KeyError, IndexError):                                         # Fallback if interpolation fails
                method_name = name

            collector.enter(method_name)
            try:
                return fn(*args, **kwargs)
            finally:
                collector.exit(method_name)

        return wrapper

    return decorator