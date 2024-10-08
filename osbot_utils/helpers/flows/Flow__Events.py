from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.helpers.flows.models.Flow__Event       import Flow__Event
from osbot_utils.helpers.flows.models.Flow__Event_Type  import Flow__Event_Type


class Flow_Events(Type_Safe):
    event_listeners : list

    def on__flow__start(self, flow):
        flow_event = Flow__Event(event_type=Flow__Event_Type.FLOW_START, event_source=flow)
        self.raise_event(flow_event)

    def on__flow__stop(self, flow):                                                         # todo: see of flow_ended or flow_completed are better names
        flow_event = Flow__Event(event_type=Flow__Event_Type.FLOW_STOP , event_source=flow)
        self.raise_event(flow_event)

    def on__task__start(self, task):
        flow_event = Flow__Event(event_type=Flow__Event_Type.TASK_START, event_source=task)
        self.raise_event(flow_event)

    def on__task__stop(self, task):                                                         # todo: see of flow_ended or flow_completed are better names
        flow_event = Flow__Event(event_type=Flow__Event_Type.TASK_STOP , event_source=task)
        self.raise_event(flow_event)

    def raise_event(self, flow_event):
        for listener in self.event_listeners:
            try:
                listener(flow_event)
            except Exception as error:
                print(f"Error in listener: {error}")

flow_events = Flow_Events()
