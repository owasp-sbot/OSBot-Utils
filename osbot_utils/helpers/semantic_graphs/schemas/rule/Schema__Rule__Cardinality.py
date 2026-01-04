# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Rule__Cardinality - Cardinality constraint rule schema
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text


class Schema__Rule__Cardinality(Type_Safe):                                          # Cardinality constraint
    source_type : Node_Type_Id                                                       # e.g., "method"
    verb        : Safe_Str__Ontology__Verb                                           # e.g., "in"
    target_type : Node_Type_Id                                                       # e.g., "class"
    min_targets : Safe_UInt                                                          # Minimum required targets
    max_targets : Safe_UInt                      = None                              # Maximum allowed (None = unlimited)
    description : Safe_Str__Text                                                     # Human explanation
