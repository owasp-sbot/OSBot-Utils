# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Ontology - Tests for ontology loading and ID generation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id

from osbot_utils.helpers.python_call_flow.Call_Flow__Ontology                        import Call_Flow__Ontology
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data


class test_Call_Flow__Ontology(TestCase):                                            # Test ontology class

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.qa       = QA__Call_Flow__Test_Data()
        cls.ontology = cls.qa.create_ontology()

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Ontology() as _:
            assert type(_)         is Call_Flow__Ontology
            assert base_classes(_) == [Type_Safe, object]
            assert _.ontology_data == {}
            assert _.taxonomy_data == {}

    def test__setup(self):                                                           # Test setup loads data
        with Call_Flow__Ontology() as _:
            result = _.setup()
            assert result              is _                                          # Returns self (fluent)
            assert _.ontology_data     is not None
            assert _.taxonomy_data     is not None
            assert _.obj()             == __(  _loaded      = True,
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


    def test__ontology_id(self):                                                     # Test ontology ID generation
        with self.ontology as _:
            ontology_id = _.ontology_id()
            assert type(ontology_id) is Ontology_Id
            assert str(ontology_id)  != ''

    def test__ontology_id__deterministic(self):                                      # Test ontology ID is deterministic
        o1 = Call_Flow__Ontology().setup()
        o2 = Call_Flow__Ontology().setup()
        assert str(o1.ontology_id()) == str(o2.ontology_id())                        # Same seed = same ID

    def test__node_type_id__class(self):                                             # Test class node type ID
        with self.ontology as _:
            node_type_id = _.node_type_id__class()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.qa.get_node_type_id__class())

    def test__node_type_id__method(self):                                            # Test method node type ID
        with self.ontology as _:
            node_type_id = _.node_type_id__method()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.qa.get_node_type_id__method())

    def test__node_type_id__function(self):                                          # Test function node type ID
        with self.ontology as _:
            node_type_id = _.node_type_id__function()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.qa.get_node_type_id__function())

    def test__node_type_id__module(self):                                            # Test module node type ID
        with self.ontology as _:
            node_type_id = _.node_type_id__module()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.qa.get_node_type_id__module())

    def test__node_type_id__external(self):                                          # Test external node type ID
        with self.ontology as _:
            node_type_id = _.node_type_id__external()
            assert type(node_type_id) is Node_Type_Id
            assert str(node_type_id)  == str(self.qa.get_node_type_id__external())

    def test__predicate_id__contains(self):                                          # Test contains predicate ID
        with self.ontology as _:
            predicate_id = _.predicate_id__contains()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.qa.get_predicate_id__contains())

    def test__predicate_id__calls(self):                                             # Test calls predicate ID
        with self.ontology as _:
            predicate_id = _.predicate_id__calls()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.qa.get_predicate_id__calls())

    def test__predicate_id__calls_self(self):                                        # Test calls_self predicate ID
        with self.ontology as _:
            predicate_id = _.predicate_id__calls_self()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.qa.get_predicate_id__calls_self())

    def test__predicate_id__calls_chain(self):                                       # Test calls_chain predicate ID
        with self.ontology as _:
            predicate_id = _.predicate_id__calls_chain()
            assert type(predicate_id) is Predicate_Id
            assert str(predicate_id)  == str(self.qa.get_predicate_id__calls_chain())

    def test__node_type_ids__all_unique(self):                                       # Test all node type IDs unique
        with self.ontology as _:
            ids = [str(_.node_type_id__class())                                      ,
                   str(_.node_type_id__method())                                     ,
                   str(_.node_type_id__function())                                   ,
                   str(_.node_type_id__module())                                     ,
                   str(_.node_type_id__external())                                   ]
            assert len(ids) == len(set(ids))

    def test__predicate_ids__all_unique(self):                                       # Test all predicate IDs unique
        with self.ontology as _:
            ids = [str(_.predicate_id__contains())                                   ,
                   str(_.predicate_id__calls())                                      ,
                   str(_.predicate_id__calls_self())                                 ,
                   str(_.predicate_id__calls_chain())                                ]
            assert len(ids) == len(set(ids))