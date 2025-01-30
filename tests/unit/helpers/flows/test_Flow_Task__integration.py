import asyncio
from unittest                                              import TestCase
from osbot_utils.helpers.flows.Task                        import Task
from osbot_utils.helpers.flows.decorators.flow             import flow
from osbot_utils.helpers.flows.decorators.task             import task
from osbot_utils.helpers.flows.models.Flow_Run__Config     import Flow_Run__Config
from osbot_utils.context_managers.disable_root_loggers     import disable_root_loggers
from osbot_utils.helpers.flows.actions.Flow__Events        import flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type import Flow_Run__Event_Type


class test_Flow_Task_Integration(TestCase):

    def setUp(self):
        self.captured_events = []

        def event_listener(event):
            self.captured_events.append(event)

        self.event_listener = event_listener
        flow_events.event_listeners.append(self.event_listener)

    def tearDown(self):
        if self.event_listener in flow_events.event_listeners:
            flow_events.event_listeners.remove(self.event_listener)

    def test_flow_with_mixed_task_types(self):
        @task()
        def decorated_task(value):
            return value * 2

        with disable_root_loggers():
            @flow()
            def test_flow(initial_value):
                # Use decorated task
                value1 = decorated_task(initial_value)

                # Use raw Task
                with Task() as task:
                    task.task_target = lambda x: x + 2
                    task.task_args = (value1,)
                    value2 = task.execute__sync()

                return value2

            flow_instance = test_flow(20).execute()
            assert flow_instance.flow_return_value == 42

    def test_nested_flow_task_error_handling(self):
        @task(raise_on_error=False)
        def failing_task():
            raise ValueError("Task failed")

        @task()
        def successful_task():
            return "success"

        @flow(flow_config=Flow_Run__Config(raise_flow_error=False))
        def test_flow():
            failing_task()
            return successful_task()

        with disable_root_loggers():
            flow_instance = test_flow().execute()
            assert flow_instance.flow_return_value == "success"

            # Verify error was logged but didn't stop execution
            error_messages = [
                event for event in self.captured_events
                if event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE
                and "Task failed" in str(event.event_data.data)
            ]
            assert len(error_messages) > 0

    async def test_async_flow_with_mixed_tasks(self):
        @task()
        async def async_task(value):
            await asyncio.sleep(0.1)
            return value * 2

        @task()
        def sync_task(value):
            return value + 2

        @flow()
        async def test_flow(initial_value):
            value1 = await async_task(initial_value)
            value2 = sync_task(value1)
            return value2

        with disable_root_loggers():
            flow_instance = test_flow(20).execute()
            assert flow_instance.flow_return_value == 42

    def test_task_data_flow_interaction(self):
        @task()
        def task_one(task_data=None, flow_data=None):
            task_data['local'] = 'task_value'
            flow_data['shared'] = 'flow_value'
            return task_data['local']

        @task()
        def task_two(task_data=None, flow_data=None):
            return {
                'local': task_data.get('local'),
                'shared': flow_data.get('shared')
            }

        @flow()
        def test_flow():
            task_one()
            return task_two()

        with disable_root_loggers():
            flow_instance = test_flow().execute()
            result = flow_instance.flow_return_value

            # Task data should not persist between tasks
            assert result['local'] is None
            # Flow data should persist
            assert result['shared'] == 'flow_value'

    def test_task_execution_order_in_flow(self):
        execution_order = []

        @task()
        def task_one():
            execution_order.append('task_one')
            return 1

        @task()
        def task_two():
            execution_order.append('task_two')
            return 2

        @flow()
        def test_flow():
            task_two()
            task_one()
            return execution_order

        with disable_root_loggers():
            flow_instance = test_flow().execute()
            assert flow_instance.flow_return_value == ['task_two', 'task_one']

    def test_flow_task_event_correlation(self):
        @task()
        def correlated_task(this_task=None, this_flow=None):
            return f"{this_task.task_id}:{this_flow.flow_id}"

        @flow()
        def test_flow():
            return correlated_task()

        with disable_root_loggers():
            flow_instance = test_flow().execute()
            result = flow_instance.flow_return_value

            # Verify task events are properly correlated with flow
            flow_id = result.split(':')[1]
            task_events = [
                event for event in self.captured_events
                if event.event_type in {Flow_Run__Event_Type.TASK_START, Flow_Run__Event_Type.TASK_STOP}
                and event.event_data.flow_run_id == flow_id
            ]
            assert len(task_events) == 2  # Start and stop events