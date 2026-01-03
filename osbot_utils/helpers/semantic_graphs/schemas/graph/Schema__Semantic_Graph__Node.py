from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt


class Schema__Semantic_Graph__Node(Type_Safe):                                       # Instance node in semantic graph
    node_id     : Node_Id                                                            # Unique identifier
    node_type   : Node_Type_Id                                                       # Reference to ontology node type
    name        : Safe_Str__Id                                                       # Display name
    line_number : Safe_UInt                                                         # Optional source location
