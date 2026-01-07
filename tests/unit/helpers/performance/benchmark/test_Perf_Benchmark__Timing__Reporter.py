# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Timing__Reporter - Tests for benchmark reporter
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.Print_Table                                                                      import Print_Table
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.testing.Temp_File                                                                        import Temp_File
from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Markdown                          import Safe_Str__Markdown
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                              import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Time_Formatted                    import Safe_Str__Time_Formatted
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html                                 import Safe_Str__Html
from osbot_utils.utils.Files import file_exists, file_contents, folder_exists
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing__Reporter                           import Perf_Benchmark__Timing__Reporter
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Time_Unit                              import Enum__Time_Unit


class test_Perf_Benchmark__Timing__Reporter(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()
        cls.config    = Schema__Perf_Benchmark__Timing__Config(title            = 'Test Report',
                                                               print_to_console = False)
        cls.results   = cls.test_data.create_results_dict(count=3)

    def test__init__(self):                                                      # Test initialization
        with Perf_Benchmark__Timing__Reporter() as _:
            assert type(_)         is Perf_Benchmark__Timing__Reporter
            assert isinstance(_, Type_Safe)
            assert type(_.results) is Dict__Benchmark_Results
            assert type(_.config)  is Schema__Perf_Benchmark__Timing__Config

    def test__init____with_values(self):                                         # Test with values
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            assert len(_.results)   == 3
            assert _.config.title   == 'Test Report'


    # ═══════════════════════════════════════════════════════════════════════════════
    # Build Output Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_build_text(self):                                                   # Test text output
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            text = _.build_text()

            assert type(text)       is Safe_Str__Text
            assert 'Test Report'    in text
            assert 'python__nop'    in text
            assert 'Total:'         in text

    def test_build_json(self):                                                   # Test JSON output
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            json_data = _.build_json()

            assert type(json_data)            is dict
            assert json_data['title']         == 'Test Report'
            assert 'results'                  in json_data
            assert 'sections'                 in json_data
            assert json_data['total_benchmarks'] == 3

    def test_build_markdown(self):                                               # Test markdown output
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            markdown = _.build_markdown()

            assert type(markdown)   is Safe_Str__Markdown
            assert '# Test Report'  in markdown
            assert '## Section'     in markdown
            assert '| ID |'         in markdown
            assert '**Total:'       in markdown

    def test_build_html(self):                                                   # Test HTML output
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            html = _.build_html()

            assert type(html)        is Safe_Str__Html
            assert '<html>'          in html
            assert 'Test Report'     in html
            assert 'chart.js'        in html
            assert '<table>'         in html
            assert 'benchmarkChart'  in html


    # ═══════════════════════════════════════════════════════════════════════════════
    # Time Unit Formatting Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_format_time__nanoseconds(self):                                     # Test ns formatting
        config = Schema__Perf_Benchmark__Timing__Config(time_unit = Enum__Time_Unit.NANOSECONDS)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = config       ) as _:
            formatted = _.format_time(1000)

            assert type(formatted) is Safe_Str__Time_Formatted
            assert 'ns'            in formatted

    def test_format_time__microseconds(self):                                    # Test µs formatting
        config = Schema__Perf_Benchmark__Timing__Config(time_unit = Enum__Time_Unit.MICROSECONDS)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = config       ) as _:
            formatted = _.format_time(1000)

            assert type(formatted) is Safe_Str__Time_Formatted
            assert 'µs'            in formatted

    def test_format_time__milliseconds(self):                                    # Test ms formatting
        config = Schema__Perf_Benchmark__Timing__Config(time_unit = Enum__Time_Unit.MILLISECONDS)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = config       ) as _:
            formatted = _.format_time(1_000_000)

            assert type(formatted) is Safe_Str__Time_Formatted
            assert 'ms'            in formatted

    def test_format_time__seconds(self):                                         # Test s formatting
        config = Schema__Perf_Benchmark__Timing__Config(time_unit = Enum__Time_Unit.SECONDS)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = config       ) as _:
            formatted = _.format_time(1_000_000_000)

            assert type(formatted) is Safe_Str__Time_Formatted
            assert 's'             in formatted


    # ═══════════════════════════════════════════════════════════════════════════════
    # Section Detection Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_detect_sections(self):                                              # Test auto section detection
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            sections = _.detect_sections()

            assert type(sections) is Dict__Benchmark__Legend
            assert len(sections)  >= 2                                           # A and B sections

    def test_detect_sections__with_legend(self):                                 # Test with provided legend
        legend = self.test_data.create_legend()
        config = Schema__Perf_Benchmark__Timing__Config(title  = 'Test',
                                                        legend = legend)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = config       ) as _:
            sections = _.detect_sections()

            assert sections is legend                                            # Uses provided legend


    # ═══════════════════════════════════════════════════════════════════════════════
    # File Operations Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_save_text(self):                                                    # Test save text file
        with Temp_File(extension='.txt', return_file_path=True) as filepath:

            with Perf_Benchmark__Timing__Reporter(results = self.results,
                                                  config  = self.config ) as _:
                _.save_text(filepath)

                assert file_exists(filepath) is True
                contents = file_contents(filepath)
                assert 'Test Report' in contents

    def test_save_json(self):                                                    # Test save JSON file
        with Temp_File(extension='.json', return_file_path=True) as filepath:
            with Perf_Benchmark__Timing__Reporter(results = self.results,
                                                  config  = self.config ) as _:
                _.save_json(filepath)

                assert file_exists(filepath) is True
                contents = file_contents(filepath)
                assert 'Test Report' in contents

    def test_save_markdown(self):                                                # Test save markdown file

        with Temp_File(extension='.md', return_file_path=True) as filepath:
            with Perf_Benchmark__Timing__Reporter(results = self.results,
                                                  config  = self.config ) as _:
                _.save_markdown(filepath)

                assert file_exists(filepath) is True
                contents = file_contents(filepath)
                assert '# Test Report' in contents

    def test_save_html(self):                                                    # Test save HTML file
        with Temp_File(extension='.html', return_file_path=True) as filepath:

            with Perf_Benchmark__Timing__Reporter(results = self.results,
                                                  config  = self.config ) as _:
                _.save_html(filepath)

                assert file_exists(filepath) is True
                contents = file_contents(filepath)
                assert '<html>' in contents

    def test_save_all(self):                                                    # Test save text file
        with Temp_Folder() as temp_folder:
            full_path = temp_folder.full_path
            config    = Schema__Perf_Benchmark__Timing__Config(title            = 'Test Report',
                                                               print_to_console = False        ,
                                                               output_path      = full_path    )
            with Perf_Benchmark__Timing__Reporter(results = self.results,
                                                  config  = config ) as _:
                _.save_all()

                assert temp_folder.files() == ['benchmark.html', 'benchmark.json', 'benchmark.md', 'benchmark.txt']

            assert folder_exists(full_path) is True

        assert folder_exists(full_path) is False



    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_compare(self):                                                      # Test compare method
        other_results = self.test_data.create_results_dict(count=3)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            other = Perf_Benchmark__Timing__Reporter(results = other_results,
                                                     config  = self.config  )
            comparison = _.compare(other)

            assert type(comparison) is Safe_Str__Text
            assert 'Comparison'     in comparison

    def test_compare_results(self):                                              # Test compare_results
        other_results = self.test_data.create_results_dict(count=3)

        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            comparison = _.compare_results(other_results)

            assert type(comparison) is Safe_Str__Text


    # ═══════════════════════════════════════════════════════════════════════════════
    # Table Creation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_results_table(self):                                         # Test Print_Table creation
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            table = _.create_results_table()

            assert type(table) is Print_Table

    def test_create_html_table(self):                                            # Test HTML table creation
        with Perf_Benchmark__Timing__Reporter(results = self.results,
                                              config  = self.config ) as _:
            html_table = _.create_html_table()

            assert type(html_table) is Safe_Str__Html
            assert '<table>'        in html_table
            assert '</table>'       in html_table
            assert '<tr>'           in html_table
            assert '<td>'           in html_table