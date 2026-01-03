from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set               import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Validation_Result     import Schema__Validation_Result
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors  import List__Validation_Errors
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb


class Semantic_Graph__Validator(Type_Safe):                                          # Validate graphs against ontology and rules
    ontology : Schema__Ontology                                                      # Ontology to validate against
    rule_set : Schema__Rule_Set                                                      # Optional rules to apply

    @type_safe
    def validate(self, graph: Schema__Semantic_Graph) -> Schema__Validation_Result:  # Validate graph, return result
        errors = List__Validation_Errors()

        errors.extend(self.validate_node_types(graph))
        errors.extend(self.validate_edges(graph))
        errors.extend(self.validate_cardinality(graph))

        return Schema__Validation_Result(valid  = len(errors) == 0,
                                         errors = errors          )

    @type_safe
    def validate_node_types(self, graph: Schema__Semantic_Graph) -> List__Validation_Errors:
        errors      = List__Validation_Errors()
        valid_types = set(self.ontology.node_type_ids())

        for node_id, node in graph.nodes.items():
            node_type = node.node_type
            if node_type not in valid_types:
                errors.append(f"Node {node_id}: unknown node_type '{node_type}'")

        return errors

    @type_safe
    def validate_edges(self, graph: Schema__Semantic_Graph) -> List__Validation_Errors:
        errors = List__Validation_Errors()

        for edge in graph.edges:
            from_node = graph.get_node(edge.from_node)
            to_node   = graph.get_node(edge.to_node)

            if from_node is None:
                errors.append(f"Edge {edge.edge_id}: from_node '{edge.from_node}' not found")
                continue
            if to_node is None:
                errors.append(f"Edge {edge.edge_id}: to_node '{edge.to_node}' not found")
                continue

            from_type = from_node.node_type
            to_type   = to_node.node_type
            verb      = edge.verb

            if self.ontology.valid_edge(from_type, verb, to_type) is False:
                errors.append(f"Edge {edge.edge_id}: invalid edge {from_type} --{verb}--> {to_type}")

        return errors

    @type_safe
    def validate_cardinality(self, graph: Schema__Semantic_Graph) -> List__Validation_Errors:
        errors = List__Validation_Errors()
        if self.rule_set is None:
            return errors

        for rule in self.rule_set.cardinality_rules:
            source_type = rule.source_type
            verb        = rule.verb
            target_type = rule.target_type

            for node_id, node in graph.nodes.items():
                if node.node_type != source_type:
                    continue

                count = 0
                for edge in graph.edges_from(node_id):
                    if edge.verb != verb:
                        continue
                    to_node = graph.get_node(edge.to_node)
                    if to_node and to_node.node_type == target_type:
                        count += 1

                if count < int(rule.min_targets):
                    errors.append(f"Node {node_id}: needs at least {rule.min_targets} "
                                  f"{verb} edges to {target_type}, has {count}")
                if rule.max_targets is not None and count > int(rule.max_targets):
                    errors.append(f"Node {node_id}: allows at most {rule.max_targets} "
                                  f"{verb} edges to {target_type}, has {count}")

        return errors

    @type_safe
    def validate_edge(self, graph        : Schema__Semantic_Graph,
                            from_node_id : Node_Id               ,
                            verb         : Safe_Str__Ontology__Verb,
                            to_node_id   : Node_Id               ) -> bool:
        from_node = graph.get_node(from_node_id)
        to_node   = graph.get_node(to_node_id)

        if from_node is None or to_node is None:
            return False

        from_type = from_node.node_type
        to_type   = to_node.node_type

        return self.ontology.valid_edge(from_type, verb, to_type)