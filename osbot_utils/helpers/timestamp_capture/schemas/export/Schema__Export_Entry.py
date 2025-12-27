"""
Schema for Export Entry - single timestamp entry for export
"""

from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Export_Entry(Type_Safe):                                           # Single timestamp entry for export
    name         : str = ''
    event        : str = ''                                                      # 'enter' or 'exit'
    timestamp_ns : int = 0
    clock_ns     : int = 0
    depth        : int = 0
    thread_id    : int = 0