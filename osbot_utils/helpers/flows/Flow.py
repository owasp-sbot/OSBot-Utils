import asyncio
import logging
import typing

from osbot_utils.helpers.Dependency_Manager             import Dependency_Manager
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.helpers.CFormat                        import CFormat, f_dark_grey, f_magenta, f_bold
from osbot_utils.helpers.flows.models.Flow_Run__Config  import Flow_Run__Config
from osbot_utils.helpers.flows.Flow__Events             import flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data import Flow_Run__Event_Data
from osbot_utils.testing.Stdout                         import Stdout
from osbot_utils.utils.Misc                             import random_id, lower
from osbot_utils.utils.Python_Logger                    import Python_Logger
from osbot_utils.utils.Str                              import ansis_to_texts
from osbot_utils.utils.Threads                          import invoke_in_new_event_loop

FLOW__RANDOM_ID__PREFIX    = 'flow_id__'
FLOW__RANDOM_NAME__PREFIX  = 'flow_name__'
FLOW__LOGGING__LOG_FORMAT  = '%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s'
FLOW__LOGGING__DATE_FORMAT = '%H:%M:%S'



class Flow(Type_Safe):
    captured_exec_logs : list
    data               : dict                   # dict available to the tasks to add and collect data
    flow_id            : str
    flow_name          : str
    flow_config        : Flow_Run__Config
    flow_error         : Exception           = None
    flow_target        : callable
    flow_args          : tuple
    flow_kwargs        : dict
    flow_return_value  : typing.Any
    flow_run_params    : dict
    logger             : Python_Logger
    cformat            : CFormat
    executed_tasks     : typing.List
    resolved_args      : tuple
    resolved_kwargs    : dict

    def add_flow_artifact(self, description=None, key=None, data=None, artifact_type=None):     # todo: figure out how to make this work since at the moment most are showing an unknown type
        event_data = Flow_Run__Event_Data()
        event_data.data= dict(artifact_data = dict(description = description or 'description',
                                                   key         = key  or 'an-artifact-key',
                                                   data        = data or {"link": "https://www.google.com", "link_text": "link to Google"},  # test data to see if it worksw
                                                   type        = artifact_type or "link"))                                                   # type clashed with built-in type
        event_data.flow_run_id = self.flow_id
        flow_events.on__new_artifact(event_data)


    def add_flow_result(self, key, description):
        event_data = Flow_Run__Event_Data()
        event_data.flow_run_id = self.flow_id
        event_data.data        = dict(result_data = dict(key         = key         ,
                                                         description = description ))
        flow_events.on__new_result(event_data)

    def config_logger(self):
        with self.logger as _:
            _.set_log_level(logging.DEBUG)
            _.set_log_format(log_format=FLOW__LOGGING__LOG_FORMAT, date_format=FLOW__LOGGING__DATE_FORMAT)
            if self.flow_config.log_to_console:
                _.add_console_logger()

    def execute(self):
        return self.execute_flow()

    def execute_flow(self, flow_run_params=None):                               # todo: see if it makes more sense to call this start_flow_run
        flow_events.on__flow__start(self.flow_event_data())
        self.log_debug(f"Created flow run '{self.f__flow_id()}' for flow '{self.f__flow_name()}'")
        self.set_flow_run_params(flow_run_params)

        if self.flow_config.log_to_memory:
            self.logger.add_memory_logger()                                     # todo: move to method that does pre-execute tasks

        self.log_debug(f"Executing flow run '{self.f__flow_id()}'")
        self.resolve_args_and_kwargs()
        try:
            with Stdout() as stdout:
                self.invoke_flow_target()
        except Exception as error:
            self.flow_error = error
            self.log_error(self.cformat.red(f"Error executing flow: {error}"))

        self.log_captured_stdout        (stdout)
        self.print_flow_return_value    ()
        self.print_flow_finished_message()

        if self.flow_config.log_to_memory:
            self.captured_exec_logs = self.log_messages_with_colors()
            self.logger.remove_memory_logger()                                                          # todo: move to method that does post-execute tasks
        if self.flow_return_value:
            self.add_flow_result(key = 'flow-return-value', description=f'{self.flow_return_value}')
        flow_events.on__flow__stop(self.flow_event_data())
        return self

    def captured_logs(self):
        return ansis_to_texts(self.captured_exec_logs)


    async def invoke_flow_target__thread(self, flow):                               # this is a REALLY important method which is used to pin the flow object to the call stack
        return await flow.flow_target(*flow.resolved_args, **flow.resolved_kwargs)          #   which is then used by the Task.find_flow method to find it

    def invoke_flow_target(self):
        if asyncio.iscoroutinefunction(self.flow_target):
            async_coroutine         = self.invoke_flow_target__thread(self)                     # use this special method to pin the flow object to the call stack
            self.flow_return_value  = invoke_in_new_event_loop(async_coroutine)                 # this will start a complete new thread to execute the flow (which is exactly what we want)
        else:
            self.flow_return_value  = self.flow_target(*self.resolved_args, **self.resolved_kwargs)     # if the flow is sync, just execute the flow target

    def f__flow_id(self):
        return self.cformat.green(self.flow_id)

    def f__flow_name(self):
        return self.cformat.blue(self.flow_name)

    def flow_event_data(self):
        kwargs = dict(flow_name = self.flow_name,
                      flow_id   = self.flow_id)
        return Flow_Run__Event_Data(**kwargs)

    def log_captured_stdout(self, stdout):
        for line in stdout.value().splitlines():
            if line:
                self.log_info(f_magenta(line))
        if self.flow_config.print_logs:
            print()
            print()
            self.print_log_messages()


    def log_debug(self, message, task_run_id=None):
        self.logger_add_message(log_level=logging.DEBUG, message=message, task_run_id=task_run_id)

    def log_error(self, message, task_run_id=None):
        self.logger_add_message(log_level=logging.ERROR, message=message, task_run_id=task_run_id)

    def log_info(self, message, task_run_id=None):
        self.logger_add_message(log_level=logging.INFO, message=message, task_run_id=task_run_id)

    def logger_add_message(self, log_level, message, task_run_id=None):
        if self.flow_config.logging_enabled:
            kwargs = dict(log_level   = log_level   ,
                          message     = message     ,
                          flow_run_id = self.flow_id,
                          task_run_id = task_run_id )
            flow_events.on__flow_run__message(**kwargs)
            if log_level == logging.DEBUG:
                self.logger.debug(message)
            elif log_level == logging.ERROR:
                self.logger.error(message)
            else:
                self.logger.info(message)

    def log_messages(self):
        return ansis_to_texts(self.log_messages_with_colors())

    def log_messages_with_colors(self):
        return self.logger.memory_handler_messages()

    def print_log_messages(self, use_colors=True):
        if use_colors:
            if self.captured_exec_logs:
                for message in self.captured_exec_logs:
                    print(message)
            else:
                for message in self.logger.memory_handler_messages():
                    print(message)
        else:
            for message in self.log_messages():
                print(message)
        return self

    def print_flow_finished_message(self):
        if self.flow_config.print_finished_message:
            self.log_debug(f"Finished flow run '{self.f__flow_id()}'")

    def print_flow_return_value(self):
        if self.flow_config.print_none_return_value is False and self.flow_return_value is None:
            return
        self.log_debug(f"{f_dark_grey('Flow return value')}: {f_bold(self.flow_return_value)}")



    def random_flow_id(self):
        return lower(random_id(prefix=FLOW__RANDOM_ID__PREFIX))

    def random_flow_name(self):
        return lower(random_id(prefix=FLOW__RANDOM_NAME__PREFIX))

    def resolve_args_and_kwargs(self):
        dependency_manager = Dependency_Manager()
        dependency_manager.add_dependency('this_flow', self)
        dependency_manager.add_dependency('flow_data', self.data)
        self.resolved_args, self.resolved_kwargs = dependency_manager.resolve_dependencies(self.flow_target,
                                                                                           *self.flow_args,
                                                                                           **self.flow_kwargs)

    def set_flow_target(self, target, *args, **kwargs):
        self.flow_target = target
        self.flow_args   = args
        self.flow_kwargs = kwargs
        return self

    def set_flow_name(self, value=None):
        if value:
            self.flow_name = value
        else:
            if not self.flow_name:
                if hasattr(self.flow_target, '__name__'):
                    self.flow_name = self.flow_target.__name__
                else:
                    self.flow_name = self.random_flow_name()

    def set_flow_run_params(self, flow_run_params=None):
        if flow_run_params:
            self.flow_run_params = flow_run_params
            self.log_info(f"flow_run_params: {flow_run_params}")
            self.add_flow_artifact(description="Data received via FastAPI's request.json()", key='post-data', data=flow_run_params)

    def setup(self, target, *args, **kwargs):
        with self as _:
            _.cformat.auto_bold = True
            _.set_flow_target (target, *args, **kwargs)
            _.config_logger   ()
            _.setup_flow_run  ()
            _.set_flow_name   ()
        return self

    def setup_flow_run(self):
        with self as _:
            if not _.flow_id:
                _.flow_id = self.random_flow_id()
