# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Call_Flow__Result - Result container for call flow analysis
# Contains the semantic graph plus metadata about the analysis
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                          import Dict, Any, Optional, List
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph


class Schema__Call_Flow__Result(Type_Safe):                                          # Result container for call flow analysis
    graph             : Schema__Semantic_Graph                                       # The semantic graph of call flow
    node_properties   : Dict[str, Dict[str, Any]]                                    # node_id -> properties mapping
    name_to_node_id   : Dict[str, str           ]                                    # qualified_name -> node_id mapping
    entry_point       : str                      = ''                                # The analyzed entry point
    max_depth_reached : int                      = 0                                 # Maximum depth actually reached
    total_nodes       : int                      = 0                                 # Total number of nodes
    total_edges       : int                      = 0                                 # Total number of edges
    errors            : List[str]                                                    # Any errors encountered
