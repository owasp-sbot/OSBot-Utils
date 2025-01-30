from typing                             import Any
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Schema__Flow__Artifact(Type_Safe):       # Represents an artifact produced during flow execution
    key         : str
    description : str
    data        : Any
    type        : str
    timestamp   : Timestamp_Now