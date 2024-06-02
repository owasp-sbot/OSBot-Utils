import logging
import types
from logging import Logger

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.CFormat import CFormat, f_grey, f_dark_grey
from osbot_utils.helpers.trace.Trace_Call__Print_Traces import text_red, text_bold_red
from osbot_utils.testing.Logging        import Logging
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Misc import random_id, lower, wait_for
from osbot_utils.utils.Python_Logger import Python_Logger
from osbot_utils.utils.Str import ansis_to_texts

FLOW__RANDOM_ID__PREFIX    = 'flow_id__'
FLOW__RANDOM_NAME__PREFIX  = 'flow_name__'
FLOW__LOGGING__LOG_FORMAT  = '%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s'
FLOW__LOGGING__DATE_FORMAT = '%H:%M:%S'

class Flow(Type_Safe):
    flow_id       : str
    flow_name     : str
    flow_target   : callable
    logger       : Python_Logger
    cformat       : CFormat
    log_to_console: bool = False
    log_to_memory : bool = True

    def config_logger(self):
        with self.logger as _:
            _.set_log_level(logging.DEBUG)
            _.set_log_format(log_format=FLOW__LOGGING__LOG_FORMAT, date_format=FLOW__LOGGING__DATE_FORMAT)
            if self.log_to_console:
                _.add_console_logger()
            if self.log_to_memory:
                _.add_memory_logger()


    def debug(self, message):
        self.logger.debug(message)

    def create_flow(self):
        self.set_flow_name()
        self.debug(f"Created flow run '{self.f__flow_id()}' for flow '{self.f__flow_name()}'")

    def execute_flow(self):
        self.debug(f"Executing flow run '{self.f__flow_id()}''")
        try:
            with Stdout() as _:
                return_value = self.flow_target()
            self.info(_.value().strip())
            self.debug(f"{f_dark_grey('return value')}: {return_value}")

        except Exception as error:
            self.logger.error(self.cformat.red(f"Error executing flow: {error}"))
        self.debug(f"Finished flow run '{self.f__flow_id()}''")
    def f__flow_id(self):
        return self.cformat.green(self.flow_id)

    def f__flow_name(self):
        return self.cformat.blue(self.flow_name)

    def info(self, message):
        self.logger.info(message)

    def log_messages(self):
        log_messages_with_colors = self.logger.memory_handler_messages()
        return ansis_to_texts(log_messages_with_colors)

    def print_log_messages(self):
        for message in self.log_messages():
            print(message)
        return self
    def random_flow_id(self):
        return lower(random_id(prefix=FLOW__RANDOM_ID__PREFIX))

    def random_flow_name(self):
        return lower(random_id(prefix=FLOW__RANDOM_NAME__PREFIX))


    def set_flow_target(self, target):
        self.flow_target = target
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
