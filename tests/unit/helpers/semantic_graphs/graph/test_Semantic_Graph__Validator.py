# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Validator - Tests for graph validation against ontology
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.7:
#   - Uses node_type_id instead of node_type ref
#   - Uses predicate_id instead of verb
#   - Uses from_node_id/to_node_id instead of from_node/to_node
#   - Validates against ontology.edge_rules instead of embedded relationships
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                              import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                       import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Validator                   import Semantic_Graph__Validator
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id             import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges    import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors        import List__Validation_Errors
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph              import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge        import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node        import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Validation_Result           import Schema__Validation_Result
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                   import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                    import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                   import Predicate_Id
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data            import QA__Semantic_Graphs__Test_Data
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                         import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                           import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id            import Safe_Str__Id


class test_Semantic_Graph__Validator(TestCase):                                            # Test graph validator

    @classmethod
    def setUpClass(cls):                                                                   # Shared test objects (performance)
        cls.test_data   = QA__Semantic_Graphs__Test_Data()
        cls.ontology    = cls.test_data.create_ontology__code_structure()
        cls.rule_set    = cls.test_data.create_rule_set__code_structure()
        cls.graph_utils = Semantic_Graph__Utils()

        # Cache commonly used IDs
        cls.module_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:module'))
        cls.class_type_id    = Node_Type_Id(Obj_Id.from_seed('test:node_type:class'))
        cls.method_type_id   = Node_Type_Id(Obj_Id.from_seed('test:node_type:method'))
        cls.function_type_id = Node_Type_Id(Obj_Id.from_seed('test:node_type:function'))
        cls.contains_pred_id = Predicate_Id(Obj_Id.from_seed('test:predicate:contains'))
        cls.calls_pred_id    = Predicate_Id(Obj_Id.from_seed('test:predicate:calls'))
        cls.ontology_id      = Ontology_Id(Obj_Id.from_seed('test:ontology:code_structure'))

    def create_empty_graph(self) -> Schema__Semantic_Graph:                                # Helper to create empty graph
        return Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id())            ,
                                      ontology_id = self.ontology_id              ,
                                      nodes       = Dict__Nodes__By_Id()          ,
                                      edges       = List__Semantic_Graph__Edges() )

    def test__init__(self):                                                                # Test initialization
        with Semantic_Graph__Validator() as _:
            assert type(_) is Semantic_Graph__Validator

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Graph Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__valid_graph(self):                                                 # Test validating valid graph
        graph = self.test_data.create_graph__simple_class()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert type(result)        is Schema__Validation_Result
            assert type(result.errors) is List__Validation_Errors
            assert result.valid        is True
            assert len(result.errors)  == 0

    def test__validate__empty_graph(self):                                                 # Test validating empty graph
        graph    = self.test_data.create_graph__empty()
        ontology = self.test_data.create_ontology__minimal()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, ontology)

            assert result.valid       is True
            assert len(result.errors) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Invalid Node Type Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__invalid_node_type(self):                                           # Test invalid node type detection
        graph = self.create_empty_graph()

        unknown_type_id = Node_Type_Id(Obj_Id())                                           # Random ID not in ontology
        invalid_node = Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())   ,
                                                    node_type_id = unknown_type_id     ,
                                                    name         = Safe_Str__Id('BadNode'))
        graph.nodes[invalid_node.node_id] = invalid_node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 1
            assert 'unknown' in str(result.errors[0]).lower()

    def test__validate__multiple_invalid_nodes(self):                                      # Test multiple invalid node types
        graph = self.create_empty_graph()

        for i in range(3):
            unknown_type_id = Node_Type_Id(Obj_Id())                                       # Random ID not in ontology
            node = Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())   ,
                                                node_type_id = unknown_type_id     ,
                                                name         = Safe_Str__Id(f'Node{i}'))
            graph.nodes[node.node_id] = node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 3

    def test__validate__mixed_valid_and_invalid_nodes(self):                               # Test graph with some valid, some invalid
        graph = self.create_empty_graph()

        valid_node   = self.test_data.create_node(self.class_type_id  , Safe_Str__Id('Valid'))
        invalid_node = self.test_data.create_node(Node_Type_Id(Obj_Id()), Safe_Str__Id('Invalid'))

        graph.nodes[valid_node.node_id]   = valid_node
        graph.nodes[invalid_node.node_id] = invalid_node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 1                                                 # Only invalid node reported

    # ═══════════════════════════════════════════════════════════════════════════
    # Invalid Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__invalid_predicate(self):                                           # Test invalid predicate detection
        graph = self.create_empty_graph()

        class_node  = self.test_data.create_node(self.class_type_id , Safe_Str__Id('MyClass'))
        method_node = self.test_data.create_node(self.method_type_id, Safe_Str__Id('my_method'))

        graph.nodes[class_node.node_id]  = class_node
        graph.nodes[method_node.node_id] = method_node

        unknown_pred_id = Predicate_Id(Obj_Id())                                           # Random ID not in ontology
        invalid_edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())       ,
                                                    from_node_id = class_node.node_id      ,
                                                    predicate_id = unknown_pred_id         ,
                                                    to_node_id   = method_node.node_id     )
        graph.edges.append(invalid_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1

    def test__validate__invalid_edge_target_type(self):                                    # Test invalid edge target type
        graph = self.create_empty_graph()

        class_node    = self.test_data.create_node(self.class_type_id   , Safe_Str__Id('MyClass'))
        function_node = self.test_data.create_node(self.function_type_id, Safe_Str__Id('my_func'))

        graph.nodes[class_node.node_id]    = class_node
        graph.nodes[function_node.node_id] = function_node

        # class 'contains' should only target 'method', not 'function' per edge_rules
        invalid_edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())       ,
                                                    from_node_id = class_node.node_id      ,
                                                    predicate_id = self.contains_pred_id   ,
                                                    to_node_id   = function_node.node_id   )
        graph.edges.append(invalid_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid is False

    def test__validate__edge_references_unknown_from_node(self):                           # Test edge with unknown from_node_id
        graph = self.create_empty_graph()

        target_node = self.test_data.create_node(self.method_type_id, Safe_Str__Id('target'))
        graph.nodes[target_node.node_id] = target_node

        orphan_edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())        ,
                                                   from_node_id = Node_Id(Obj_Id())        ,  # Unknown node
                                                   predicate_id = self.contains_pred_id    ,
                                                   to_node_id   = target_node.node_id      )
        graph.edges.append(orphan_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1
            assert 'from_node_id' in str(result.errors[0]).lower()

    def test__validate__edge_references_unknown_to_node(self):                             # Test edge with unknown to_node_id
        graph = self.create_empty_graph()

        source_node = self.test_data.create_node(self.class_type_id, Safe_Str__Id('source'))
        graph.nodes[source_node.node_id] = source_node

        orphan_edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())        ,
                                                   from_node_id = source_node.node_id      ,
                                                   predicate_id = self.contains_pred_id    ,
                                                   to_node_id   = Node_Id(Obj_Id())        )  # Unknown node
        graph.edges.append(orphan_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1
            assert 'to_node_id' in str(result.errors[0]).lower()

    # ═══════════════════════════════════════════════════════════════════════════
    # Validate Nodes Method
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate_nodes__all_valid(self):                                             # Test validate_nodes with valid nodes
        graph  = self.test_data.create_graph__simple_class()
        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_nodes(graph, self.ontology, errors)

            assert len(errors) == 0

    def test__validate_nodes__with_invalid(self):                                          # Test validate_nodes with invalid
        graph = self.create_empty_graph()

        bad_node = Schema__Semantic_Graph__Node(node_id      = Node_Id(Obj_Id())   ,
                                                node_type_id = Node_Type_Id(Obj_Id()),  # Unknown type
                                                name         = Safe_Str__Id('Bad') )
        graph.nodes[bad_node.node_id] = bad_node

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_nodes(graph, self.ontology, errors)

            assert len(errors) == 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Validate Edges Method
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate_edges__all_valid(self):                                             # Test validate_edges with valid edges
        graph  = self.test_data.create_graph__simple_class()
        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) == 0

    def test__validate_edges__missing_from_node(self):                                     # Test edge with missing from_node_id
        graph = self.create_empty_graph()

        target_node = self.test_data.create_node(self.method_type_id, Safe_Str__Id('target'))
        graph.nodes[target_node.node_id] = target_node

        edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())       ,
                                            from_node_id = Node_Id(Obj_Id())       ,  # Unknown node
                                            predicate_id = self.contains_pred_id   ,
                                            to_node_id   = target_node.node_id     )
        graph.edges.append(edge)

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) >= 1
            assert 'from_node_id' in str(errors[0]).lower()

    def test__validate_edges__missing_to_node(self):                                       # Test edge with missing to_node_id
        graph = self.create_empty_graph()

        source_node = self.test_data.create_node(self.class_type_id, Safe_Str__Id('source'))
        graph.nodes[source_node.node_id] = source_node

        edge = Schema__Semantic_Graph__Edge(edge_id      = Edge_Id(Obj_Id())       ,
                                            from_node_id = source_node.node_id     ,
                                            predicate_id = self.contains_pred_id   ,
                                            to_node_id   = Node_Id(Obj_Id())       )  # Unknown node
        graph.edges.append(edge)

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) >= 1
            assert 'to_node_id' in str(errors[0]).lower()

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__qa_data_is_self_consistent(self):                                  # Test QA data validates correctly
        graph    = self.test_data.create_graph__simple_class()
        ontology = self.test_data.create_ontology__code_structure()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, ontology)

            assert result.valid       is True
            assert len(result.errors) == 0

    def test__validate__graph_node_types_match_ontology(self):                             # Test all node types exist in ontology
        graph    = self.test_data.create_graph__simple_class()
        ontology = self.test_data.create_ontology__code_structure()

        ontology_type_ids = set(ontology.node_types.keys())
        graph_type_ids    = set(n.node_type_id for n in graph.nodes.values())

        assert graph_type_ids.issubset(ontology_type_ids)

    def test__validate__complex_graph(self):                                               # Test larger graph
        graph = self.create_empty_graph()

        module   = self.test_data.create_node(self.module_type_id  , Safe_Str__Id('my_module'))
        class_a  = self.test_data.create_node(self.class_type_id   , Safe_Str__Id('ClassA'))
        class_b  = self.test_data.create_node(self.class_type_id   , Safe_Str__Id('ClassB'))
        method_1 = self.test_data.create_node(self.method_type_id  , Safe_Str__Id('method1'))
        method_2 = self.test_data.create_node(self.method_type_id  , Safe_Str__Id('method2'))
        func     = self.test_data.create_node(self.function_type_id, Safe_Str__Id('helper'))

        for node in [module, class_a, class_b, method_1, method_2, func]:
            graph.nodes[node.node_id] = node

        edges_data = [(module.node_id , self.contains_pred_id, class_a.node_id) ,
                      (module.node_id , self.contains_pred_id, class_b.node_id) ,
                      (class_a.node_id, self.contains_pred_id, method_1.node_id),
                      (class_b.node_id, self.contains_pred_id, method_2.node_id),
                      (module.node_id , self.contains_pred_id, func.node_id)    ]

        for from_id, pred_id, to_id in edges_data:
            edge = self.test_data.create_edge(from_id, pred_id, to_id)
            graph.edges.append(edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is True
            assert len(result.errors) == 0