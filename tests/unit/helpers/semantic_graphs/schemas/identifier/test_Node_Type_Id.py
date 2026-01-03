from unittest                                                            import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id import Node_Type_Id


class test_Node_Type_Id(TestCase):                                                   # Test node type identifier

    def test__init__(self):                                                          # Test initialization
        with Node_Type_Id('class') as _:
            assert str(_) == 'class'

    def test__in_list(self):                                                         # Test list membership
        targets = [Node_Type_Id('class'), Node_Type_Id('function')]
        assert Node_Type_Id('class') in targets
        assert Node_Type_Id('method') not in targets
