from unittest                                                                               import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                     import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                    import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb


class test_Schema__Ontology__Node_Type(TestCase):                                    # Test node type schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Ontology__Node_Type() as _:
            assert str(_.description)   == ''
            assert _.relationships      == {}
            assert type(_.taxonomy_ref) is Category_Id
            assert str(_.taxonomy_ref)  == ''

    def test__with_relationships(self):                                              # Test with relationships
        defines_rel = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb('defined_in') ,
                                                     targets = [Node_Type_Id('class')]                )
        with Schema__Ontology__Node_Type(description   = 'Python module'             ,
                                         relationships = {'defines': defines_rel}    ,
                                         taxonomy_ref  = Category_Id('container')    ) as _:
            assert str(_.description)                      == 'Python module'
            assert 'defines'                               in _.relationships
            assert str(_.taxonomy_ref)                     == 'container'
            assert str(_.relationships['defines'].inverse) == 'defined_in'