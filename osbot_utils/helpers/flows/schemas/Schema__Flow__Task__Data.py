from typing                                                                       import Optional, Any
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now  import Timestamp_Now



class Schema__Flow__Task__Data(Type_Safe):                      # Represents the data associated with a task execution
    task_id          : str
    task_name        : str
    start_time       : Timestamp_Now
    end_time         : Optional[Timestamp_Now]
    status           : str                                      # 'completed', 'failed', 'running'
    error_message    : Optional[str]
    return_value     : Any
    input_args       : tuple
    input_kwargs     : dict