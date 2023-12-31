from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T', bound=Callable[..., Any])

# todo: create signature based on request params so that we don't cache when the params are different
# todo: add capability to reset or change the cache value currently stored in the cache_id value
def cache(function: T) -> T:
    """
    Use this decorator when wanting to cache a value for all executions of the current process
    """
    @wraps(function)
    def wrapper(*args,**kwargs):
        cache_id= f'osbot_cache_return_value__{function.__name__}'
        if hasattr(function, cache_id) is False:                     # check if return_value has been set
            setattr(function, cache_id,  function(*args,**kwargs))   # invoke function and capture the return value
        return getattr(function, cache_id)                           # return the return value
    return wrapper