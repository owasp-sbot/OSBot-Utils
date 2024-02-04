from unittest import TestCase

from osbot_utils.graphs.mermaid.Mermaid                              import Mermaid
from osbot_utils.graphs.mermaid.examples.Mermaid_Examples__FlowChart import Mermain_Examples__FlowChart
from osbot_utils.graphs.mermaid.models.Mermaid__Diagram__Type        import Diagram__Type
from osbot_utils.utils.Str                                           import str_dedent


class test_Mermain_Examples__FlowChart(TestCase):

    def setUp(self):
        self.mermaid             = Mermaid()
        self.examples            = Mermain_Examples__FlowChart()
        self.target_example      = None
        self.assert_on_exit      = True
        self.print_expected_code = False
        self.print_on_exit       = False
        self.save_on_exit        = False

    def tearDown(self):
        test_name      = self.id().split('.')[-1]                       # This will get the name of the current test method
        target_example = test_name.replace('test_','')      # Replace 'test_' with an empty string to follow your naming convention

        expected_code = self.examples.__getattribute__(target_example)
        rendered_code = self.mermaid.code()
        if self.assert_on_exit      : assert rendered_code.strip() == str_dedent(expected_code)
        if self.print_expected_code : print(f"\n______expected code______\n{expected_code}")
        if self.print_on_exit       : print(f"\n______rendered code______\n{rendered_code}")
        if self.save_on_exit        : self.mermaid.save()

    def test_example_1__a_node_default(self):
        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='id').show_label(False)

    def test_example_2__a_node_with_text(self):
        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='id1', label='This is the text in the box').wrap_with_quotes(False)

    def test_example_3__a_node_with_unicode_text(self):
        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='id', label='This ❤ Unicode')


    def test_example_4__a_node_with_markdown_formating(self):

        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_directive('init: {"flowchart": {"htmlLabels": false}} ')
            _.add_node(key='markdown', label='This **is** _Markdown_').markdown()
            _.add_node(key='newLines', label="""Line1
    Line 2
    Line 3""").markdown()
            _.add_edge('markdown', 'newLines')
            _.renderer.config.line_before_edges = False
            _.save()


    def test_example_5__direction__from_top_to_bottom(self):

        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.set_direction('TD')
            _.renderer.config.line_before_edges = False
            _.renderer.config.add_nodes = False
            _.add_edge('Start', 'Stop')


    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)

    # def test_(self):
    #
    #     self.assert_on_exit      = False
    #     self.print_on_exit       = True
    #     self.print_expected_code = True
    #
    #     with self.mermaid as _:
    #         _.set_diagram_type(Diagram__Type.flowchart)



