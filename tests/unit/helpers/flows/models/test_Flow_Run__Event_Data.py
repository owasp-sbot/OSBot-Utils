import logging
from unittest                                               import TestCase
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data  import Flow_Run__Event_Data
from osbot_utils.utils.Objects                              import __


class test_Flow_Run__Event_Data(TestCase):

    def setUp(self):
        self.event_data = Flow_Run__Event_Data()

    def test_initialization(self):
        assert self.event_data.flow_name    is None
        assert self.event_data.flow_run_id  is None
        assert self.event_data.task_name    is None
        assert self.event_data.task_run_id  is None
        assert self.event_data.log_level    == logging.INFO

    def test_data_assignment(self):
        test_data             = {"key": "value"}
        self.event_data.data  = test_data
        assert self.event_data.data == test_data

    def test_field_assignment(self):
        self.event_data.flow_name   = "test_flow"
        self.event_data.flow_run_id = "flow_123"
        self.event_data.task_name   = "test_task"
        self.event_data.task_run_id = "task_123"
        self.event_data.log_level   = logging.DEBUG

        assert self.event_data.flow_name    == "test_flow"
        assert self.event_data.flow_run_id  == "flow_123"
        assert self.event_data.task_name    == "test_task"
        assert self.event_data.task_run_id  == "task_123"
        assert self.event_data.log_level    == logging.DEBUG

    def test_constructor_with_kwargs(self):
        kwargs = {  "flow_name"  : "flow1"              ,
                    "flow_run_id": "run1"               ,
                    "task_name"  : "task1"              ,
                    "task_run_id": "task_run1"          ,
                    "log_level"  : logging.ERROR        ,
                    "data"       : {"status": "complete"}}
        event_data = Flow_Run__Event_Data(**kwargs)

        assert event_data.obj() == __( flow_name    = 'flow1'             ,
                                       flow_run_id  = 'run1'              ,
                                       log_level    = 40                  ,
                                       task_name    = 'task1'             ,
                                       task_run_id  = 'task_run1'         ,
                                       data         = __(status='complete'),
                                       event_source = ''                  )