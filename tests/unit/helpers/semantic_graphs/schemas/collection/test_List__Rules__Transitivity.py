# ═══════════════════════════════════════════════════════════════════════════════
# Test List__Rules__Transitivity - Tests for transitivity rule list typed collection
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Rules__Transitivity import List__Rules__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity     import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class test_List__Rules__Transitivity(TestCase):                                      # Test transitivity rule list collection

    def test__init__(self):                                                          # Test initialization
        with List__Rules__Transitivity() as _:
            assert type(_)         is List__Rules__Transitivity
            assert isinstance(_, Type_Safe__List)
            assert _.expected_type is Schema__Rule__Transitivity
            assert len(_)          == 0

    def test__append_and_retrieve(self):                                             # Test appending and retrieving rules
        with List__Rules__Transitivity() as _:
            rule = Schema__Rule__Transitivity(source_type = Node_Type_Id('class'),
                                              verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                              target_type = Node_Type_Id('class'))
            _.append(rule)

            assert len(_) == 1
            assert _[0]   is rule

    def test__multiple_rules(self):                                                  # Test multiple rule operations
        with List__Rules__Transitivity() as _:
            rule1 = Schema__Rule__Transitivity(source_type=Node_Type_Id('class'),
                                               verb=Safe_Str__Ontology__Verb('inherits_from'),
                                               target_type=Node_Type_Id('class'))
            rule2 = Schema__Rule__Transitivity(source_type=Node_Type_Id('package'),
                                               verb=Safe_Str__Ontology__Verb('has'),
                                               target_type=Node_Type_Id('package'))

            _.append(rule1)
            _.append(rule2)

            assert len(_) == 2
            assert _[0]   is rule1
            assert _[1]   is rule2

    def test__iteration(self):                                                       # Test iteration over rules
        with List__Rules__Transitivity() as _:
            rule1 = Schema__Rule__Transitivity(source_type=Node_Type_Id('class'),
                                               verb=Safe_Str__Ontology__Verb('inherits_from'),
                                               target_type=Node_Type_Id('class'))
            rule2 = Schema__Rule__Transitivity(source_type=Node_Type_Id('package'),
                                               verb=Safe_Str__Ontology__Verb('has'),
                                               target_type=Node_Type_Id('package'))
            _.extend([rule1, rule2])

            rules = list(_)
            assert len(rules) == 2
            assert rule1 in rules
            assert rule2 in rules