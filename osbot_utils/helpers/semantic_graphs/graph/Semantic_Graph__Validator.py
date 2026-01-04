# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Validator - Validates semantic graphs against ontology
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                   import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors import List__Validation_Errors
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph       import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Validation_Result    import Schema__Validation_Result
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology          import Schema__Ontology
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                      import type_safe


class Semantic_Graph__Validator(Type_Safe):                                          # Validates graphs against ontology
    ontology_utils : Ontology__Utils                                                 # Utils for ontology operations

    @type_safe
    def validate(self                              ,
                 graph    : Schema__Semantic_Graph ,
                 ontology : Schema__Ontology       ) -> Schema__Validation_Result:   # Validate graph against ontology
        errors = List__Validation_Errors()

        self.validate_nodes(graph, ontology, errors)                                 # Validate all nodes
        self.validate_edges(graph, ontology, errors)                                 # Validate all edges

        return Schema__Validation_Result(valid  = len(errors) == 0,
                                         errors = errors          )

    @type_safe
    def validate_nodes(self                              ,
                       graph    : Schema__Semantic_Graph ,
                       ontology : Schema__Ontology       ,
                       errors   : List__Validation_Errors) -> None:                  # Validate all nodes
        for node_id, node in graph.nodes.items():
            if not self.ontology_utils.has_node_type(ontology, node.node_type):
                error = Safe_Str__Text(f"Node '{node_id}' has unknown type: {node.node_type}")
                errors.append(error)

    @type_safe
    def validate_edges(self                              ,
                       graph    : Schema__Semantic_Graph ,
                       ontology : Schema__Ontology       ,
                       errors   : List__Validation_Errors) -> None:                  # Validate all edges
        for edge in graph.edges:
            if not self.validate_edge_nodes_exist(graph, edge, errors):              # Check nodes exist
                continue
            self.validate_edge_against_ontology(graph, ontology, edge, errors)       # Check edge is valid

    @type_safe
    def validate_edge_nodes_exist(self                                 ,
                                  graph  : Schema__Semantic_Graph      ,
                                  edge   : Schema__Semantic_Graph__Edge,
                                  errors : List__Validation_Errors     ) -> bool:       # Check edge nodes exist
        valid = True
        if edge.from_node not in graph.nodes:
            error = Safe_Str__Text(f"Edge references unknown from_node: {edge.from_node}")
            errors.append(error)
            valid = False
        if edge.to_node not in graph.nodes:
            error = Safe_Str__Text(f"Edge references unknown to_node: {edge.to_node}")
            errors.append(error)
            valid = False
        return valid

    @type_safe
    def validate_edge_against_ontology(self                                   ,
                                       graph    : Schema__Semantic_Graph      ,
                                       ontology : Schema__Ontology            ,
                                       edge     : Schema__Semantic_Graph__Edge,
                                       errors   : List__Validation_Errors     ) -> None:  # Check edge is valid per ontology
        from_node   = graph.nodes.get(edge.from_node)
        to_node     = graph.nodes.get(edge.to_node)
        source_type = from_node.node_type
        target_type = to_node.node_type

        if not self.ontology_utils.is_valid_edge(ontology, source_type, edge.verb, target_type):
            error = Safe_Str__Text(f"Invalid edge: {source_type} --[{edge.verb}]--> {target_type}")
            errors.append(error)
