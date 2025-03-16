from unittest                                           import TestCase
from osbot_utils.helpers.flows.Task                     import Task, TASK__RANDOM_ID__PREFIX
from osbot_utils.helpers.flows.Flow                     import Flow
from osbot_utils.context_managers.disable_root_loggers  import disable_root_loggers
from osbot_utils.helpers.flows.models.Flow_Run__Config  import Flow_Run__Config
from osbot_utils.testing.Stderr                         import Stderr
from osbot_utils.utils.Dev import pprint


class test_Task(TestCase):

    def setUp(self):
        self.task = Task()
        self.flow = Flow()
        self.flow.flow_config = Flow_Run__Config()
        self.flow.setup(lambda: None)                           # Setup with dummy function

    def test_task_initialization(self):
        assert self.task.task_error         is None
        assert self.task.raise_on_error     is True
        assert self.task.task_return_value  is None

    def test_random_task_id(self):
        task_id = self.task.random_task_id()
        assert isinstance(task_id, str)
        assert task_id.startswith(TASK__RANDOM_ID__PREFIX)

    def test_find_flow(self):
        an_flow = Flow()

        def parent_flow(self):
            def task_function():
                with Task() as task:
                    return task.find_flow()


            found_flow = task_function()
            assert found_flow       == an_flow
            assert type(found_flow) is Flow

        parent_flow(an_flow)

    def test_execute_sync(self):
        def task_target():
            return "task completed"

        with disable_root_loggers():
            def execute_flow(self):
                with Task() as task:
                    task.task_target = task_target
                    result = task.execute__sync()
                    assert result == "task completed"
                    assert task.task_error is None

            execute_flow(self.flow)

    def test_execute_sync_with_error(self):
        def task_target():
            raise ValueError("Task error")

        with disable_root_loggers():
            def execute_flow(self):
                with Task() as task:
                    task.task_target    = task_target
                    task.raise_on_error = False                         # Don't raise to test error handling
                    with Stderr() as stderr:
                        result              = task.execute__sync()
                    assert stderr.value()       == "\x1b[31mError executing 'task_target' task: Task error\x1b[0m\n"
                    assert result                is None
                    assert type(task.task_error) is ValueError
                    assert str (task.task_error) == "Task error"

            execute_flow(self.flow)

    def test_task_logging(self):
        with disable_root_loggers():
            with self.flow as flow:
                flow.logger.add_memory_logger()
                with Task() as task:
                    task.task_name = "test_task"
                    task.log_info ("Info message")
                    task.log_debug("Debug message")
                    task.log_error("Error message")
                logs = flow.log_messages()
                assert logs == ['Info message', 'Debug message', 'Error message']

    # todo: fix this test since this doesn't work like this in the normal (sync TestCase)
    async def test_execute_async(self):
        async def async_task_target():
            return "async task completed"

        with disable_root_loggers():
            with self.flow as flow:
                with Task() as task:
                    task.task_target = async_task_target
                    result = await task.execute__async()
                    assert result == "async task completed"
                    assert task.task_error is None

    def test_find_flow_contexts(self):                                                                                  # Test that find_flow works in different contexts

        def test_task():
            with Task() as task:
                return task.find_flow()

        with disable_root_loggers():                        # Test with context manager
            with self.flow as flow:
                flow.setup(lambda: None)
                found_flow = test_task()
                assert found_flow is flow

            self.flow.setup(lambda: None)                   # Test with direct variable
            flow_var = self.flow
            found_flow = test_task()
            assert found_flow is flow_var

            def method_with_flow(flow_instance):            # Test with method context
                found_flow = test_task()
                assert found_flow is flow_instance

            method_with_flow(self.flow)