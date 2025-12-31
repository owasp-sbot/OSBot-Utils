from unittest                                       import TestCase
from osbot_utils.testing.Graph__Deterministic__Ids  import Graph__Deterministic__Ids
from osbot_utils.testing.__                         import __
from osbot_utils.utils.Objects                      import base_classes
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class test_Graph__Deterministic__Ids(TestCase):

    def test__init__(self):                                                                     # Test Graph__Deterministic__Ids initialization
        with Graph__Deterministic__Ids() as _:
            assert type(_)            is Graph__Deterministic__Ids
            assert base_classes(_)    == [Type_Safe, object]
            assert _.counter_graph    == 0
            assert _.counter_node     == 0
            assert _.counter_edge     == 0
            assert _.counter_obj      == 0
            assert _.obj()            == __(counter_graph = 0,
                                            counter_node  = 0,
                                            counter_edge  = 0,
                                            counter_obj   = 0)

    def test_reset(self):                                                                       # Test reset method clears all counters
        with Graph__Deterministic__Ids() as _:
            _.counter_graph = 5                                                                 # Set counters to non-zero values
            _.counter_node  = 10
            _.counter_edge  = 15
            _.counter_obj   = 20

            result = _.reset()                                                                  # Reset and verify

            assert result             is _                                                      # Returns self for chaining
            assert _.counter_graph    == 0
            assert _.counter_node     == 0
            assert _.counter_edge     == 0
            assert _.counter_obj      == 0

    def test_next_graph_id(self):                                                               # Test Graph_Id generation with 'a' prefix
        with Graph__Deterministic__Ids() as _:
            assert _.next_graph_id()  == 'a0000001'                                             # First call
            assert _.next_graph_id()  == 'a0000002'                                             # Sequential
            assert _.next_graph_id()  == 'a0000003'
            assert _.counter_graph    == 3                                                      # Counter tracks calls

    def test_next_node_id(self):                                                                # Test Node_Id generation with 'd' prefix
        with Graph__Deterministic__Ids() as _:
            assert _.next_node_id()   == 'c0000001'                                             # First call
            assert _.next_node_id()   == 'c0000002'                                             # Sequential
            assert _.next_node_id()   == 'c0000003'
            assert _.counter_node     == 3                                                      # Counter tracks calls

    def test_next_edge_id(self):                                                                # Test Edge_Id generation with 'e' prefix
        with Graph__Deterministic__Ids() as _:
            assert _.next_edge_id()   == 'e0000001'                                             # First call
            assert _.next_edge_id()   == 'e0000002'                                             # Sequential
            assert _.next_edge_id()   == 'e0000003'
            assert _.counter_edge     == 3                                                      # Counter tracks calls

    def test_next_obj_id(self):                                                                 # Test direct Obj_Id generation with 'o' prefix
        with Graph__Deterministic__Ids() as _:
            assert _.next_obj_id()    == 'f0000001'                                             # First call
            assert _.next_obj_id()    == 'f0000002'                                             # Sequential
            assert _.next_obj_id()    == 'f0000003'
            assert _.counter_obj      == 3                                                      # Counter tracks calls

    def test_next_id_from_context__direct_obj_id(self):                                         # Test context detection falls back to obj_id
        with Graph__Deterministic__Ids() as _:
            result = _.next_id_from_context()                                                   # Called directly, not wrapped
            assert result             == 'f0000001'                                             # Falls back to obj_id
            assert _.counter_obj      == 1

    def test__counters_are_independent(self):                                                   # Test each counter increments independently
        with Graph__Deterministic__Ids() as _:
            _.next_graph_id()                                                                   # Increment each type
            _.next_graph_id()
            _.next_node_id()
            _.next_edge_id()
            _.next_edge_id()
            _.next_edge_id()

            assert _.obj()            == __(counter_graph = 2,                                  # Each counter independent
                                            counter_node  = 1,
                                            counter_edge  = 3,
                                            counter_obj   = 0)

    def test__id_format_padding(self):                                                          # Test ID format uses 7-digit zero padding
        with Graph__Deterministic__Ids() as _:
            for i in range(999):                                                                # Generate many IDs
                _.next_node_id()

            assert _.next_node_id()   == 'c0001000'                                             # Properly padded
            assert len('d0001000')    == 8                                                      # Prefix + 7 digits
