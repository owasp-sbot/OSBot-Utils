import re
import pytest
from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                 import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe


class test_Ontology__Registry(TestCase):                                             # Test ontology registry

    def setUp(self):                                                                 # Fresh registry for each test
        self.registry = Ontology__Registry()

    def test__init__(self):                                                          # Test basic creation
        with Ontology__Registry() as _:
            assert type(_.cache) is Dict__Ontologies__By_Id
            assert _.cache       == {}

    def test__load_from_dict__simple(self):                                          # Test loading minimal ontology
        data = { 'ontology_id': 'simple_ontology'     ,
                 'version'    : '1.0.0'               ,
                 'description': 'Simple test ontology',
                 'node_types' : {}                    }

        with self.registry as _:
            ontology = _.load_from_dict(data)

            assert type(ontology)            is Schema__Ontology
            assert str(ontology.ontology_id) == 'simple_ontology'
            assert str(ontology.version)     == '1.0.0'
            assert str(ontology.description) == 'Simple test ontology'
            assert ontology.node_types       == {}

    def test__load_from_dict__with_node_types(self):                                 # Test loading with relationships
        data = {
            'ontology_id': 'test_ontology'                                           ,
            'version'    : '2.0.0'                                                   ,
            'description': 'Test ontology with node types'                           ,
            'node_types' : {
                'package': {
                    'description' : 'Python package'                                 ,
                    'relationships': {
                        'has': {
                            'inverse': 'in'                                          ,
                            'targets': ['package', 'module']                         ,
                        }
                    }
                }                                                                    ,
                'module': {
                    'description' : 'Python module'                                  ,
                    'relationships': {
                        'defines': {
                            'inverse': 'defined_in'                                  ,
                            'targets': ['class', 'function']                         ,
                        }                                                            ,
                        'imports': {
                            'inverse': 'imported_by'                                 ,
                            'targets': ['module']                                    ,
                        }
                    }
                }                                                                    ,
                'class': {
                    'description' : 'Python class'                                   ,
                    'relationships': {}
                }                                                                    ,
                'function': {
                    'description' : 'Python function'                                ,
                    'relationships': {}
                }                                                                    ,
            }
        }

        with self.registry as _:
            ontology = _.load_from_dict(data)

            assert len(ontology.node_types) == 4                                     # Check node types

            assert ontology.valid_edge('package', 'has', 'module')    is True        # Check relationships
            assert ontology.valid_edge('package', 'has', 'package')   is True
            assert ontology.valid_edge('module', 'defines', 'class')  is True
            assert ontology.valid_edge('module', 'defines', 'function') is True
            assert ontology.valid_edge('module', 'imports', 'module') is True

            assert ontology.valid_edge('package', 'has', 'class')     is False       # Invalid edges
            assert ontology.valid_edge('class', 'defines', 'function') is False

            assert ontology.get_inverse_verb('module', 'defines') == 'defined_in'    # Check inverses

    def test__load_from_dict__is_cached(self):                                       # Test ontology is cached after load
        data = {'ontology_id': 'cached_test', 'node_types': {}}

        with self.registry as _:
            ontology = _.load_from_dict(data)
            cached   = _.get('cached_test')

            assert cached is ontology                                                # Same instance
            assert 'cached_test' in _.list_ontologies()

    def test__get__returns_none_for_unknown(self):                                   # Test missing ontology lookup
        with self.registry as _:
            assert _.get('unknown')      is None
            assert _.get('nonexistent')  is None
            assert _.get('')             is None

    def test__register(self):                                                        # Test manual registration
        ontology = Schema__Ontology(
            ontology_id = Ontology_Id('manual_ontology')                              ,
            version     = '1.0.0'                                                    ,
            node_types  = {}                                                         ,
        )

        with self.registry as _:
            _.register(ontology)

            assert _.get('manual_ontology') is ontology
            assert 'manual_ontology' in _.list_ontologies()

    def test__list_ontologies(self):                                                 # Test listing all ontologies
        with self.registry as _:
            assert _.list_ontologies() == []                                         # Initially empty

            _.load_from_dict({'ontology_id': 'ont1', 'node_types': {}})
            _.load_from_dict({'ontology_id': 'ont2', 'node_types': {}})
            _.load_from_dict({'ontology_id': 'ont3', 'node_types': {}})

            ontologies = _.list_ontologies()
            assert len(ontologies) == 3
            assert 'ont1' in ontologies
            assert 'ont2' in ontologies
            assert 'ont3' in ontologies

    def test__clear(self):                                                           # Test cache clearing
        with self.registry as _:
            _.load_from_dict({'ontology_id': 'test1', 'node_types': {}})
            _.load_from_dict({'ontology_id': 'test2', 'node_types': {}})

            assert len(_.cache) == 2

            _.clear()

            assert len(_.cache) == 0
            assert _.get('test1') is None
            assert _.get('test2') is None

    def test__load_from_dict__preserves_taxonomy_ref(self):                          # Test taxonomy_ref is parsed
        data = {
            'ontology_id' : 'with_taxonomy'                                          ,
            'taxonomy_ref': 'code_elements'                                          ,
            'node_types'  : {
                'class': {
                    'description' : 'Python class'                                   ,
                    'taxonomy_ref': 'code_unit'                                      ,
                    'relationships': {}
                }
            }
        }

        with self.registry as _:
            ontology = _.load_from_dict(data)

            assert str(ontology.taxonomy_ref) == 'code_elements'
            assert str(ontology.node_types['class'].taxonomy_ref) == 'code_unit'

    def test__overwrite_existing(self):                                              # Test loading same ID overwrites
        data_v1 = {'ontology_id': 'versioned', 'version': '1.0.0', 'node_types': {}}
        data_v2 = {'ontology_id': 'versioned', 'version': '2.0.0', 'node_types': {}}

        with self.registry as _:
            v1 = _.load_from_dict(data_v1)
            assert str(_.get('versioned').version) == '1.0.0'

            v2 = _.load_from_dict(data_v2)
            assert str(_.get('versioned').version) == '2.0.0'

            assert len(_.list_ontologies()) == 1                                     # Still just one entry


    def test__type_safe__check_optional_behaviour(self):
        @type_safe
        def an_method_1(value: str) -> str:
            return value

        @type_safe
        def an_method_2(value: str=None) -> str:
            return value

        @type_safe
        def an_method_3(value: str) -> str:
            return None


        assert an_method_1('abc') == 'abc'
        assert an_method_2('abc') == 'abc'
        assert an_method_3('abc') is None

        assert an_method_2(None ) is None

        error_message_1 = "Parameter 'value' is not optional but got None"
        with pytest.raises(ValueError, match=error_message_1):
            an_method_1(None)

        error_message_2 = "Parameter 'value' expected type <class 'str'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            an_method_1(42)

        error_message_2 = "Parameter 'value' expected type <class 'str'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            an_method_3(42)

        error_message_2 = "Parameter 'value' expected type <class 'str'>, but got <class 'int'>"
        with pytest.raises(ValueError, match=re.escape(error_message_2)):
            an_method_3(42)

