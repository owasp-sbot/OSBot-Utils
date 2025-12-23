from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Method_Timing(Type_Safe):                     # Aggregated timing for a method
    name        : str   = ''
    call_count  : int   = 0
    total_ns    : int   = 0
    min_ns      : int   = 0
    max_ns      : int   = 0
    self_ns     : int   = 0                                 # Exclusive time (minus children)