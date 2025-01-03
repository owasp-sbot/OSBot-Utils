from unittest                                           import TestCase
from osbot_utils.type_safe.Type_Safe                 import Type_Safe
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers
from osbot_utils.helpers.flows.Flow                     import Flow
from osbot_utils.helpers.flows.models.Flow_Run__Config  import Flow_Run__Config
from osbot_utils.helpers.flows.Task                     import Task
from osbot_utils.helpers.flows.decorators.flow          import flow
from osbot_utils.helpers.flows.decorators.task          import task


class test_decorator__flow(TestCase):

    def test__invoke_method_flow(self):

        @flow()
        def an_method_with_flow(value):
            print('this is inside the flow!')
            return 40 + value

        with disable_root_loggers():
            flow_1 = an_method_with_flow(2).execute()
            assert type(flow_1) is Flow
            assert flow_1.flow_return_value == 42

    def test__invoke_method_flow__with_task(self):
        flow_config = Flow_Run__Config(print_logs=False)

        @flow(flow_config=flow_config, flow_id='THE-FLOW-ID')
        def an_method_with_flow(name):
            print('this is inside the flow!')

            with Task().find_flow() as _:
                _.log_info(f'hello {name}')
                _.log_info('this is from an TASK that found the flow')

                return  _.log_messages()

        with disable_root_loggers():
            flow_1 = an_method_with_flow('world').execute()
            assert flow_1.flow_return_value == [ "Executing flow run 'THE-FLOW-ID'"         ,
                                                 'hello world'                              ,
                                                 'this is from an TASK that found the flow' ]

    def test__invoke_decorators__with_flow_and_task(self):

        kwargs      = dict(print_none_return_value=True,
                           print_finished_message=True )
        flow_config = Flow_Run__Config(**kwargs)

        class An_Class(Type_Safe):

            @task()
            def exec_task_1(self, value):
                print(f'inside task 1 with {value}')
                value+=1
                return value

            @task()
            def exec_task_2(self):
                print('inside task 2')

            @flow(flow_config=flow_config)
            def an_method_with_flow(self, value):
                print('inside the flow!')
                new_value = self.exec_task_1(value)
                self.exec_task_2()
                return 40 + new_value

        an_class = An_Class()

        with disable_root_loggers():
            flow_1 = an_class.an_method_with_flow(1).execute()
            assert flow_1.flow_return_value == 42
            assert type(flow_1) is Flow
            flow_id = flow_1.flow_id
            assert flow_1.captured_logs() == [ f"Executing flow run '{flow_id}'",
                                                "Executing task 'exec_task_1'",
                                                'inside task 1 with 1',
                                                'Task return value: 2',
                                                "Finished task 'exec_task_1'",
                                                "Executing task 'exec_task_2'",
                                                'inside task 2',
                                                'Task return value: None',
                                                "Finished task 'exec_task_2'",
                                                'inside the flow!',
                                                'Flow return value: 42',
                                               f"Finished flow run '{flow_id}'"]


