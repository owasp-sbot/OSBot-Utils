# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__integration - End-to-end integration tests
# ═══════════════════════════════════════════════════════════════════════════════

import tempfile
from pathlib                                                                         import Path
from unittest                                                                        import TestCase
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Storage                    import Call_Flow__Storage
from osbot_utils.helpers.python_call_flow.export.Call_Flow__Exporter__Mermaid        import Call_Flow__Exporter__Mermaid
from osbot_utils.helpers.python_call_flow.extract.Call_Flow__Analyzer                import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config          import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import (QA__Call_Flow__Test_Data   ,
                                                                                             Sample__Self_Calls         ,
                                                                                             Sample__Multiple_Self_Calls,
                                                                                             Sample__Deep_Calls         )


class test_Call_Flow__integration(TestCase):                                         # End-to-end integration tests

    @classmethod
    def setUpClass(cls):
        cls.qa = QA__Call_Flow__Test_Data()

    def test__full_pipeline__analyze_export(self):                                   # Test analyze -> export
        with Call_Flow__Analyzer() as analyzer:
            result = analyzer.analyze(Sample__Self_Calls)

        with Call_Flow__Exporter__Mermaid(result=result) as exporter:
            mermaid = exporter.export()
            html    = exporter.to_html()

        assert result.total_nodes  >= 3
        assert 'flowchart'         in mermaid
        assert '<!DOCTYPE html>'   in html
        assert 'Sample__Self_Calls' in mermaid

    def test__full_pipeline__analyze_save_load_export(self):                         # Test analyze -> save -> load -> export
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            # Analyze
            with Call_Flow__Analyzer() as analyzer:
                result = analyzer.analyze(Sample__Multiple_Self_Calls)

            # Save
            storage = Call_Flow__Storage()
            storage.save(result, filepath)

            # Load
            loaded = storage.load(filepath)

            # Export from loaded
            with Call_Flow__Exporter__Mermaid(result=loaded) as exporter:
                mermaid = exporter.export()

            # Verify consistency
            assert loaded.total_nodes  == result.total_nodes
            assert loaded.total_edges  == result.total_edges
            assert loaded.entry_point  == result.entry_point
            assert 'flowchart'         in mermaid

        finally:
            filepath.unlink(missing_ok=True)

    def test__multiple_analyses__independent(self):                                  # Test multiple independent analyses
        with Call_Flow__Analyzer() as analyzer1:
            result1 = analyzer1.analyze(Sample__Self_Calls)

        with Call_Flow__Analyzer() as analyzer2:
            result2 = analyzer2.analyze(Sample__Deep_Calls)

        assert result1.entry_point != result2.entry_point
        assert result1.total_nodes != result2.total_nodes

    def test__config_affects_analysis(self):                                         # Test config changes analysis
        config_shallow = Schema__Call_Flow__Config(max_depth=1)
        config_deep    = Schema__Call_Flow__Config(max_depth=20)

        with Call_Flow__Analyzer(config=config_shallow) as analyzer:
            result_shallow = analyzer.analyze(Sample__Deep_Calls)

        with Call_Flow__Analyzer(config=config_deep) as analyzer:
            result_deep = analyzer.analyze(Sample__Deep_Calls)

        # Both should complete without error
        assert result_shallow.total_nodes >= 1
        assert result_deep.total_nodes    >= 1

    def test__qa_fixtures__all_consistent(self):                                     # Test all QA fixtures are consistent
        with self.qa as _:
            all_fixtures = _.create_all_fixtures()

            for name, fixture in all_fixtures.items():
                target   = fixture['target']
                config   = fixture['config']
                result   = fixture['result']
                exporter = fixture['exporter']
                mermaid  = fixture['mermaid']
                ontology = fixture['ontology']

                # All components present
                assert target   is not None
                assert config   is not None
                assert result   is not None
                assert exporter is not None
                assert ontology is not None

                # Result matches expected
                assert target.__name__ in result.entry_point
                assert result.total_nodes >= 1

                # Mermaid is valid
                assert 'flowchart' in mermaid

    def test__graph_structure__nodes_match_edges(self):                              # Test graph structure consistency
        with self.qa as _:
            result = _.create_result__self_calls()
            graph  = result.graph

            # All edge endpoints exist as nodes
            for edge in graph.edges:
                from_id = str(edge.from_node_id)
                to_id   = str(edge.to_node_id)

                assert from_id in graph.nodes or any(str(n) == from_id for n in graph.nodes.keys())
                assert to_id   in graph.nodes or any(str(n) == to_id   for n in graph.nodes.keys())

    def test__serialization__round_trip_preserves_structure(self):                   # Test serialization preserves structure
        with self.qa as _:
            original = _.create_result__multiple_self_calls()
            storage  = _.create_storage()

            json_str = storage.to_json(original)
            loaded   = storage.from_json(json_str)

            assert loaded.entry_point      == original.entry_point
            assert loaded.total_nodes      == original.total_nodes
            assert loaded.total_edges      == original.total_edges
            assert loaded.max_depth_reached == original.max_depth_reached
            assert len(loaded.name_to_node_id) == len(original.name_to_node_id)

    def test__mermaid_export__different_directions(self):                            # Test mermaid export directions
        with self.qa as _:
            result = _.create_result__self_calls()

            exporter_td = _.create_exporter__default(result)
            exporter_lr = _.create_exporter__left_right(result)

            mermaid_td = exporter_td.export()
            mermaid_lr = exporter_lr.export()

            assert 'flowchart TD' in mermaid_td
            assert 'flowchart LR' in mermaid_lr

    def test__meta__analyzer_analyzing_itself(self):                                 # Test analyzer can analyze itself
        config = Schema__Call_Flow__Config(max_depth=2)

        with Call_Flow__Analyzer(config=config) as analyzer:
            result = analyzer.analyze(Call_Flow__Analyzer)

        assert 'Call_Flow__Analyzer' in result.entry_point
        assert result.total_nodes    >= 5                                            # Class + several methods

        with Call_Flow__Exporter__Mermaid(result=result) as exporter:
            mermaid = exporter.export()

        assert 'flowchart' in mermaid