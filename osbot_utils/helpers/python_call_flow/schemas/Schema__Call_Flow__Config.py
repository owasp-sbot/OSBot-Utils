# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Call_Flow__Config - Configuration for call flow analysis
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                     import Optional
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class Schema__Call_Flow__Config(Type_Safe):                                      # Configuration for call flow analysis
    target_method      : str                                                     # Method to analyze (e.g., 'MyClass.method')
    max_depth          : int            = 10                                     # Maximum call depth to trace
    include_external   : bool           = True                                   # Include external/library calls
    include_builtins   : bool           = False                                  # Include Python builtins
    include_source     : bool           = False                                  # Include source code in nodes
    filter_module      : Optional[str]  = None                                   # Only include calls within this module
    ontology_ref       : str            = 'call_flow'                            # Ontology reference name
