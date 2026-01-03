from unittest                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id import Category_Id


class test_Category_Id(TestCase):                                                    # Test category identifier

    def test__init__(self):                                                          # Test initialization
        with Category_Id('code_unit') as _:
            assert str(_) == 'code_unit'
