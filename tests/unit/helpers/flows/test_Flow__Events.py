from unittest                                   import TestCase
from osbot_utils.helpers.flows.Flow             import Flow
from osbot_utils.helpers.flows.decorators.flow  import flow
from osbot_utils.helpers.flows.Flow__Events     import Flow__Event_Type, Flow_Events, flow_events


class test_Flow__Events(TestCase):

    def setUp(self):
        self.flow_events = Flow_Events()

    def test_on__flow__start(self):
        def event_listener(flow_event):
            assert flow_event.event_type == Flow__Event_Type.FLOW_START
            assert flow_event.event_source == 'flow'
            assert flow_event.event_data == {}
        self.flow_events.event_listeners.append(event_listener)
        self.flow_events.on__flow__start('flow')

    def test_global_flow_events(self):
        def event_listener(flow_event):
            assert flow_event.event_type         == Flow__Event_Type.FLOW_START
            assert flow_event.event_type         == Flow__Event_Type.FLOW_START
            assert type(flow_event.event_source) is Flow

        @flow()
        def an_flow() -> Flow:
            print('inside the flow')

        flow_events.event_listeners.append(event_listener)
        assert event_listener in flow_events.event_listeners

        an_flow().execute_flow()

        flow_events.event_listeners.remove(event_listener)
        assert event_listener not in flow_events.event_listeners


