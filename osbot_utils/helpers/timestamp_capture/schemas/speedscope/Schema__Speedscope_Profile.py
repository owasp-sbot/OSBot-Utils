"""
Schema for Speedscope Profile - profile in speedscope format
"""

from typing                                                                             import List
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Event  import Schema__Speedscope_Event


class Schema__Speedscope_Profile(Type_Safe):                                     # Profile in speedscope format
    type       : str   = 'evented'
    name       : str   = ''
    unit       : str   = 'microseconds'
    startValue : float = 0.0
    endValue   : float = 0.0
    events     : List[Schema__Speedscope_Event]