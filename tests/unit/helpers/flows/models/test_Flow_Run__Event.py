from unittest                                               import TestCase
from osbot_utils.helpers.flows.models.Flow_Run__Event       import Flow_Run__Event
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type  import Flow_Run__Event_Type
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data  import Flow_Run__Event_Data
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now
from osbot_utils.utils.Misc                                 import is_guid, is_int


class test_Flow_Run__Event(TestCase):

    def setUp(self):
        self.event_data = Flow_Run__Event_Data()
        self.event      = Flow_Run__Event(event_type = Flow_Run__Event_Type.FLOW_START,
                                          event_data = self.event_data                )

    def test_initialization(self):
        assert isinstance(self.event.event_id , Random_Guid  )
        assert isinstance(self.event.timestamp, Timestamp_Now)
        assert self.event.event_type == Flow_Run__Event_Type.FLOW_START
        assert self.event.event_data == self.event_data

    def test_event_types(self):
        for event_type in Flow_Run__Event_Type:                                 # Test with each event type
            event = Flow_Run__Event( event_type = event_type     ,
                                     event_data = self.event_data)
            assert event.event_type == event_type

    def test_event_data_modification(self):
        self.event_data.flow_name = "test_flow"
        self.event_data.task_name = "test_task"

        event = Flow_Run__Event( event_type = Flow_Run__Event_Type.TASK_START,
                                 event_data = self.event_data                )

        assert event.event_data.flow_name == "test_flow"
        assert event.event_data.task_name == "test_task"

    def test_json_serialization(self):
        event_json = self.event.json()
        event_id   = event_json.get('event_id')
        timestamp  = event_json.get('timestamp')
        assert is_guid(event_id ) is True
        assert is_int (timestamp) is True
        assert event_json         == { 'event_data': { 'data'           : {}    ,
                                                       'event_source'   : ''    ,
                                                       'flow_name'      : None  ,
                                                       'flow_run_id'    : None  ,
                                                       'log_level'      : 20    ,
                                                       'task_name'      : None  ,
                                                       'task_run_id'    : None  },
                                       'event_id'  : event_id                    ,
                                       'event_type': 'FLOW_START'                ,
                                       'timestamp' : timestamp                   }