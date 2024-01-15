import random
from unittest import TestCase

import pytest

from osbot_utils.graphs.mem_graph.Mem_Graph__Config import Mem_Graph__Config
from osbot_utils.utils.Misc import random_number

from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mem_graph.Mem_Graphs import Mem_Graphs


class test_Mem_Graphs(TestCase):

    def setUp(self):
        self.mem_graphs = Mem_Graphs()
        self.config     = Mem_Graph__Config()

    @pytest.mark.skip("todo: implement pickle save")
    def test_new__random(self):
        self.config.graph_title = 'Random Graph - from tests'
        mem_graph = self.mem_graphs.new__random(self.config)
        pprint(mem_graph)
        mem_graph.data().print()
        saved_graph = mem_graph.save()
        pprint(saved_graph)
        mem_graph_2 = self.mem_graphs.load(saved_graph)
        pprint(mem_graph_2)
        #mem_graph_2.print()

    @pytest.mark.skip("todo: remove hard coded path")
    def test_load(self):
        saved_graph = '/var/folders/sj/ks1b_pjd749gk5ssdd1769kc0000gn/T/tmpo3emajer.pickle'
        mem_graph = self.mem_graphs.load(saved_graph)
        mem_graph.print()