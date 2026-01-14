# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Storage__File_System - Tests for file system storage
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                                    import TestCase
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                                          import Schema__Perf_Report
from osbot_utils.helpers.performance.report.storage.Perf_Report__Storage__Base                                   import Perf_Report__Storage__Base
from osbot_utils.helpers.performance.report.storage.Perf_Report__Storage__File_System                            import Perf_Report__Storage__File_System
from osbot_utils.helpers.performance.report.testing.QA__Perf_Report__Test_Data                                   import QA__Perf_Report__Test_Data
from osbot_utils.testing.Temp_Folder                                                                             import Temp_Folder
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe
from osbot_utils.utils.Files import file_exists, path_combine, folder_exists


class test_Perf_Report__Storage__File_System(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Storage__File_System() as _:
            assert type(_)            is Perf_Report__Storage__File_System
            assert isinstance(_, Type_Safe)
            assert isinstance(_, Perf_Report__Storage__Base)
            assert type(_.storage_path) is str

    def test__init____with_path(self):                              # Test with storage path
        with Temp_Folder() as folder:
            with Perf_Report__Storage__File_System(storage_path=folder.path()) as _:
                assert _.storage_path == folder.path()

    # ═══════════════════════════════════════════════════════════════════════════
    # Save Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_save(self):                                            # Test save method
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            result = storage.save(report, key='test_report', formats=['txt', 'md', 'json'])

            assert result is True
            assert file_exists(path_combine(folder.path(), 'test_report.txt'))  is True
            assert file_exists(path_combine(folder.path(), 'test_report.md'))   is True
            assert file_exists(path_combine(folder.path(), 'test_report.json')) is True

    def test_save__single_format(self):                             # Test single format
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            result = storage.save(report, key='single', formats=['json'])

            assert result is True
            assert file_exists(path_combine(folder.path(), 'single.json')) is True
            assert file_exists(path_combine(folder.path(), 'single.txt'))  is False

    def test_save__default_formats(self):                           # Test default formats
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            result = storage.save(report, key='defaults')

            assert result is True
            assert file_exists(path_combine(folder.path(), 'defaults.txt'))  is True
            assert file_exists(path_combine(folder.path(), 'defaults.md'))   is True
            assert file_exists(path_combine(folder.path(), 'defaults.json')) is True

    def test_save_content(self):                                    # Test save_content method
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())

            result = storage.save_content('test_key', 'test content', 'txt')

            assert result is True
            assert file_exists(path_combine(folder.path(), 'test_key.txt')) is True

    # ═══════════════════════════════════════════════════════════════════════════
    # Load Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_load(self):                                            # Test load method
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report(title='Load Test')

            storage.save(report, key='load_test', formats=['json'])
            loaded = storage.load('load_test')

            assert type(loaded)               is Schema__Perf_Report
            assert str(loaded.metadata.title) == 'Load Test'

    def test_load__round_trip(self):                                # Test full round-trip
        with Temp_Folder() as folder:
            storage  = Perf_Report__Storage__File_System(storage_path=folder.path())
            original = self.test_data.create_report(title='Round Trip')

            storage.save(original, key='round_trip')
            loaded = storage.load('round_trip')

            assert len(loaded.benchmarks)                   == len(original.benchmarks)
            assert len(loaded.categories)                   == len(original.categories)
            assert str(loaded.analysis.bottleneck_id)       == str(original.analysis.bottleneck_id)
            assert int(loaded.metadata.benchmark_count)     == int(original.metadata.benchmark_count)

    def test_load__missing_file(self):                              # Test missing file
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())

            loaded = storage.load('nonexistent')

            assert loaded is None

    # ═══════════════════════════════════════════════════════════════════════════
    # List and Exists Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_list_reports(self):                                    # Test list_reports
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            storage.save(report, key='report_1')
            storage.save(report, key='report_2')

            reports = storage.list_reports()

            assert 'report_1' in reports
            assert 'report_2' in reports

    def test_list_reports__empty(self):                             # Test empty folder
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())

            reports = storage.list_reports()

            assert reports == []

    def test_exists(self):                                          # Test exists method
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            storage.save(report, key='exists_test')

            assert storage.exists('exists_test')  is True
            assert storage.exists('not_exists')   is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Delete Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_delete(self):                                          # Test delete method
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            storage.save(report, key='delete_test')
            assert storage.exists('delete_test') is True

            result = storage.delete('delete_test')

            assert result is True
            assert storage.exists('delete_test') is False

    def test_delete__missing(self):                                 # Test delete missing
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())

            result = storage.delete('not_there')

            assert result is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__full_workflow(self):                      # Test complete workflow
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report(title='Workflow Test')

            storage.save(report, key='workflow')

            assert storage.exists('workflow') is True
            assert 'workflow' in storage.list_reports()

            loaded = storage.load('workflow')
            assert str(loaded.metadata.title) == 'Workflow Test'

            storage.delete('workflow')
            assert storage.exists('workflow') is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Additional Coverage Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_save__formats_none_uses_defaults(self):                # Test formats=None uses defaults
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            result = storage.save(report, key='default_formats', formats=None)

            assert result is True
            assert file_exists(path_combine(folder.path(), 'default_formats.txt'))  is True
            assert file_exists(path_combine(folder.path(), 'default_formats.md'))   is True
            assert file_exists(path_combine(folder.path(), 'default_formats.json')) is True

    def test_save__invalid_format(self):                            # Test invalid format returns False
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            result = storage.save(report, key='invalid', formats=['xyz'])

            assert result is False

    def test_list_reports__folder_not_exists(self):                 # Test list when folder doesn't exist
        storage = Perf_Report__Storage__File_System(storage_path='/nonexistent/path')

        reports = storage.list_reports()

        assert reports == []

    def test_list_reports__files_with_extensions(self):             # Test list extracts keys from filenames
        with Temp_Folder() as folder:
            storage = Perf_Report__Storage__File_System(storage_path=folder.path())
            report  = self.test_data.create_report()

            storage.save(report, key='report_a', formats=['txt', 'json'])
            storage.save(report, key='report_b', formats=['md'])

            reports = storage.list_reports()

            assert 'report_a' in reports
            assert 'report_b' in reports
            assert len(reports) == 2                                # Unique keys only

    def test_delete__folder_not_exists(self):                       # Test delete when folder doesn't exist
        storage = Perf_Report__Storage__File_System(storage_path='/nonexistent/path')

        result = storage.delete('any_key')

        assert result is False

    def test_ensure_storage_path__creates_folder(self):             # Test ensure_storage_path creates folder
        with Temp_Folder() as folder:
            new_path = path_combine(folder.path(), 'new_subfolder')
            storage  = Perf_Report__Storage__File_System(storage_path=new_path)

            assert folder_exists(new_path) is False

            storage.ensure_storage_path()

            assert folder_exists(new_path) is True
