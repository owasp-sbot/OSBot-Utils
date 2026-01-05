from unittest                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref import Ontology_Ref


class test_Ontology_Ref(TestCase):                                                    # Test ontology identifier

    def test__init__(self):                                                          # Test initialization
        with Ontology_Ref('code_structure') as _:
            assert str(_) == 'code_structure'

    def test__empty(self):                                                           # Test empty value
        with Ontology_Ref('') as _:
            assert str(_) == ''

    def test__comparison(self):                                                      # Test comparison
        id1 = Ontology_Ref('test')
        id2 = Ontology_Ref('test')
        id3 = Ontology_Ref('other')

        assert id1 == id2
        assert id1 != id3
        assert id1 == 'test'
