import time
from unittest                                                               import TestCase
from osbot_utils.helpers.duration.Duration                                  import Duration
from osbot_utils.helpers.flows.Task                                         import Task
from osbot_utils.helpers.flows.Flow                                         import Flow
from osbot_utils.helpers.flows.actions.Flow__Stats__Collector import Flow__Stats__Collector, \
    FLOW__ERROR_MESSAGE__TASK_FAILED
from osbot_utils.helpers.flows.schemas.Schema__Flow__Status                 import Schema__Flow__Status
from osbot_utils.helpers.flows.schemas.Schema__Task__Stats                  import Schema__Task__Stats
from osbot_utils.utils.Misc                                                 import list_set
from osbot_utils.testing.__                                                 import __
from osbot_utils.context_managers.disable_root_loggers                      import disable_root_loggers

class test_Flow__Stats__Collector(TestCase):

    def setUp(self):
        self.flow_stats_collector = Flow__Stats__Collector()
        self.flow_id              = "test_flow_id"
        self.flow_name            = "test_flow"

    def test__init__(self):
        with self.flow_stats_collector as _:
            assert list_set(_.__locals__()) == ['duration', 'stats', 'task_execution_counter']
            assert type(_.duration)          is Duration
            assert _.duration.print_result   is True
            assert _.duration.use_utc        is True
            assert _.task_execution_counter  == 0
            assert _.stats.tasks_stats       == {}
            assert _.stats.obj()             == __(error_message = None                      ,
                                                  flow_id       = ''                        ,
                                                  flow_name     = ''                        ,
                                                  total_tasks   = 0                         ,
                                                  failed_tasks  = 0                         ,
                                                  duration      = __(utc              = True,
                                                                     timestamp_start  = 0.0 ,
                                                                     timestamp_end    = 0.0 ,
                                                                     duration_seconds = 0.0 ),
                                                  status        = None                      ,
                                                  tasks_stats   = __()                      )

    def test_start(self):
        with self.flow_stats_collector as _:
            _.start(flow_id=self.flow_id, flow_name=self.flow_name)        # Test start method

            with _.stats as stats:
                assert stats.flow_id    == self.flow_id
                assert stats.flow_name  == self.flow_name
                assert stats.status     == Schema__Flow__Status.RUNNING

            assert _.duration.start_time    is not None                     # Start timestamp should be set in duration
            assert _.duration.end_time      is None                         # End not called yet

    def test_end(self):
        with self.flow_stats_collector as _:

            _.start   (flow_id=self.flow_id, flow_name=self.flow_name)                  # Start first to set up initial state
            time.sleep(0.0001)                                                          # Ensure measurable duration
            _.end     (flow_error=None)                                                 # Test basic end method (success case)

            with _.stats as stats:
                assert stats.status                     == Schema__Flow__Status.COMPLETED
                assert stats.error_message              is None
                assert stats.duration.duration_seconds  >= 0.0001                   # At least 0.0001 seconds
                assert stats.total_tasks                == 0
                assert stats.failed_tasks               == 0

            assert _.duration.end_time is not None                          # End timestamp should be set in duration

    def test_end_with_error(self):
        error_message = "Test flow error"
        flow_error    = ValueError(error_message)

        with Flow__Stats__Collector() as _:
            _.start(flow_id='', flow_name='')                               # Start
            _.end(flow_error=flow_error)                                    # Test end method with error

            with _.stats as stats:
                assert stats.status        == Schema__Flow__Status.FAILED
                assert stats.error_message == error_message

    def test_get_next_execution_order(self):
        with self.flow_stats_collector as _:
            assert _.task_execution_counter     == 0                        # Should start at 0 and increment
            assert _.get_next_execution_order() == 1
            assert _.get_next_execution_order() == 2
            assert _.get_next_execution_order() == 3
            assert _.task_execution_counter     == 3

    def test_add_task_stats(self):
        task_stats1 = Schema__Task__Stats(task_id         = "task1"                       ,     # Create a couple of task stats
                                          task_name       = "First Task"                  ,
                                          execution_order = 1                             ,
                                          duration        = None                          ,
                                          status          = Schema__Flow__Status.COMPLETED,
                                          parent_flow_id  = self.flow_id                  ,
                                          error_message   = None                          )

        task_stats2 = Schema__Task__Stats(task_id         = "task2"                       ,
                                          task_name       = "Second Task"                 ,
                                          execution_order = 2                             ,
                                          duration        = None                          ,
                                          status          = Schema__Flow__Status.FAILED   ,
                                          parent_flow_id  = self.flow_id                  ,
                                          error_message   ="Task failed"                  )

        with self.flow_stats_collector as _:
            _.add_task_stats(task_stats1)                   # Add task stats to collector
            _.add_task_stats(task_stats2)

            # Verify they were added correctly
            assert len(_.stats.tasks_stats)     == 2
            assert _.stats.tasks_stats["task1"] == task_stats1
            assert _.stats.tasks_stats["task2"] == task_stats2

            _.start(flow_id=self.flow_id, flow_name=self.flow_name)
            _.end  (flow_error=None)

            with _.stats as stats:
                assert stats.total_tasks  == 2
                assert stats.failed_tasks == 1

    def test_full_lifecycle_with_real_flow(self):
        with disable_root_loggers():
            flow_name = "full_lifecycle_flow"
            flow      = Flow(flow_name=flow_name)                                                    # Setup a flow

            def flow_function():
                with Task() as task1:
                    task1.task_id        = "task1_id"
                    task1.task_name      = "task1_name"
                    task1.task_target    = lambda: "task1 result"
                    task1.execute__sync()

                with Task() as task2:
                    task2.task_id        = "task2_id"
                    task2.task_name      = "task2_name"
                    task2.task_target    = lambda: 1/0  # Will raise error
                    task2.raise_on_error = False
                    task2.execute__sync()
                return "flow completed"

            flow.setup(flow_function)
            collector = flow.flow_stats
            flow.execute()                                  # Execute flow
            duration_flow   = collector.duration.data().obj()
            duration_task_1 = collector.stats.tasks_stats['task1_id'].duration.obj()
            duration_task_2 = collector.stats.tasks_stats['task2_id'].duration.obj()
            assert collector.stats.obj() == __(error_message = FLOW__ERROR_MESSAGE__TASK_FAILED ,
                                               duration      = duration_flow                    ,
                                               failed_tasks  = 1                                ,
                                               flow_id       = flow.flow_id                     ,
                                               flow_name     = flow_name                        ,
                                               status        = 'failed'                         ,
                                               tasks_stats=__(task1_id=__(error_message   = None            ,
                                                                          task_id         = 'task1_id'      ,
                                                                          task_name       = 'task1_name'    ,
                                                                          execution_order = 1               ,
                                                                          duration        = duration_task_1 ,
                                                                          status          = 'completed'     ,
                                                                          parent_flow_id  = flow.flow_id    ),
                                                              task2_id=__(error_message   = 'division by zero',
                                                                          task_id         = 'task2_id'        ,
                                                                          task_name       = 'task2_name'      ,
                                                                          execution_order = 2                 ,
                                                                          duration        = duration_task_2   ,
                                                                          status          = 'failed'          ,
                                                                          parent_flow_id  = flow.flow_id      )),
                                               total_tasks=2)
            assert flow.flow_stats.json() == flow.flow_stats.stats.json()


            assert flow.durations()                     == { 'flow_duration':  duration_flow.duration_seconds,
                                                             'flow_name'    : 'full_lifecycle_flow'                ,
                                                             'flow_status'  : 'failed'                             ,
                                                             'flow_tasks'   : { 'task1_name': duration_task_1.duration_seconds,
                                                                                'task2_name': duration_task_2.duration_seconds }}
            assert flow.durations__with_tasks_status()  == { 'flow_duration':  duration_flow.duration_seconds,
                                                             'flow_name'    : 'full_lifecycle_flow'                ,
                                                             'flow_status'  : 'failed'                             ,
                                                             'flow_tasks'   : { 1: { 'task_duration': duration_task_1.duration_seconds,
                                                                                     'task_name'    : 'task1_name' ,
                                                                                     'task_status'  : 'completed'  },
                                                                                2: { 'task_duration': duration_task_2.duration_seconds,
                                                                                     'task_name'    : 'task2_name' ,
                                                                                     'task_status'  : 'failed'     }}}
