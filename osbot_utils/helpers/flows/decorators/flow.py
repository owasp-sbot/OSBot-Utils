from functools                      import wraps
from typing import TypeVar, Callable, Any

from osbot_utils.helpers.flows.Flow import Flow

# todo: find way to make the casting below work for the users of this decorator

def flow(**flow_kwargs):
    def decorator(function) -> Flow:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Flow:
            with Flow(**flow_kwargs) as _:
                _.set_flow_target(function, *args, **kwargs)
                _.setup()
                _.create_flow()
                return _
        return wrapper
    return decorator