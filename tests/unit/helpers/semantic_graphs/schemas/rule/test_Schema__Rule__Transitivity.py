from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity    import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb


class test_Schema__Rule__Transitivity(TestCase):                                     # Test transitivity rule schema

    def test__init__(self):                                                          # Test initialization
        with Schema__Rule__Transitivity() as _:
            assert type(_.source_type) is Node_Type_Id
            assert type(_.verb)        is Safe_Str__Ontology__Verb
            assert type(_.target_type) is Node_Type_Id
            assert str(_.source_type)  == ''
            assert str(_.verb)         == ''
            assert str(_.target_type)  == ''

    def test__with_values(self):                                                     # Test with explicit values
        with Schema__Rule__Transitivity(source_type = Node_Type_Id('class')            ,
                                        verb        = Safe_Str__Ontology__Verb('inherits_from'),
                                        target_type = Node_Type_Id('class')            ) as _:
            assert str(_.source_type)  == 'class'
            assert str(_.verb)         == 'inherits_from'
            assert str(_.target_type)  == 'class'

