from osbot_utils.utils.Str import ansis_to_texts, ansi_to_text

from osbot_utils.utils.Dev import pprint

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

    def on__flow_run__message(self, flow, log_level, flow_run_id, task_run_id, message):
        event_data = dict(flow_run_id  = flow_run_id           ,
                          log_level    = log_level             ,
                          message      = message               ,
                          message_text = ansi_to_text(message) ,
                          task_run_id = task_run_id            )
        flow_event = Flow__Event(event_type=Flow__Event_Type.FLOW_MESSAGE, event_source=flow, event_data=event_data)
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
