# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Builder - Tests for fluent graph builder
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Builder                    import Call_Flow__Builder
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Ontology                   import Call_Flow__Ontology
from osbot_utils.testing.__                                                          import __, __SKIP__
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data


class test_Call_Flow__Builder(TestCase):                                             # Test builder class

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.qa = QA__Call_Flow__Test_Data()

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Builder() as _:
            assert type(_)              is Call_Flow__Builder
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.ontology)     is Call_Flow__Ontology
            assert _.name_to_node_id    == {}
            assert _.node_properties    == {}

    def test__setup(self):                                                           # Test setup initializes ontology
        with Call_Flow__Builder() as _:
            result = _.setup()
            assert result           is _                                             # Returns self (fluent)
            assert type(_.ontology) is Call_Flow__Ontology
            assert _.builder        is not None

    def test__add_class(self):                                                       # Test adding class node
        with self.qa as _:
            builder = _.create_builder()
            result  = builder.add_class(qualified_name='test.MyClass'                ,
                                        module_name   ='test'                        )

            assert result                           is builder                           # Fluent API
            assert 'test.MyClass'                   in builder.name_to_node_id
            assert builder.has_node('test.MyClass') is True
            assert type(result)                     is Call_Flow__Builder
            assert result.obj()                     == __(ontology = __SKIP__,
                                                          builder  = __(ontology_registry = None,
                                                                        graph             = __(graph_id_source = None      ,
                                                                                               rule_set_id     = None      ,
                                                                                               graph_id        = ''        ,
                                                                                               ontology_id     = '1079fc5c',
                                                                                               nodes           = __(b116297e = __(node_id_source = __(source_type = 'deterministic'              ,
                                                                                                                                                      seed        = 'call_flow:node:test.MyClass'),
                                                                                                                                  properties     = None      ,
                                                                                                                                  node_id        = 'b116297e',
                                                                                                                                  node_type_id   = 'ce44e48f',
                                                                                                                                  name           = 'MyClass' )),
                                                                                               edges           = []        )),
                                                        name_to_node_id   = __(test_MyClass = 'b116297e'),
                                                        node_properties   = __(b116297e = __(qualified_name = 'test.MyClass',
                                                                         module_name    = 'test'        )))

    def test__add_method(self):                                                      # Test adding method node
        with self.qa as _:
            builder = _.create_builder()
            builder.add_method(qualified_name = 'test.MyClass.do_work'               ,
                               module_name     = 'test'                              ,
                               is_entry        = True                                )

            assert 'test.MyClass.do_work'      in builder.name_to_node_id
            node_id = str(builder.name_to_node_id['test.MyClass.do_work'])
            assert builder.node_properties[node_id]['is_entry'] == True
            assert builder.graph().obj()  == __(graph_id_source = None,
                                                rule_set_id     = None,
                                                graph_id        = '',
                                                ontology_id     = '1079fc5c',
                                                nodes           = __(_3ceeb0e0=__(node_id_source=__(source_type='deterministic',
                                                                                                    seed='call_flow:node:test.MyClass.do_work'),
                                                                                  properties=None,
                                                                                  node_id='3ceeb0e0',
                                                                                  node_type_id='143fb9ef',
                                                                                  name='do_work')),
                                                edges=[])

    def test__add_function(self):                                                    # Test adding function node
        with self.qa as _:
            builder = _.create_builder()
            builder.add_function(qualified_name = 'test.my_func'                     ,
                                module_name     = 'test'                             )

            assert 'test.my_func' in builder.name_to_node_id

    def test__add_module(self):                                                      # Test adding module node
        with self.qa as _:
            builder = _.create_builder()
            builder.add_module(qualified_name = 'test.module'                        ,
                              file_path       = '/path/to/module.py'                 )

            assert 'test.module' in builder.name_to_node_id

    def test__add_external(self):                                                    # Test adding external node
        with self.qa as _:
            builder = _.create_builder()
            builder.add_external(qualified_name = 'external.func'                    ,
                                module_name     = 'external'                         )

            assert 'external.func' in builder.name_to_node_id

    def test__add_contains(self):                                                    # Test adding contains edge
        with self.qa as _:
            builder = _.create_builder()
            builder.add_class('test.MyClass')
            builder.add_method('test.MyClass.method')
            builder.add_contains('test.MyClass', 'test.MyClass.method')

            graph = builder.build()
            assert len(graph.edges) == 1

            edge = graph.edges[0]
            contains_id = str(_.get_predicate_id__contains())
            assert str(edge.predicate_id) == contains_id

    def test__add_calls(self):                                                       # Test adding calls edge
        with self.qa as _:
            builder = _.create_builder()
            builder.add_function('test.caller')
            builder.add_function('test.callee')
            builder.add_calls('test.caller', 'test.callee')

            graph   = builder.build()
            edge    = graph.edges[0]
            calls_id = str(_.get_predicate_id__calls())
            assert str(edge.predicate_id) == calls_id

    def test__add_calls_self(self):                                                  # Test adding self-call edge
        with self.qa as _:
            builder = _.create_builder()
            builder.add_method('test.MyClass.caller')
            builder.add_method('test.MyClass.callee')
            builder.add_calls_self('test.MyClass.caller', 'test.MyClass.callee')

            graph = builder.build()
            edge  = graph.edges[0]
            calls_self_id = str(_.get_predicate_id__calls_self())
            assert str(edge.predicate_id) == calls_self_id

    def test__add_calls_chain(self):                                                 # Test adding chain-call edge
        with self.qa as _:
            builder = _.create_builder()
            builder.add_method('test.MyClass.caller')
            builder.add_external('other.callee')
            builder.add_calls_chain('test.MyClass.caller', 'other.callee')

            graph = builder.build()
            edge  = graph.edges[0]
            calls_chain_id = str(_.get_predicate_id__calls_chain())
            assert str(edge.predicate_id) == calls_chain_id

    def test__has_node(self):                                                        # Test node existence check
        with self.qa as _:
            builder = _.create_builder()
            builder.add_class('test.MyClass')

            assert builder.has_node('test.MyClass')   == True
            assert builder.has_node('test.Other')     == False

    def test__build(self):                                                           # Test building graph
        with self.qa as _:
            builder = _.create_builder()
            builder.add_class('test.MyClass')
            builder.add_method('test.MyClass.foo')
            builder.add_contains('test.MyClass', 'test.MyClass.foo')

            graph = builder.build()
            assert type(graph)                   is Schema__Semantic_Graph
            assert len(list(graph.nodes.keys())) == 2
            assert len(graph.edges)              == 1
            assert graph.obj()                   == __(graph_id_source = None      ,
                                                       rule_set_id     = None      ,
                                                       graph_id        = ''        ,
                                                       ontology_id     = '1079fc5c',
                                                       nodes           = __(b116297e = __(node_id_source = __(source_type = 'deterministic'              ,
                                                                                                              seed        = 'call_flow:node:test.MyClass'),
                                                                                          properties     = None      ,
                                                                                          node_id        = 'b116297e',
                                                                                          node_type_id   = 'ce44e48f',
                                                                                          name           = 'MyClass' ),
                                                                            f168c361 = __(node_id_source = __(source_type = 'deterministic'                  ,
                                                                                                              seed        = 'call_flow:node:test.MyClass.foo'),
                                                                                          properties     = None      ,
                                                                                          node_id        = 'f168c361',
                                                                                          node_type_id   = '143fb9ef',
                                                                                          name           = 'foo'     )),
                                                       edges           = [__(edge_id_source = __(source_type = 'deterministic'                                      ,
                                                                                                 seed        = 'call_flow:edge:test.MyClass:test.MyClass.foo:28386687'),
                                                                             properties     = None      ,
                                                                             edge_id        = 'cada5772',
                                                                             from_node_id   = 'b116297e',
                                                                             to_node_id     = 'f168c361',
                                                                             predicate_id   = '28386687')])

    def test__fluent_api(self):                                                      # Test fluent method chaining
        with self.qa as _:
            graph = (_.create_builder()
                     .add_class('test.A')
                     .add_method('test.A.foo')
                     .add_method('test.A.bar')
                     .add_contains('test.A', 'test.A.foo')
                     .add_contains('test.A', 'test.A.bar')
                     .add_calls_self('test.A.foo', 'test.A.bar')
                     .build())

            assert len(list(graph.nodes.keys())) == 3                                # class + 2 methods
            assert len(graph.edges)              == 3                                # 2 contains + 1 calls_self

    def test__builder_with_class__from_qa(self):                                     # Test QA factory method
        with self.qa as _:
            builder = _.create_builder_with_class(class_name   = 'my.Test'           ,
                                                  method_names = ['a', 'b', 'c']     )

            assert 'my.Test'   in builder.name_to_node_id
            assert 'my.Test.a' in builder.name_to_node_id
            assert 'my.Test.b' in builder.name_to_node_id
            assert 'my.Test.c' in builder.name_to_node_id

    def test__builder_with_self_calls__from_qa(self):                                # Test QA self-calls builder
        with self.qa as _:
            builder = _.create_builder_with_self_calls()
            graph   = builder.build()

            assert len(list(graph.nodes.keys())) == 3                                # class + 2 methods
            assert len(graph.edges)              == 3                                # 2 contains + 1 calls_self

    def test__edge_not_found__raises(self):                                          # Test error on missing node
        with self.qa as _:
            builder = _.create_builder()
            builder.add_class('test.MyClass')

            with self.assertRaises(ValueError) as ctx:
                builder.add_contains('test.MyClass', 'test.Missing')

            assert 'Target node not found' in str(ctx.exception)