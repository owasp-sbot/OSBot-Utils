import asyncio
from unittest                                               import TestCase
from osbot_utils.helpers.flows.decorators.task              import task
from osbot_utils.helpers.flows.Flow                         import Flow
from osbot_utils.context_managers.disable_root_loggers      import disable_root_loggers
from osbot_utils.helpers.flows.models.Flow_Run__Config      import Flow_Run__Config
from osbot_utils.helpers.flows.Flow__Events                 import flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type  import Flow_Run__Event_Type



class test_decorator__task(TestCase):

    def setUp(self):
        self.flow = Flow()
        self.flow.flow_config = Flow_Run__Config()
        self.captured_events = []

        def event_listener(event):
            self.captured_events.append(event)

        self.event_listener = event_listener
        flow_events.event_listeners.append(self.event_listener)

    def tearDown(self):
        if self.event_listener in flow_events.event_listeners:
            flow_events.event_listeners.remove(self.event_listener)

    def test_task_dependency_injection(self):
        @task()
        def task_with_deps(this_task=None, this_flow=None, task_data=None, flow_data=None):
            assert this_task is not None
            assert this_flow is not None
            assert isinstance(task_data, dict)
            assert isinstance(flow_data, dict)
            return "success"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = task_with_deps()
                assert result == "success"

    def test_task_error_handling_modes(self):
        @task(raise_on_error=True)
        def failing_task_raises():
            raise ValueError("Task error")

        @task(raise_on_error=False)
        def failing_task_continues():
            raise ValueError("Task error")

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)

                # Test raising error
                with self.assertRaises(Exception):
                    failing_task_raises()

                # Test continuing after error
                result = failing_task_continues()
                assert result is None

    async def test_async_task_execution(self):
        async def async_operation():
            await asyncio.sleep(0.1)
            return 42

        @task()
        async def async_task():
            result = await async_operation()
            return result

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = await async_task()
                assert result == 42

    def test_task_event_sequence(self):
        @task()
        def monitored_task():
            return "completed"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                monitored_task()

        task_events = [
            event for event in self.captured_events
            if event.event_type in {
                Flow_Run__Event_Type.TASK_START,
                Flow_Run__Event_Type.TASK_STOP,
                Flow_Run__Event_Type.FLOW_MESSAGE
            }
        ]

        # Verify event sequence
        assert len(task_events) >= 3  # Start, Stop, and at least one message
        assert task_events[0].event_type == Flow_Run__Event_Type.TASK_START
        assert task_events[-1].event_type == Flow_Run__Event_Type.TASK_STOP

    def test_task_data_sharing(self):
        @task()
        def first_task(task_data=None):
            print(task_data)
            task_data['key'] = 'value 1'
            return task_data['key']

        @task()
        def second_task(task_data=None):
            task_data['key'] = 'value 2'
            return task_data.get('key')

        with disable_root_loggers():
            with self.flow as flow:
                result1 = first_task()
                result2 = second_task()

                assert result1 == 'value 1'
                assert result2 == 'value 2'

    def test_task_with_args_and_kwargs(self):
        @task()
        def parameterized_task(x, y, z=None):
            return x + y + (z or 0)

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)

                # Test positional args
                result1 = parameterized_task(1, 2)
                assert result1 == 3

                # Test with kwargs
                result2 = parameterized_task(x=1, y=2, z=3)
                assert result2 == 6

    def test_task_stdout_capture(self):
        @task()
        def task_with_print():
            print("This should be captured")
            return "done"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                task_with_print()

        # Verify stdout was captured in flow messages
        stdout_messages = [
            event for event in self.captured_events
            if event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE
            and "This should be captured" in str(event.event_data.data)
        ]
        assert len(stdout_messages) > 0

    def test_nested_tasks(self):
        @task()
        def inner_task():
            return 42

        @task()
        def outer_task():
            return inner_task() + 1

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = outer_task()
                assert result == 43

                # Verify both tasks were executed
                task_starts = len([
                    event for event in self.captured_events
                    if event.event_type == Flow_Run__Event_Type.TASK_START
                ])
                assert task_starts == 2

    def test_task_name_handling(self):
        @task(task_name="custom_name")
        def task_with_custom_name():
            return "done"

        @task()
        def task_with_default_name():
            return "done"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                task_with_custom_name()
                task_with_default_name()

        task_starts = [
            event.event_data.task_name
            for event in self.captured_events
            if event.event_type == Flow_Run__Event_Type.TASK_START
        ]

        assert "custom_name" in task_starts
        assert "task_with_default_name" in task_starts

    def test_task_id_uniqueness(self):
        @task()
        def repeated_task():
            return "done"

        task_ids = set()
        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                for _ in range(3):
                    repeated_task()
                    task_id = self.captured_events[-1].event_data.task_run_id
                    task_ids.add(task_id)

        # Verify all task IDs were unique
        assert len(task_ids) == 3

    def test_sync_task_decorator(self):
        @task()
        def sync_task(value):
            return value * 2

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = sync_task(21)
                assert result == 42

    def test_sync_task_with_error(self):
        @task(raise_on_error=False)
        def failing_task():
            raise ValueError("Task failed")

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = failing_task()
                assert result is None

    async def test_async_task_decorator(self):
        @task()
        async def async_task(value):
            await asyncio.sleep(0.1)
            return value * 2

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = await async_task(21)
                assert result == 42

    def test_task_with_flow_context(self):
        @task()
        def task_with_flow(this_flow=None):
            assert isinstance(this_flow, Flow)
            return "success"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = task_with_flow()
                assert result == "success"

    def test_task_with_custom_name(self):
        @task(task_name="custom_task")
        def some_task():
            return "done"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)
                result = some_task()
                assert result == "done"
                # Verify the task name in flow's executed tasks
                assert any(task.task_name == "custom_task"
                         for task in flow.executed_tasks)