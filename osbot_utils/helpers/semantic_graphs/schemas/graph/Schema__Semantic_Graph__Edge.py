from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt



class Schema__Semantic_Graph__Edge(Type_Safe):                                       # Instance edge in semantic graph
    edge_id     : Edge_Id                                                            # Unique identifier
    from_node   : Node_Id                                                            # Source node
    verb        : Safe_Str__Ontology__Verb                                           # Relationship verb
    to_node     : Node_Id                                                            # Target node
    line_number : Safe_UInt                      = Safe_UInt(0)                      # Optional source location
