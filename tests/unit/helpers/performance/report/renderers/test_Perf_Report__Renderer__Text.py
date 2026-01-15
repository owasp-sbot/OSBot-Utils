# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Renderer__Text - Tests for text format renderer with Print_Table
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                 import TestCase
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base             import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Text             import Perf_Report__Renderer__Text
from osbot_utils.helpers.performance.report.schemas.collections.List__Perf_Report__Categories import List__Perf_Report__Categories
from osbot_utils.helpers.performance.testing.QA__Perf_Report__Test_Data                       import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe


class test_Perf_Report__Renderer__Text(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()
        cls.renderer  = Perf_Report__Renderer__Text()

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Renderer__Text() as _:
            assert type(_)            is Perf_Report__Renderer__Text
            assert isinstance(_, Type_Safe)
            assert isinstance(_, Perf_Report__Renderer__Base)

    # ═══════════════════════════════════════════════════════════════════════════
    # Format Helper Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_format_ns(self):                                       # Test nanosecond formatting
        with self.renderer as _:
            assert _.format_ns(500)           == '500ns'
            assert _.format_ns(1_500)         == '1.50µs'
            assert _.format_ns(1_500_000)     == '1.50ms'
            assert _.format_ns(1_500_000_000) == '1.50s'

    def test_format_ns_padded(self):                                # Test padded formatting
        with self.renderer as _:
            assert _.format_ns_padded(500, 10)   == '     500ns'
            assert _.format_ns_padded(1_500, 10) == '    1.50µs'

    def test_format_pct(self):                                      # Test percentage formatting
        with self.renderer as _:
            assert _.format_pct(50.0)    == ' 50.0%'
            assert _.format_pct(5.5)     == '  5.5%'
            assert _.format_pct(100.0)   == '100.0%'

    def test_format_timestamp(self):                                # Test timestamp formatting
        with self.renderer as _:
            result = _.format_timestamp(1704067200000)              # 2024-01-01 00:00:00 UTC
            assert '2024' in result
            assert '01' in result

    def test__format_ns__negative_values(self):
        with Perf_Report__Renderer__Base() as _:
            assert _.format_ns(-500)           == '-500ns'
            assert _.format_ns(-1_500)         == '-1.50µs'
            assert _.format_ns(-1_500_000)     == '-1.50ms'
            assert _.format_ns(-1_202_800)     == '-1.20ms'  # The specific bug case
            assert _.format_ns(-1_500_000_000) == '-1.50s'

    def test_calculate_overhead(self):                              # Test overhead calculation
        with self.test_data as td:
            categories = td.create_categories_list()

            with self.renderer as _:
                overhead = _.calculate_overhead(categories)

                assert overhead is not None
                assert type(overhead) is int

    def test_calculate_overhead__no_data(self):                              # Test overhead calculation
        with self.renderer as _:
            assert _.calculate_overhead(List__Perf_Report__Categories()) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Render Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_render(self):                                          # Test render method
        report = self.test_data.create_report(title='Text Render Test')

        with self.renderer as _:
            output = _.render(report)

            assert type(output) is str
            assert len(output)  > 0

    def test_render__contains_title(self):                          # Test title in output
        report = self.test_data.create_report(title='My Test Title')

        with self.renderer as _:
            output = _.render(report)

            assert 'MY TEST TITLE' in output                        # Uppercased

    def test_render__contains_metadata(self):                       # Test metadata section (Print_Table)
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'BENCHMARK METADATA' in output
            assert 'Property' in output                             # Print_Table header
            assert 'Value' in output                                # Print_Table header
            assert 'Version' in output

    def test_render__contains_description(self):                    # Test description section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'DESCRIPTION' in output
            assert '─' in output                                    # Separator

    def test_render__contains_legend(self):                         # Test legend section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'LEGEND' in output
            assert 'A_xx' in output
            assert 'B_xx' in output
            assert 'C_xx' in output

    def test_render__contains_benchmarks_table(self):               # Test benchmarks table (Print_Table)
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'DETAILED CONVERSION BREAKDOWN' in output
            assert 'Benchmark' in output                            # Print_Table header
            assert 'Time' in output                                 # Print_Table header
            assert 'Category' in output                             # Print_Table header
            assert 'A_01__' in output

    def test_render__contains_category_summary(self):               # Test category summary
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'CATEGORY SUMMARY' in output
            assert '_xx benchmarks' in output
            assert 'Overhead:' in output

    def test_render__contains_percentage_analysis(self):            # Test percentage analysis
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'PERCENTAGE ANALYSIS' in output
            assert 'Converter Creation:' in output
            assert 'Convert Only:' in output
            assert 'Overhead:' in output

    def test_render__contains_stage_breakdown(self):                # Test stage breakdown
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'STAGE BREAKDOWN' in output
            assert '█' in output                                    # Visual bar

    def test_render__contains_bottleneck_analysis(self):            # Test bottleneck analysis
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'BOTTLENECK ANALYSIS' in output
            assert 'Primary Bottleneck:' in output
            assert 'Time:' in output
            assert 'Percentage:' in output

    def test_render__contains_key_insight(self):                    # Test key insight
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'KEY INSIGHT' in output

    def test_render__contains_footer(self):                         # Test footer
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'Report generated:' in output
            assert 'Version:' in output
            assert output.strip().endswith('═' * 80)

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__output_structure(self):                   # Test output structure
        report = self.test_data.create_report(title='Structure Test')

        with self.renderer as _:
            output = _.render(report)
            lines  = output.split('\n')

            assert len(lines) > 40                                  # Print_Table adds more lines
            assert lines[0].startswith('═')                         # Header border

    def test_integration__print_table_format(self):                 # Test Print_Table formatting
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '┌' in output                                    # Table top border
            assert '├' in output                                    # Table separator
            assert '└' in output                                    # Table bottom border
            assert '│' in output                                    # Table columns