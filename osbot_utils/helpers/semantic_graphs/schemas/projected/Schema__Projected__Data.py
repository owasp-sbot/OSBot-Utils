# ═══════════════════════════════════════════════════════════════════════════════
# Projected__Data - The human-readable projection content
#
# Contains the actual graph data in human-readable form - NO IDs.
# This is what humans look at to understand the graph.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Edges   import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Nodes   import List__Projected__Nodes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Projected__Data(Type_Safe):                                                    # Human-readable graph content
    nodes : List__Projected__Nodes                                                   # All nodes with ref + name
    edges : List__Projected__Edges                                                   # All edges with from_name + to_name + ref
