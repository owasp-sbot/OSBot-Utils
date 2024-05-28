import sys
from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid import Mermaid
from osbot_utils.graphs.mermaid.models.Mermaid__Node__Shape import Mermaid__Node__Shape
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Misc import list_set

from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.utils.Objects import type_mro


class test_Mermaid_Node(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

    def setUp(self):
        self.mermaid_node = Mermaid__Node()
        self.node_config  = self.mermaid_node.config

    def test__init__(self):
        assert type(self.mermaid_node) is Mermaid__Node
        assert list_set(self.mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

    # def test_code(self):
    #     with self.mermaid_node as _:
    #         assert _.code() == f'  {_.key}["{_.key}"]'
    #         assert _.label  == _.key
    #         _.label = 'my label'
    #         assert _.code() == f'  {_.key}["my label"]'

    def test_data(self):
        assert self.mermaid_node.data() == self.mermaid_node.__locals__()

    def test_shape(self):
        assert self.mermaid_node.shape(Mermaid__Node__Shape.round_edges).config.node_shape == Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape(Mermaid__Node__Shape.rhombus    ).config.node_shape == Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape(Mermaid__Node__Shape.default    ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('round_edges'                   ).config.node_shape == Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape('rhombus'                       ).config.node_shape == Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape('default'                       ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('aaaa'                          ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(' '                             ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(''                              ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(None                            ).config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(                                ).config.node_shape == Mermaid__Node__Shape.default

    def test_shape__shape_name(self):
        assert self.mermaid_node.shape_hexagon()            is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.hexagon
        assert self.mermaid_node.shape_parallelogram()      is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.parallelogram
        assert self.mermaid_node.shape_parallelogram_alt()  is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.parallelogram_alt
        assert self.mermaid_node.shape_rectangle()          is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.rectangle
        assert self.mermaid_node.shape_trapezoid()          is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.trapezoid
        assert self.mermaid_node.shape_trapezoid_alt()      is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.trapezoid_alt
        assert self.mermaid_node.shape_default()            is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.default
        assert self.mermaid_node.shape_round_edges()        is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape_rhombus()            is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape_circle()             is self.mermaid_node;  assert self.mermaid_node.config.node_shape == Mermaid__Node__Shape.circle


    def test_wrap_with_quotes(self):
        assert self.node_config.wrap_with_quotes                                 == True
        assert self.mermaid_node.wrap_with_quotes(     ).config.wrap_with_quotes == True
        assert self.mermaid_node.wrap_with_quotes(False).config.wrap_with_quotes == False
        assert self.mermaid_node.wrap_with_quotes(True ).config.wrap_with_quotes == True

    def test__render_node__node_shape(self):
        with Mermaid().add_node(key='id') as _:
            assert _                     .render_node() == '    id["id"]'
            assert _.shape(''           ).render_node() == '    id["id"]'
            assert _.shape('aaaaa'      ).render_node() == '    id["id"]'
            assert _.shape('round_edges').render_node() == '    id("id")'
            assert _.shape('rhombus'    ).render_node() == '    id{"id"}'

            assert _.shape(Mermaid__Node__Shape.default    ).render_node() == '    id["id"]'
            assert _.shape(Mermaid__Node__Shape.rectangle  ).render_node() == '    id["id"]'
            assert _.shape(Mermaid__Node__Shape.round_edges).render_node() == '    id("id")'
            assert _.shape(Mermaid__Node__Shape.rhombus    ).render_node() == '    id{"id"}'


    def test__config__wrap_with_quotes(self):
        new_node = self.mermaid_node.set_key('id').set_label('id')
        new_node.wrap_with_quotes()
        assert type(new_node) is Mermaid__Node
        assert new_node.config.wrap_with_quotes == True
        assert new_node.key == 'id'

        assert new_node.data() == {'attributes' : {}                        ,
                                   'config'     : new_node.config           ,
                                   'key'        : 'id'                      ,
                                   'label'      : 'id'                      }
        assert type_mro(new_node) == [Mermaid__Node, MGraph__Node, Kwargs_To_Self, object]

        with Mermaid() as _:
            _.add_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'
        with Mermaid() as _:
            _.add_node(key='id').wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = Mermaid()
        new_node = mermaid.add_node(key='id')
        new_node.wrap_with_quotes(False)
        assert type(new_node) == Mermaid__Node
        assert new_node.attributes == {}
        assert mermaid.code() == 'graph LR\n    id[id]\n'

