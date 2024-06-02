import logging
from logging import Logger

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.CFormat import CFormat
from osbot_utils.helpers.trace.Trace_Call__Print_Traces import text_red, text_bold_red
from osbot_utils.testing.Logging        import Logging
from osbot_utils.utils.Misc import random_id, lower, wait_for

FLOW__ID__PREFIX          = 'flow_'
FLOW__LOGGING__LOG_FORMAT = '%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s'
FLOW__LOGGING__DATE_FORMAT = '%H:%M:%S'

class Flow(Type_Safe):
    flow_id   : str     = 'an flow id'
    flow_name : str     = 'an flow name'
    logging: Logging


    def config_logger(self):
        with self.logging as _:
            _.set_logger_level(logging.DEBUG)
            _.set_log_format(log_format=FLOW__LOGGING__LOG_FORMAT, date_format=FLOW__LOGGING__DATE_FORMAT)
            _.enable_log_to_console()


    def random_flow_id(self):
        return lower(random_id(prefix=FLOW__ID__PREFIX))

    def create_flow(self):
        cformat = CFormat(auto_bold=True)
        self.info(f"Created flow run '{cformat.blue(self.flow_id)}' for flow '{cformat.green(self.flow_name)}'")

    def execute_flow(self):
        self.info(f"executing flow run '{text_red(self.flow_id)}'")

    def info(self, message):
        self.logging.info(message)

    def setup(self):
        with self as _:
            _.config_logger()
            _.setup_flow_run()
        return self

    def setup_flow_run(self):
        with self as _:
            if _.flow_id is None:
                _.flow_id = random_id()
