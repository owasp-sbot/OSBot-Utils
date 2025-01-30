import asyncio
from osbot_utils.testing.Stdout                         import Stdout
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.helpers.flows.Task                     import Task
from unittest                                           import TestCase
from osbot_utils.helpers.flows.decorators.flow          import flow
from osbot_utils.helpers.flows.decorators.task          import task
from osbot_utils.helpers.flows.Flow                     import Flow
from osbot_utils.helpers.flows.models.Flow_Run__Config  import Flow_Run__Config
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers


class test_decorator__flow(TestCase):

    def setUp(self):
        self.flow_config = Flow_Run__Config(
            print_logs=False,
            print_finished_message=True
        )

    def test_basic_flow_decorator(self):
        @flow()
        def simple_flow():
            return 42

        with disable_root_loggers():
            flow_instance = simple_flow().execute()
            assert isinstance(flow_instance, Flow)
            assert flow_instance.flow_return_value == 42

    def test_flow_with_args(self):
        @flow(flow_config=self.flow_config)
        def parameterized_flow(x, y):
            return x + y

        with disable_root_loggers():
            flow_instance = parameterized_flow(20, 22).execute()
            assert flow_instance.flow_return_value == 42

    def test_flow_with_custom_config(self):
        custom_config = Flow_Run__Config(print_logs             = True ,
                                         print_finished_message = True ,
                                         raise_flow_error       = False)

        @flow(flow_config=custom_config)
        def configured_flow():
            raise ValueError("Test error")

        with disable_root_loggers():
            with Stdout() as stdout:
                flow_instance = configured_flow().execute()
                assert isinstance(flow_instance.flow_error, ValueError)
                assert str(flow_instance.flow_error) == "Test error"
            assert stdout.value() == ( '\n'
                                       '\n'
                                       '\n'
                                       '\n'
                                      f"Executing flow run '\x1b[1m\x1b[32m{flow_instance.flow_id}\x1b[0m\x1b[0m'\n"
                                       '\x1b[1m\x1b[31mError executing flow: Test error\x1b[0m\x1b[0m\n'      )


    async def test_async_flow_decorator(self):
        @flow(flow_config=self.flow_config)
        async def async_flow():
            await asyncio.sleep(0.1)
            return 42

        with disable_root_loggers():
            flow_instance = async_flow().execute()
            assert flow_instance.flow_return_value == 42

    def test_flow_print(self):
        @task()
        def task_one(value):
            return value + 22

        @flow(flow_config=self.flow_config)
        def flow_1(initial_value):
            print('in task_1')
            return_value = task_one(initial_value)
            return return_value

        with disable_root_loggers():
            flow_instance = flow_1(20).execute()
            assert flow_instance.flow_return_value == 42
            assert len(flow_instance.executed_tasks) == 1
        assert flow_instance.obj().flow_data.logs.__sizeof__() == 104
    def test_flow_with_nested_tasks(self):
        @task()
        def task_one(value):
            return value * 2

        @task()
        def task_two(value):
            return value + 2

        @flow(flow_config=self.flow_config)
        def nested_flow(initial_value):
            value = task_one(initial_value)
            return task_two(value)

        with disable_root_loggers():
            flow_instance = nested_flow(20).execute()
            assert flow_instance.flow_return_value == 42
            assert len(flow_instance.executed_tasks) == 2
        #from osbot_utils.utils.Dev import pprint
        #pprint(flow_instance.json())

    def test_flow_with_error_propagation(self):
        error_config = Flow_Run__Config(raise_flow_error=True)

        @flow(flow_config=error_config)
        def failing_flow():
            raise ValueError("Flow failed")

        with disable_root_loggers():
            with self.assertRaises(ValueError) as context:
                failing_flow().execute()
            assert str(context.exception) == "Flow failed"

    def test_flow_with_custom_id(self):
        @flow(flow_config=self.flow_config)
        def custom_id_flow():
            return "success"

        with disable_root_loggers():
            flow_instance = custom_id_flow()
            flow_instance.flow_id = "custom-flow-id"
            result = flow_instance.execute()
            assert result.flow_id == "custom-flow-id"

    def test_flow_data_sharing(self):
        @task()
        def share_data(flow_data=None):
            flow_data['key'] = 'value'
            return flow_data

        @flow(flow_config=self.flow_config)
        def data_flow():
            return share_data()

        with disable_root_loggers():
            flow_instance = data_flow().execute()
            assert flow_instance.data.get('key') == 'value'


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


