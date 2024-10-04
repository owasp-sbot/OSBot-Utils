from functools import wraps
import asyncio
from osbot_utils.helpers.flows.Task import Task


def task(**task_kwargs):
    def decorator(function):
        @wraps(function)
        async def async_wrapper(*args, **kwargs):
            with Task(task_target=function, task_args=args, task_kwargs=kwargs, **task_kwargs) as _:
                return await _.execute__async()

        @wraps(function)
        def sync_wrapper(*args, **kwargs):
            with Task(task_target=function, task_args=args, task_kwargs=kwargs, **task_kwargs) as _:
                return _.execute__sync()

        if asyncio.iscoroutinefunction(function):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
