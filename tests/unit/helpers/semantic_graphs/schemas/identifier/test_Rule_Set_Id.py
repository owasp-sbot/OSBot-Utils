from unittest                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id import Rule_Set_Id


class test_Rule_Set_Id(TestCase):                                                    # Test rule set identifier

    def test__init__(self):                                                          # Test initialization
        with Rule_Set_Id('python_rules') as _:
            assert str(_) == 'python_rules'
