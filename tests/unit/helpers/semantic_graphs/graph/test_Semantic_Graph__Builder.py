# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Builder - Tests for graph builder using Utils classes
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                      import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                        import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph               import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.testing.Graph__Deterministic__Ids                                          import graph_ids_for_tests

# todo:
#     :
#       - see applicable to this test/class comments in the test_Taxonomy__Utils files


class test_Semantic_Graph__Builder(TestCase):                                        # Test graph builder

    @classmethod
    def setUpClass(cls):                                                             # Create test ontology once
        cls.ontology     = cls.create_test_ontology()
        cls.graph_utils  = Semantic_Graph__Utils()

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                               # Build test ontology
        class_has = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in'),
                                                   targets = [Node_Type_Id('method')]      )
        class_inherits = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('inherited_by'),
                                                        targets = [Node_Type_Id('class')]                 )
        class_node_type = Schema__Ontology__Node_Type(description   = 'Python class'                      ,
                                                      relationships = {'has': class_has,
                                                                       'inherits_from': class_inherits}   )

        method_calls = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('called_by')          ,
                                                      targets = [Node_Type_Id('method'), Node_Type_Id('function')])
        method_node_type = Schema__Ontology__Node_Type(description   = 'Python method'  ,
                                                       relationships = {'calls': method_calls})

        function_node_type = Schema__Ontology__Node_Type(description   = 'Python function',
                                                         relationships = {}               )

        return Schema__Ontology(ontology_id = Ontology_Id('test_ontology'),
                                node_types  = {'class'   : class_node_type   ,
                                               'method'  : method_node_type  ,
                                               'function': function_node_type})

    def test__init__(self):                                                          # Test initialization
        with Semantic_Graph__Builder() as _:
            assert type(_.graph)          is Schema__Semantic_Graph
            assert type(_.ontology)       is Schema__Ontology
            assert type(_.graph_utils)    is Semantic_Graph__Utils
            assert type(_.ontology_utils) is Ontology__Utils

    def test__create(self):                                                          # Test graph creation
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                result = _.create('test_ontology')

                assert result is _                                                   # Returns self for chaining
                assert _.graph is not None
                assert type(_.graph) is Schema__Semantic_Graph
                assert str(_.graph.ontology_ref) == 'test_ontology'

    def test__create__with_rule_set(self):                                           # Test with rule set
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test_ontology', 'test_rules')

                assert str(_.graph.ontology_ref) == 'test_ontology'
                assert str(_.graph.rule_set_ref) == 'test_rules'

    def test__with_ontology(self):                                                   # Test setting ontology
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                result = _.create('test').with_ontology(self.ontology)

                assert result     is _
                assert _.ontology is self.ontology

    def test__add_node(self):                                                        # Test adding nodes
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test')

                node_id = _.add_node('class', 'MyClass', line_number=10)

                assert node_id is not None
                assert self.graph_utils.node_count(_.graph) == 1

                node = self.graph_utils.get_node(_.graph, node_id)
                assert str(node.name)        == 'MyClass'
                assert str(node.node_type)   == 'class'
                assert int(node.line_number) == 10

    def test__add_edge__without_validation(self):                                    # Test adding edges (no ontology)
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test')

                class_id  = _.add_node('class', 'MyClass')
                method_id = _.add_node('method', 'my_method')

                edge_id = _.add_edge(class_id, 'has', method_id, line_number=20)

                assert edge_id is None                                               # No ontology, returns None
                assert self.graph_utils.edge_count(_.graph) == 0

    def test__add_edge__with_validation__valid(self):                                # Test valid edge with ontology
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test').with_ontology(self.ontology)

                class_id  = _.add_node('class', 'MyClass')
                method_id = _.add_node('method', 'my_method')

                edge_id = _.add_edge(class_id, 'has', method_id)

                assert edge_id is not None
                assert self.graph_utils.edge_count(_.graph) == 1

    def test__add_edge__with_validation__invalid(self):                              # Test invalid edge with ontology
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test').with_ontology(self.ontology)

                class_id    = _.add_node('class', 'MyClass')
                function_id = _.add_node('function', 'my_func')

                edge_id = _.add_edge(class_id, 'has', function_id)
                assert edge_id is None                                               # Invalid edge returns None

    def test__build(self):                                                           # Test building final graph
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test')
                _.add_node('class', 'A')
                _.add_node('class', 'B')

                graph = _.build()

                assert type(graph) is Schema__Semantic_Graph
                assert self.graph_utils.node_count(graph) == 2

    def test__find_node_by_name(self):                                               # Test finding nodes by name
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test')
                _.add_node('class', 'Alpha')
                _.add_node('class', 'Beta')

                alpha_id = _.find_node_by_name('Alpha')
                beta_id  = _.find_node_by_name('Beta')
                none_id  = _.find_node_by_name('Gamma')

                assert alpha_id is not None
                assert beta_id  is not None
                assert none_id  is None

    def test__find_nodes_by_type(self):                                              # Test finding nodes by type
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                _.create('test')
                _.add_node('class', 'A')
                _.add_node('class', 'B')
                _.add_node('method', 'foo')

                classes = _.find_nodes_by_type('class')
                methods = _.find_nodes_by_type('method')

                assert len(classes) == 2
                assert len(methods) == 1

    def test__fluent_api_chaining(self):                                             # Test full fluent API
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as _:
                class_id  = _.create('test').with_ontology(self.ontology).add_node('class', 'MyClass')
                method_id = _.add_node('method', 'foo')
                _.add_edge(class_id, 'has', method_id)

                graph = _.build()

                assert self.graph_utils.node_count(graph) == 2
                assert self.graph_utils.edge_count(graph) == 1