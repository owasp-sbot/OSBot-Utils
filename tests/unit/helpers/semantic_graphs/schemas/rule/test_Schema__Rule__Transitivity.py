# ═══════════════════════════════════════════════════════════════════════════════
# Test Schema__Rule__Transitivity - Tests for transitivity rule schema
#
# Note: Rule schemas still use ref-based approach (Node_Type_Ref, verb string)
#       as they haven't been migrated to Brief 3.7 ID-based architecture yet.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref           import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity    import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb


class test_Schema__Rule__Transitivity(TestCase):                                     # Test transitivity rule schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Rule__Transitivity() as _:
            assert type(_.source_type) is Node_Type_Ref
            assert type(_.verb)        is Safe_Str__Ontology__Verb
            assert type(_.target_type) is Node_Type_Ref
            assert str(_.source_type)  == ''
            assert str(_.verb)         == ''
            assert str(_.target_type)  == ''

    def test__with_values(self):                                                     # Test with explicit values
        with Schema__Rule__Transitivity(source_type = Node_Type_Ref('class')                  ,
                                        verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                        target_type = Node_Type_Ref('class')                  ) as _:
            assert str(_.source_type)  == 'class'
            assert str(_.verb)         == 'inherits_from'
            assert str(_.target_type)  == 'class'

    def test__json_serialization(self):                                              # Test JSON round-trip
        original = Schema__Rule__Transitivity(source_type = Node_Type_Ref('class')                  ,
                                              verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                              target_type = Node_Type_Ref('class')                  )

        json_data = original.json()
        restored  = Schema__Rule__Transitivity.from_json(json_data)

        assert str(restored.source_type) == str(original.source_type)
        assert str(restored.verb)        == str(original.verb)
        assert str(restored.target_type) == str(original.target_type)