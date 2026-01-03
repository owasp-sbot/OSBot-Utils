from unittest                                                                       import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality     import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb


class test_Schema__Rule__Cardinality(TestCase):                                      # Test cardinality rule schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Rule__Cardinality() as _:
            assert type(_.source_type) is Node_Type_Id
            assert type(_.verb)        is Safe_Str__Ontology__Verb
            assert type(_.target_type) is Node_Type_Id
            assert int(_.min_targets)  == 0
            assert _.max_targets       is None                                       # Unlimited by default
            assert str(_.description)  == ''

    def test__with_exact_one(self):                                                  # Test "exactly one" constraint
        with Schema__Rule__Cardinality(source_type = Node_Type_Id('method')            ,
                                       verb        = Safe_Str__Ontology__Verb('in')    ,
                                       target_type = Node_Type_Id('class')             ,
                                       min_targets = 1                                 ,
                                       max_targets = 1                                 ,
                                       description = 'A method belongs to exactly one class') as _:
            assert str(_.source_type)  == 'method'
            assert str(_.verb)         == 'in'
            assert str(_.target_type)  == 'class'
            assert int(_.min_targets)  == 1
            assert int(_.max_targets)  == 1

    def test__with_at_least_one(self):                                               # Test "at least one" constraint
        with Schema__Rule__Cardinality(source_type = Node_Type_Id('function')          ,
                                       verb        = Safe_Str__Ontology__Verb('defined_in'),
                                       target_type = Node_Type_Id('module')            ,
                                       min_targets = 1                                 ,
                                       max_targets = None                              ) as _:
            assert int(_.min_targets)  == 1
            assert _.max_targets       is None                                       # Unlimited max

