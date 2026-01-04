# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Validator - Tests for graph validation against ontology
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
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
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                  import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                   import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb         import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data            import QA__Semantic_Graphs__Test_Data
from osbot_utils.type_safe.primitives.core.Safe_UInt                                       import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                         import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                           import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id            import Safe_Str__Id


class test_Semantic_Graph__Validator(TestCase):                                            # Test graph validator

    @classmethod
    def setUpClass(cls):                                                                   # Shared test objects (performance)
        cls.qa          = QA__Semantic_Graphs__Test_Data()
        cls.ontology    = cls.qa.create_ontology__code_structure()
        cls.rule_set    = cls.qa.create_rule_set__code_structure()
        cls.graph_utils = Semantic_Graph__Utils()

    def create_empty_graph(self) -> Schema__Semantic_Graph:                                # Helper to create empty graph
        return Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id())             ,
                                      ontology_ref = Ontology_Ref('code_structure') ,
                                      nodes        = Dict__Nodes__By_Id()           ,
                                      edges        = List__Semantic_Graph__Edges()  )

    def test__init__(self):                                                                # Test initialization
        with Semantic_Graph__Validator() as _:
            assert type(_) is Semantic_Graph__Validator

    # ═══════════════════════════════════════════════════════════════════════════
    # Valid Graph Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__valid_graph(self):                                                 # Test validating valid graph
        graph = self.qa.create_graph__simple_class()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert type(result)        is Schema__Validation_Result
            assert type(result.errors) is List__Validation_Errors
            assert result.valid        is True
            assert len(result.errors)  == 0

    def test__validate__empty_graph(self):                                                 # Test validating empty graph
        graph    = self.qa.create_graph__empty()
        ontology = self.qa.create_ontology__minimal()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, ontology)

            assert result.valid       is True
            assert len(result.errors) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Invalid Node Type Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__invalid_node_type(self):                                           # Test invalid node type detection
        graph = self.create_empty_graph()

        invalid_node = Schema__Semantic_Graph__Node(node_id     = Node_Id(Obj_Id())            ,
                                                    node_type   = Node_Type_Ref('unknown_type'),
                                                    name        = Safe_Str__Id('BadNode')      ,
                                                    line_number = Safe_UInt(0)                 )
        graph.nodes[invalid_node.node_id] = invalid_node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 1
            assert 'unknown' in str(result.errors[0]).lower()

    def test__validate__multiple_invalid_nodes(self):                                      # Test multiple invalid node types
        graph = self.create_empty_graph()

        for i, type_name in enumerate(['bad_type_1', 'bad_type_2', 'bad_type_3']):
            node = Schema__Semantic_Graph__Node(node_id     = Node_Id(Obj_Id())        ,
                                                node_type   = Node_Type_Ref(type_name) ,
                                                name        = Safe_Str__Id(f'Node{i}') ,
                                                line_number = Safe_UInt(0)             )
            graph.nodes[node.node_id] = node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 3

    def test__validate__mixed_valid_and_invalid_nodes(self):                               # Test graph with some valid, some invalid
        graph = self.create_empty_graph()

        valid_node   = self.qa.create_node(Node_Type_Ref('class')  , Safe_Str__Id('Valid'))
        invalid_node = self.qa.create_node(Node_Type_Ref('invalid'), Safe_Str__Id('Invalid'))

        graph.nodes[valid_node.node_id]   = valid_node
        graph.nodes[invalid_node.node_id] = invalid_node

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) == 1                                                 # Only invalid node reported

    # ═══════════════════════════════════════════════════════════════════════════
    # Invalid Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__invalid_edge_verb(self):                                           # Test invalid edge verb
        graph = self.create_empty_graph()

        class_node  = self.qa.create_node(Node_Type_Ref('class') , Safe_Str__Id('MyClass'))
        method_node = self.qa.create_node(Node_Type_Ref('method'), Safe_Str__Id('my_method'))

        graph.nodes[class_node.node_id]  = class_node
        graph.nodes[method_node.node_id] = method_node

        invalid_edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                      ,
                                                    from_node   = class_node.node_id                     ,
                                                    verb        = Safe_Str__Ontology__Verb('invalid_verb'),
                                                    to_node     = method_node.node_id                    ,
                                                    line_number = Safe_UInt(0)                           )
        graph.edges.append(invalid_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1

    def test__validate__invalid_edge_target_type(self):                                    # Test invalid edge target type
        graph = self.create_empty_graph()

        class_node    = self.qa.create_node(Node_Type_Ref('class')   , Safe_Str__Id('MyClass'))
        function_node = self.qa.create_node(Node_Type_Ref('function'), Safe_Str__Id('my_func'))

        graph.nodes[class_node.node_id]    = class_node
        graph.nodes[function_node.node_id] = function_node

        # class 'contains' should only target 'method', not 'function' per ontology
        invalid_edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                   ,
                                                    from_node   = class_node.node_id                  ,
                                                    verb        = Safe_Str__Ontology__Verb('contains'),
                                                    to_node     = function_node.node_id               ,
                                                    line_number = Safe_UInt(0)                        )
        graph.edges.append(invalid_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid is False

    def test__validate__edge_references_unknown_from_node(self):                           # Test edge with unknown from_node
        graph = self.create_empty_graph()

        target_node = self.qa.create_node(Node_Type_Ref('method'), Safe_Str__Id('target'))
        graph.nodes[target_node.node_id] = target_node

        orphan_edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                   ,
                                                   from_node   = Node_Id(Obj_Id())                   ,  # Unknown node
                                                   verb        = Safe_Str__Ontology__Verb('contains'),
                                                   to_node     = target_node.node_id                 ,
                                                   line_number = Safe_UInt(0)                        )
        graph.edges.append(orphan_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1
            assert 'from_node' in str(result.errors[0]).lower()

    def test__validate__edge_references_unknown_to_node(self):                             # Test edge with unknown to_node
        graph = self.create_empty_graph()

        source_node = self.qa.create_node(Node_Type_Ref('class'), Safe_Str__Id('source'))
        graph.nodes[source_node.node_id] = source_node

        orphan_edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                   ,
                                                   from_node   = source_node.node_id                 ,
                                                   verb        = Safe_Str__Ontology__Verb('contains'),
                                                   to_node     = Node_Id(Obj_Id())              ,  # Unknown node
                                                   line_number = Safe_UInt(0)                        )
        graph.edges.append(orphan_edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is False
            assert len(result.errors) >= 1
            assert 'to_node' in str(result.errors[0]).lower()

    # ═══════════════════════════════════════════════════════════════════════════
    # Validate Nodes Method
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate_nodes__all_valid(self):                                             # Test validate_nodes with valid nodes
        graph  = self.qa.create_graph__simple_class()
        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_nodes(graph, self.ontology, errors)

            assert len(errors) == 0

    def test__validate_nodes__with_invalid(self):                                          # Test validate_nodes with invalid
        graph = self.create_empty_graph()

        bad_node = Schema__Semantic_Graph__Node(node_id     = Node_Id(Obj_Id())           ,
                                                node_type   = Node_Type_Ref(Obj_Id()),
                                                name        = Safe_Str__Id('Bad')         ,
                                                line_number = Safe_UInt(0)                )
        graph.nodes[bad_node.node_id] = bad_node

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_nodes(graph, self.ontology, errors)

            assert len(errors) == 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Validate Edges Method
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate_edges__all_valid(self):                                             # Test validate_edges with valid edges
        graph  = self.qa.create_graph__simple_class()
        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) == 0

    def test__validate_edges__missing_from_node(self):                                     # Test edge with missing from_node
        graph = self.create_empty_graph()

        target_node = self.qa.create_node(Node_Type_Ref('method'), Safe_Str__Id('target'))
        graph.nodes[target_node.node_id] = target_node

        edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                   ,
                                            from_node   = Node_Id(Obj_Id())                  ,
                                            verb        = Safe_Str__Ontology__Verb('contains'),
                                            to_node     = target_node.node_id                 ,
                                            line_number = Safe_UInt(0)                        )
        graph.edges.append(edge)

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) >= 1
            assert 'from_node' in str(errors[0]).lower()

    def test__validate_edges__missing_to_node(self):                                       # Test edge with missing to_node
        graph = self.create_empty_graph()

        source_node = self.qa.create_node(Node_Type_Ref('class'), Safe_Str__Id('source'))
        graph.nodes[source_node.node_id] = source_node

        edge = Schema__Semantic_Graph__Edge(edge_id     = Edge_Id(Obj_Id())                   ,
                                            from_node   = source_node.node_id                 ,
                                            verb        = Safe_Str__Ontology__Verb('contains'),
                                            to_node     = Node_Id(Obj_Id())                   ,
                                            line_number = Safe_UInt(0)                        )
        graph.edges.append(edge)

        errors = List__Validation_Errors()

        with Semantic_Graph__Validator() as validator:
            validator.validate_edges(graph, self.ontology, errors)

            assert len(errors) >= 1
            assert 'to_node' in str(errors[0]).lower()

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__validate__qa_data_is_self_consistent(self):                                  # Test QA data validates correctly
        graph    = self.qa.create_graph__simple_class()
        ontology = self.qa.create_ontology__code_structure()

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, ontology)

            assert result.valid       is True
            assert len(result.errors) == 0

    def test__validate__graph_node_types_match_ontology(self):                             # Test all node types exist in ontology
        graph    = self.qa.create_graph__simple_class()
        ontology = self.qa.create_ontology__code_structure()

        ontology_types = set(str(k) for k in ontology.node_types.keys())
        graph_types    = set(str(n.node_type) for n in graph.nodes.values())

        assert graph_types.issubset(ontology_types)

    def test__validate__complex_graph(self):                                               # Test larger graph
        graph = self.create_empty_graph()

        module   = self.qa.create_node(Node_Type_Ref('module')  , Safe_Str__Id('my_module'))
        class_a  = self.qa.create_node(Node_Type_Ref('class')   , Safe_Str__Id('ClassA'))
        class_b  = self.qa.create_node(Node_Type_Ref('class')   , Safe_Str__Id('ClassB'))
        method_1 = self.qa.create_node(Node_Type_Ref('method')  , Safe_Str__Id('method1'))
        method_2 = self.qa.create_node(Node_Type_Ref('method')  , Safe_Str__Id('method2'))
        func     = self.qa.create_node(Node_Type_Ref('function'), Safe_Str__Id('helper'))

        for node in [module, class_a, class_b, method_1, method_2, func]:
            graph.nodes[node.node_id] = node

        edges_data = [(module.node_id , 'contains', class_a.node_id) ,
                      (module.node_id , 'contains', class_b.node_id) ,
                      (class_a.node_id, 'contains', method_1.node_id),
                      (class_b.node_id, 'contains', method_2.node_id),
                      (module.node_id , 'contains', func.node_id)    ]

        for from_id, verb, to_id in edges_data:
            edge = self.qa.create_edge(from_id, Safe_Str__Ontology__Verb(verb), to_id)
            graph.edges.append(edge)

        with Semantic_Graph__Validator() as validator:
            result = validator.validate(graph, self.ontology)

            assert result.valid       is True
            assert len(result.errors) == 0