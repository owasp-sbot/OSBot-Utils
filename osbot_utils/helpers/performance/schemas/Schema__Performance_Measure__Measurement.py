from typing                                             import List
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float   import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_Int     import Safe_Int


class Schema__Performance_Measure__Measurement(Type_Safe):                                     # Pure data container for measurement metrics
    avg_time     : Safe_Int                                                                    # Average time in nanoseconds
    min_time     : Safe_Int                                                                    # Minimum time observed
    max_time     : Safe_Int                                                                    # Maximum time observed
    median_time  : Safe_Int                                                                    # Median time
    stddev_time  : Safe_Float                                                                  # Standard deviation
    raw_times    : List[Safe_Int]                                                              # Raw measurements for analysis
    sample_size  : Safe_Int                                                                    # Number of measurements taken
    score        : Safe_Int
    raw_score    : Safe_Int