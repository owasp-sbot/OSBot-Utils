from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                     import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                      import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality             import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Validation_Result            import Schema__Validation_Result
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors         import List__Validation_Errors
from osbot_utils.testing.Graph__Deterministic__Ids                                          import graph_ids_for_tests
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                      import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Validator                    import Semantic_Graph__Validator
from osbot_utils.testing.__ import __


class test_Semantic_Graph__Validator(TestCase):                                      # Test graph validator

    @classmethod
    def setUpClass(cls):                                                             # Create test ontology and rule set once
        cls.ontology = cls.create_test_ontology()
        cls.rule_set = cls.create_test_rule_set()

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                               # Build test ontology
        class_has = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in'),
                                                   targets = [Node_Type_Id('method')]      )
        class_node_type = Schema__Ontology__Node_Type(description   = 'Python class'  ,
                                                      relationships = {'has': class_has})

        method_node_type = Schema__Ontology__Node_Type(description   = 'Python method',
                                                       relationships = {}              )

        return Schema__Ontology(ontology_id = Ontology_Id('test')           ,
                                node_types  = {'class' : class_node_type ,
                                               'method': method_node_type})

    @classmethod
    def create_test_rule_set(cls) -> Schema__Rule_Set:                               # Build test rule set
        cardinality_rule = Schema__Rule__Cardinality(source_type = Node_Type_Id('method')              ,
                                                     verb        = Safe_Str__Ontology__Verb('in')      ,
                                                     target_type = Node_Type_Id('class')               ,
                                                     min_targets = 1                                   ,
                                                     max_targets = 1                                   ,
                                                     description = 'Method must belong to exactly one class')

        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules')  ,
                                ontology_ref       = Ontology_Id('test')        ,
                                transitivity_rules = []                         ,
                                cardinality_rules  = [cardinality_rule]         )

    def test__init__(self):                                                          # Test initialization
        with Semantic_Graph__Validator(ontology=self.ontology) as _:
            assert _.ontology           is self.ontology
            assert type(_.rule_set)     is Schema__Rule_Set

    def test__init__with_rule_set(self):                                             # Test with rule set
        with Semantic_Graph__Validator(ontology=self.ontology, rule_set=self.rule_set) as _:
            assert _.ontology  is self.ontology
            assert _.rule_set  is self.rule_set

    def test__validate__valid_graph(self):                                           # Test validating valid graph
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as builder:
                builder.create('test')
                class_id  = builder.add_node('class', 'MyClass')
                method_id = builder.add_node('method', 'foo')
                builder.add_edge(class_id, 'has', method_id)
                graph = builder.build()

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)

                assert type(result)        is Schema__Validation_Result
                assert type(result.errors) is List__Validation_Errors
                assert result.valid        is True
                assert len(result.errors)  == 0

    def test__validate__invalid_node_type(self):                                     # Test invalid node type
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as builder:
                builder.create('test')
                builder.add_node('invalid_type', 'BadNode')
                graph = builder.build()

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)

                assert type(result)        is Schema__Validation_Result
                assert result.valid        is False
                assert len(result.errors)  == 1
                assert 'unknown node_type' in result.errors[0].lower()

    def test__validate__invalid_edge(self):                                          # Test invalid edge
        with graph_ids_for_tests():
            ontology = None                                                             # disable ontology validation for this test
            with Semantic_Graph__Builder(ontology=ontology) as builder:
                builder.create('test')
                class_id  = builder.add_node('class', 'A')
                method_id = builder.add_node('method', 'foo')
                edge_id   = builder.add_edge(method_id, 'has', class_id)
                graph    = builder.build()
                assert class_id      == 'c0000001'
                assert method_id     == 'c0000002'
                assert edge_id       == 'e0000001'
                assert builder.obj() == __(graph= graph.obj(),
                                           ontology=None)
                assert graph.obj() == __(version='1.0.0',
                                         graph_id='a0000001',
                                         ontology_ref='test',
                                         rule_set_ref='',
                                         nodes=__(c0000001=__(node_id='c0000001',
                                                              node_type='class',
                                                              name='A',
                                                              line_number=0),
                                                  c0000002=__(node_id='c0000002',
                                                              node_type='method',
                                                              name='foo',
                                                              line_number=0)),
                                            edges=[__(line_number=0,
                                                      edge_id='e0000001',
                                                      from_node='c0000002',
                                                      verb='has',
                                                      to_node='c0000001')])

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)
                assert result.obj()       == __(valid=False,
                                                errors=['Edge e0000001: invalid edge method --has--_ class'])

                assert type(result)       is Schema__Validation_Result
                assert result.valid       is False
                assert len(result.errors) == 1
                assert 'invalid edge'     in result.errors[0].lower()

    def test__validate_edge__single_edge(self):                                      # Test single edge validation
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as builder:
                builder.create('test')
                class_id  = builder.add_node('class', 'MyClass')
                method_id = builder.add_node('method', 'foo')
                graph = builder.build()

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                valid_edge   = validator.validate_edge(graph, class_id, 'has', method_id)
                invalid_edge = validator.validate_edge(graph, method_id, 'has', class_id)

                assert valid_edge   is True
                assert invalid_edge is False

    def test__validate_edge__missing_nodes(self):                                    # Test edge with missing nodes
        with graph_ids_for_tests():
            with Semantic_Graph__Builder() as builder:
                builder.create('test')
                graph = builder.build()

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate_edge(graph, 'nonexistent', 'has', 'also_nonexistent')

                assert result is False