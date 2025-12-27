"""
Schema for Export Metadata - summary info about the collection
"""

from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Export_Metadata(Type_Safe):                                        # Metadata about the timestamp collection
    name              : str   = ''
    total_duration_ns : int   = 0
    total_duration_ms : float = 0.0
    entry_count       : int   = 0
    method_count      : int   = 0
    start_time_ns     : int   = 0
    end_time_ns       : int   = 0