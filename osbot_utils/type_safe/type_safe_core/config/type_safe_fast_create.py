# ═══════════════════════════════════════════════════════════════════════════════
# Decorator: type_safe_fast_create
# Wraps function execution in Type_Safe__Config(fast_create=True, skip_validation=True)
# ═══════════════════════════════════════════════════════════════════════════════

from functools import wraps
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config import Type_Safe__Config


def type_safe_fast_create(func):
    """
    Decorator that wraps function execution with fast_create mode enabled.

    Usage:
        @type_safe_fast_create
        def test__my_benchmark(self):
            # All Type_Safe objects created here use fast_create
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Type_Safe__Config(fast_create=True, skip_validation=True):
            return func(*args, **kwargs)
    return wrapper