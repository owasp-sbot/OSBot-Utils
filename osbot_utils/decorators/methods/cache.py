from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T', bound=Callable[..., Any])

def cache(function: T) -> T:
    """
    Use this decorator when wanting to cache a value for all executions of the current process and want to preserve the type completion
    which the one from  "from functools import cache" doesn't
    note: that this will cache only one value per function (regardless of the values of *args,**kwargs).
          if you have multiple params that should be cached separately, use the @cache_on_self decorator (or the native @cache from functools)
    """
    @wraps(function)
    def wrapper(*args,**kwargs):
        cache_id= f'osbot_cache_return_value__{function.__name__}'
        if hasattr(function, cache_id) is False:                     # check if return_value has been set
            setattr(function, cache_id,  function(*args,**kwargs))   # invoke function and capture the return value
        return getattr(function, cache_id)                           # return the return value
    return wrapper