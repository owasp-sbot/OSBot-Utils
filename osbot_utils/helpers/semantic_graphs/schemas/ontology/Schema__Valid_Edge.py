# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Valid_Edge - Represents a valid edge combination from ontology
# Used by Ontology__Utils.all_valid_edges()
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Valid_Edge(Type_Safe):                                                 # Valid edge combination
    source_type : Node_Type_Id                                                       # Source node type
    verb        : Safe_Str__Ontology__Verb                                           # Relationship verb
    target_type : Node_Type_Id                                                       # Target node type
