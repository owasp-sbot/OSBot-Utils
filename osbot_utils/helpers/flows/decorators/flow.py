from functools                      import wraps
from osbot_utils.helpers.flows.Flow import Flow


def flow(**flow_kwargs):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with Flow(**flow_kwargs) as _:
                _.set_flow_target(function, *args, **kwargs)
                _.setup()
                _.create_flow()
                return _
        return wrapper
    return decorator