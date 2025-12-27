"""
Schema for Export Summary - compact summary export
"""

from typing                                                                      import List
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.helpers.timestamp_capture.schemas.export.Schema__Export_Hotspot import Schema__Export_Hotspot


class Schema__Export_Summary(Type_Safe):                                         # Compact summary export
    name              : str   = ''
    total_duration_ms : float = 0.0
    method_count      : int   = 0
    entry_count       : int   = 0
    hotspots          : List[Schema__Export_Hotspot]
