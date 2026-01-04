# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Rule_Set - Collection of rules for a domain (pure data)
# Business logic has been moved to Rule_Set__Utils
#
# Fields:
#   - rule_set_id + rule_set_id_source: Instance identity with provenance
#   - rule_set_ref: Human-readable reference name for lookup
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality  import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref              import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id               import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref              import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source        import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text          import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version       import Safe_Str__Version


class Schema__Rule_Set(Type_Safe):                                                   # Collection of rules for a domain
    rule_set_id        : Rule_Set_Id                                                 # Unique instance identifier
    rule_set_id_source : Schema__Id__Source      = None                              # ID provenance (optional sidecar)
    rule_set_ref       : Rule_Set_Ref                                                # Human-readable reference name
    ontology_ref       : Ontology_Ref                                                # Which ontology this applies to
    version            : Safe_Str__Version       = '1.0.0'                           # Semantic version
    description        : Safe_Str__Text                                              # What rules this contains
    transitivity_rules : List__Rules__Transitivity                                   # Transitive relationships
    cardinality_rules  : List__Rules__Cardinality                                    # Cardinality constraints
