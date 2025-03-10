from typing                             import Optional
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__Flow__Log(Type_Safe):                         # Represents a log entry from the flow execution
    timestamp   : Timestamp_Now
    level       : int
    message     : str
    task_id     : Optional[str]