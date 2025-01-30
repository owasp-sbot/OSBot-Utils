import asyncio

import pytest

from osbot_utils.helpers.flows.models.Flow_Run__Config      import Flow_Run__Config
from osbot_utils.helpers.flows.Flow__Events                 import flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type  import Flow_Run__Event_Type
from unittest                                               import TestCase
from osbot_utils.context_managers.disable_root_loggers      import disable_root_loggers
from osbot_utils.helpers.flows.Flow                         import Flow
from osbot_utils.helpers.flows.Task                         import Task
from osbot_utils.utils.Str                                  import ansis_to_texts

class test_Flow(TestCase):

    def setUp(self):
        self.flow = Flow()
        self.captured_events = []

        # Setup event listener for testing
        def event_listener(event):
            self.captured_events.append(event)

        self.event_listener = event_listener
        flow_events.event_listeners.append(self.event_listener)

    def tearDown(self):
        if self.event_listener in flow_events.event_listeners:
            flow_events.event_listeners.remove(self.event_listener)

    def test_flow_lifecycle_events(self):
        def simple_function():
            return 42

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(simple_function)
                flow.execute()

        event_types = [event.event_type for event in self.captured_events]          # Verify event sequence
        assert event_types == [ Flow_Run__Event_Type.FLOW_START ,
                                Flow_Run__Event_Type.FLOW_MESSAGE,                  # Execution start message
                                Flow_Run__Event_Type.FLOW_MESSAGE,                  # Return value message
                                Flow_Run__Event_Type.FLOW_MESSAGE,
                                Flow_Run__Event_Type.NEW_RESULT ,
                                Flow_Run__Event_Type.FLOW_STOP  ]

    def test_flow_with_nested_tasks(self):
        def task_function(task_data=None):
            task_data['executed'] = True
            return 'task completed'

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(lambda: None)

                with Task() as task:
                    task.task_target = task_function
                    task.execute__sync()

        task_events = [
            event for event in self.captured_events
            if event.event_type in {Flow_Run__Event_Type.TASK_START, Flow_Run__Event_Type.TASK_STOP}
        ]
        assert len(task_events) == 2
        assert task_events[0].event_type == Flow_Run__Event_Type.TASK_START
        assert task_events[1].event_type == Flow_Run__Event_Type.TASK_STOP

    async def test_async_flow_execution(self):
        async def async_function():
            await asyncio.sleep(0.1)
            return 'async completed'

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(async_function)
                result = flow.execute()
                assert result.flow_return_value == 'async completed'

        assert any(
            event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE and
            'async completed' in str(event.event_data.data)
            for event in self.captured_events
        )

    def test_flow_error_handling_with_config(self):
        def failing_function():
            raise ValueError("Test error")

        # Test with raise_flow_error = True
        config = Flow_Run__Config(raise_flow_error=True)
        with disable_root_loggers():
            with self.flow as flow:
                flow.flow_config = config
                flow.setup(failing_function)
                with self.assertRaises(ValueError):
                    flow.execute()

        # Test with raise_flow_error = False
        config = Flow_Run__Config(raise_flow_error=False)
        with disable_root_loggers():
            with Flow() as flow:
                flow.flow_config = config
                flow.setup(failing_function)
                result = flow.execute()
                assert isinstance(result.flow_error, ValueError)

    def test_flow_artifacts_and_results(self):
        def function_with_artifacts(this_flow=None):
            this_flow.add_flow_artifact(
                description="Test artifact",
                key="test-key",
                data={"value": 42},
                artifact_type="test"
            )
            this_flow.add_flow_result("result-key", "Test result")
            return "completed"

        with disable_root_loggers():
            with self.flow as flow:
                flow.setup(function_with_artifacts)
                flow.execute()

        artifact_events = [event for event in self.captured_events
                            if event.event_type == Flow_Run__Event_Type.NEW_ARTIFACT ]
        result_events   = [event for event in self.captured_events
                            if event.event_type == Flow_Run__Event_Type.NEW_RESULT
        ]

        assert len(artifact_events) == 1
        assert len(result_events  ) == 2

        # Verify artifact data
        artifact_data = artifact_events[0].event_data.data['artifact_data']
        assert artifact_data['key'] == 'test-key'
        assert artifact_data['data']['value'] == 42

        # Verify result data
        result_data = result_events[0].event_data.data['result_data']
        assert result_data['key'] == 'result-key'
        assert result_data['description'] == 'Test result'

    @pytest.mark.skip("test needs fixing")
    def test_flow_logging_configuration(self):
        configs = [
            (Flow_Run__Config(log_to_console=True, log_to_memory=False), 'console'),
            (Flow_Run__Config(log_to_console=False, log_to_memory=True), 'memory'),
            (Flow_Run__Config(logging_enabled=False), 'disabled')
        ]

        for config, mode in configs:
            with disable_root_loggers():
                with Flow() as flow:
                    flow.flow_config = config
                    flow.setup(lambda: "test")
                    flow.execute()

            if mode == 'disabled':
                assert not any(event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE
                                for event in self.captured_events )
            else:
                assert any(
                    event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE
                    for event in self.captured_events
                )
    def test_random_flow_id(self):
        with self.flow as _:
            assert _.flow_id == self.flow.flow_id

    def test_execute_flow(self):

        def just_print_a_message():
            print('this is inside the flow')
            return 'some return value'

        with disable_root_loggers():
            with self.flow as _:
                _.flow_id = 'AN-FLOW-ID'
                _.setup(just_print_a_message)
                #_.set_flow_target(lambda : print('this is a lambda function'))
                _.flow_config.print_none_return_value = True
                _.flow_config.print_finished_message  = True
                _.execute_flow()
                assert ansis_to_texts(_.captured_exec_logs) == ["Executing flow run 'AN-FLOW-ID'",
                                                                'this is inside the flow',
                                                                'Flow return value: some return value',
                                                                "Finished flow run 'AN-FLOW-ID'"]

    def test_execute_flow_with_error_handling(self):
        def flow_with_error():
            with Task() as task:
                task.task_name = 'task__load_current_feed'
                raise Exception("Failed to load current data feed")

        with disable_root_loggers():
            with self.flow as _:
                _.flow_id = 'AN-FLOW-ID'
                _.setup(flow_with_error)
                _.flow_config.print_none_return_value = True
                _.flow_config.print_finished_message = True

                # Test when raise_flow_error is True (default)
                with self.assertRaises(Exception) as context:
                    _.execute_flow()
                assert str(context.exception) == "Failed to load current data feed"

                # Test when raise_flow_error is False
                _.flow_config.raise_flow_error = False
                flow_result = _.execute_flow()
                assert isinstance(flow_result, Flow)
                assert isinstance(flow_result.flow_error, Exception)
                assert str(flow_result.flow_error) == "Failed to load current data feed"



