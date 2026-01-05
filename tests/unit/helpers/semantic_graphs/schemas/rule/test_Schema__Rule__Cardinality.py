# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Rule__Cardinality - Tests for cardinality rule schema
#
# Note: Rule schemas still use ref-based approach (Node_Type_Ref, verb string)
#       as they haven't been migrated to Brief 3.7 ID-based architecture yet.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref           import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality     import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text


class test_Schema__Rule__Cardinality(TestCase):                                      # Test cardinality rule schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Rule__Cardinality() as _:
            assert type(_.source_type) is Node_Type_Ref
            assert type(_.verb)        is Safe_Str__Ontology__Verb
            assert type(_.target_type) is Node_Type_Ref
            assert int(_.min_targets)  == 0
            assert _.max_targets       is None                                       # Unlimited by default

    def test__with_exact_one(self):                                                  # Test "exactly one" constraint
        with Schema__Rule__Cardinality(source_type = Node_Type_Ref('method')                  ,
                                       verb        = Safe_Str__Ontology__Verb('in')           ,
                                       target_type = Node_Type_Ref('class')                   ,
                                       min_targets = Safe_UInt(1)                             ,
                                       max_targets = Safe_UInt(1)                             ,
                                       description = Safe_Str__Text('A method belongs to exactly one class')) as _:
            assert str(_.source_type)  == 'method'
            assert str(_.verb)         == 'in'
            assert str(_.target_type)  == 'class'
            assert int(_.min_targets)  == 1
            assert int(_.max_targets)  == 1

    def test__with_at_least_one(self):                                               # Test "at least one" constraint
        with Schema__Rule__Cardinality(source_type = Node_Type_Ref('function')                ,
                                       verb        = Safe_Str__Ontology__Verb('defined_in')   ,
                                       target_type = Node_Type_Ref('module')                  ,
                                       min_targets = Safe_UInt(1)                             ,
                                       max_targets = None                                     ) as _:
            assert int(_.min_targets)  == 1
            assert _.max_targets       is None                                       # Unlimited max

    def test__json_serialization(self):                                              # Test JSON round-trip
        original = Schema__Rule__Cardinality(source_type = Node_Type_Ref('method')                      ,
                                             verb        = Safe_Str__Ontology__Verb('in')               ,
                                             target_type = Node_Type_Ref('class')                       ,
                                             min_targets = Safe_UInt(1)                                 ,
                                             max_targets = Safe_UInt(1)                                 ,
                                             description = Safe_Str__Text('Method in one class')        )

        json_data = original.json()
        restored  = Schema__Rule__Cardinality.from_json(json_data)

        assert str(restored.source_type) == str(original.source_type)
        assert str(restored.verb)        == str(original.verb)
        assert str(restored.target_type) == str(original.target_type)
        assert int(restored.min_targets) == int(original.min_targets)
        assert int(restored.max_targets) == int(original.max_targets)