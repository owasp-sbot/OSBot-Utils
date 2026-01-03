from typing                                                                         import Optional, Any
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class Schema__Call__Info(Type_Safe):                                                 # Resolved call information from AST
    name        : Safe_Str__Label                                                    # Name of called function/method
    edge_type   : Enum__Call_Graph__Edge_Type                                        # Type of call (SELF, CHAIN, CALLS)
    resolved    : Optional[Any]                                                      # Resolved function object if available
    class_ref   : Optional[type]                                                     # Class context for self calls
    line_number : Safe_UInt                                                          # Line number of the call
