import time
from unittest                                                               import TestCase
from osbot_utils.helpers.duration.Duration                                  import Duration
from osbot_utils.helpers.flows.Task                                         import Task
from osbot_utils.helpers.flows.actions.Task__Stats__Collector               import Task__Stats__Collector
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status                 import Schema__Flow__Status
from osbot_utils.helpers.flows.schemas.Schema__Task__Stats                  import Schema__Task__Stats
from osbot_utils.utils.Misc                                                 import list_set
from osbot_utils.utils.Objects                                              import __
from osbot_utils.context_managers.disable_root_loggers                      import disable_root_loggers


class test_Task__Stats__Collector(TestCase):

    def setUp(self):
        self.task_stats_collector = Task__Stats__Collector()
        self.flow_id              = "test_flow_id"
        self.task_id              = "test_task_id"
        self.task_name            = "test_task"
        self.parent_flow_id       = "test_flow_id"

    def test__init__(self):
        with self.task_stats_collector as _:
            assert list_set(_.__locals__()) == ['duration', 'stats']
            assert type(_.duration)         is Duration
            assert _.duration.print_result  is True
            assert _.duration.use_utc       is True
            assert _.stats.obj()            == __(error_message   = None                      ,
                                                  task_id         = ''                        ,
                                                  task_name       = ''                        ,
                                                  execution_order = 0                         ,
                                                  duration        = __(utc              = True,
                                                                       timestamp_start  = 0.0 ,
                                                                       timestamp_end    = 0.0 ,
                                                                       duration_seconds = 0.0 ),
                                                  status          = None                      ,
                                                  parent_flow_id  = ''                        )

    def test_start(self):
        with self.task_stats_collector as _:
            execution_order = 42
            _.start(task_id=self.task_id, task_name=self.task_name, flow_id=self.parent_flow_id,execution_order=execution_order)

            with _.stats as stats:
                assert stats.task_id            == self.task_id
                assert stats.task_name          == self.task_name
                assert stats.parent_flow_id     == self.parent_flow_id
                assert stats.execution_order    == execution_order
                assert stats.status             == Schema__Flow__Status.RUNNING

            assert _.duration.start_time is not None            # Start timestamp should be set in duration
            assert _.duration.end_time   is None                # End not called yet

    def test_end(self):
        with self.task_stats_collector as _:
            _.start(task_id=self.task_id, task_name=self.task_name, flow_id=self.parent_flow_id, execution_order=1)
            time.sleep(0.0001)                                       # Ensure measurable duration
            _.end(task_error=None)                                   # Test basic end method (success case)

            with _.stats as stats:
                assert stats.status                    == Schema__Flow__Status.COMPLETED
                assert stats.error_message             is None
                assert stats.duration.duration_seconds >= 0.0001    # At least 0.0001 seconds

            assert _.duration.end_time is not None          # End timestamp should be set in duration

    def test_end_with_error(self):
        error_message = "Test error"
        task_error    = ValueError(error_message)

        with Task__Stats__Collector() as _:
            _.start(task_id='', task_name='', flow_id='', execution_order=1)    # Start first
            _.end(task_error=task_error)                                        # Test end method with error

            with _.stats as stats:
                assert stats.status        == Schema__Flow__Status.FAILED
                assert stats.error_message == error_message

    def test_full_lifecycle_with_real_task(self):
        with disable_root_loggers():

            task             = Task()                                           # Create a task that does something measurable
            task.task_id     = "task1_id"
            task.task_name   = "test_task_func"
            task.task_target = lambda : "result"

            collector = task.task_stats                                         # Access the task's stats collector
            task.execute__sync()

            assert task.task_return_value == "result"                           # Verify results
            with collector.stats as stats:
                assert stats.task_name                  == "test_task_func"
                assert stats.status                     == Schema__Flow__Status.COMPLETED
                assert stats.duration.duration_seconds  >= 0.0001
                assert stats.execution_order            == 1

    def test_json(self):
        with self.task_stats_collector as _:
            _.start(task_id=self.task_id, task_name=self.task_name, flow_id=self.parent_flow_id, execution_order=1)
            _.end(task_error=None)

            json_data = _.stats.json()                                          # Test json representation
            assert json_data == _.json()
            assert json_data == Schema__Task__Stats.from_json(json_data).json()  # confirm round trip
            assert json_data == { 'duration'        : json_data.get('duration'),
                                  'error_message'   : None                      ,
                                  'execution_order' : 1                         ,
                                  'parent_flow_id'  : self.parent_flow_id       ,
                                  'status'          : 'COMPLETED'               ,
                                  'task_id'         : self.task_id              ,
                                  'task_name'       : self.task_name            }