import inspect
from functools import wraps

from osbot_utils.helpers.duration.Duration import Duration


def duration(func):
    if inspect.iscoroutinefunction(func):
        # It's an async function
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with Duration(prefix=f'.{func.__name__} took'):
                return await func(*args, **kwargs)
        return async_wrapper
    else:
        # It's a regular function
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with Duration(prefix=f'.{func.__name__} took'):
                return func(*args, **kwargs)
        return sync_wrapper