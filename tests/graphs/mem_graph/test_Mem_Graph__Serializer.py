from unittest import TestCase

from osbot_utils.graphs.mem_graph.Mem_Graph__Edge import Mem_Graph__Edge
from osbot_utils.helpers.Local_Cache import Local_Cache

from osbot_utils.graphs.mem_graph.Mem_Graph import Mem_Graph
from osbot_utils.utils.Misc import list_set

from osbot_utils.graphs.mem_graph.Mem_Graphs import Mem_Graphs
from osbot_utils.helpers.Random_Seed import Random_Seed
from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mem_graph.Mem_Graph__Serializer import Mem_Graph__Serializer, Serialization_Mode


class test_Mem_Graph__Serializer(TestCase):

    def setUp(self):
        with Random_Seed():
            self.mgraph        = Mem_Graphs().new__random()              # todo: see if we need to make this non-random
        self.graph_serializer = Mem_Graph__Serializer(mgraph = self.mgraph)


    def test__init__(self):
        print()
        print()
        expected_attrs = [ '__type_safety__', 'key', 'local_cache', 'mgraph', 'mode']
        with self.graph_serializer as _:
            assert _.__attr_names__() == expected_attrs
            #assert _.local_cache      is None
            assert _.mgraph.__class__ is Mem_Graph
            assert _.mode             == Serialization_Mode.PICKLE
            assert _.key              == f'serialiser_for {self.mgraph.key}'

            pprint(_.__annotations__.get('local_cache') is Local_Cache)
            #_.local_cache = 123



    def test_save(self):
        result = self.mgraph.save()
        pprint(result)

    def test_save_to_json(self):
        with self.graph_serializer as _:
            assert _.save_to_json() == '...json save - to be implemented...'

    def test_save_to_pickle(self):
        with self.graph_serializer as _:
            assert _.save_to_pickle() == '...pickle save - to be implemented...'

    def test_save_to_yaml(self):
        with self.graph_serializer as _:
            assert _.save_to_yaml() == '...yaml save - to be implemented...'
