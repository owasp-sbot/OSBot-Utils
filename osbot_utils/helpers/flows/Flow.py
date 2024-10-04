import asyncio
import logging
import typing

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.CFormat import CFormat, f_dark_grey, f_magenta, f_bold
from osbot_utils.helpers.flows.Flow__Config import Flow__Config
from osbot_utils.testing.Stdout         import Stdout
from osbot_utils.utils.Misc             import random_id, lower
from osbot_utils.utils.Python_Logger    import Python_Logger
from osbot_utils.utils.Str              import ansis_to_texts
from osbot_utils.utils.Threads import invoke_async, invoke_in_new_event_loop

FLOW__RANDOM_ID__PREFIX    = 'flow_id__'
FLOW__RANDOM_NAME__PREFIX  = 'flow_name__'
FLOW__LOGGING__LOG_FORMAT  = '%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s'
FLOW__LOGGING__DATE_FORMAT = '%H:%M:%S'



class Flow(Type_Safe):
    captured_exec_logs : list
    data               : dict                   # dict available to the tasks to add and collect data
    flow_id            : str
    flow_name          : str
    flow_config        : Flow__Config
    flow_error         : Exception           = None
    flow_target        : callable
    flow_args          : tuple
    flow_kwargs        : dict
    flow_return_value  : typing.Any
    logger             : Python_Logger
    cformat            : CFormat
    executed_tasks     : typing.List



    def config_logger(self):
        with self.logger as _:
            _.set_log_level(logging.DEBUG)
            _.set_log_format(log_format=FLOW__LOGGING__LOG_FORMAT, date_format=FLOW__LOGGING__DATE_FORMAT)
            if self.flow_config.log_to_console:
                _.add_console_logger()


    def debug(self, message):
        self.logger.debug(message)

    def create_flow(self):
        self.set_flow_name()
        self.debug(f"Created flow run '{self.f__flow_id()}' for flow '{self.f__flow_name()}'")

    def execute(self):
        return self.execute_flow()

    def execute_flow(self):
        if self.flow_config.log_to_memory:
            self.logger.add_memory_logger()                                     # todo: move to method that does pre-execute tasks

        self.debug(f"Executing flow run '{self.f__flow_id()}''")
        try:
            with Stdout() as stdout:
                self.invoke_flow_target()
        except Exception as error:
            self.flow_error = error
            self.logger.error(self.cformat.red(f"Error executing flow: {error}"))

        self.log_captured_stdout        (stdout)
        self.print_flow_return_value    ()
        self.print_flow_finished_message()

        if self.flow_config.log_to_memory:
            self.captured_exec_logs = self.log_messages_with_colors()
            self.logger.remove_memory_logger()                                                          # todo: move to method that does post-execute tasks
        return self

    def f__flow_id(self):
        return self.cformat.green(self.flow_id)

    def f__flow_name(self):
        return self.cformat.blue(self.flow_name)

    def captured_logs(self):
        return ansis_to_texts(self.captured_exec_logs)

    def info(self, message):
        self.logger.info(message)

    def invoke_flow_target(self):
        if asyncio.iscoroutinefunction(self.flow_target):
            #self.flow_return_value = invoke_async(self.flow_target(*self.flow_args, **self.flow_kwargs))
            self.flow_return_value = invoke_in_new_event_loop(self.flow_target(*self.flow_args, **self.flow_kwargs))
        else:
            self.flow_return_value = self.flow_target(*self.flow_args, **self.flow_kwargs)

    def log_captured_stdout(self, stdout):
        for line in stdout.value().splitlines():
            if line:
                self.info(f_magenta(line))
        if self.flow_config.print_logs:
            print()
            print()
            self.print_log_messages()


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
            self.debug(f"Finished flow run '{self.f__flow_id()}''")

    def print_flow_return_value(self):
        if self.flow_config.print_none_return_value is False and self.flow_return_value is None:
            return
        self.debug(f"{f_dark_grey('Flow return value')}: {f_bold(self.flow_return_value)}")



    def random_flow_id(self):
        return lower(random_id(prefix=FLOW__RANDOM_ID__PREFIX))

    def random_flow_name(self):
        return lower(random_id(prefix=FLOW__RANDOM_NAME__PREFIX))


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
    def setup(self):
        with self as _:
            _.cformat.auto_bold = True
            _.config_logger()
            _.setup_flow_run()
        return self

    def setup_flow_run(self):
        with self as _:
            if not _.flow_id:
                _.flow_id = self.random_flow_id()
            #if not _.flow_name:
            #    _.flow_name = self.flow_target.__name__
                #self.random_flow_name()
