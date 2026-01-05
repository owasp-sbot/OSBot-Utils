# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Storage - Tests for JSON serialization and file storage
# ═══════════════════════════════════════════════════════════════════════════════

import json
import tempfile
from pathlib                                                                         import Path
from unittest                                                                        import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                        import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.actions.Call_Flow__Exporter__Mermaid       import Call_Flow__Exporter__Mermaid
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.python_call_flow.Call_Flow__Storage                         import Call_Flow__Storage
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result          import Schema__Call_Flow__Result
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data, Sample__Self_Calls


class test_Call_Flow__Storage(TestCase):                                             # Test storage class

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.qa     = QA__Call_Flow__Test_Data()
        cls.result = cls.qa.create_result__self_calls()                              # Cached result

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Storage() as _:
            assert type(_)          is Call_Flow__Storage
            assert base_classes(_)  == [Type_Safe, object]
            assert _.base_path      == ''

    def test__to_json(self):                                                         # Test JSON serialization
        with self.qa as _:
            storage  = _.create_storage()
            json_str = storage.to_json(self.result)

            assert type(json_str)    is str
            assert 'entry_point'     in json_str
            assert 'total_nodes'     in json_str

    def test__to_json__valid_json(self):                                             # Test output is valid JSON
        with self.qa as _:
            storage  = _.create_storage()
            json_str = storage.to_json(self.result)

            data = json.loads(json_str)                                              # Should not raise
            assert type(data) is dict

    def test__from_json(self):                                                       # Test JSON deserialization
        with self.qa as _:
            storage  = _.create_storage()
            json_str = storage.to_json(self.result)
            loaded   = storage.from_json(json_str)

            assert type(loaded)       is Schema__Call_Flow__Result
            assert loaded.entry_point == self.result.entry_point
            assert loaded.total_nodes == self.result.total_nodes
            assert loaded.total_edges == self.result.total_edges

    def test__save(self):                                                            # Test file save
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            with self.qa as _:
                storage = _.create_storage()
                success = storage.save(self.result, filepath)

                assert success       is True
                assert filepath.exists()

                content = filepath.read_text()
                assert 'entry_point' in content
        finally:
            filepath.unlink(missing_ok=True)

    def test__load(self):                                                            # Test file load
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            with self.qa as _:
                storage = _.create_storage()
                storage.save(self.result, filepath)

                loaded = storage.load(filepath)

                assert type(loaded)       is Schema__Call_Flow__Result
                assert loaded.entry_point == self.result.entry_point
                assert loaded.total_nodes == self.result.total_nodes
        finally:
            filepath.unlink(missing_ok=True)

    def test__load__missing_file(self):                                              # Test load non-existent file
        with self.qa as _:
            storage = _.create_storage()
            loaded  = storage.load('/nonexistent/path.json')

            assert loaded is None

    def test__exists(self):                                                          # Test file exists check
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            with self.qa as _:
                storage = _.create_storage()

                assert storage.exists(filepath)      == True                         # File exists (empty)
                assert storage.exists('/nonexistent') == False
        finally:
            filepath.unlink(missing_ok=True)

    def test__delete(self):                                                          # Test file deletion
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            with self.qa as _:
                storage = _.create_storage()
                storage.save(self.result, filepath)

                assert filepath.exists()
                storage.delete(filepath)
                assert not filepath.exists()
        finally:
            filepath.unlink(missing_ok=True)

    def test__round_trip(self):                                                      # Test save -> load -> compare
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            with self.qa as _:
                storage = _.create_storage()
                storage.save(self.result, filepath)
                loaded = storage.load(filepath)

                assert loaded.entry_point      == self.result.entry_point
                assert loaded.total_nodes      == self.result.total_nodes
                assert loaded.total_edges      == self.result.total_edges
                assert len(loaded.name_to_node_id) == len(self.result.name_to_node_id)
        finally:
            filepath.unlink(missing_ok=True)



    def test__full_pipeline(self):                                                   # Test analyze -> save -> load -> export

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            filepath = Path(f.name)

        try:
            # Analyze
            with Call_Flow__Analyzer() as analyzer:
                result = analyzer.analyze(Sample__Self_Calls)

            # Save
            storage = Call_Flow__Storage()
            storage.save(result, filepath)

            # Load
            loaded = storage.load(filepath)

            # Export from loaded
            with Call_Flow__Exporter__Mermaid(result=loaded) as exporter:
                mermaid = exporter.export()

            # Verify
            assert loaded.total_nodes  == result.total_nodes
            assert 'flowchart'         in mermaid
            assert 'Sample__Self_Calls' in mermaid

        finally:
            filepath.unlink(missing_ok=True)

    def test__serialized_result__from_qa(self):                                      # Test QA serialized result
        with self.qa as _:
            json_str = _.create_serialized_result()

            assert type(json_str)        is str
            assert 'Sample__Self_Calls'  in json_str
            assert 'entry_point'         in json_str

            # Verify can be loaded
            storage = _.create_storage()
            loaded  = storage.from_json(json_str)
            assert type(loaded) is Schema__Call_Flow__Result