from typing                                                                        import Optional, Dict, List, Any
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now   import Timestamp_Now
from osbot_utils.helpers.flows.models.Flow_Run__Event                              import Flow_Run__Event
from osbot_utils.helpers.flows.models.Schema__Flow__Artifact                       import Schema__Flow__Artifact
from osbot_utils.helpers.flows.models.Schema__Flow__Result                         import Schema__Flow__Result
from osbot_utils.helpers.flows.schemas.Schema__Flow__Log                           import Schema__Flow__Log
from osbot_utils.helpers.flows.schemas.Schema__Flow__Task__Data                    import Schema__Flow__Task__Data
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
#from osbot_utils.helpers.flows.schemas.Schema__Flow__Event      import Schema__Flow__Event


class Schema__Flow__Data(Type_Safe):                        # Main container for flow execution data
    flow_id      : str
    flow_name    : str
    start_time   : Timestamp_Now
    end_time     : Optional[Timestamp_Now]
    status       : str                                      # 'completed', 'failed', 'running'
    error        : Optional[str]
    tasks        : Dict[str, Schema__Flow__Task__Data]      # task_id -> task_data
    #events       : List[Schema__Flow__Event]               # todo: this needs refactoring with the Flow_Run__Event events used below
    events       : List[Flow_Run__Event]
    results      : List[Schema__Flow__Result]
    artifacts    : List[Schema__Flow__Artifact]
    logs         : List[Schema__Flow__Log]
    return_value : Any