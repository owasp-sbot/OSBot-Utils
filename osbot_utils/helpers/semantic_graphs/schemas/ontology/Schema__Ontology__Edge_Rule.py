# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Edge_Rule - Defines valid edge constraints
#
# An edge rule specifies which edges are allowed in graphs using this ontology:
#   source_type --predicate--> target_type
#
# Example: method --calls--> function
#          class  --contains--> method
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Ontology__Edge_Rule(Type_Safe):                                        # Valid edge constraint
    source_type_id : Node_Type_Id                                                    # Source node type (e.g., method)
    predicate_id   : Predicate_Id                                                    # Relationship predicate (e.g., calls)
    target_type_id : Node_Type_Id                                                    # Target node type (e.g., function)
