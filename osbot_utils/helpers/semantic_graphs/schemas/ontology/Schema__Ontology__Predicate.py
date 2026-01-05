# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Predicate - First-class predicate definition
#
# Predicates are relationship types like "calls", "contains", "inherits_from".
# Each predicate is defined ONCE and referenced by ID throughout the system.
#
# Fields:
#   - predicate_id + predicate_id_source: Instance identity with provenance
#   - predicate_ref: Human-readable label (defined once here)
#   - inverse_id: Points to the inverse predicate (e.g., "calls" → "called_by")
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text


class Schema__Ontology__Predicate(Type_Safe):                                        # First-class predicate definition
    predicate_id        : Predicate_Id                                               # Unique instance identifier
    predicate_id_source : Schema__Id__Source = None                                  # ID provenance (optional sidecar)
    predicate_ref       : Predicate_Ref                                              # Human-readable label ("calls", "contains")
    inverse_id          : Predicate_Id       = None                                  # Points to inverse predicate
    description         : Safe_Str__Text     = None                                  # Optional description
