# ═══════════════════════════════════════════════════════════════════════════════
# Tests for QA__Call_Flow__Test_Data
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.testing.__                                                          import __, __SKIP__
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph

from osbot_utils.helpers.python_call_flow.Call_Flow__Ontology                        import Call_Flow__Ontology
from osbot_utils.helpers.python_call_flow.Call_Flow__Builder                         import Call_Flow__Builder
from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                        import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.actions.Call_Flow__Exporter__Mermaid       import Call_Flow__Exporter__Mermaid
from osbot_utils.helpers.python_call_flow.Call_Flow__Storage                         import Call_Flow__Storage
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config          import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result          import Schema__Call_Flow__Result
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import (QA__Call_Flow__Test_Data  ,
                                                                                             Sample__Simple_Class      ,
                                                                                             Sample__Self_Calls        ,
                                                                                             Sample__Multiple_Self_Calls,
                                                                                             Sample__Chain_Calls       ,
                                                                                             Sample__Conditional_Calls ,
                                                                                             Sample__Deep_Calls        ,
                                                                                             Sample__Recursive         ,
                                                                                             Sample__With_Builtins     ,
                                                                                             Sample__External_Calls    ,
                                                                                             sample_standalone_function,
                                                                                             sample_helper_function    )


class test_QA__Call_Flow__Test_Data(TestCase):

    @classmethod
    def setUpClass(cls):                                                             # Expensive setup done once
        cls.qa = QA__Call_Flow__Test_Data()
        cls.ontology = cls.qa.create_ontology()                                      # Cache ontology for reuse

    # ═══════════════════════════════════════════════════════════════════════════
    # Core Class Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                          # Test QA class initialization
        with QA__Call_Flow__Test_Data() as _:
            assert type(_)         is QA__Call_Flow__Test_Data
            assert base_classes(_) == [Type_Safe, object]

    # ═══════════════════════════════════════════════════════════════════════════
    # Sample Class Accessor Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_get_sample_class__simple(self):                                         # Test simple class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__simple()
            assert sample_class is Sample__Simple_Class
            assert hasattr(sample_class, 'method_a')
            assert hasattr(sample_class, 'method_b')

    def test_get_sample_class__self_calls(self):                                     # Test self calls class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__self_calls()
            assert sample_class is Sample__Self_Calls
            assert hasattr(sample_class, 'do_work')
            assert hasattr(sample_class, 'process')

    def test_get_sample_class__multiple_self_calls(self):                            # Test multiple self calls accessor
        with self.qa as _:
            sample_class = _.get_sample_class__multiple_self_calls()
            assert sample_class is Sample__Multiple_Self_Calls
            assert hasattr(sample_class, 'run')
            assert hasattr(sample_class, 'validate')
            assert hasattr(sample_class, 'transform')
            assert hasattr(sample_class, 'output')

    def test_get_sample_class__chain_calls(self):                                    # Test chain calls class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__chain_calls()
            assert sample_class is Sample__Chain_Calls

    def test_get_sample_class__conditional_calls(self):                              # Test conditional calls accessor
        with self.qa as _:
            sample_class = _.get_sample_class__conditional_calls()
            assert sample_class is Sample__Conditional_Calls

    def test_get_sample_class__deep_calls(self):                                     # Test deep calls class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__deep_calls()
            assert sample_class is Sample__Deep_Calls
            assert hasattr(sample_class, 'level_1')
            assert hasattr(sample_class, 'level_4')

    def test_get_sample_class__recursive(self):                                      # Test recursive class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__recursive()
            assert sample_class is Sample__Recursive
            assert hasattr(sample_class, 'factorial')

    def test_get_sample_class__with_builtins(self):                                  # Test builtins class accessor
        with self.qa as _:
            sample_class = _.get_sample_class__with_builtins()
            assert sample_class is Sample__With_Builtins

    def test_get_sample_class__external_calls(self):                                 # Test external calls accessor
        with self.qa as _:
            sample_class = _.get_sample_class__external_calls()
            assert sample_class is Sample__External_Calls

    def test_get_sample_function__standalone(self):                                  # Test standalone function accessor
        with self.qa as _:
            func = _.get_sample_function__standalone()
            assert func is sample_standalone_function
            assert callable(func)

    def test_get_sample_function__helper(self):                                      # Test helper function accessor
        with self.qa as _:
            func = _.get_sample_function__helper()
            assert func is sample_helper_function
            assert callable(func)

    def test_get_all_sample_classes(self):                                           # Test all sample classes list
        with self.qa as _:
            all_classes = _.get_all_sample_classes()
            assert type(all_classes) is list
            assert len(all_classes)  == 9                                            # 9 sample classes defined
            assert Sample__Simple_Class in all_classes
            assert Sample__Self_Calls   in all_classes
            assert Sample__Deep_Calls   in all_classes

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_ontology(self):                                                  # Test ontology creation
        with self.qa as _:
            ontology = _.create_ontology()
            assert type(ontology)              is Call_Flow__Ontology
            assert ontology.ontology_data      is not None
            assert ontology.taxonomy_data      is not None
            assert ontology.obj()              == __(  _loaded      = True,
                                                       ontology_data = __(ontology_id  = '1079fc5c',
                                                                          ontology_ref = 'call_flow',
                                                                          taxonomy_id  = '8ff7f7e0',
                                                                          version      = '1.0.0',
                                                                          node_types   = __(ce44e48f  = __(node_type_id='ce44e48f', node_type_ref='class',    category_id='9abaaadc'),
                                                                                            _143fb9ef = __(node_type_id='143fb9ef', node_type_ref='method',   category_id='4561e12e'),
                                                                                            _188fe0cb = __(node_type_id='188fe0cb', node_type_ref='function', category_id='4561e12e'),
                                                                                            dc07a3ae  = __(node_type_id='dc07a3ae', node_type_ref='module',   category_id='9abaaadc'),
                                                                                            bd2f2d3e  = __(node_type_id='bd2f2d3e', node_type_ref='external', category_id='61d5c76e')),
                                                                          predicates   = __(_28386687 = __(predicate_id='28386687', predicate_ref='contains',     inverse_id='9ced5f76'),
                                                                                            _9ced5f76 = __(predicate_id='9ced5f76', predicate_ref='contained_by', inverse_id='28386687'),
                                                                                            _35ab2291 = __(predicate_id='35ab2291', predicate_ref='calls',        inverse_id='74372214'),
                                                                                            _74372214 = __(predicate_id='74372214', predicate_ref='called_by',    inverse_id='35ab2291'),
                                                                                            _38e66c6b = __(predicate_id='38e66c6b', predicate_ref='calls_self',   inverse_id=None      ),
                                                                                            _21c9b1b6 = __(predicate_id='21c9b1b6', predicate_ref='calls_chain',  inverse_id=None      )),
                                                                          property_names = __(_2b7607b1 = __(property_name_id='2b7607b1', property_name_ref='qualified_name',   property_type_id='27184299'),
                                                                                              _69a8b10a = __(property_name_id='69a8b10a', property_name_ref='module_name',      property_type_id='27184299'),
                                                                                              e3241d31  = __(property_name_id='e3241d31', property_name_ref='file_path',        property_type_id='27184299'),
                                                                                              fb6e1ec9  = __(property_name_id='fb6e1ec9', property_name_ref='line_number',      property_type_id='c856288a'),
                                                                                              _6229138c = __(property_name_id='6229138c', property_name_ref='call_depth',       property_type_id='c856288a'),
                                                                                              _11cfe2d4 = __(property_name_id='11cfe2d4', property_name_ref='source_code',      property_type_id='34c7b89b'),
                                                                                              _65ad210e = __(property_name_id='65ad210e', property_name_ref='is_entry',         property_type_id='c169bc41'),
                                                                                              dd626c33  = __(property_name_id='dd626c33', property_name_ref='is_external',      property_type_id='c169bc41'),
                                                                                              dba368ef  = __(property_name_id='dba368ef', property_name_ref='is_recursive',     property_type_id='c169bc41'),
                                                                                              _91a093a2 = __(property_name_id='91a093a2', property_name_ref='is_conditional',   property_type_id='c169bc41'),
                                                                                              _30f38a6f = __(property_name_id='30f38a6f', property_name_ref='call_line_number', property_type_id='c856288a')),
                                                                          property_types = __(_27184299 = __(property_type_id='27184299', property_type_ref='string' ),
                                                                                              _34c7b89b = __(property_type_id='34c7b89b', property_type_ref='text'   ),
                                                                                              c856288a  = __(property_type_id='c856288a', property_type_ref='integer'),
                                                                                              c169bc41  = __(property_type_id='c169bc41', property_type_ref='boolean')),
                                                                          edge_rules     = [__(source_type_id='dc07a3ae', predicate_id='28386687', target_type_id='ce44e48f'),
                                                                                            __(source_type_id='dc07a3ae', predicate_id='28386687', target_type_id='188fe0cb'),
                                                                                            __(source_type_id='ce44e48f', predicate_id='28386687', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='35ab2291', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='35ab2291', target_type_id='188fe0cb'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='35ab2291', target_type_id='bd2f2d3e'),
                                                                                            __(source_type_id='188fe0cb', predicate_id='35ab2291', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='188fe0cb', predicate_id='35ab2291', target_type_id='188fe0cb'),
                                                                                            __(source_type_id='188fe0cb', predicate_id='35ab2291', target_type_id='bd2f2d3e'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='38e66c6b', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='21c9b1b6', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='143fb9ef', predicate_id='21c9b1b6', target_type_id='bd2f2d3e'),
                                                                                            __(source_type_id='188fe0cb', predicate_id='21c9b1b6', target_type_id='143fb9ef'),
                                                                                            __(source_type_id='188fe0cb', predicate_id='21c9b1b6', target_type_id='bd2f2d3e')]),
                                                       taxonomy_data = __(taxonomy_id  = '8ff7f7e0',
                                                                          taxonomy_ref = 'call_flow_taxonomy',
                                                                          version      = '1.0.0',
                                                                          root_id      = '073143fe',
                                                                          categories   = __(_073143fe = __(category_id='073143fe', category_ref='code_element', parent_id=None,       child_ids=['9abaaadc', '4561e12e', '61d5c76e']),
                                                                                            _9abaaadc = __(category_id='9abaaadc', category_ref='container',    parent_id='073143fe', child_ids=[]                                 ),
                                                                                            _4561e12e = __(category_id='4561e12e', category_ref='callable',     parent_id='073143fe', child_ids=[]                                 ),
                                                                                            _61d5c76e = __(category_id='61d5c76e', category_ref='reference',    parent_id='073143fe', child_ids=[]                                 ))),
                                                       node_type_ref_to_id = __(_class         = 'ce44e48f', method       = '143fb9ef', function     = '188fe0cb', module       = 'dc07a3ae', external        = 'bd2f2d3e'),
                                                       predicate_ref_to_id = __(contains       = '28386687', contained_by = '9ced5f76', calls        = '35ab2291', called_by    = '74372214', calls_self      = '38e66c6b', calls_chain = '21c9b1b6'),
                                                       prop_name_ref_to_id = __(qualified_name = '2b7607b1', module_name  = '69a8b10a', file_path    = 'e3241d31', line_number  = 'fb6e1ec9', call_depth      = '6229138c', source_code = '11cfe2d4',
                                                                                is_entry       = '65ad210e', is_external  = 'dd626c33', is_recursive = 'dba368ef', is_conditional = '91a093a2', call_line_number = '30f38a6f'),
                                                       prop_type_ref_to_id = __(string         = '27184299', text         = '34c7b89b', integer      = 'c856288a', boolean      = 'c169bc41'),
                                                       category_ref_to_id  = __(code_element   = '073143fe', container    = '9abaaadc', callable     = '4561e12e', reference    = '61d5c76e'))

    def test_get_node_type_id__class(self):                                          # Test class node type ID
        with self.qa as _:
            node_type_id = _.get_node_type_id__class()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.ontology.node_type_id__class())

    def test_get_node_type_id__method(self):                                         # Test method node type ID
        with self.qa as _:
            node_type_id = _.get_node_type_id__method()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.ontology.node_type_id__method())

    def test_get_node_type_id__function(self):                                       # Test function node type ID
        with self.qa as _:
            node_type_id = _.get_node_type_id__function()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.ontology.node_type_id__function())

    def test_get_node_type_id__module(self):                                         # Test module node type ID
        with self.qa as _:
            node_type_id = _.get_node_type_id__module()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.ontology.node_type_id__module())

    def test_get_node_type_id__external(self):                                       # Test external node type ID
        with self.qa as _:
            node_type_id = _.get_node_type_id__external()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.ontology.node_type_id__external())

    def test_get_predicate_id__contains(self):                                       # Test contains predicate ID
        with self.qa as _:
            predicate_id = _.get_predicate_id__contains()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.ontology.predicate_id__contains())

    def test_get_predicate_id__calls(self):                                          # Test calls predicate ID
        with self.qa as _:
            predicate_id = _.get_predicate_id__calls()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.ontology.predicate_id__calls())

    def test_get_predicate_id__calls_self(self):                                     # Test calls_self predicate ID
        with self.qa as _:
            predicate_id = _.get_predicate_id__calls_self()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.ontology.predicate_id__calls_self())

    def test_get_predicate_id__calls_chain(self):                                    # Test calls_chain predicate ID
        with self.qa as _:
            predicate_id = _.get_predicate_id__calls_chain()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.ontology.predicate_id__calls_chain())

    # ═══════════════════════════════════════════════════════════════════════════
    # Config Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_config__default(self):                                           # Test default config creation
        with self.qa as _:
            config = _.create_config__default()
            assert type(config)           is Schema__Call_Flow__Config
            assert config.max_depth       == 10
            assert config.include_builtins == False
            assert config.include_external == True

            assert config.obj() == __(max_depth         = 10          ,
                                      include_external  = True        ,
                                      include_builtins  = False       ,
                                      include_source    = False       ,
                                      filter_module     = None        ,
                                      ontology_ref      = 'call_flow' ,
                                      target_method     = ''          )

    def test_create_config__include_builtins(self):                                  # Test builtins config
        with self.qa as _:
            config = _.create_config__include_builtins()
            assert type(config)            is Schema__Call_Flow__Config
            assert config.include_builtins == True
            assert config.obj() == __(max_depth         = 10          ,
                                      include_external  = True        ,
                                      include_builtins  = True        ,
                                      include_source    = False       ,
                                      filter_module     = None        ,
                                      ontology_ref      = 'call_flow' ,
                                      target_method     = ''          )

    def test_create_config__exclude_external(self):                                  # Test exclude external config
        with self.qa as _:
            config = _.create_config__exclude_external()
            assert type(config)            is Schema__Call_Flow__Config
            assert config.include_external == False

    def test_create_config__shallow(self):                                           # Test shallow depth config
        with self.qa as _:
            config = _.create_config__shallow()
            assert type(config)     is Schema__Call_Flow__Config
            assert config.max_depth == 1

    def test_create_config__deep(self):                                              # Test deep depth config
        with self.qa as _:
            config = _.create_config__deep()
            assert type(config)     is Schema__Call_Flow__Config
            assert config.max_depth == 20

    def test_create_config__full(self):                                              # Test full options config
        with self.qa as _:
            config = _.create_config__full()
            assert type(config)            is Schema__Call_Flow__Config
            assert config.max_depth        == 20
            assert config.include_builtins == True
            assert config.include_external == True

    # ═══════════════════════════════════════════════════════════════════════════
    # Builder Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_builder(self):                                                   # Test basic builder creation
        with self.qa as _:
            builder = _.create_builder()
            assert type(builder)          is Call_Flow__Builder
            assert builder.ontology       is not None
            assert builder.name_to_node_id == {}
            assert builder.obj()           == __(ontology = __SKIP__,
                                                 builder=__(ontology_registry=None,
                                                            graph=__(graph_id_source=None,
                                                                     rule_set_id=None,
                                                                     graph_id='',
                                                                     ontology_id='1079fc5c',
                                                                     nodes=__(),
                                                                     edges=[])),
                                                 name_to_node_id=__(),
                                                 node_properties=__())

    def test_create_builder_with_class(self):                                        # Test builder with class
        with self.qa as _:
            builder = _.create_builder_with_class()
            assert type(builder)                    is Call_Flow__Builder
            assert 'test.TestClass'                 in builder.name_to_node_id
            assert 'test.TestClass.method_a'        in builder.name_to_node_id
            assert 'test.TestClass.method_b'        in builder.name_to_node_id

    def test_create_builder_with_class__custom_names(self):                          # Test builder with custom names
        with self.qa as _:
            builder = _.create_builder_with_class(class_name   = 'my.Custom'        ,
                                                  method_names = ['foo', 'bar', 'baz'])
            assert 'my.Custom'     in builder.name_to_node_id
            assert 'my.Custom.foo' in builder.name_to_node_id
            assert 'my.Custom.bar' in builder.name_to_node_id
            assert 'my.Custom.baz' in builder.name_to_node_id

    def test_create_builder_with_self_calls(self):                                   # Test builder with self calls
        with self.qa as _:
            builder = _.create_builder_with_self_calls()
            graph   = builder.build()
            assert type(builder) is Call_Flow__Builder
            assert len(list(graph.nodes.keys())) == 3                                # class + 2 methods
            assert len(graph.edges)              == 3                                # 2 contains + 1 calls_self

    def test_create_graph__empty(self):                                              # Test empty graph creation
        with self.qa as _:
            graph = _.create_graph__empty()
            assert type(graph)                   is Schema__Semantic_Graph
            assert len(list(graph.nodes.keys())) == 0
            assert len(graph.edges)              == 0

    def test_create_graph__simple_class(self):                                       # Test simple class graph
        with self.qa as _:
            graph = _.create_graph__simple_class()
            assert type(graph)                   is Schema__Semantic_Graph
            assert len(list(graph.nodes.keys())) == 3                                # class + 2 methods
            assert len(graph.edges)              >= 2                                # at least 2 contains

    def test_create_graph__with_self_calls(self):                                    # Test self calls graph
        with self.qa as _:
            graph = _.create_graph__with_self_calls()
            assert type(graph)                   is Schema__Semantic_Graph
            assert len(list(graph.nodes.keys())) == 3
            assert len(graph.edges)              == 3

    # ═══════════════════════════════════════════════════════════════════════════
    # Analyzer Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_analyzer__default(self):                                         # Test default analyzer creation
        with self.qa as _:
            analyzer = _.create_analyzer__default()
            assert type(analyzer)        is Call_Flow__Analyzer
            assert analyzer.config       is not None
            assert analyzer.builder      is not None

    def test_create_analyzer__with_config(self):                                     # Test analyzer with custom config
        with self.qa as _:
            config   = _.create_config__shallow()
            analyzer = _.create_analyzer__with_config(config)
            assert type(analyzer)        is Call_Flow__Analyzer
            assert analyzer.config       is config
            assert analyzer.config.max_depth == 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Analysis Result Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_result__simple_class(self):                                      # Test simple class result
        with self.qa as _:
            result = _.create_result__simple_class()
            assert type(result)        is Schema__Call_Flow__Result
            assert result.total_nodes  >= 3                                          # class + 2 methods
            assert result.total_edges  >= 2                                          # contains edges
            assert 'Sample__Simple_Class' in result.entry_point

    def test_create_result__self_calls(self):                                        # Test self calls result
        with self.qa as _:
            result = _.create_result__self_calls()
            assert type(result)       is Schema__Call_Flow__Result
            assert result.total_nodes == 3                                           # class + 2 methods
            assert result.total_edges >= 2
            assert 'Sample__Self_Calls' in result.entry_point

    def test_create_result__multiple_self_calls(self):                               # Test multiple self calls result
        with self.qa as _:
            result = _.create_result__multiple_self_calls()
            assert type(result)       is Schema__Call_Flow__Result
            assert result.total_nodes == 5                                           # class + 4 methods
            assert 'Sample__Multiple_Self_Calls' in result.entry_point

    def test_create_result__chain_calls(self):                                       # Test chain calls result
        with self.qa as _:
            result = _.create_result__chain_calls()
            assert type(result) is Schema__Call_Flow__Result
            assert 'Sample__Chain_Calls' in result.entry_point

    def test_create_result__deep_calls(self):                                        # Test deep calls result
        with self.qa as _:
            result = _.create_result__deep_calls()
            assert type(result)       is Schema__Call_Flow__Result
            assert result.total_nodes == 5                                           # class + 4 level methods
            assert 'Sample__Deep_Calls' in result.entry_point

    def test_create_result__function(self):                                          # Test function result
        with self.qa as _:
            result = _.create_result__function()
            assert type(result) is Schema__Call_Flow__Result
            assert 'sample_standalone_function' in result.entry_point

    def test_create_result__with_config(self):                                       # Test result with custom config
        with self.qa as _:
            config = _.create_config__shallow()
            result = _.create_result__with_config(Sample__Deep_Calls, config)
            assert type(result)              is Schema__Call_Flow__Result
            assert result.max_depth_reached  <= 2                                    # Limited by shallow config

    # ═══════════════════════════════════════════════════════════════════════════
    # Exporter Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_exporter__default(self):                                         # Test default exporter
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__default(result)
            assert type(exporter)     is Call_Flow__Exporter__Mermaid
            assert exporter.direction == 'TD'
            assert exporter.result    is result

    def test_create_exporter__left_right(self):                                      # Test LR direction exporter
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__left_right(result)
            assert type(exporter)     is Call_Flow__Exporter__Mermaid
            assert exporter.direction == 'LR'

    def test_create_exporter__no_contains(self):                                     # Test exporter without contains
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__no_contains(result)
            assert type(exporter)       is Call_Flow__Exporter__Mermaid
            assert exporter.show_contains == False

    # ═══════════════════════════════════════════════════════════════════════════
    # Expected Mermaid Output Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_get_expected_mermaid__header_td(self):                                  # Test TD header expectation
        with self.qa as _:
            expected = _.get_expected_mermaid__header_td()
            assert expected == 'flowchart TD'

    def test_get_expected_mermaid__header_lr(self):                                  # Test LR header expectation
        with self.qa as _:
            expected = _.get_expected_mermaid__header_lr()
            assert expected == 'flowchart LR'

    def test_get_expected_mermaid__self_call_arrow(self):                            # Test self call arrow
        with self.qa as _:
            expected = _.get_expected_mermaid__self_call_arrow()
            assert expected == '-.->'

    def test_get_expected_mermaid__self_call_label(self):                            # Test self call label
        with self.qa as _:
            expected = _.get_expected_mermaid__self_call_label()
            assert expected == '|self|'

    def test_get_expected_mermaid__chain_call_arrow(self):                           # Test chain call arrow
        with self.qa as _:
            expected = _.get_expected_mermaid__chain_call_arrow()
            assert expected == '==>'

    def test_get_expected_mermaid__contains_arrow(self):                             # Test contains arrow
        with self.qa as _:
            expected = _.get_expected_mermaid__contains_arrow()
            assert expected == '-->'

    # ═══════════════════════════════════════════════════════════════════════════
    # Storage Factory Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_storage(self):                                                   # Test storage creation
        with self.qa as _:
            storage = _.create_storage()
            assert type(storage) is Call_Flow__Storage

    def test_create_serialized_result(self):                                         # Test serialized result
        with self.qa as _:
            json_str = _.create_serialized_result()
            assert type(json_str)      is str
            assert 'entry_point'       in json_str
            assert 'Sample__Self_Calls' in json_str

    # ═══════════════════════════════════════════════════════════════════════════
    # Complete Fixture Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_create_complete_fixture__simple(self):                                  # Test simple fixture
        with self.qa as _:
            fixture = _.create_complete_fixture__simple()
            assert 'target'                   in fixture
            assert fixture['target']          is Sample__Simple_Class
            assert type(fixture['config'])    is Schema__Call_Flow__Config
            assert type(fixture['result'])    is Schema__Call_Flow__Result
            assert type(fixture['exporter'])  is Call_Flow__Exporter__Mermaid
            assert type(fixture['mermaid'])   is str
            assert type(fixture['ontology'])  is Call_Flow__Ontology

    def test_create_complete_fixture__self_calls(self):                              # Test self calls fixture
        with self.qa as _:
            fixture = _.create_complete_fixture__self_calls()
            assert fixture['target'] is Sample__Self_Calls
            assert 'flowchart TD'    in fixture['mermaid']

    def test_create_complete_fixture__multiple_self_calls(self):                     # Test multiple self calls fixture
        with self.qa as _:
            fixture = _.create_complete_fixture__multiple_self_calls()
            assert fixture['target'] is Sample__Multiple_Self_Calls
            assert fixture['result'].total_nodes == 5

    def test_create_complete_fixture__deep_calls(self):                              # Test deep calls fixture
        with self.qa as _:
            fixture = _.create_complete_fixture__deep_calls()
            assert fixture['target'] is Sample__Deep_Calls
            assert fixture['result'].total_nodes == 5

    def test_create_all_fixtures(self):                                              # Test all fixtures creation
        with self.qa as _:
            all_fixtures = _.create_all_fixtures()
            assert 'simple'                    in all_fixtures
            assert 'self_calls'                in all_fixtures
            assert 'multiple_self_calls'       in all_fixtures
            assert 'deep_calls'                in all_fixtures
            assert len(all_fixtures)           == 4

    # ═══════════════════════════════════════════════════════════════════════════
    # Assertion Helper Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_assert_result_has_nodes(self):                                          # Test nodes assertion
        with self.qa as _:
            result = _.create_result__simple_class()
            assert _.assert_result_has_nodes(result, min_count=3) == True
            assert _.assert_result_has_nodes(result, min_count=100) == False

    def test_assert_result_has_edges(self):                                          # Test edges assertion
        with self.qa as _:
            result = _.create_result__simple_class()
            assert _.assert_result_has_edges(result, min_count=2) == True
            assert _.assert_result_has_edges(result, min_count=100) == False

    def test_assert_result_has_entry_point(self):                                    # Test entry point assertion
        with self.qa as _:
            result = _.create_result__simple_class()
            assert _.assert_result_has_entry_point(result, 'Sample__Simple_Class') == True
            assert _.assert_result_has_entry_point(result, 'NonExistent') == False

    def test_assert_mermaid_has_header(self):                                        # Test mermaid header assertion
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__default(result)
            mermaid  = exporter.export()
            assert _.assert_mermaid_has_header(mermaid, 'TD') == True
            assert _.assert_mermaid_has_header(mermaid, 'LR') == False

    def test_assert_mermaid_has_node(self):                                          # Test mermaid node assertion
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__default(result)
            mermaid  = exporter.export()
            assert _.assert_mermaid_has_node(mermaid, 'Sample__Self_Calls') == True

    def test_assert_mermaid_has_self_call(self):                                     # Test self call assertion
        with self.qa as _:
            result   = _.create_result__self_calls()
            exporter = _.create_exporter__default(result)
            mermaid  = exporter.export()
            assert _.assert_mermaid_has_self_call(mermaid) == True

    def test_count_edges_by_predicate(self):                                         # Test edge counting
        with self.qa as _:
            result       = _.create_result__self_calls()
            contains_id  = _.get_predicate_id__contains()
            calls_self_id = _.get_predicate_id__calls_self()

            contains_count   = _.count_edges_by_predicate(result, contains_id)
            calls_self_count = _.count_edges_by_predicate(result, calls_self_id)

            assert contains_count   >= 2                                             # At least 2 contains edges
            assert calls_self_count >= 1                                             # At least 1 self call

    def test_get_node_names(self):                                                   # Test node name extraction
        with self.qa as _:
            result = _.create_result__simple_class()
            names  = _.get_node_names(result)
            assert type(names)                is list
            assert 'Sample__Simple_Class'     in names or any('Simple_Class' in n for n in names)

    def test_get_edge_count(self):                                                   # Test edge count extraction
        with self.qa as _:
            result = _.create_result__simple_class()
            count  = _.get_edge_count(result)
            assert type(count) is int
            assert count       >= 2


