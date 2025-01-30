from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now

class Schema__Flow__Result(Type_Safe):                      # Represents a result produced by the flow
    key         : str
    description : str
    timestamp   : Timestamp_Now