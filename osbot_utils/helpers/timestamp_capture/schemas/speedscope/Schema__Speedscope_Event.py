"""
Schema for Speedscope Event - event in speedscope format
"""

from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Speedscope_Event(Type_Safe):                                       # Event in speedscope format
    type  : str   = ''                                                           # 'O' for open, 'C' for close
    frame : int   = 0                                                            # Index into frames array
    at    : float = 0.0                                                          # Time in microseconds