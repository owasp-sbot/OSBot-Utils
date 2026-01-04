# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Utils - Utility operations for ontology validation and lookup
# Extracted from Schema__Ontology to keep schemas as pure data containers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids      import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology__Verbs    import List__Ontology__Verbs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Valid_Edges        import List__Valid_Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Valid_Edge         import Schema__Valid_Edge
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe


class Ontology__Utils(Type_Safe):                                                    # Utility operations for ontologies

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Validation
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def valid_edge(self, ontology   : Schema__Ontology        ,
                         source_type: Node_Type_Id            ,
                         verb       : Safe_Str__Ontology__Verb,
                         target_type: Node_Type_Id            ) -> bool:             # Check if edge is valid per ontology
        node_type = ontology.node_types.get(source_type)
        if not node_type:
            return False
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return False
        return target_type in relationship.targets

    @type_safe
    def all_valid_edges(self, ontology: Schema__Ontology) -> List__Valid_Edges:      # Get all valid edge combinations
        edges = List__Valid_Edges()
        for source_id, node_type in ontology.node_types.items():
            for verb, rel in node_type.relationships.items():
                for target_id in rel.targets:
                    edge = Schema__Valid_Edge(source_type = Node_Type_Id(source_id)       ,
                                              verb        = Safe_Str__Ontology__Verb(verb),
                                              target_type = Node_Type_Id(target_id)       )
                    edges.append(edge)
        return edges

    # ═══════════════════════════════════════════════════════════════════════════════
    # Verb Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_inverse_verb(self, ontology   : Schema__Ontology        ,
                               source_type: Node_Type_Id            ,
                               verb       : Safe_Str__Ontology__Verb) -> Safe_Str__Ontology__Verb:
        node_type = ontology.node_types.get(source_type)                             # Get inverse verb for relationship
        if not node_type:
            return None
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return None
        return relationship.inverse

    @type_safe
    def verbs_for_node_type(self, ontology    : Schema__Ontology,
                                  node_type_id: Node_Type_Id    ) -> List__Ontology__Verbs:
        result = List__Ontology__Verbs()                                             # Get all verbs for node type
        node_type = ontology.node_types.get(node_type_id)
        if not node_type:
            return result
        for verb in node_type.relationships.keys():
            result.append(Safe_Str__Ontology__Verb(verb))
        return result

    @type_safe
    def targets_for_verb(self, ontology    : Schema__Ontology        ,
                               node_type_id: Node_Type_Id            ,
                               verb        : Safe_Str__Ontology__Verb) -> List__Node_Type_Ids:
        result = List__Node_Type_Ids()                                               # Get valid targets for verb
        node_type = ontology.node_types.get(node_type_id)
        if not node_type:
            return result
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return result
        for target in relationship.targets:
            result.append(target)
        return result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Naming
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def edge_forward_name(self, source_type: Node_Type_Id            ,
                                verb       : Safe_Str__Ontology__Verb,
                                target_type: Node_Type_Id            ) -> str:       # Compute forward edge name
        return f"{source_type}_{verb}_{target_type}"

    @type_safe
    def edge_inverse_name(self, ontology   : Schema__Ontology        ,
                                source_type: Node_Type_Id            ,
                                verb       : Safe_Str__Ontology__Verb,
                                target_type: Node_Type_Id            ) -> str:       # Compute inverse edge name
        inverse_verb = self.get_inverse_verb(ontology, source_type, verb)
        if inverse_verb:
            return f"{target_type}_{inverse_verb}_{source_type}"
        return ""

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Type Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def node_type_ids(self, ontology: Schema__Ontology) -> List__Node_Type_Ids:      # Get all node type IDs
        result = List__Node_Type_Ids()
        for type_id in ontology.node_types.keys():
            result.append(Node_Type_Id(type_id))
        return result
