# ═══════════════════════════════════════════════════════════════════════════════
# Test Rule__Engine - Tests for rule engine with typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.rule.Rule__Engine                          import Rule__Engine
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id  import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id             import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set              import Schema__Rule_Set

# todo:
#     :
#       - the dict from test__load_from_dict below should come from the QA_...testing... file

class test_Rule__Engine(TestCase):                                                   # Test rule engine

    def setUp(self):                                                                 # Fresh engine for each test
        self.engine = Rule__Engine()

    def test__init__(self):                                                          # Test basic creation
        with Rule__Engine() as _:
            assert type(_.cache) is Dict__Rule_Sets__By_Id
            assert len(_.cache)  == 0

    def test__load_from_dict(self):                                                  # Test loading from dictionary
        data = {'rule_set_id' : 'test_rules'                                         ,
                'ontology_ref': 'test_ontology'                                      ,
                'version'     : '2.0.0'                                              ,
                'description' : 'Test rule set'                                      ,
                'transitivity_rules': [{'source_type': 'class'                       ,
                                        'verb'       : 'inherits_from'               ,
                                        'target_type': 'class'                       }],
                'cardinality_rules': [{'source_type' : 'method'                      ,
                                       'verb'        : 'in'                          ,
                                       'target_type' : 'class'                       ,
                                       'min_targets' : 1                             ,
                                       'max_targets' : 1                             ,
                                       'description' : 'Method in one class'         },
                                      {'source_type' : 'class'                       ,
                                       'verb'        : 'has'                         ,
                                       'target_type' : 'method'                      ,
                                       'min_targets' : 0                             ,
                                       'max_targets' : None                          ,
                                       'description' : 'Class can have any methods'  }]}

        with self.engine as _:
            rule_set = _.load_from_dict(data)

            assert type(rule_set)             is Schema__Rule_Set
            assert str(rule_set.rule_set_id)  == 'test_rules'
            assert str(rule_set.ontology_ref) == 'test_ontology'
            assert len(rule_set.transitivity_rules) == 1
            assert len(rule_set.cardinality_rules)  == 2

    def test__get_and_register(self):                                                # Test get and register operations
        with self.engine as _:
            assert _.get('unknown') is None

            rule_set = Schema__Rule_Set(rule_set_id        = Rule_Set_Id('manual'),
                                        ontology_ref       = Ontology_Id('test') ,
                                        transitivity_rules = []                  ,
                                        cardinality_rules  = []                  )
            _.register(rule_set)

            assert _.get('manual') is rule_set

    def test__list_rule_sets(self):                                                  # Test listing rule sets
        with self.engine as _:
            assert _.list_rule_sets() == []

            _.load_from_dict({'rule_set_id': 'rs1', 'ontology_ref': 'o1',
                             'transitivity_rules': [], 'cardinality_rules': []})
            _.load_from_dict({'rule_set_id': 'rs2', 'ontology_ref': 'o2',
                             'transitivity_rules': [], 'cardinality_rules': []})

            rule_sets = _.list_rule_sets()
            assert len(rule_sets) == 2
            assert 'rs1' in rule_sets
            assert 'rs2' in rule_sets

    def test__clear(self):                                                           # Test cache clearing
        with self.engine as _:
            _.load_from_dict({'rule_set_id': 'test', 'ontology_ref': 'o',
                             'transitivity_rules': [], 'cardinality_rules': []})
            assert len(_.cache) == 1

            _.clear()
            assert len(_.cache) == 0

    def test__cache_type(self):                                                      # Test cache is properly typed
        with self.engine as _:
            _.load_from_dict({'rule_set_id': 'test', 'ontology_ref': 'o',
                             'transitivity_rules': [], 'cardinality_rules': []})

            assert type(_.cache) is Dict__Rule_Sets__By_Id
            assert type(_.cache['test']) is Schema__Rule_Set