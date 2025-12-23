from dataclasses import dataclass

@dataclass(slots=True)
class Schema__Method_Timing():                               # Aggregated timing for a method
    name        : str   = ''
    call_count  : int   = 0
    total_ns    : int   = 0
    min_ns      : int   = 0
    max_ns      : int   = 0
    self_ns     : int   = 0                                 # Exclusive time (minus children)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False