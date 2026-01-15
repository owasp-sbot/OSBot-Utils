# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Renderer__Markdown - Tests for markdown format renderer
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                                    import TestCase

import pytest

from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base                                import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Markdown                            import Perf_Report__Renderer__Markdown
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report import Schema__Perf_Report
from osbot_utils.helpers.performance.testing.QA__Perf_Report__Test_Data                                          import QA__Perf_Report__Test_Data
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe


class test_Perf_Report__Renderer__Markdown(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        cls.test_data = QA__Perf_Report__Test_Data()
        cls.renderer  = Perf_Report__Renderer__Markdown()

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Renderer__Markdown() as _:
            assert type(_)            is Perf_Report__Renderer__Markdown
            assert isinstance(_, Type_Safe)
            assert isinstance(_, Perf_Report__Renderer__Base)

    # ═══════════════════════════════════════════════════════════════════════════
    # Escape Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_escape_markdown(self):                                 # Test markdown escaping
        with self.renderer as _:
            assert _.escape_markdown('test|pipe')   == 'test\\|pipe'
            assert _.escape_markdown('test`code`')  == 'test\\`code\\`'
            assert _.escape_markdown('*bold*')      == '\\*bold\\*'

    # ═══════════════════════════════════════════════════════════════════════════
    # Render Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_render(self):                                          # Test render method
        report = self.test_data.create_report(title='Markdown Test')

        with self.renderer as _:
            output = _.render(report)

            assert type(output) is str
            assert len(output)  > 0

    def test_render__contains_title(self):                          # Test title in output
        report = self.test_data.create_report(title='My Markdown Title')

        with self.renderer as _:
            output = _.render(report)

            assert '# My Markdown Title' in output

    def test_render__contains_metadata_table(self):                 # Test metadata table
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Metadata' in output
            assert '| Property | Value |' in output
            assert '|----------|-------|' in output

    def test_render__contains_legend(self):                         # Test legend section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Legend' in output
            assert '**A**:' in output
            assert '**B**:' in output

    def test_render__contains_benchmarks_table(self):               # Test benchmarks table
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Individual Benchmarks' in output
            assert '| Benchmark | Time | Percentage |' in output

    def test_render__contains_categories_table(self):               # Test categories table
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Category Totals' in output
            assert '| Category | Time | Percentage | Benchmarks |' in output

    def test_render__contains_analysis(self):                       # Test analysis section
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Analysis' in output
            assert '| Metric | Value |' in output
            assert 'Bottleneck' in output

    def test_render__contains_key_insight(self):                    # Test key insight quote
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '## Key Insight' in output or '>' in output      # Blockquote format

    def test__render_in_super(self):
        with pytest.raises(NotImplementedError):
            Perf_Report__Renderer__Base().render(Schema__Perf_Report())

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__valid_markdown(self):                     # Test valid markdown
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert output.startswith('#')                           # Starts with header
            assert output.count('|') > 10                           # Has tables
            assert output.count('##') >= 4                          # Has multiple sections
