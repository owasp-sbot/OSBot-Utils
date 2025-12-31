# ═══════════════════════════════════════════════════════════════════════════════
# Meta Tests - Analyzer analyzing itself
# ═══════════════════════════════════════════════════════════════════════════════
from unittest import TestCase

from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                       import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.actions.Call_Flow__Exporter__Mermaid      import Call_Flow__Exporter__Mermaid
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class test_Call_Flow__Analyzer__meta(TestCase):                                      # Meta tests - analyzer analyzing itself

    @classmethod
    def setUpClass(cls):                                                             # Analyze analyzer once for all tests
        config = Schema__Call_Graph__Config(max_depth       = Safe_UInt(3) ,
                                            include_private = False        ,
                                            include_dunder  = False        )
        with Call_Flow__Analyzer(config=config) as analyzer:
            cls.graph = analyzer.analyze(Call_Flow__Analyzer)

    def test__meta__finds_class_node(self):                                          # Verify class is entry point
        entry_node = self.graph.get_node(str(self.graph.entry_point))
        assert entry_node.is_entry  is True
        assert entry_node.node_type == Enum__Call_Graph__Node_Type.CLASS
        assert str(entry_node.name) == 'Call_Flow__Analyzer'

    def test__meta__discovers_methods(self):                                         # Verify key methods discovered
        method_names = [str(n.name) for n in self.graph.nodes.values()]

        expected_methods = ['analyze', 'reset_state', 'initialize_graph'            ,
                           'analyze_class', 'analyze_function', 'extract_calls'     ,
                           'resolve_call', 'process_call'                           ]

        found   = [m for m in expected_methods if m in method_names]
        missing = [m for m in expected_methods if m not in method_names]

        # print(f"\n  Methods found:   {found}")
        # print(f"  Methods missing: {missing}")

        assert 'analyze' in method_names                                             # Entry method must be found
        assert len(found) >= 5                                                       # Should find most methods

    def test__meta__has_contains_edges(self):                                        # Verify CONTAINS edges exist
        contains_edges = [e for e in self.graph.edges
                         if e.edge_type == Enum__Call_Graph__Edge_Type.CONTAINS]
        assert len(contains_edges) >= 5                                              # At least several methods

    def test__meta__identifies_call_flow(self):                                      # Verify call relationships captured
        #print("\n  Sample edges:")
        for edge in self.graph.edges[:10]:
            from_name = self.graph.nodes.get(str(edge.from_node))
            to_name   = self.graph.nodes.get(str(edge.to_node))

            from_label = str(from_name.name) if from_name else str(edge.from_node)[:8]
            to_label   = str(to_name.name) if to_name else str(edge.to_node)[:8]
            edge_type  = edge.edge_type.value
            # todo: add asserts
            #print(f"    {from_label} --[{edge_type}]--> {to_label}")

    def test__meta__generates_mermaid(self):                                         # Generate Mermaid from self-analysis
        with Call_Flow__Exporter__Mermaid(graph=self.graph, show_depth=True) as exporter:
            mermaid = exporter.export()

            assert 'flowchart'                      in mermaid                                            # Has flowchart declaration
            assert 'analyze'                    not in mermaid or 'Call_Flow__Analyzer' in mermaid # BUG
            assert 'osbot_utils.helpers.python_...' in mermaid                                     # BUG

            # print(f"\n{'═'*60}")
            # print("MERMAID OUTPUT (first 30 lines):")
            # print(f"{'═'*60}")
            # for line in mermaid.split('\n')[:30]:
            #     print(line)