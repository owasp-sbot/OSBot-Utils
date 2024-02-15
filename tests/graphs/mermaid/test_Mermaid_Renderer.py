from unittest import TestCase

from osbot_utils.graphs.mermaid.Mermaid             import Diagram__Direction, Diagram__Type, Mermaid
from osbot_utils.graphs.mermaid.Mermaid__Renderer   import Mermaid__Renderer
from osbot_utils.utils.Str                          import str_dedent


class test_Mermaid_Renderer(TestCase):

    def setUp(self):
        self.mermaid  = Mermaid()
        self.renderer = Mermaid__Renderer()

    def test__init__(self):
        with self.renderer as _:
            expected_locals = {'config'             : _.config              ,
                               'diagram_direction'  : Diagram__Direction.LR ,
                               'diagram_type'       : Diagram__Type.graph   ,
                               'mermaid_code'       : []                    }
            assert _                           is not None
            assert _.__locals__()              == expected_locals
            assert _.config.__class__.__name__ == 'Mermaid__Render__Config'



    def test_code(self):
        expected_code = str_dedent("""
                                        flowchart TD
                                            A[Christmas] -->|Get money| B(Go shopping)
                                            B --> C{Let me think}
                                            C -->|One| D[Laptop]
                                            C -->|Two| E[iPhone]
                                            C -->|Three| F[fa:fa-car Car]
                                            """)

        with self.mermaid as _:
            _.renderer.config.add_nodes         = False
            _.renderer.config.line_before_edges = False
            _.set_direction(Diagram__Direction.TD)
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='A').set_label('Christmas'    ).wrap_with_quotes(False).shape_default    ()
            _.add_node(key='B').set_label('Go shopping'  ).wrap_with_quotes(False).shape_round_edges()
            _.add_node(key='C').set_label('Let me think' ).wrap_with_quotes(False).shape_rhombus    ()
            _.add_node(key='D').set_label('Laptop'       ).wrap_with_quotes(False)
            _.add_node(key='E').set_label('iPhone'       ).wrap_with_quotes(False)
            _.add_node(key='F').set_label('fa:fa-car Car').wrap_with_quotes(False)
            _.add_edge('A', 'B', label='Get money').output_node_from().output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('B', 'C'                   ).output_node_to()
            _.add_edge('C', 'D', label='One'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'E', label='Two'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'F', label='Three'    ).output_node_to().edge_mode__lr_using_pipe()

            assert expected_code ==_.code()
            #file_path = self.mermaid.save()