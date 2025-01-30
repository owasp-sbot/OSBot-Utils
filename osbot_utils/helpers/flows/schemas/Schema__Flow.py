from typing import List

from osbot_utils.helpers.flows.models.Flow_Run__Event     import Flow_Run__Event
from osbot_utils.helpers.flows.schemas.Schema__Flow__Data import Schema__Flow__Data
from osbot_utils.type_safe.Type_Safe                      import Type_Safe

class Schema__Flow(Type_Safe):                              # Root schema for flow execution data
    flow_data  : Schema__Flow__Data
    flow_events: List[Flow_Run__Event]                      # todo: refactor this Flow_Run__Event class with the respective Schema_* classes