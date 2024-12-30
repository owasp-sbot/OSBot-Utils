from unittest                                               import TestCase
from osbot_utils.helpers.flows.models.Flow_Run__Config      import Flow_Run__Config
from osbot_utils.helpers.flows.Flow                         import Flow
from osbot_utils.helpers.flows.decorators.flow              import flow
from osbot_utils.helpers.flows.Flow__Events                 import Flow_Run__Event_Type, Flow_Events, flow_events
from osbot_utils.helpers.flows.models.Flow_Run__Event       import Flow_Run__Event
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data  import Flow_Run__Event_Data


class test_Flow__Events(TestCase):

    def setUp(self):
        self.flow_events = Flow_Events()

    def test_on__flow__start(self):
        def event_listener(event: Flow_Run__Event()):
            event_data = event.event_data.json()
            assert event_data.event_type == Flow_Run__Event_Type.FLOW_START
            assert event_data == { 'data': {'a': 'b'},
                                   'event_source': '',
                                   'flow_id': None,
                                   'flow_name': None,
                                   'flow_run_id': None,
                                   'log_level': 20,
                                   'task_name': None,
                                   'task_run_id': None}

        self.flow_events.event_listeners.append(event_listener)

        self.flow_events.on__flow__start(Flow_Run__Event_Data(data={'a':'b'}))

    def test_global_flow_events(self):
        def event_listener(event: Flow_Run__Event()):
            assert type(event) is Flow_Run__Event

        @flow(flow_config=Flow_Run__Config(logging_enabled = False))
        def an_flow() -> Flow:
            print('inside the flow')

        flow_events.event_listeners.append(event_listener)
        assert event_listener in flow_events.event_listeners

        an_flow().execute_flow()

        flow_events.event_listeners.remove(event_listener)
        assert event_listener not in flow_events.event_listeners