# ═══════════════════════════════════════════════════════════════════════════════
# Sample Class Behavior Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_Sample_Classes(TestCase):                                                 # Test sample classes work correctly

    def test_Sample__Simple_Class(self):                                             # Test simple class methods
        instance = Sample__Simple_Class()
        assert instance.method_a() == 1
        assert instance.method_b() == 2

    def test_Sample__Self_Calls(self):                                               # Test self call class
        instance = Sample__Self_Calls()
        assert instance.do_work(5) == 10                                             # 5 * 2 = 10
        assert instance.process(3) == 6                                              # 3 * 2 = 6

    def test_Sample__Multiple_Self_Calls(self):                                      # Test multiple self calls
        instance = Sample__Multiple_Self_Calls()
        result   = instance.run([1, None, 2, 3])
        assert result['count'] == 3                                                  # None filtered out
        assert result['items'] == [2, 4, 6]                                          # [1,2,3] * 2

    def test_Sample__Deep_Calls(self):                                               # Test deep call chain
        instance = Sample__Deep_Calls()
        assert instance.level_1() == "deep"
        assert instance.level_4() == "deep"

    def test_Sample__Recursive(self):                                                # Test recursive calls
        instance = Sample__Recursive()
        assert instance.factorial(5) == 120                                          # 5! = 120
        assert instance.factorial(1) == 1

    def test_sample_standalone_function(self):                                       # Test standalone function
        result = sample_standalone_function(2, 3)
        assert result == 23                                                          # (2 * 10) + 3 = 23

    def test_sample_helper_function(self):                                           # Test helper function
        result = sample_helper_function(5)
        assert result == 50                                                          # 5 * 10 = 50


