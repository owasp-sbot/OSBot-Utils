from functools                      import wraps
from osbot_utils.helpers.flows.Task import Task

def task(**task_kwargs):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with Task(task_target=function, task_args=args, task_kwargs=kwargs, **task_kwargs) as _:
                return _.execute()
        return wrapper
    return decorator