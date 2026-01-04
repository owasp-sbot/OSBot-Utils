# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Ontologies__By_Ref - Typed collection mapping ontology refs to ontologies
# Used by Ontology__Registry for lookup by reference name
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref             import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Ontologies__By_Ref(Type_Safe__Dict):                                     # Maps ontology refs to ontology objects
    expected_key_type   = Ontology_Ref
    expected_value_type = Schema__Ontology
