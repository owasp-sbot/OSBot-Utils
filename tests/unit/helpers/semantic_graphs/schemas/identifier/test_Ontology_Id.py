from unittest                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id import Ontology_Id


class test_Ontology_Id(TestCase):                                                    # Test ontology identifier

    def test__init__(self):                                                          # Test initialization
        with Ontology_Id('code_structure') as _:
            assert str(_) == 'code_structure'

    def test__empty(self):                                                           # Test empty value
        with Ontology_Id('') as _:
            assert str(_) == ''

    def test__comparison(self):                                                      # Test comparison
        id1 = Ontology_Id('test')
        id2 = Ontology_Id('test')
        id3 = Ontology_Id('other')

        assert id1 == id2
        assert id1 != id3
        assert id1 == 'test'
