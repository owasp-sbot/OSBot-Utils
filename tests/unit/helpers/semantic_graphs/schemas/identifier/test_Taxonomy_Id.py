from unittest                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id import Taxonomy_Id


class test_Taxonomy_Id(TestCase):                                                    # Test taxonomy identifier

    def test__init__(self):                                                          # Test initialization
        with Taxonomy_Id('code_elements') as _:
            assert str(_) == 'code_elements'
