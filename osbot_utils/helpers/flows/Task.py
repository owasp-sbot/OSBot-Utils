import inspect
import typing
from functools import wraps

from osbot_utils.testing.Stdout import Stdout

from osbot_utils.helpers.CFormat        import CFormat, f_dark_grey, f_red, f_blue
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.flows.Flow     import Flow


def task(**task_kwargs):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with Task(task_target=function, task_args=args, task_kwargs=kwargs, **task_kwargs) as _:
                return _.execute()

        return wrapper
    return decorator

class Task(Type_Safe):
    task_id       : str                         # todo add a random Id value to this
    task_name     : str                         # make this the function mame
    cformat       : CFormat
    task_target   : callable          # todo refactor this to to Task__Function class
    task_args     : tuple
    task_kwargs   : dict
    task_flow     : Flow
    task_result   : typing.Any

    def execute(self):
        self.task_flow = self.find_flow()
        if self.task_flow is None:
            raise Exception("No Flow found for Task")

        self.task_flow.executed_tasks.append(self)
        self.task_flow.logger.debug(f"Executing task '{f_blue(self.task_target.__name__)}'")

        try:
            with Stdout() as stdout:
                self.task_result = self.task_target(*self.task_args, **self.task_kwargs)           # todo, capture *args, **kwargs in logs
        except Exception as error:
            self.task_flow.logger.error(f_red(f"Error executing flow: {error}"))
        self.task_flow.log_captured_stdout(stdout)
        self.task_flow.logger.debug(f"{f_dark_grey('return value')}: {self.task_result}")

        self.task_flow.logger.debug(f"Finished task '{f_blue(self.task_target.__name__)}'")
        return self.task_result

    def find_flow(self):
        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            if 'self' in frame.f_locals:
                instance = frame.f_locals['self']
                if type(instance) is Flow:
                    return instance
