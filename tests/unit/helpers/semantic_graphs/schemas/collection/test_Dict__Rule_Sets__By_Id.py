# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Rule_Sets__By_Id - Tests for rule set dictionary typed collection
#
# Updated for Brief 3.7:
#   - Rule_Set_Id is now Obj_Id-based
#   - Added rule_set_ref for human-readable name
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                          import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id     import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Cardinality   import List__Rules__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity  import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref               import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref               import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                 import Schema__Rule_Set
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                       import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                  import Type_Safe__Dict


class test_Dict__Rule_Sets__By_Id(TestCase):                                           # Test rule set dictionary collection

    def test__init__(self):                                                            # Test initialization
        with Dict__Rule_Sets__By_Id() as _:
            assert type(_)               is Dict__Rule_Sets__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Rule_Set_Id
            assert _.expected_value_type is Schema__Rule_Set
            assert len(_)                == 0

    def test__add_and_retrieve(self):                                                  # Test adding and retrieving rule sets
        with Dict__Rule_Sets__By_Id() as _:
            rule_set_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:test'))
            rule_set    = Schema__Rule_Set(rule_set_id        = rule_set_id                  ,
                                           rule_set_ref       = Rule_Set_Ref('test_rules')   ,
                                           ontology_ref       = Ontology_Ref('test')         ,
                                           transitivity_rules = List__Rules__Transitivity()  ,
                                           cardinality_rules  = List__Rules__Cardinality()   )
            _[rule_set_id] = rule_set

            assert len(_)             == 1
            assert _[rule_set_id]     is rule_set
            assert _.get(rule_set_id) is rule_set

    def test__multiple_rule_sets(self):                                                # Test multiple rule set operations
        with Dict__Rule_Sets__By_Id() as _:
            rs1_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:rs1'))
            rs2_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:rs2'))
            rs1    = Schema__Rule_Set(rule_set_id        = rs1_id                            ,
                                      rule_set_ref       = Rule_Set_Ref('rules_1')           ,
                                      ontology_ref       = Ontology_Ref('ont1')              ,
                                      transitivity_rules = List__Rules__Transitivity()       ,
                                      cardinality_rules  = List__Rules__Cardinality()        )
            rs2    = Schema__Rule_Set(rule_set_id        = rs2_id                            ,
                                      rule_set_ref       = Rule_Set_Ref('rules_2')           ,
                                      ontology_ref       = Ontology_Ref('ont2')              ,
                                      transitivity_rules = List__Rules__Transitivity()       ,
                                      cardinality_rules  = List__Rules__Cardinality()        )

            _[rs1_id] = rs1
            _[rs2_id] = rs2

            assert len(_)    == 2
            assert _[rs1_id] is rs1
            assert _[rs2_id] is rs2

    def test__iteration(self):                                                         # Test iteration over rule sets
        with Dict__Rule_Sets__By_Id() as _:
            rs1_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:iter1'))
            rs2_id = Rule_Set_Id(Obj_Id.from_seed('test:rules:iter2'))
            rs1    = Schema__Rule_Set(rule_set_id        = rs1_id                            ,
                                      rule_set_ref       = Rule_Set_Ref('rules_1')           ,
                                      ontology_ref       = Ontology_Ref('ont1')              ,
                                      transitivity_rules = List__Rules__Transitivity()       ,
                                      cardinality_rules  = List__Rules__Cardinality()        )
            rs2    = Schema__Rule_Set(rule_set_id        = rs2_id                            ,
                                      rule_set_ref       = Rule_Set_Ref('rules_2')           ,
                                      ontology_ref       = Ontology_Ref('ont2')              ,
                                      transitivity_rules = List__Rules__Transitivity()       ,
                                      cardinality_rules  = List__Rules__Cardinality()        )

            _[rs1_id] = rs1
            _[rs2_id] = rs2

            keys   = list(_.keys())
            values = list(_.values())

            assert len(keys)   == 2
            assert len(values) == 2