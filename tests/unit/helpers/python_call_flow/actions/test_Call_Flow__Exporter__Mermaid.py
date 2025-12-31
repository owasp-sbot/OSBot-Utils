# ═══════════════════════════════════════════════════════════════════════════════
# Mermaid Exporter Tests
# ═══════════════════════════════════════════════════════════════════════════════
from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                       import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.actions.Call_Flow__Exporter__Mermaid      import Call_Flow__Exporter__Mermaid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from tests.unit.helpers.python_call_flow.test_Call_Flow__Analyzer                   import Sample__Helper


class test_Call_Flow__Exporter__Mermaid(TestCase):                                   # Test Mermaid export

    @classmethod
    def setUpClass(cls):                                                             # Create sample graph by analyzing
        with Call_Flow__Analyzer() as analyzer:
            cls.graph = analyzer.analyze(Sample__Helper)

    def test__init__(self):                                                          # Test exporter initialization
        with Call_Flow__Exporter__Mermaid(graph=self.graph) as _:
            assert _.graph          is self.graph
            assert str(_.direction) == 'TD'
            assert _.show_modules   is False
            assert _.show_depth     is True
            assert _.show_contains  is True
            assert _.max_label_len  == 30

    def test__export__basic(self):                                                   # Test basic export
        with Call_Flow__Exporter__Mermaid(graph=self.graph) as exporter:
            mermaid = exporter.export()

            assert mermaid.startswith('flowchart')
            assert '-->'  in mermaid or '-.->' in mermaid

    def test__export__direction(self):                                               # Test direction option
        with Call_Flow__Exporter__Mermaid(graph=self.graph, direction=Safe_Str__Label('LR')) as exporter:
            mermaid = exporter.export()
            assert 'flowchart LR' in mermaid

    def test__export__contains_edge_style(self):                                     # Test CONTAINS edge rendering
        with Call_Flow__Exporter__Mermaid(graph=self.graph, show_contains=True) as exporter:
            mermaid = exporter.export()
            assert '-.->|contains|' in mermaid                                       # Dotted with label

    def test__to_html(self):                                                         # Test HTML generation
        with Call_Flow__Exporter__Mermaid(graph=self.graph) as exporter:
            html = exporter.to_html()

            assert '<!DOCTYPE html>' in html
            assert '<html>'          in html
            assert 'mermaid'         in html

    def test__sanitize_id(self):                                                     # Test ID sanitization
        with Call_Flow__Exporter__Mermaid(graph=self.graph) as exporter:
            assert exporter.sanitize_id('a.b.c')    == 'a_b_c'
            assert exporter.sanitize_id('a-b-c')    == 'a_b_c'
            assert exporter.sanitize_id('<module>') == 'module'
            assert exporter.sanitize_id('a b c')    == 'a_b_c'

    def test__escape_label(self):                                                    # Test label escaping
        with Call_Flow__Exporter__Mermaid(graph=self.graph) as exporter:
            assert exporter.escape_label('a"b')  == "a'b"
            assert exporter.escape_label('a<b>') == 'a&lt;b&gt;'

