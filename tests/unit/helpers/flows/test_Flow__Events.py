import logging
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
        self.event_data = Flow_Run__Event_Data( flow_name   = "test_flow"   ,
                                                flow_run_id = "test_run_id" ,
                                                task_name   = "test_task"   ,
                                                task_run_id = "test_task_id")
        self.received_events = []

    def test_event_listener_registration(self):
        def test_listener(event):
            self.received_events.append(event)

        self.flow_events.event_listeners.append(test_listener)
        assert test_listener in self.flow_events.event_listeners

        # Clean up
        self.flow_events.event_listeners.remove(test_listener)

    def test_flow_start_event(self):
        def start_listener(event: Flow_Run__Event):
            assert event.event_type == Flow_Run__Event_Type.FLOW_START
            assert event.event_data.flow_name == "test_flow"
            self.received_events.append(event)

        self.flow_events.event_listeners.append(start_listener)
        self.flow_events.on__flow__start(self.event_data)
        assert len(self.received_events) == 1

    def test_flow_stop_event(self):
        def stop_listener(event: Flow_Run__Event):
            assert event.event_type == Flow_Run__Event_Type.FLOW_STOP
            assert event.event_data.flow_run_id == "test_run_id"
            self.received_events.append(event)

        self.flow_events.event_listeners.append(stop_listener)
        self.flow_events.on__flow__stop(self.event_data)
        assert len(self.received_events) == 1

    def test_flow_message_event(self):
        def message_listener(event: Flow_Run__Event):
            assert event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE
            message_data = event.event_data.data['message_data']
            assert message_data['message'] == "test message"
            assert message_data['log_level'] == logging.INFO
            self.received_events.append(event)

        self.flow_events.event_listeners.append(message_listener)
        self.flow_events.on__flow_run__message(
            log_level=logging.INFO,
            message="test message",
            flow_run_id="test_run_id",
            task_run_id="test_task_id"
        )
        assert len(self.received_events) == 1

    def test_new_artifact_event(self):
        def artifact_listener(event: Flow_Run__Event):
            assert event.event_type == Flow_Run__Event_Type.NEW_ARTIFACT
            artifact_data = event.event_data.data['artifact_data']
            assert artifact_data['key'] == "test_artifact"
            self.received_events.append(event)

        self.event_data.data = {
            'artifact_data': {
                'key': 'test_artifact',
                'description': 'test description',
                'data': {'value': 42},
                'type': 'test_type'
            }
        }

        self.flow_events.event_listeners.append(artifact_listener)
        self.flow_events.on__new_artifact(self.event_data)
        assert len(self.received_events) == 1

    def test_new_result_event(self):
        def result_listener(event: Flow_Run__Event):
            assert event.event_type == Flow_Run__Event_Type.NEW_RESULT
            result_data = event.event_data.data['result_data']
            assert result_data['key'] == "test_result"
            self.received_events.append(event)

        self.event_data.data = {
            'result_data': {
                'key': 'test_result',
                'description': 'test description'
            }
        }

        self.flow_events.event_listeners.append(result_listener)
        self.flow_events.on__new_result(self.event_data)
        assert len(self.received_events) == 1

    def test_task_lifecycle_events(self):
        def lifecycle_listener(event: Flow_Run__Event):
            self.received_events.append(event.event_type)

        self.flow_events.event_listeners.append(lifecycle_listener)

        # Simulate task lifecycle
        self.flow_events.on__task__start(self.event_data)
        self.flow_events.on__task__stop(self.event_data)

        assert self.received_events == [
            Flow_Run__Event_Type.TASK_START,
            Flow_Run__Event_Type.TASK_STOP
        ]

    def test_multiple_listeners(self):
        count_1 = {'value': 0}
        count_2 = {'value': 0}

        def listener_1(event: Flow_Run__Event):
            count_1['value'] += 1

        def listener_2(event: Flow_Run__Event):
            count_2['value'] += 1

        self.flow_events.event_listeners.extend([listener_1, listener_2])
        self.flow_events.on__flow__start(self.event_data)

        assert count_1['value'] == 1
        assert count_2['value'] == 1

    def test_listener_error_handling(self):
        def failing_listener(event):
            raise Exception("Listener failed")

        def working_listener(event):
            self.received_events.append(event)

        self.flow_events.event_listeners.extend([failing_listener, working_listener])
        self.flow_events.on__flow__start(self.event_data)

        # The working listener should still receive the event
        assert len(self.received_events) == 1

    def test_global_flow_events_singleton(self):
        # Test that flow_events is a singleton
        assert isinstance(flow_events, Flow_Events)

        original_listeners = flow_events.event_listeners.copy()

        def test_listener(event):
            pass

        flow_events.event_listeners.append(test_listener)
        assert test_listener in flow_events.event_listeners

        # Clean up
        flow_events.event_listeners = original_listeners
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