# ═══════════════════════════════════════════════════════════════════════════════
# Integration Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_Integration(TestCase):                                                    # Integration tests for QA patterns

    @classmethod
    def setUpClass(cls):
        cls.qa = QA__Call_Flow__Test_Data()

    def test_full_pipeline__analyze_export_serialize(self):                          # Test complete pipeline
        with self.qa as _:
            # Analyze
            result = _.create_result__self_calls()
            assert result.total_nodes >= 3

            # Export
            exporter = _.create_exporter__default(result)
            mermaid  = exporter.export()
            assert 'flowchart TD' in mermaid

            # Serialize
            storage  = _.create_storage()
            json_str = storage.to_json(result)
            loaded   = storage.from_json(json_str)
            assert loaded.total_nodes == result.total_nodes

    def test_fixture_consistency(self):                                              # Test fixture data consistency
        with self.qa as _:
            fixture = _.create_complete_fixture__self_calls()

            # Verify fixture components are consistent
            assert fixture['result'].graph is fixture['exporter'].graph
            assert fixture['target'] is Sample__Self_Calls

            # Verify mermaid matches result
            mermaid = fixture['mermaid']
            assert _.assert_mermaid_has_node(mermaid, 'Sample__Self_Calls')

    def test_all_sample_classes_analyzable(self):                                    # Test all samples can be analyzed
        with self.qa as _:
            for sample_class in _.get_all_sample_classes():
                with Call_Flow__Analyzer() as analyzer:
                    result = analyzer.analyze(sample_class)
                    assert result.total_nodes >= 1                                   # At least the class itself
                    assert sample_class.__name__ in result.entry_point