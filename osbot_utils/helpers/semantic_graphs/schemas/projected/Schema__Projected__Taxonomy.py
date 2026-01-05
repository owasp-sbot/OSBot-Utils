# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Projected__Taxonomy - Human-readable taxonomy information in projections
#
# Provides two mappings for understanding the taxonomy structure:
#   - node_type_categories: Which category each node type belongs to
#   - category_parents: The parent of each category (for hierarchy navigation)
#
# Uses refs (not IDs) for human readability.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Refs__By_Category_Ref  import Dict__Category_Refs__By_Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Refs__By_Node_Type_Ref import Dict__Category_Refs__By_Node_Type_Ref
from osbot_utils.type_safe.Type_Safe                                                              import Type_Safe


class Schema__Projected__Taxonomy(Type_Safe):                                        # Human-readable taxonomy in projections
    node_type_categories : Dict__Category_Refs__By_Node_Type_Ref                     # Node type ref → category ref
    category_parents     : Dict__Category_Refs__By_Category_Ref                      # Category ref → parent category ref
