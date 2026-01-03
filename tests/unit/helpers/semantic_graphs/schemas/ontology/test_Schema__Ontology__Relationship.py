from unittest                                                                            import TestCase

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb       import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                    import Type_Safe__List


class test_Schema__Ontology__Relationship(TestCase):                                 # Test relationship schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Ontology__Relationship() as _:
            assert type(_.inverse) is Safe_Str__Ontology__Verb
            assert type(_.targets) is List__Node_Type_Ids
            assert str(_.inverse)  == ''
            assert _.targets       == []

    def test__with_values(self):                                                     # Test with explicit values
        targets = [Node_Type_Id('class'), Node_Type_Id('function')]
        with Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('defined_in'),
                                            targets = targets                        ) as _:
            assert str(_.inverse)  == 'defined_in'
            assert len(_.targets)  == 2
            assert _.targets[0]    == Node_Type_Id('class')

