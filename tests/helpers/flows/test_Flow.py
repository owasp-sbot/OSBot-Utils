from unittest                                           import TestCase
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers
from osbot_utils.helpers.flows.Flow import Flow, flow
from osbot_utils.utils.Dev import pprint


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

        with disable_root_loggers():
            with self.flow as _:
                _.flow_id = 'AN-FLOW-ID'
                _.setup()
                _.set_flow_target(just_print_a_message)
                #_.set_flow_target(lambda : print('this is a lambda function'))
                _.create_flow()
                _.execute_flow()
                assert _.log_messages() == [  "Created flow run 'AN-FLOW-ID' for flow 'just_print_a_message'",
                                              "Executing flow run 'AN-FLOW-ID''",
                                              'this is inside the flow',
                                              'return value: None',
                                              "Finished flow run 'AN-FLOW-ID''"]

@flow()
def an_method_with_flow(value):
    print('this is inside the flow!')
    return 40 + value

class test_flow__decorator(TestCase):

    def test__invoke_method_flow(self):
        result_value = an_method_with_flow(2)
        assert result_value == 42





