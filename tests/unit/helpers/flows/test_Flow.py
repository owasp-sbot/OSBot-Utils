from unittest                                           import TestCase
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers
from osbot_utils.helpers.flows.Flow import Flow, flow
from osbot_utils.helpers.flows.Task import Task
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Str import ansis_to_texts


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
                _.execute_flow()
                assert ansis_to_texts(_.captured_exec_logs) == ["Executing flow run 'AN-FLOW-ID''",
                                                                'this is inside the flow',
                                                                'return value: None',
                                                                "Finished flow run 'AN-FLOW-ID''"]



class test_flow__decorator(TestCase):


    def test__invoke_method_flow(self):

        @flow()
        def an_method_with_flow(value):
            print('this is inside the flow!')
            return 40 + value

        with disable_root_loggers():
            result_value = an_method_with_flow(2)
            assert result_value == 42

    def test__invoke_method_flow__with_task(self):

        @flow(print_logs=False, flow_id='THE-FLOW-ID')
        def an_method_with_flow(name):
            print('this is inside the flow!')

            task = Task()
            with task.find_flow() as _:
                _.info(f'hello {name}')
                _.info('this is from an TASK that found the flow')

                return  _.log_messages()

        with disable_root_loggers():
            result_value = an_method_with_flow('world')
            assert result_value == [ "Executing flow run 'THE-FLOW-ID''"        ,
                                     'hello world'                              ,
                                     'this is from an TASK that found the flow' ]






