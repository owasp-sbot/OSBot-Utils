# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Validator - Validates semantic graphs against ontology
#
# Updated for Brief 3.7:
#   - Validates node_type_id exists in ontology.node_types dict
#   - Validates predicate_id exists in ontology.predicates dict
#   - Validates edges against ontology.edge_rules (source_type + predicate + target_type)
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
            if not self.ontology_utils.has_node_type(ontology, node.node_type_id):   # Check node_type_id exists
                node_type = ontology.node_types.get(node.node_type_id)
                error = Safe_Str__Text(f"Node '{node_id}' has unknown node_type_id: {node.node_type_id}")
                errors.append(error)

    @type_safe
    def validate_edges(self                              ,
                       graph    : Schema__Semantic_Graph ,
                       ontology : Schema__Ontology       ,
                       errors   : List__Validation_Errors) -> None:                  # Validate all edges
        for edge in graph.edges:
            if not self.validate_edge_nodes_exist(graph, edge, errors):              # Check nodes exist
                continue
            if not self.validate_edge_predicate_exists(ontology, edge, errors):      # Check predicate exists
                continue
            self.validate_edge_against_rules(graph, ontology, edge, errors)          # Check edge is valid per rules

    @type_safe
    def validate_edge_nodes_exist(self                                 ,
                                  graph  : Schema__Semantic_Graph      ,
                                  edge   : Schema__Semantic_Graph__Edge,
                                  errors : List__Validation_Errors     ) -> bool:    # Check edge nodes exist
        valid = True
        if edge.from_node_id not in graph.nodes:
            error = Safe_Str__Text(f"Edge references unknown from_node_id: {edge.from_node_id}")
            errors.append(error)
            valid = False
        if edge.to_node_id not in graph.nodes:
            error = Safe_Str__Text(f"Edge references unknown to_node_id: {edge.to_node_id}")
            errors.append(error)
            valid = False
        return valid

    @type_safe
    def validate_edge_predicate_exists(self                                   ,
                                       ontology : Schema__Ontology            ,
                                       edge     : Schema__Semantic_Graph__Edge,
                                       errors   : List__Validation_Errors     ) -> bool:  # Check predicate exists
        if not self.ontology_utils.has_predicate(ontology, edge.predicate_id):
            error = Safe_Str__Text(f"Edge references unknown predicate_id: {edge.predicate_id}")
            errors.append(error)
            return False
        return True

    @type_safe
    def validate_edge_against_rules(self                                   ,
                                    graph    : Schema__Semantic_Graph      ,
                                    ontology : Schema__Ontology            ,
                                    edge     : Schema__Semantic_Graph__Edge,
                                    errors   : List__Validation_Errors     ) -> None:  # Check edge is valid per rules
        from_node       = graph.nodes.get(edge.from_node_id)
        to_node         = graph.nodes.get(edge.to_node_id)
        source_type_id  = from_node.node_type_id
        target_type_id  = to_node.node_type_id

        if not self.ontology_utils.is_valid_edge(ontology, source_type_id, edge.predicate_id, target_type_id):
            source_type = self.ontology_utils.get_node_type(ontology, source_type_id)  # Get refs for error message
            target_type = self.ontology_utils.get_node_type(ontology, target_type_id)
            predicate   = self.ontology_utils.get_predicate(ontology, edge.predicate_id)

            source_ref  = source_type.node_type_ref if source_type else source_type_id
            target_ref  = target_type.node_type_ref if target_type else target_type_id
            pred_ref    = predicate.predicate_ref   if predicate   else edge.predicate_id

            error = Safe_Str__Text(f"Invalid edge: {source_ref} --[{pred_ref}]--> {target_ref}")
            errors.append(error)
