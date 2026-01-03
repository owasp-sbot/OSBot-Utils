# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Validator - Tests for graph validator using Utils classes
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                      import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                        import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Validator                    import Semantic_Graph__Validator
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                           import Ontology__Utils
from osbot_utils.helpers.semantic_graphs.rule.Rule_Set__Utils                               import Rule_Set__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors         import List__Validation_Errors
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Validation_Result            import Schema__Validation_Result
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                     import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                     import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                      import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality             import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.testing.Graph__Deterministic__Ids                                          import graph_ids_for_tests
from osbot_utils.testing.__ import __
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id


# todo:
#     :
#       - see applicable to this test/class comments in the test_Taxonomy__Utils files


class test_Semantic_Graph__Validator(TestCase):                                      # Test graph validator

    @classmethod
    def setUpClass(cls):                                                             # Create test ontology and rule set once
        cls.ontology     = cls.create_test_ontology()
        cls.rule_set     = cls.create_test_rule_set()
        cls.graph_utils  = Semantic_Graph__Utils()

    @classmethod
    def create_test_ontology(cls) -> Schema__Ontology:                               # Build test ontology
        class_has = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('in'),
                                                   targets = [Node_Type_Id('method')]      )
        class_node_type = Schema__Ontology__Node_Type(description   = 'Python class',
                                                      relationships = {'has': class_has})

        method_node_type = Schema__Ontology__Node_Type(description   = 'Python method',
                                                       relationships = {}              )

        return Schema__Ontology(ontology_id = Ontology_Id('test'),
                                node_types  = {'class' : class_node_type ,
                                               'method': method_node_type})

    @classmethod
    def create_test_rule_set(cls) -> Schema__Rule_Set:                               # Build test rule set
        cardinality_rule = Schema__Rule__Cardinality(source_type = Node_Type_Id('method')              ,
                                                     verb        = Safe_Str__Ontology__Verb('in')      ,
                                                     target_type = Node_Type_Id('class')               ,
                                                     min_targets = 1                                   ,
                                                     max_targets = 1                                   ,
                                                     description = 'Method must belong to one class'  )

        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                ontology_ref       = Ontology_Id('test')      ,
                                transitivity_rules = []                       ,
                                cardinality_rules  = [cardinality_rule]       )

    def test__init__(self):                                                          # Test initialization
        with Semantic_Graph__Validator(ontology=self.ontology) as _:
            assert _.ontology             is self.ontology
            assert type(_.rule_set)       is Schema__Rule_Set
            assert type(_.graph_utils)    is Semantic_Graph__Utils
            assert type(_.ontology_utils) is Ontology__Utils
            assert type(_.rule_set_utils) is Rule_Set__Utils

    def test__init__with_rule_set(self):                                             # Test with rule set
        with Semantic_Graph__Validator(ontology=self.ontology, rule_set=self.rule_set) as _:
            assert _.ontology is self.ontology
            assert _.rule_set is self.rule_set

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
            with Semantic_Graph__Builder(ontology=None) as builder:                  # Disable ontology validation
                builder.create('test')
                class_id  = builder.add_node('class', 'A')
                method_id = builder.add_node('method', 'foo')
                edge_id   = builder.add_edge(method_id, 'has', class_id)             # Invalid: method has class
                graph     = builder.build()

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)

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

    # ═══════════════════════════════════════════════════════════════════════════════
    # validate_edges - missing from_node (lines 59-60)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__validate_edges__from_node_not_found(self):                             # Cover lines 59-60
        with graph_ids_for_tests():
            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            # Add only to_node, not from_node
            to_node = Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id()),
                                                   node_type = Node_Type_Id('method'),
                                                   name      = 'foo')
            self.graph_utils.add_node(graph, to_node)

            # Create edge with non-existent from_node
            missing_from_id = Node_Id(Obj_Id())
            edge = Schema__Semantic_Graph__Edge(edge_id   = Edge_Id(Obj_Id()),
                                                from_node = missing_from_id  ,
                                                verb      = Safe_Str__Ontology__Verb('has'),
                                                to_node   = to_node.node_id  )
            self.graph_utils.add_edge(graph, edge)

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)

                assert result.valid is False
                assert len(result.errors) >= 1
                assert 'from_node' in result.errors[0]
                assert 'not found' in result.errors[0]

    # ═══════════════════════════════════════════════════════════════════════════════
    # validate_edges - missing to_node (lines 62-63)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__validate_edges__to_node_not_found(self):                               # Cover lines 62-63
        with graph_ids_for_tests():
            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            # Add only from_node, not to_node
            from_node = Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id()),
                                                     node_type = Node_Type_Id('class'),
                                                     name      = 'MyClass')
            self.graph_utils.add_node(graph, from_node)

            # Create edge with non-existent to_node
            missing_to_id = Node_Id(Obj_Id())
            edge = Schema__Semantic_Graph__Edge(edge_id   = Edge_Id(Obj_Id()),
                                                from_node = from_node.node_id,
                                                verb      = Safe_Str__Ontology__Verb('has'),
                                                to_node   = missing_to_id    )
            self.graph_utils.add_edge(graph, edge)

            with Semantic_Graph__Validator(ontology=self.ontology) as validator:
                result = validator.validate(graph)

                assert result.valid is False
                assert len(result.errors) >= 1
                assert 'to_node' in result.errors[0]
                assert 'not found' in result.errors[0]

    # ═══════════════════════════════════════════════════════════════════════════════
    # validate_cardinality - with rule_set (lines 78, 81-101)
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__validate_cardinality__min_targets_violation(self):                     # Cover min_targets check
        with graph_ids_for_tests():
            # Rule: method must have exactly 1 'in' edge to class
            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                        ontology_ref       = Ontology_Id('test')      ,
                                        transitivity_rules = []                       ,
                                        cardinality_rules  = [
                                            Schema__Rule__Cardinality(source_type = Node_Type_Id('method')         ,
                                                                      verb        = Safe_Str__Ontology__Verb('in') ,
                                                                      target_type = Node_Type_Id('class')          ,
                                                                      min_targets = 1                              ,
                                                                      max_targets = 1                              ,
                                                                      description = 'Method must be in one class' )])

            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            # Add method with NO 'in' edges (violates min_targets=1)
            method_node = Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id()),
                                                       node_type = Node_Type_Id('method'),
                                                       name      = 'orphan_method')
            self.graph_utils.add_node(graph, method_node)

            with Semantic_Graph__Validator(ontology=self.ontology, rule_set=rule_set) as validator:
                result = validator.validate(graph)

                assert result.valid is False
                assert len(result.errors) >= 1
                assert 'needs at least' in result.errors[0]
                assert 'in' in result.errors[0]

    def test__validate_cardinality__max_targets_violation(self):                     # Cover max_targets check
        with graph_ids_for_tests():
            # Rule: method can have at most 1 'in' edge to class
            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                        ontology_ref       = Ontology_Id('test')      ,
                                        transitivity_rules = []                       ,
                                        cardinality_rules  = [
                                            Schema__Rule__Cardinality(
                                                source_type = Node_Type_Id('method')         ,
                                                verb        = Safe_Str__Ontology__Verb('in') ,
                                                target_type = Node_Type_Id('class')          ,
                                                min_targets = 0                              ,
                                                max_targets = 1                              ,
                                                description = 'Method in at most one class' )
                                        ])

            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            # Add method and two classes
            method = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('method'), name='foo')
            class1 = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('class'), name='A')
            class2 = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('class'), name='B')

            self.graph_utils.add_node(graph, method)
            self.graph_utils.add_node(graph, class1)
            self.graph_utils.add_node(graph, class2)

            # Add TWO 'in' edges from method (violates max_targets=1)
            edge1 = Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node=method.node_id,
                                                 verb=Safe_Str__Ontology__Verb('in'), to_node=class1.node_id)
            edge2 = Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node=method.node_id,
                                                 verb=Safe_Str__Ontology__Verb('in'), to_node=class2.node_id)

            self.graph_utils.add_edge(graph, edge1)
            self.graph_utils.add_edge(graph, edge2)

            with Semantic_Graph__Validator(ontology=self.ontology, rule_set=rule_set) as validator:
                result = validator.validate(graph)

                assert result.valid is False
                assert len(result.errors) >= 1
                assert result.obj()       == __( valid=False,
                                                 errors=['Edge e0000001: invalid edge method --in--_ class',
                                                         'Edge e0000002: invalid edge method --in--_ class',
                                                         'Node c0000001: allows at most 1 in edges to class, has 2']) != __()

                assert 'allows at most' in result.errors[2]

    def test__validate_cardinality__node_type_mismatch_skipped(self):                # Cover node_type != source_type branch
        with graph_ids_for_tests():
            # Rule only applies to 'method' nodes
            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                        ontology_ref       = Ontology_Id('test')      ,
                                        transitivity_rules = []                       ,
                                        cardinality_rules  = [
                                            Schema__Rule__Cardinality(
                                                source_type = Node_Type_Id('method')         ,
                                                verb        = Safe_Str__Ontology__Verb('in') ,
                                                target_type = Node_Type_Id('class')          ,
                                                min_targets = 1                              ,
                                                max_targets = 1                              ,
                                                description = 'Method must be in one class' )
                                        ])

            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            # Add only a class node (not method) - rule should be skipped
            class_node = Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id()),
                                                      node_type = Node_Type_Id('class'),
                                                      name      = 'MyClass')
            self.graph_utils.add_node(graph, class_node)

            with Semantic_Graph__Validator(ontology=self.ontology, rule_set=rule_set) as validator:
                result = validator.validate(graph)

                # Should pass - no method nodes to validate
                assert result.valid is True

    def test__validate_cardinality__edge_verb_mismatch_skipped(self):                # Cover edge.verb != verb branch
        with graph_ids_for_tests():
            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                        ontology_ref       = Ontology_Id('test')      ,
                                        transitivity_rules = []                       ,
                                        cardinality_rules  = [
                                            Schema__Rule__Cardinality(
                                                source_type = Node_Type_Id('method')         ,
                                                verb        = Safe_Str__Ontology__Verb('in') ,
                                                target_type = Node_Type_Id('class')          ,
                                                min_targets = 0                              ,
                                                max_targets = 1                              ,
                                                description = '' )
                                        ])

            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            method = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('method'), name='foo')
            class1 = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('class'), name='A')

            self.graph_utils.add_node(graph, method)
            self.graph_utils.add_node(graph, class1)

            # Edge with DIFFERENT verb ('calls' instead of 'in') - should not count
            edge = Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node=method.node_id,
                                                verb=Safe_Str__Ontology__Verb('calls'), to_node=class1.node_id)
            self.graph_utils.add_edge(graph, edge)

            with Semantic_Graph__Validator(ontology=self.ontology, rule_set=rule_set) as validator:
                result = validator.validate_cardinality(graph)

                # Should pass - 'calls' edges don't count for 'in' rule
                assert len(result) == 0

    def test__validate_cardinality__target_type_mismatch_skipped(self):              # Cover to_node.node_type != target_type
        with graph_ids_for_tests():
            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('test_rules'),
                                        ontology_ref       = Ontology_Id('test')      ,
                                        transitivity_rules = []                       ,
                                        cardinality_rules  = [
                                            Schema__Rule__Cardinality(
                                                source_type = Node_Type_Id('method')         ,
                                                verb        = Safe_Str__Ontology__Verb('in') ,
                                                target_type = Node_Type_Id('class')          ,
                                                min_targets = 0                              ,
                                                max_targets = 1                              ,
                                                description = '' )
                                        ])

            graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                           ontology_ref = Ontology_Id('test'))

            method1 = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('method'), name='foo')
            method2 = Schema__Semantic_Graph__Node(node_id=Node_Id(Obj_Id()), node_type=Node_Type_Id('method'), name='bar')

            self.graph_utils.add_node(graph, method1)
            self.graph_utils.add_node(graph, method2)

            # Edge to another method (not class) - should not count toward 'in class' rule
            edge = Schema__Semantic_Graph__Edge(edge_id=Edge_Id(Obj_Id()), from_node=method1.node_id,
                                                verb=Safe_Str__Ontology__Verb('in'), to_node=method2.node_id)
            self.graph_utils.add_edge(graph, edge)

            with Semantic_Graph__Validator(ontology=self.ontology, rule_set=rule_set) as validator:
                result = validator.validate_cardinality(graph)

                # Should pass - edge to 'method' doesn't count for rule targeting 'class'
                assert len(result) == 0