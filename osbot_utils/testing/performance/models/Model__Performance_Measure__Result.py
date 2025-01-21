from typing                                                                         import Dict
from osbot_utils.testing.performance.models.Model__Performance_Measure__Measurement import Model__Performance_Measure__Measurement
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

class Model__Performance_Measure__Result(Type_Safe):                                         # Pure data container for measurement results
    measurements : Dict[int, Model__Performance_Measure__Measurement]                        # Results per loop size
    name         : str                                                                       # Name of measured target
    raw_score    : float
    final_score  : float

