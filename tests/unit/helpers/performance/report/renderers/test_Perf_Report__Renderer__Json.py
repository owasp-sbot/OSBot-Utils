# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Renderer__Json - Tests for JSON format renderer
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base   import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Json   import Perf_Report__Renderer__Json
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report             import Schema__Perf_Report
from osbot_utils.helpers.performance.testing.QA__Perf_Report__Test_Data             import QA__Perf_Report__Test_Data
from osbot_utils.testing.Pytest                                                     import skip__if_not__in_github_actions
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.utils.Json                                                         import json_loads


class test_Perf_Report__Renderer__Json(TestCase):

    @classmethod
    def setUpClass(cls):                                            # Shared test data
        skip__if_not__in_github_actions()
        cls.test_data = QA__Perf_Report__Test_Data()
        cls.renderer  = Perf_Report__Renderer__Json()

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Renderer__Json() as _:
            assert type(_)            is Perf_Report__Renderer__Json
            assert isinstance(_, Type_Safe)
            assert isinstance(_, Perf_Report__Renderer__Base)

    # ═══════════════════════════════════════════════════════════════════════════
    # Render Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_render(self):                                          # Test render method
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert type(output) is str
            assert len(output)  > 0

    def test_render__valid_json(self):                              # Test valid JSON output
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert type(parsed) is dict

    def test_render__contains_metadata(self):                       # Test metadata in JSON
        report = self.test_data.create_report(title='JSON Test')

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert 'metadata' in parsed
            assert parsed['metadata']['title'] == 'JSON Test'

    def test_render__contains_benchmarks(self):                     # Test benchmarks in JSON
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert 'benchmarks' in parsed
            assert type(parsed['benchmarks']) is list
            assert len(parsed['benchmarks']) == len(report.benchmarks)

    def test_render__contains_categories(self):                     # Test categories in JSON
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert 'categories' in parsed
            assert type(parsed['categories']) is list

    def test_render__contains_analysis(self):                       # Test analysis in JSON
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert 'analysis' in parsed
            assert 'bottleneck_id' in parsed['analysis']
            assert 'total_ns' in parsed['analysis']

    def test_render__contains_legend(self):                         # Test legend in JSON
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)
            parsed = json_loads(output)

            assert 'legend' in parsed
            assert type(parsed['legend']) is dict

    # ═══════════════════════════════════════════════════════════════════════════
    # Round-trip Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_render__round_trip(self):                              # Test round-trip
        original = self.test_data.create_report(title='Round Trip Test')

        with self.renderer as _:
            output   = _.render(original)
            parsed   = json_loads(output)
            restored = Schema__Perf_Report.from_json(parsed)

            assert str(restored.metadata.title)   == str(original.metadata.title)
            assert len(restored.benchmarks)       == len(original.benchmarks)
            assert len(restored.categories)       == len(original.categories)

    def test_render__preserves_benchmark_data(self):                # Test benchmark preservation
        original = self.test_data.create_report()

        with self.renderer as _:
            output   = _.render(original)
            parsed   = json_loads(output)
            restored = Schema__Perf_Report.from_json(parsed)

            for i in range(len(original.benchmarks)):
                assert str(restored.benchmarks[i].benchmark_id) == str(original.benchmarks[i].benchmark_id)
                assert int(restored.benchmarks[i].time_ns)      == int(original.benchmarks[i].time_ns)

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_integration__indented_output(self):                    # Test output is indented
        report = self.test_data.create_report()

        with self.renderer as _:
            output = _.render(report)

            assert '\n  ' in output                                 # Has indentation
            assert output.count('\n') > 10                          # Multiple lines
