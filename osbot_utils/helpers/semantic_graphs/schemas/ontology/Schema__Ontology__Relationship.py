# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Relationship - Defines a relationship from source node type
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Refs     import List__Node_Type_Refs
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Ontology__Relationship(Type_Safe):                                     # Defines a relationship from source node type
    inverse : Safe_Str__Ontology__Verb                                               # Inverse verb name
    targets : List__Node_Type_Refs                                                   # Valid target node type refs
