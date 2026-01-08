from typing                                                                               import Dict
from osbot_utils.helpers.performance.schemas.Schema__Performance_Measure__Measurement     import Schema__Performance_Measure__Measurement
from osbot_utils.helpers.performance.schemas.safe_str.Safe_Str__Performance__Name         import Safe_Str__Performance__Name
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Int                                       import Safe_Int


class Schema__Performance_Measure__Result(Type_Safe):                                         # Pure data container for measurement results
    measurements : Dict[int, Schema__Performance_Measure__Measurement]                        # Results per loop size
    name         : Safe_Str__Performance__Name                                                     # Name of measured target
    raw_score    : Safe_Int
    final_score  : Safe_Int

