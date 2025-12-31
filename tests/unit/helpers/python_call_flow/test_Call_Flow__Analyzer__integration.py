# ═══════════════════════════════════════════════════════════════════════════════
# Integration Tests
# ═══════════════════════════════════════════════════════════════════════════════
from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                       import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.actions.Call_Flow__Exporter__Mermaid      import Call_Flow__Exporter__Mermaid
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt
from tests.unit.helpers.python_call_flow.test_Call_Flow__Analyzer                   import Sample__Processor, Sample__Helper


class test_Call_Flow__Analyzer__integration(TestCase):                                                    # End-to-end integration tests

    def test__full_pipeline(self):                                                   # Complete analyze -> export pipeline
        config = Schema__Call_Graph__Config(max_depth       = Safe_UInt(2) ,
                                            include_private = False        )

        with Call_Flow__Analyzer(config=config) as analyzer:                         # Analyze
            graph = analyzer.analyze(Sample__Processor)

        with Call_Flow__Exporter__Mermaid(graph=graph) as exporter:                  # Export
            mermaid = exporter.export()
            html    = exporter.to_html()

        assert graph.node_count()    >= 1                                            # Validate
        assert 'flowchart'           in mermaid
        assert '<!DOCTYPE html>'     in html

        # print(f"\n{'═'*60}")
        # print("INTEGRATION TEST: Sample__Processor")
        # print(f"{'═'*60}")
        # print(f"  Nodes: {graph.node_count()}")
        # print(f"  Edges: {graph.edge_count()}")
        # print(f"\nMermaid output:")
        # print(mermaid)

    def test__graph_structure__class_analysis(self):                                 # Verify correct graph structure
        with Call_Flow__Analyzer() as analyzer:
            graph = analyzer.analyze(Sample__Helper)

            entry = graph.get_node(str(graph.entry_point))                           # Verify structure
            assert entry.node_type  == Enum__Call_Graph__Node_Type.CLASS
            assert int(entry.depth) == 0

            methods_at_1 = graph.nodes_at_depth(1)                                   # All methods at depth 1
            for method in methods_at_1:
                assert method.node_type == Enum__Call_Graph__Node_Type.METHOD

            contains_count = sum(1 for e in graph.edges                              # CONTAINS edges count
                                if e.edge_type == Enum__Call_Graph__Edge_Type.CONTAINS)
            assert contains_count == len(methods_at_1)                               # One per method

    def test__edge_types__distribution(self):                                        # Test edge type distribution
        with Call_Flow__Analyzer() as analyzer:
            graph = analyzer.analyze(Sample__Processor)

            edge_types = {}
            for edge in graph.edges:
                t = edge.edge_type.value
                edge_types[t] = edge_types.get(t, 0) + 1

            #print(f"\n  Edge type distribution: {edge_types}")

            assert 'contains' in edge_types                                          # Must have CONTAINS
            assert edge_types.get('contains', 0) >= 4                                # At least 4 methods