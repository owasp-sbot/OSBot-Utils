from unittest import TestCase
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type import Flow_Run__Event_Type


class test_Flow_Run__Event_Type(TestCase):

    def test_event_types_exist(self):
        expected_types = {
            'FLOW_MESSAGE',
            'FLOW_START',
            'FLOW_STOP',
            'NEW_ARTIFACT',
            'NEW_RESULT',
            'TASK_START',
            'TASK_STOP'
        }

        actual_types = {member.name for member in Flow_Run__Event_Type}
        assert expected_types == actual_types

    def test_event_type_values(self):
        assert Flow_Run__Event_Type.FLOW_MESSAGE.value == 'flow_message'
        assert Flow_Run__Event_Type.FLOW_START.value == 'flow_start'
        assert Flow_Run__Event_Type.FLOW_STOP.value == 'flow_stop'
        assert Flow_Run__Event_Type.NEW_ARTIFACT.value == 'new_artifact'
        assert Flow_Run__Event_Type.NEW_RESULT.value == 'new_result'
        assert Flow_Run__Event_Type.TASK_START.value == 'task_start'
        assert Flow_Run__Event_Type.TASK_STOP.value == 'task_stop'

    def test_enum_immutability(self):
        with self.assertRaises(AttributeError):
            Flow_Run__Event_Type.FLOW_START = 'new_value'

    def test_enum_comparison(self):
        assert Flow_Run__Event_Type.FLOW_START == Flow_Run__Event_Type.FLOW_START
        assert Flow_Run__Event_Type.FLOW_START != Flow_Run__Event_Type.FLOW_STOP

        # Test that string values don't equal the enum
        assert Flow_Run__Event_Type.FLOW_START != 'flow_start'

    def test_enum_usage_in_switch(self):
        def get_event_category(event_type: Flow_Run__Event_Type) -> str:
            if event_type in {Flow_Run__Event_Type.FLOW_START,
                            Flow_Run__Event_Type.FLOW_STOP}:
                return "flow_lifecycle"
            elif event_type in {Flow_Run__Event_Type.TASK_START,
                              Flow_Run__Event_Type.TASK_STOP}:
                return "task_lifecycle"
            elif event_type == Flow_Run__Event_Type.FLOW_MESSAGE:
                return "message"
            else:
                return "other"

        assert get_event_category(Flow_Run__Event_Type.FLOW_START) == "flow_lifecycle"
        assert get_event_category(Flow_Run__Event_Type.TASK_START) == "task_lifecycle"
        assert get_event_category(Flow_Run__Event_Type.FLOW_MESSAGE) == "message"
        assert get_event_category(Flow_Run__Event_Type.NEW_ARTIFACT) == "other"

    def test_iteration_and_membership(self):
        # Test iteration over enum members
        event_types = list(Flow_Run__Event_Type)
        assert len(event_types) == 7

        # Test membership
        assert Flow_Run__Event_Type.FLOW_START in Flow_Run__Event_Type
        assert 'not_an_event' not in Flow_Run__Event_Type

    def test_name_and_value_attributes(self):
        event_type = Flow_Run__Event_Type.FLOW_START
        assert event_type.name == 'FLOW_START'
        assert event_type.value == 'flow_start'

        # Test that all enum members have string values
        for event_type in Flow_Run__Event_Type:
            assert isinstance(event_type.value, str)
            assert isinstance(event_type.name, str)

    def test_event_type_uniqueness(self):
        # Test that all values are unique
        values = [event_type.value for event_type in Flow_Run__Event_Type]
        assert len(values) == len(set(values))  # No duplicates

        # Test that all names are unique
        names = [event_type.name for event_type in Flow_Run__Event_Type]
        assert len(names) == len(set(names))  # No duplicates