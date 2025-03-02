import inspect
import traceback
import typing

from osbot_utils.helpers.flows.actions.Task__Stats__Collector import Task__Stats__Collector
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data    import Flow_Run__Event_Data
from osbot_utils.utils.Misc                                   import random_id, lower
from osbot_utils.helpers.Dependency_Manager                   import Dependency_Manager
from osbot_utils.helpers.flows.actions.Flow__Events           import flow_events
from osbot_utils.testing.Stdout                               import Stdout
from osbot_utils.helpers.CFormat                              import CFormat, f_dark_grey, f_red, f_blue, f_bold
from osbot_utils.type_safe.Type_Safe                          import Type_Safe
from osbot_utils.helpers.flows.Flow                           import Flow

TASK__RANDOM_ID__PREFIX    = 'task_id__'

# todo: add task duration

class Task(Type_Safe):
    data                : dict                          # dict available to the task to add and collect data
    task_id             : str
    task_stats          : Task__Stats__Collector
    task_name           : str                           # make this the function mame
    cformat             : CFormat
    resolved_args       : tuple
    resolved_kwargs     : dict
    task_target         : callable                      # todo refactor this to to Task__Function class
    task_args           : tuple
    task_kwargs         : dict
    task_flow           : Flow
    task_return_value   : typing.Any
    task_error          : Exception  = None
    raise_on_error      : bool       = True

    def log_info(self, message):
        self.task_flow.log_info(message, self.task_id)

    def log_debug(self, message):
        self.task_flow.log_debug(message, self.task_id)

    def log_error(self, message):
        self.task_flow.log_error(message, self.task_id)

    def execute__sync(self):
        self.execute__before()
        self.execute__task_target__sync()
        return self.execute__after()

    async def execute__async(self):
        self.execute__before()
        await self.execute__task_target__async()
        return self.execute__after()

    def execute__before(self):
        flow_from_stack = self.find_flow()
        if flow_from_stack:
            self.task_flow = flow_from_stack

        if self.task_flow is None:
            raise Exception("No Flow found for Task")

        if not self.task_name and self.task_target:
            self.task_name = self.task_target.__name__

        if not self.task_id:
            self.task_id = self.random_task_id()

        execution_order = self.task_flow.flow_stats.get_next_execution_order()
        self.task_stats.start(flow_id=self.task_flow.flow_id, task_id=self.task_id, task_name=self.task_name, execution_order=execution_order)

        self.on_task_start()
        flow_events.on__task__start(self.task_event_data())

        self.task_flow.executed_tasks.append(self)
        self.log_debug(f"Executing task '{f_blue(self.task_name)}'")
        self.resolve_args_and_kwargs()

    def task_event_data(self):
        kwargs = dict(flow_name   = self.task_flow.flow_name,
                      flow_run_id = self.task_flow.flow_id  ,
                      task_name   = self.task_name          ,
                      task_run_id = self.task_id            )
        return Flow_Run__Event_Data(**kwargs)

    def resolve_args_and_kwargs(self):
        dependency_manager = Dependency_Manager()
        dependency_manager.add_dependency('this_task', self               )
        dependency_manager.add_dependency('this_flow', self.task_flow     )
        dependency_manager.add_dependency('task_data', self.data          )
        dependency_manager.add_dependency('flow_data', self.task_flow.data)
        self.resolved_args, self.resolved_kwargs = dependency_manager.resolve_dependencies(self.task_target, *self.task_args, **self.task_kwargs)

    def execute__task_target__sync(self):
        try:
            with Stdout() as stdout:
                self.task_return_value =  self.task_target(*self.resolved_args, **self.resolved_kwargs)
        except Exception as error:
            self.task_error = error
            if self.task_flow.flow_config.print_error_stack_trace:
                tb = traceback.format_exc()
                print(f'{tb}')
        self.task_flow.log_captured_stdout(stdout)

    async def execute__task_target__async(self):
        try:
            with Stdout() as stdout:
                self.task_return_value =  await self.task_target(*self.resolved_args, **self.resolved_kwargs)
        except Exception as error:
            self.task_error = error
        self.task_flow.log_captured_stdout(stdout)

    def execute__after(self):

        self.task_stats.end(task_error=self.task_error)
        self.task_flow.flow_stats.add_task_stats(self.task_stats.stats)


        self.print_task_return_value()

        if self.task_error:
            self.log_error(f_red(f"Error executing '{self.task_name}' task: {self.task_error}"))
            if self.raise_on_error:
                raise Exception(f"'{self.task_name}' failed and task raise_on_error was set to True. Stopping flow execution", self.task_error)

        self.print_task_finished_message()

        flow_events.on__task__stop(self.task_event_data())
        self.on_task_end()
        return self.task_return_value

    def find_flow(self):                                                            # Find the closest Flow instance in the call stack by examining both self parameters and local variables in each frame
        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            for var_name, var_value in list(frame.f_locals.items()):                      # Check all local variables in the frame
                if isinstance(var_value, Flow):
                    return var_value
        return None

    def print_task_finished_message(self):
        if self.task_flow.flow_config.print_finished_message:
            self.log_debug(f"Finished task '{f_blue(self.task_name)}'")

    def print_task_return_value(self):
        flow_config = self.task_flow.flow_config
        if flow_config.print_none_return_value is False and self.task_return_value is None:
            return
        self.log_debug(f"{f_dark_grey('Task return value')}: {f_bold(self.task_return_value)}")


    def random_task_id(self):
        return lower(random_id(prefix=TASK__RANDOM_ID__PREFIX))


    def on_task_start(self):                                             # Handle task start event
        self.task_flow.flow_data.add_task(self.task_id, self.task_name)

    def on_task_end(self):                                               # Handle task end event
        status = 'failed' if self.task_error else 'completed'
        self.task_flow.flow_data.update_task(self.task_id     ,
                                             status           ,
                                             self.task_error  ,
                                             self.task_return_value)