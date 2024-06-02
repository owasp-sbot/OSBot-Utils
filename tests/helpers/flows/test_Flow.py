import logging
from unittest import TestCase

from osbot_utils.helpers.flows.Flow import Flow
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_info


class test_Flow(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow = Flow()

    def test_random_flow_id(self):
        with self.flow as _:
            assert _.flow_id == self.flow.flow_id
            #assert _.flow_id.startswith('FLOW_ID__PREFIX_')

    def test_execute_flow(self):

        def just_print_a_message():
            print('this is inside the flow')

        print('\n\n\n')
        with self.flow as _:
            _.logger.root_logger__clear_handlers()
            _.log_to_console = False
            mem_logger = _.logger.add_memory_logger()
            _.setup()
            _.set_flow_target(just_print_a_message)
            #_.set_flow_target(lambda : print('this is a lambda function'))
            _.create_flow()
            _.execute_flow()

            pprint(mem_logger)




