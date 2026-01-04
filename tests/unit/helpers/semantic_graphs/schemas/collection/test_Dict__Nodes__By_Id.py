# ═══════════════════════════════════════════════════════════════════════════════
# Test Dict__Nodes__By_Id - Tests for node dictionary typed collection
#
# Updated for Brief 3.7:
#   - node_type → node_type_id (Obj_Id-based foreign key)
#   - name uses Safe_Str__Id type
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id       import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class test_Dict__Nodes__By_Id(TestCase):                                             # Test node dictionary collection

    @classmethod
    def setUpClass(cls):                                                             # Cache type IDs for tests
        cls.class_type_id  = Node_Type_Id(Obj_Id.from_seed('test:nt:class'))
        cls.method_type_id = Node_Type_Id(Obj_Id.from_seed('test:nt:method'))

    def test__init__(self):                                                          # Test initialization
        with Dict__Nodes__By_Id() as _:
            assert type(_)               is Dict__Nodes__By_Id
            assert isinstance(_, Type_Safe__Dict)
            assert _.expected_key_type   is Node_Id
            assert _.expected_value_type is Schema__Semantic_Graph__Node
            assert len(_)                == 0

    def test__add_and_retrieve(self):                                                # Test adding and retrieving nodes
        with graph_ids_for_tests():
            with Dict__Nodes__By_Id() as _:
                node_id = Node_Id(Obj_Id())
                node    = Schema__Semantic_Graph__Node(node_id      = node_id              ,
                                                       node_type_id = self.class_type_id   ,
                                                       name         = Safe_Str__Id('MyClass'))
                _[node_id] = node

                assert len(_)         == 1
                assert _[node_id]     is node
                assert _.get(node_id) is node

    def test__type_enforcement__key(self):                                           # Test key type enforcement
        with graph_ids_for_tests():
            with Dict__Nodes__By_Id() as _:
                node_id = Node_Id(Obj_Id())
                node    = Schema__Semantic_Graph__Node(node_id      = node_id              ,
                                                       node_type_id = self.class_type_id   ,
                                                       name         = Safe_Str__Id('MyClass'))

                _[node_id] = node                                                    # Valid key type
                assert len(_) == 1

    def test__type_enforcement__value(self):                                         # Test value type enforcement
        with graph_ids_for_tests():
            with Dict__Nodes__By_Id() as _:
                node_id = Node_Id(Obj_Id())
                node    = Schema__Semantic_Graph__Node(node_id      = node_id              ,
                                                       node_type_id = self.class_type_id   ,
                                                       name         = Safe_Str__Id('MyClass'))

                _[node_id] = node                                                    # Valid value type
                assert _[node_id] is node

    def test__iteration(self):                                                       # Test iteration over nodes
        with graph_ids_for_tests():
            with Dict__Nodes__By_Id() as _:
                node1_id = Node_Id(Obj_Id())
                node2_id = Node_Id(Obj_Id())
                node1    = Schema__Semantic_Graph__Node(node_id      = node1_id            ,
                                                        node_type_id = self.class_type_id  ,
                                                        name         = Safe_Str__Id('A')   )
                node2    = Schema__Semantic_Graph__Node(node_id      = node2_id            ,
                                                        node_type_id = self.class_type_id  ,
                                                        name         = Safe_Str__Id('B')   )

                _[node1_id] = node1
                _[node2_id] = node2

                keys   = list(_.keys())
                values = list(_.values())
                items  = list(_.items())

                assert len(keys)   == 2
                assert len(values) == 2
                assert len(items)  == 2