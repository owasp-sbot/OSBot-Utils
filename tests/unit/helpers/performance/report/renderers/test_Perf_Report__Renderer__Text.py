# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Renderer__Text - Tests for text format renderer
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                                    import TestCase
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base                                import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Text                                import Perf_Report__Renderer__Text
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report import Schema__Perf_Report
from osbot_utils.helpers.performance.report.testing.QA__Perf_Report__Test_Data                                   import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe


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
            assert _.format_ns(500)         == '500ns'
            assert _.format_ns(1_500)       == '1.50µs'
            assert _.format_ns(1_500_000)   == '1.50ms'
            assert _.format_ns(1_500_000_000) == '1.50s'

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

    def test_render__contains_metadata(self):                       # Test metadata section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'BENCHMARK METADATA' in output
            assert 'Version' in output
            assert 'Mode' in output

    def test_render__contains_legend(self):                         # Test legend section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'LEGEND' in output
            assert 'A =' in output
            assert 'B =' in output
            assert 'C =' in output

    def test_render__contains_benchmarks(self):                     # Test benchmarks section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'INDIVIDUAL BENCHMARKS' in output
            assert 'A_01__' in output

    def test_render__contains_categories(self):                     # Test categories section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'CATEGORY TOTALS' in output
            assert 'benchmarks]' in output

    def test_render__contains_analysis(self):                       # Test analysis section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'ANALYSIS' in output
            assert 'Bottleneck' in output
            assert 'Total' in output

    def test_render__stage_breakdown(self):                         # Test stage breakdown
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert 'STAGE BREAKDOWN' in output
            assert '█' in output                                    # Visual bar

    def test__improve_code_coverage(self):
        with self.renderer as _:
            _.config.include_stage_breakdown     = False
            _.config.include_percentage_analysis = False

            assert _.render_legend             (Schema__Perf_Report(legend= None)) == []
            assert _.render_stage_breakdown    (Schema__Perf_Report(            )) == []
            assert _.render_percentage_analysis(Schema__Perf_Report(            )) == []

            _.config.include_percentage_analysis = True
            _.config.include_stage_breakdown     = True

    def test_render_percentage_analysis__full_total_zero(self):     # Test when full category total is zero
        with self.test_data as _:
            report = _.create_report()

            # Set category A's total_ns to 0
            for category in report.categories:
                if str(category.category_id) == 'A':
                    category.total_ns = 0

            with self.renderer as renderer:
                result = renderer.render_percentage_analysis(report)

                assert result == []

    def test_render_percentage_analysis__disabled_in_config(self):  # Test when percentage analysis disabled
        with self.test_data as _:
            report = _.create_report()
            config = _.create_builder_config()
            config.include_percentage_analysis = False

            renderer = Perf_Report__Renderer__Text(config=config)
            result   = renderer.render_percentage_analysis(report)

            assert result == []

    def test_render_percentage_analysis__with_categories(self):     # Test percentage analysis renders B/C vs A
        with self.test_data as _:
            report = _.create_report()

            with self.renderer as renderer:
                result = renderer.render_percentage_analysis(report)

                assert len(result) > 0
                assert 'PERCENTAGE ANALYSIS' in result[0]

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__output_structure(self):                   # Test output structure
        report = self.test_data.create_report(title='Structure Test')

        with self.renderer as _:
            output = _.render(report)
            lines  = output.split('\n')

            assert len(lines) > 20                                  # Reasonable output size
            assert lines[0].startswith('═')                         # Header border

    def test_render_percentage_analysis__only_create_category(self):
        with self.test_data as _:
            report = _.create_report()

            # Remove category C entirely
            report.categories = [
                c for c in report.categories if str(c.category_id) != 'C'
            ]

            with self.renderer as renderer:
                lines = renderer.render_percentage_analysis(report)

                assert any('B / A =' in line for line in lines)
                assert not any('C / A =' in line for line in lines)

