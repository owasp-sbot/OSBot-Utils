"""
Schema for Export Hotspot - hotspot entry for summary export
"""

from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Export_Hotspot(Type_Safe):                                         # Hotspot entry for summary
    name       : str   = ''
    self_ms    : float = 0.0
    percentage : float = 0.0
    calls      : int   = 0