# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Node_Type - Defines a node type with relationships
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Relationships__By_Verb import Dict__Relationships__By_Verb
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                 import Category_Ref
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text


class Schema__Ontology__Node_Type(Type_Safe):                                            # Defines a node type with relationships
    description   : Safe_Str__Text                                                       # Human-readable description
    relationships : Dict__Relationships__By_Verb                                         # verb → relationship definition
    taxonomy_ref  : Category_Ref                                                         # Reference to taxonomy category
