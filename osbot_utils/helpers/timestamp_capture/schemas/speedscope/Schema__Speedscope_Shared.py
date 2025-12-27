"""
Schema for Speedscope Shared - shared data in speedscope format
"""

from typing                                                                             import List
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Frame  import Schema__Speedscope_Frame


class Schema__Speedscope_Shared(Type_Safe):                                      # Shared data in speedscope format
    frames : List[Schema__Speedscope_Frame]