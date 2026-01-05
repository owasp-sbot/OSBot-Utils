# ═══════════════════════════════════════════════════════════════════════════════
# List__Node_Type_Refs - Typed collection for lists of node type references
# Used by Schema__Ontology__Relationship for target types
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Node_Type_Refs(Type_Safe__List):                                         # List of node type references
    expected_type = Node_Type_Ref
