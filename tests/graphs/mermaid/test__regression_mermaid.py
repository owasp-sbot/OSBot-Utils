from unittest import TestCase

from osbot_utils.graphs.mermaid.Mermaid import Mermaid
from osbot_utils.graphs.mermaid.Mermaid__Edge import Mermaid__Edge
from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.graphs.mermaid.configs.Mermaid__Edge__Config import Mermaid__Edge__Config
from osbot_utils.graphs.mgraph.MGraph__Edge import MGraph__Edge
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_data


class test__regression__mermaid(TestCase):

    def test__regression__Mermaid_Node__config_is_not_being_set(self):
        new_node_1 = Mermaid__Node()

        assert type(new_node_1) is Mermaid__Node
        assert list_set(new_node_1.__dict__        ) == ['attributes', 'config', 'key', 'label']
        assert list_set(new_node_1.__locals__()    ) == ['attributes', 'config', 'key', 'label']
        assert list_set(obj_data(new_node_1)       ) == ['attributes', 'config', 'key', 'label']
        assert list_set(obj_data(new_node_1.config)) == ['markdown', 'node_shape','show_label', 'wrap_with_quotes'       ]

        new_node_2 = Mermaid().add_node(key='id')
        assert type(new_node_2) is Mermaid__Node
        assert list_set(new_node_2.__dict__        ) == ['attributes', 'config', 'key', 'label']                # FIXED, BUG: missing config
        assert list_set(new_node_2.__locals__()     ) == ['attributes', 'config', 'key', 'label']
        assert list_set(obj_data(new_node_2)        ) == ['attributes', 'config', 'key', 'label']                         # FIXED, BUG: missing config
        assert new_node_2.config                                                                                    # FIXED, BUG: missing config

        # with self.assertRaises(Exception) as context:
        #   new_node_2.config                                                                           # BUG: should not raise an exception
        # assert str(context.exception) == "'Mermaid__Node' object has no attribute 'config'"


    def test__regression__Mermaid__Edge__is_failing_on_ctor(self):
        MGraph__Edge()                                                  # MGraph__Edge  ctor doesn't raise an exception
        mermaid_edge = Mermaid__Edge()                                  # FIXED: MGraph__Edge also now doesn't raise an exception

        assert type(mermaid_edge.from_node) is Mermaid__Node            # confirm that correct types of
        assert type(mermaid_edge.to_node  ) is Mermaid__Node            # both from_node and to_node vars

        # with self.assertRaises(Exception) as context:
        #     Mermaid__Edge()                                             # Mermaid__Edge ctor raises an exception
        # assert str(context.exception) == ("Invalid type for attribute 'from_node'. Expected '<class "
        #                                   "'osbot_utils.graphs.mermaid.Mermaid__Node.Mermaid__Node'>' but got '<class "
        #                                   "'osbot_utils.graphs.mgraph.MGraph__Node.MGraph__Node'>'")



    def test__regression__Mermaid__Edge__init__is_not_enforcing_type_safety(self):
        from_node_key = 'from_node_key'
        to_node_key   = 'to_node_key'
        from_node     = from_node_key
        to_node       = to_node_key

        assert Mermaid__Edge.__annotations__ == { 'config'   : Mermaid__Edge__Config ,
                                                  'from_node': Mermaid__Node         ,           # confirm the type annotations
                                                  'to_node'  : Mermaid__Node         }
        assert type(from_node) is str                                                           # confirm that both variables are of type str
        assert type(to_node  ) is str

        with self.assertRaises(Exception) as context:
            Mermaid__Edge(from_node=from_node, to_node=to_node)                  # FIXED: this now raises exception: BUG, this should have not worked (an exception should have been raised)
        assert str(context.exception) == ("Invalid type for attribute 'from_node'. Expected '<class "
                                          "'osbot_utils.graphs.mermaid.Mermaid__Node.Mermaid__Node'>' but got '<class "
                                          "'str'>'")

        # assert new_edge.from_node       == from_node                                    # confirm that assigment worked
        # assert new_edge.to_node         == to_node                                      # BUG, to_node should never be anything else than a Mermaid__Node object
        # assert type(new_edge.from_node) is str                                          # confirm that the type of the variables is still str
        # assert type(new_edge.to_node  ) is str                                          # BUG, to_node should never be anything else than a Mermaid__Node object

        # with self.assertRaises(Exception) as context:
        #     new_edge.to_node = to_node                                                  # confirm that this type safety is working (i.e. assigment post ctor)
        # assert str(context.exception) == ("Invalid type for attribute 'to_node'."
        #                                   " Expected '<class 'osbot_utils.graphs."      # note how the type safety correctly picked up that we were expecting
        #                                   "mermaid.Mermaid__Node.Mermaid__Node'>' "     #     an object of type Mermaid__Node
        #                                   "but got '<class 'str'>'")                    #     but we got an object of type str