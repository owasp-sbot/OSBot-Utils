# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Projected__Semantic_Graph - Human-readable projection of a semantic graph
#
# Updated for Brief 3.8:
#   - Added taxonomy section: Maps node types to categories and shows hierarchy
#
# A projection has exactly four sections:
#   - projection: The human-readable content (nodes and edges with properties) - NO IDs
#   - references: Lookup index from refs to IDs (filtered to only what's used)
#   - taxonomy:   Node type → category mapping and category hierarchy
#   - sources:    Provenance information (for tracing)
#
# This is GENERATED, not edited. To modify data, work with Schema__ directly.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Data       import Schema__Projected__Data
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Sources    import Schema__Projected__Sources
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Taxonomy   import Schema__Projected__Taxonomy
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe


class Schema__Projected__Semantic_Graph(Type_Safe):                                  # Complete projection
    projection : Schema__Projected__Data                                             # Human-readable nodes/edges
    references : Schema__Projected__References                                       # Ref → ID lookups (filtered)
    taxonomy   : Schema__Projected__Taxonomy                                         # Type → category mapping
    sources    : Schema__Projected__Sources                                          # Provenance info
