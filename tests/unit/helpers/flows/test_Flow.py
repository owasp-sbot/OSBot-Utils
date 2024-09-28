from unittest                                           import TestCase
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers
from osbot_utils.helpers.flows.Flow                     import Flow
from osbot_utils.utils.Str                              import ansis_to_texts

class test_Flow(TestCase):

    def setUp(self):
        self.flow = Flow()

    def test_random_flow_id(self):
        with self.flow as _:
            assert _.flow_id == self.flow.flow_id

    def test_execute_flow(self):

        def just_print_a_message():
            print('this is inside the flow')

        with disable_root_loggers():
            with self.flow as _:
                _.flow_id = 'AN-FLOW-ID'
                _.setup()
                _.set_flow_target(just_print_a_message)
                #_.set_flow_target(lambda : print('this is a lambda function'))
                _.create_flow()
                _.flow_config.print_none_return_value = True
                _.flow_config.print_finished_message  = True
                _.execute_flow()
                assert ansis_to_texts(_.captured_exec_logs) == ["Executing flow run 'AN-FLOW-ID''",
                                                                'this is inside the flow',
                                                                'Flow return value: None',
                                                                "Finished flow run 'AN-FLOW-ID''"]



