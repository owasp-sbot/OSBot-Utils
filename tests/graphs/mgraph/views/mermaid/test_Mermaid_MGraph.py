import io
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch

from osbot_utils.utils.Files import file_contents

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mgraph.views.mermaid.Mermaid_Node import Mermaid_Node

from osbot_utils.utils.Objects import base_classes, base_types

from osbot_utils.graphs.mgraph.MGraph import MGraph
from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mgraph.MGraphs                      import MGraphs
from osbot_utils.graphs.mgraph.views.mermaid.Mermaid_MGraph import Mermaid_MGraph


class test_Mermaid_MGraph(TestCase):

    def setUp(self):
        self.mgraph         = MGraphs().new__random(x_nodes=3,y_edges=4)
        self.mermaid_mgraph = Mermaid_MGraph(self.mgraph)


    def test__init__(self):
        assert type(self.mermaid_mgraph) is Mermaid_MGraph
        assert base_types(self.mermaid_mgraph) == [MGraph, Kwargs_To_Self, object]
        assert hasattr(self.mermaid_mgraph, "convert_nodes") is True
        assert hasattr(self.mgraph        , "convert_nodes") is False

    def test_code(self):
        with self.mermaid_mgraph as _:
            print()
            print(_.code())
            #assert _.code() == 'aaa'



    def test_convert_nodes(self):
        assert len(self.mermaid_mgraph.nodes) == len(self.mgraph.nodes)
        assert len(self.mermaid_mgraph.edges  ) == len(self.mgraph.edges)

        for node in self.mgraph.nodes:
            assert type(node) is Mermaid_Node

        for node in self.mermaid_mgraph.nodes:
            assert type(node) is Mermaid_Node


        # comparing print outputs using mock patch technique
        with patch('builtins.print') as _:
            self.mgraph         .print()
            self.mermaid_mgraph.print()

        print_calls   = int(_.call_count / 2)
        mgraph_calls  = _.call_args_list[:print_calls]
        mermaid_calls = _.call_args_list[print_calls:]
        assert len(mgraph_calls) == len(mermaid_calls)
        assert mgraph_calls      == mermaid_calls

        # comparing print outputs using redirect_stdout technique
        output_mgraph = io.StringIO()
        with redirect_stdout(output_mgraph):
            self.mgraph.print()

        output_mermaid = io.StringIO()
        with redirect_stdout(output_mermaid):
            self.mermaid_mgraph.print()
        assert output_mgraph.getvalue() == output_mermaid.getvalue()

    def test_save(self):
        file_path = self.mermaid_mgraph.save()
        print()
        print(file_path)
        print(file_contents(file_path))