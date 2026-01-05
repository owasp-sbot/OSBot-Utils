# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Node_Types__By_Ref - Typed collection mapping node type refs to definitions
# Used by Schema__Ontology for node type storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type import Schema__Ontology__Node_Type
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Node_Types__By_Ref(Type_Safe__Dict):                                     # Maps node type refs to definitions
    expected_key_type   = Node_Type_Ref
    expected_value_type = Schema__Ontology__Node_Type
