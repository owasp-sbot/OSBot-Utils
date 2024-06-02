import inspect

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.flows.Flow import Flow


class Task(Type_Safe):
    task_id       : str
    task_name     : str

    def find_flow(self):
        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            if 'self' in frame.f_locals:
                instance = frame.f_locals['self']
                if type(instance) is Flow:
                    return instance