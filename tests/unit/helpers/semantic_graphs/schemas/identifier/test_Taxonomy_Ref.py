from unittest                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref import Taxonomy_Ref


class test_Taxonomy_Ref(TestCase):                                                    # Test taxonomy identifier

    def test__init__(self):                                                          # Test initialization
        with Taxonomy_Ref('code_elements') as _:
            assert str(_) == 'code_elements'
