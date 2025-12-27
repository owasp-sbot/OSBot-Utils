"""
Schema for Export Method Timing - method timing data for export
"""

from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Export_Method_Timing(Type_Safe):                                   # Method timing data for export
    name       : str   = ''
    call_count : int   = 0
    total_ns   : int   = 0
    total_ms   : float = 0.0
    self_ns    : int   = 0
    self_ms    : float = 0.0
    avg_ms     : float = 0.0
    min_ns     : int   = 0
    max_ns     : int   = 0