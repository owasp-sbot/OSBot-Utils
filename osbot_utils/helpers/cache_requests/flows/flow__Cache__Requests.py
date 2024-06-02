import functools


def flow(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'FLOW  {func.__name__} with args: {args} and kwargs: {kwargs}')
        return func(*args, **kwargs)
    return wrapper


class flow__Cache_Requests:

    @flow
    def invoke_function(self, function, *args, **kwargs):
        return function(*args, **kwargs)