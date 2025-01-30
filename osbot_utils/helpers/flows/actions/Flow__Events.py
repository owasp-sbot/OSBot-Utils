from osbot_utils.helpers.flows.models.Flow_Run__Event_Data import Flow_Run__Event_Data
from osbot_utils.utils.Str                                  import ansi_to_text
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.helpers.flows.models.Flow_Run__Event       import Flow_Run__Event
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type  import Flow_Run__Event_Type


class Flow_Events(Type_Safe):
    event_listeners : list

    def on__flow__start(self, event_data: Flow_Run__Event_Data):
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.FLOW_START, event_data=event_data)
        self.raise_event(flow_event)

    def on__flow__stop(self, event_data: Flow_Run__Event_Data):                                                         # todo: see of flow_ended or flow_completed are better names
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.FLOW_STOP , event_data=event_data)
        self.raise_event(flow_event)

    def on__flow_run__message(self, log_level, flow_run_id, task_run_id, message):
        event_data = Flow_Run__Event_Data()
        event_data.flow_run_id = flow_run_id
        event_data.task_run_id = task_run_id
        event_data.data = dict(message_data = dict(log_level    = log_level             ,
                                                   message      = message               ,
                                                   message_text = ansi_to_text(message) ))
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.FLOW_MESSAGE, event_data=event_data)
        self.raise_event(flow_event)

    def on__new_artifact(self, event_data: Flow_Run__Event_Data):
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.NEW_ARTIFACT, event_data=event_data)
        self.raise_event(flow_event)

    def on__new_result(self, event_data: Flow_Run__Event_Data):
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.NEW_RESULT, event_data=event_data)
        self.raise_event(flow_event)

    def on__task__start(self, event_data: Flow_Run__Event_Data):
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.TASK_START, event_data=event_data)
        self.raise_event(flow_event)

    def on__task__stop(self, event_data: Flow_Run__Event_Data):                                                         # todo: see of flow_ended or flow_completed are better names
        flow_event = Flow_Run__Event(event_type=Flow_Run__Event_Type.TASK_STOP , event_data=event_data)
        self.raise_event(flow_event)

    def raise_event(self, flow_event):
        for listener in self.event_listeners:
            try:
                listener(flow_event)
            except Exception as error:
                print(f"Error in listener: {error}")

flow_events = Flow_Events()
