from typing                             import List
from osbot_utils.type_safe.Type_Safe    import Type_Safe


class Model__Performance_Measure__Measurement(Type_Safe):                                     # Pure data container for measurement metrics
    avg_time     : int                                                                       # Average time in nanoseconds
    min_time     : int                                                                       # Minimum time observed
    max_time     : int                                                                       # Maximum time observed
    median_time  : int                                                                       # Median time
    stddev_time  : float                                                                     # Standard deviation
    raw_times    : List[int]                                                                 # Raw measurements for analysis
    sample_size  : int                                                                       # Number of measurements taken
    score        : float
    raw_score    : float