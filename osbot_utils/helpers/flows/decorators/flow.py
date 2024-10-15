from functools                      import wraps
from typing import TypeVar, Callable, Any

from osbot_utils.helpers.flows.Flow import Flow

# todo: BUG find way to make the casting below work for the users of this decorator
#           since at the moment we need to use: flow = cast(Flow, _.create_flow()) where create_flow is the method with the @flow decorator
def flow(**flow_kwargs):
    def decorator(function) -> Flow:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Flow:
            with Flow(**flow_kwargs) as _:
                _.setup(function, *args, **kwargs)
                return _
        return wrapper
    return decorator