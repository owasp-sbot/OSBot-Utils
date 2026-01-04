from unittest                                                             import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref import Node_Type_Ref


class test_Node_Type_Ref(TestCase):                                                   # Test node type identifier

    def test__init__(self):                                                          # Test initialization
        with Node_Type_Ref('class') as _:
            assert str(_) == 'class'


    def test__in_list(self):                                                         # Test list membership
        targets = [Node_Type_Ref('class'), Node_Type_Ref('function')]
        assert Node_Type_Ref('class') in targets
        assert Node_Type_Ref('method') not in targets
