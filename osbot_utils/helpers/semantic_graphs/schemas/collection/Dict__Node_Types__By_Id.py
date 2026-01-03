from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type import Schema__Ontology__Node_Type
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict     import Type_Safe__Dict


class Dict__Node_Types__By_Id(Type_Safe__Dict):                                          # Maps node type IDs to definitions
    expected_key_type   = Node_Type_Id
    expected_value_type = Schema__Ontology__Node_Type