from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Duration(Type_Safe):
    utc             : bool = True
    timestamp_start : float
    timestamp_end   : float
    duration_seconds: float
