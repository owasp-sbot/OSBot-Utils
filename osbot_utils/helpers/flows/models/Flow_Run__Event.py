from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now
from osbot_utils.helpers.flows.models.Flow_Run__Event_Data  import Flow_Run__Event_Data
from osbot_utils.helpers.flows.models.Flow_Run__Event_Type  import Flow_Run__Event_Type

class Flow_Run__Event(Type_Safe):
    event_id    : Random_Guid
    event_type  : Flow_Run__Event_Type
    event_data  : Flow_Run__Event_Data
    timestamp   : Timestamp_Now

